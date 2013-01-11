# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
import sys
import re
from contextlib import contextmanager
from .util import memoize
from . import buffering
from .exceptions import *  # @UnusedWildImport
from .ast import AST

class Parser(object):
    def __init__(self, text,
                        whitespace=None,
                        comments_re=None,
                        ignorecase=False,
                        verbose=False,
                        bufferClass=buffering.Buffer):
        self.text = text
        self.whitespace = set(whitespace if whitespace else '\t\v\n\r ')
        self.comments_re = comments_re
        self.ignorecase = ignorecase
        self.verbose = verbose
        self._bufferClass = bufferClass
        self._buffer = None
        self._ast_stack = []
        self._concrete_stack = []
        self._rule_stack = []

    def parse(self, rule_name):
        try:
            self._buffer = self._bufferClass(self.text, self.whitespace)
            self._push_ast()
            self._concrete_stack.append([])
            self._call(rule_name, rule_name)
            return self.ast
        finally:
            del self._ast_stack[1:]

    @property
    def ast(self):
        return self._ast_stack[-1]

    def result(self):
        return self.ast

    def rulestack(self):
        return '.'.join(self._rule_stack)

    @property
    def _pos(self):
        return self._buffer.pos

    def _goto(self, pos):
        self._buffer.goto(pos)

    def _eatwhitespace(self):
        self._buffer.eatwhitespace()

    def _eatcomments(self):
        if self.comments_re is not None:
            opts = re.MULTILINE if '\n' in self.comments_re else 0
            while self._buffer.matchre(self.comments_re, opts):
                pass

    def _next_token(self):
        p = None
        while self._pos != p:
            p = self._pos
            self._eatwhitespace()
            self._eatcomments()


    def _call(self, name, node_name=None, force_list=False):
        self._rule_stack.append(name)
        if name[0].islower():
            self._next_token()
        pos = self._pos
        try:
            self.trace('%s <<\n\t->%s', self.rulestack(), self._buffer.lookahead())
            result, newpos = self._invoke_rule(name, pos)
            self.trace('SUCCESS %s', self.rulestack())
            self._add_ast_node(node_name, result, force_list)
            self._goto(newpos)
            return result
        except FailedParse:
            self.trace('FAILED %s', self.rulestack())
            self._goto(pos)
            raise
        finally:
            self._rule_stack.pop()

    @memoize
    def _invoke_rule(self, name, pos):
        rule = self._find_rule(name)
        self._push_ast()
        self._concrete_stack.append([])
        try:
            rule()
            node = self.ast
            if not node:
                node = self._concrete_stack[-1]
                if len(node) == 1:
                    node = node[0]
        finally:
            self._concrete_stack.pop()
            self._pop_ast()
        semantic_rule = self._find_semantic_rule(name)
        if semantic_rule:
            node = semantic_rule(node)
        return (node, self._pos)

    def _token(self, token, node_name=None, force_list=False):
        self._next_token()
        self.trace('match <%s> \n\t->%s', token, self._buffer.lookahead())
        if self._buffer.match(token, self.ignorecase) is None:
            self.trace('failed <%s>', token)
            raise FailedToken(self._buffer, token)
        self._add_ast_node(node_name, token, force_list)
        return token

    def _try(self, token, node_name=None, force_list=False):
        self._next_token()
        self.trace('try <%s> \n\t->%s', token, self._buffer.lookahead())
        if self._buffer.match(token, self.ignorecase) is not None:
            self._add_ast_node(node_name, token, force_list)
            return True


    def _pattern(self, pattern, node_name=None, force_list=False):
        self.trace('match %s\n\t->%s', pattern, self._buffer.lookahead())
        token = self._buffer.matchre(pattern, self.ignorecase)
        if token is None:
            self.trace('failed %s', pattern)
            raise FailedPattern(self._buffer, pattern)
        self.trace('matched %s', token)
        self._add_ast_node(node_name, token, force_list)
        return token

    def _try_pattern(self, pattern, node_name=None, force_list=False):
        self.trace('match %s\n\t->%s', pattern, self._buffer.lookahead())
        token = self._buffer.matchre(pattern, self.ignorecase)
        if token is None:
            self.trace('failed %s', pattern)
        self._add_ast_node(node_name, token, force_list)
        return token

    def _find_rule(self, name):
        rule = getattr(self, '_%s_' % name, None)
        if rule is None or not isinstance(rule, type(self._find_rule)):
            raise FailedRef(self._buffer, name)
        return rule

    def _find_semantic_rule(self, name):
        result = getattr(self, name, None)
        if result is None or not isinstance(result, type(self._find_rule)):
            return None
        return result

    def _push_ast(self):
        self._ast_stack.append(AST())

    def _pop_ast(self):
        return self._ast_stack.pop()

    def _add_ast_node(self, name, node, force_list=False):
        if name is not None:  # and node:
            self.ast.add(name, node, force_list)
        self._concrete_stack[-1].append(node)
        return node

    def error(self, item, etype=FailedParse):
        raise etype(self._buffer, item)

    def trace(self, msg, *params):
        if self.verbose:
            print(msg % params, file=sys.stderr)

    @contextmanager
    def _choice_context(self):
        p = self._pos
        try:
            yield
        except FailedCut:
            raise
        except FailedParse:
            self._goto(p)

    @contextmanager
    def _repeat_context(self):
        p = self._pos
        try:
            yield
        except FailedParse:
            self._goto(p)
            raise

    def _repeat_iterator(self, f):
        while 1:
            with self._repeat_context():
                try:
                    value = f()
                    if value is not None:
                        yield value
                except FailedCut as e:
                    raise e.nested
                except FailedParse:
                    raise StopIteration()

    def _repeat(self, f):
        return list(self._repeat_iterator(f))

    def _eof(self):
        return self._buffer.atend()

    def _eol(self):
        return self._buffer.ateol()

    def _check_eof(self):
        self._next_token()
        if not self._buffer.atend():
            raise FailedParse(self._buffer, 'expecting end of file')
