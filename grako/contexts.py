# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from contextlib import contextmanager

from grako.buffering import Buffer
from grako.ast import AST
from grako.exceptions import (
    FailedLeftRecursion, FailedParse, FailedPattern, FailedToken,
    FailedSemantics, FailedKeywordSemantics, OptionSucceeded)
from grako.util import prune_dict, is_list


class Parser(object):
    def __init__(self, eol_comments_re=None, whitespace=None, keywords=None):

        self.eol_comments_re = eol_comments_re
        self.whitespace = whitespace
        self.keywords = set(keywords)

        self._buffer = None

        self._ast_stack = [AST()]
        self._concrete_stack = [None]
        self._rule_stack = []
        self._cut_stack = [False]
        self._memoization_cache = dict()

        self._last_node = None
        self._state = None
        self._lookahead = 0

        self._recursive_results = dict()
        self._recursive_head = []

    def _reset(self, text=None):
        self._buffer = Buffer(text, whitespace=self.whitespace,
                              eol_comments_re=self.eol_comments_re)
        self._ast_stack = [AST()]
        self._concrete_stack = [None]
        self._rule_stack = []
        self._cut_stack = [False]
        self._memoization_cache = dict()

        self._last_node = None
        self._state = None
        self._lookahead = 0

        self._recursive_results = dict()
        self._recursive_head = []

    def parse(self, text, rule_name='start'):
        self._reset(text=text)
        rule = self._find_rule(rule_name)
        result = rule()
        self._clear_cache()
        return result

    def goto(self, pos):
        self._buffer.goto(pos)

    @property
    def last_node(self):
        return self._last_node

    @last_node.setter
    def last_node(self, value):
        self._last_node = value

    @property
    def _pos(self):
        return self._buffer.pos

    def _clear_cache(self):
        self._memoization_cache = dict()
        self._recursive_results = dict()

    def _next_token(self):
        self._buffer.next_token()

    @property
    def ast(self):
        return self._ast_stack[-1]

    @ast.setter
    def ast(self, value):
        self._ast_stack[-1] = value

    def _push_ast(self):
        self._push_cst()
        self._ast_stack.append(AST())

    def _pop_ast(self):
        self._pop_cst()
        return self._ast_stack.pop()

    @property
    def cst(self):
        return self._concrete_stack[-1]

    @cst.setter
    def cst(self, value):
        self._concrete_stack[-1] = value

    def _push_cst(self):
        self._concrete_stack.append(None)

    def _pop_cst(self):
        return self._concrete_stack.pop()

    def _add_cst_node(self, node):
        if node is None:
            return
        previous = self.cst
        if previous is None:
            self.cst = self._copy_node(node)
        elif is_list(previous):
            previous.append(node)
        else:
            self.cst = [previous, node]

    def _extend_cst(self, node):
        if node is None:
            return
        previous = self.cst
        if previous is None:
            self.cst = self._copy_node(node)
        elif is_list(node):
            if is_list(previous):
                previous.extend(node)
        else:
            self.cst = [previous, node]

    def _copy_node(self, node):
        if is_list(node):
            return list(node)
        else:
            return node

    def _cut(self):
        self._cut_stack[-1] = True

        # Kota Mizushima et al say that we can throw away
        # memos for previous positions in the buffer under
        # certain circumstances, without affecting the linearity
        # of PEG parsing.
        #   http://goo.gl/VaGpj
        #
        # We adopt the heuristic of always dropping the cache for
        # positions less than the current cut position. It remains to
        # be proven if doing it this way affects linearity. Empirically,
        # it hasn't.
        cutpos = self._pos

        def prune_cache(cache):
            prune_dict(cache, lambda k, _: k[0] < cutpos)

        prune_cache(self._memoization_cache)
        prune_cache(self._recursive_results)

    def _push_cut(self):
        self._cut_stack.append(False)

    def _pop_cut(self):
        return self._cut_stack.pop()

    def _find_rule(self, name):
        rule = getattr(self, '_' + name + '_', None)
        if isinstance(rule, type(self._find_rule)):
            return rule

    def _error(self, item, etype=FailedParse):
        raise etype(self._buffer, list(reversed(self._rule_stack)), item)

    def _call(self, rule, name):
        self._rule_stack.append(name)
        pos = self._pos
        try:
            self._last_node = None
            node, newpos, newstate = self._invoke_rule(rule, name)
            self.goto(newpos)
            self._state = newstate
            self._add_cst_node(node)
            self._last_node = node
            return node
        except FailedPattern:
            self._error('Expecting <%s>' % name)
        except FailedParse:
            self.goto(pos)
            raise
        finally:
            self._rule_stack.pop()

    def _invoke_rule(self, rule, name):
        cache = self._memoization_cache
        pos = self._pos

        key = (pos, rule, self._state)
        if key in cache:
            memo = cache[key]
            if isinstance(memo, Exception):
                raise memo
            return memo

        self._set_left_recursion_guard(name, key)
        self._push_ast()
        try:
            if name[0].islower():
                self._next_token()
            try:
                rule(self)

                node = self.ast
                if not node:
                    node = self.cst

                result = (node, self._pos, self._state)
                self._recursive_results[key] = result

                cache[key] = result
                return result
            except FailedSemantics as e:
                self._error(str(e), FailedParse)
        except FailedParse as e:
            cache[key] = e
            raise
        finally:
            self._pop_ast()

    def _set_left_recursion_guard(self, name, key):
        exception = FailedLeftRecursion(self._buffer,
                                        list(reversed(self._rule_stack)), name)

        # Alessandro Warth et al say that we can deal with
        # direct and indirect left-recursion by seeding the
        # memoization cache with a parse failure.
        #
        #   http://www.vpri.org/pdf/tr2007002_packrat.pdf
        #
        self._memoization_cache[key] = exception

    def _token(self, token):
        self._next_token()
        if self._buffer.match(token) is None:
            self._error(token, etype=FailedToken)
        self._add_cst_node(token)
        self._last_node = token
        return token

    def _pattern(self, pattern):
        token = self._buffer.matchre(pattern)
        if token is None:
            self._error(pattern, etype=FailedPattern)
        self._add_cst_node(token)
        self._last_node = token
        return token

    def _check_eof(self):
        self._next_token()
        if not self._buffer.at_end():
            self._error('Expecting end of text.')

    @contextmanager
    def _try(self):
        p = self._pos
        s = self._state
        ast_copy = self.ast.copy()
        self._push_ast()
        self.last_node = None
        try:
            self.ast = ast_copy
            yield
            ast = self.ast
            cst = self.cst
        except:
            self.goto(p)
            self._state = s
            raise
        finally:
            self._pop_ast()
        self.ast = ast
        self._extend_cst(cst)
        self.last_node = cst

    @contextmanager
    def _option(self):
        self.last_node = None
        self._push_cut()
        try:
            with self._try():
                yield
            raise OptionSucceeded()
        except FailedParse:
            pass
        finally:
            self._pop_cut()

    @contextmanager
    def _choice(self):
        self.last_node = None
        with self._try():
            try:
                yield
            except OptionSucceeded:
                pass

    @contextmanager
    def _optional(self):
        self.last_node = None
        with self._choice():
            with self._option():
                yield

    @contextmanager
    def _ignore(self):
        self._push_cst()
        try:
            self.cst = None
            yield
        finally:
            self._pop_cst()

    def _repeater(self, block, prefix=None):
        while True:
            self._push_cut()
            self._push_cst()
            try:
                p = self._pos
                with self._try():
                    if prefix:
                        with self._ignore():
                            prefix()
                            self._cut()

                    block()
                    cst = self.cst

                    if self._pos == p:
                        self._error('empty closure')
            except FailedParse:
                break
            finally:
                self._pop_cst()
                self._pop_cut()
            self._add_cst_node(cst)

    def _closure(self, block):
        self._push_cst()
        try:
            self.cst = []
            self._repeater(block)
            cst = list(self.cst)
        finally:
            self._pop_cst()
        self._add_cst_node(cst)
        self.last_node = cst
        return cst

    def _positive_closure(self, block, prefix=None):
        self._push_cst()
        try:
            self.cst = None
            with self._try():
                block()
            self.cst = [self.cst]
            self._repeater(block, prefix=prefix)
            cst = list(self.cst)
        finally:
            self._pop_cst()
        self._add_cst_node(cst)
        self.last_node = cst
        return cst

    def _check_name(self):
        name = self.last_node.upper()  # bcuz ignorecase == True
        if name in self.keywords:
            raise FailedKeywordSemantics('"%s" is a reserved word' % name)
