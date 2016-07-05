# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from contextlib import contextmanager

from grako.buffering import Buffer
from grako.exceptions import (
    FailedLeftRecursion, FailedParse, FailedPattern, FailedToken,
    FailedSemantics, FailedKeywordSemantics, OptionSucceeded)


@contextmanager
def suppress(*exceptions):
    try:
        yield
    except exceptions:
        pass


class Parser(object):
    def __init__(self, eol_comments_re=None, whitespace=None, keywords=None):

        self.eol_comments_re = eol_comments_re
        self.whitespace = whitespace
        self.keywords = set(keywords)

        self._concrete_stack = [None]
        self._memoization_cache = dict()
        self.last_node = None
        self._buffer = None

    def _reset(self, text=None):
        self._concrete_stack = [None]
        self._memoization_cache = dict()
        self.last_node = None
        self._buffer = Buffer(text, whitespace=self.whitespace,
                              eol_comments_re=self.eol_comments_re)

    def parse(self, text, rule_name='start'):
        self._reset(text=text)
        rule = self._find_rule(rule_name)
        result = rule()
        return result

    @property
    def cst(self):
        return self._concrete_stack[-1]

    @cst.setter
    def cst(self, value):
        self._concrete_stack[-1] = value

    def _add_cst_node(self, node):
        if node is None:
            return
        previous = self.cst
        if previous is None:
            self.cst = self._copy_node(node)
        elif isinstance(previous, list):
            previous.append(node)
        else:
            self.cst = [previous, node]

    def _extend_cst(self, node):
        if node is None:
            return
        previous = self.cst
        if previous is None:
            self.cst = self._copy_node(node)
        elif isinstance(node, list):
            if isinstance(previous, list):
                previous.extend(node)
        else:
            self.cst = [previous, node]

    @staticmethod
    def _copy_node(node):
        # unicode or list
        return list(node) if isinstance(node, list) else node

    def _find_rule(self, name):
        return getattr(self, '_' + name + '_', None)

    def _error(self, item, etype=FailedParse):
        raise etype(item)

    def _call(self, rule, name):
        pos = self._buffer.pos
        try:
            self.last_node = None
            node, newpos = self._invoke_rule(rule, name)
            self._buffer.goto(newpos)
            self._add_cst_node(node)
            self.last_node = node
            return node
        except FailedPattern:
            self._error('Expecting <%s>' % name)
        except FailedParse:
            self._buffer.goto(pos)
            raise

    def _invoke_rule(self, rule, name):
        cache = self._memoization_cache
        pos = self._buffer.pos

        key = pos, rule
        if key in cache:
            memo = cache[key]
            if isinstance(memo, Exception):
                raise memo
            return memo
        self._memoization_cache[key] = FailedLeftRecursion(name)  # left rc grd
        self._concrete_stack.append(None)
        try:
            if name[0].islower():
                self._buffer.next_token()
            try:
                rule(self)
                node = self.cst
                result = node, self._buffer.pos
                cache[key] = result
                return result
            except FailedSemantics as e:
                self._error(str(e))
        except FailedParse as e:
            cache[key] = e
            raise
        finally:
            self._concrete_stack.pop()

    def _token(self, token):
        self._buffer.next_token()
        if self._buffer.match(token) is None:
            self._error(token, etype=FailedToken)
        self._add_cst_node(token)
        self.last_node = token
        return token

    def _pattern(self, pattern):
        token = self._buffer.matchre(pattern)
        if token is None:
            self._error(pattern, etype=FailedPattern)
        self._add_cst_node(token)
        self.last_node = token
        return token

    def _check_eof(self):
        self._buffer.next_token()
        if not self._buffer.at_end():
            self._error('Expecting end of text.')

    @contextmanager
    def _try(self):
        p = self._buffer.pos
        self._concrete_stack.append(None)
        self.last_node = None
        try:
            yield
            cst = self.cst
        except:
            self._buffer.goto(p)
            raise
        finally:
            self._concrete_stack.pop()
        self._extend_cst(cst)
        self.last_node = cst

    @contextmanager
    def _option(self):
        self.last_node = None
        with suppress(FailedParse):
            with self._try():
                yield
            raise OptionSucceeded()

    @contextmanager
    def _choice(self):
        self.last_node = None
        with self._try():
            with suppress(OptionSucceeded):
                yield

    @contextmanager
    def _optional(self):
        self.last_node = None
        with self._choice():
            with self._option():
                yield

    @contextmanager
    def _ignore(self):
        self._concrete_stack.append(None)
        try:
            self.cst = None
            yield
        finally:
            self._concrete_stack.pop()

    def _repeater(self, block, prefix=None):
        while True:
            self._concrete_stack.append(None)
            try:
                p = self._buffer.pos
                with self._try():
                    if prefix:
                        with self._ignore():
                            prefix()

                    block()
                    cst = self.cst

                    if self._buffer.pos == p:
                        self._error('empty closure')
            except FailedParse:
                break
            finally:
                self._concrete_stack.pop()
            self._add_cst_node(cst)

    def _closure(self, block):
        self._concrete_stack.append(None)
        try:
            self.cst = []
            self._repeater(block)
            cst = list(self.cst)
        finally:
            self._concrete_stack.pop()
        self._add_cst_node(cst)
        self.last_node = cst
        return cst

    def _positive_closure(self, block, prefix=None):
        self._concrete_stack.append(None)
        try:
            self.cst = None
            with self._try():
                block()
            self.cst = [self.cst]
            self._repeater(block, prefix=prefix)
            cst = list(self.cst)
        finally:
            self._concrete_stack.pop()
        self._add_cst_node(cst)
        self.last_node = cst
        return cst

    def _check_name(self):
        name = self.last_node.upper()  # bcuz ignorecase == True
        if name in self.keywords:
            raise FailedKeywordSemantics('"%s" is a reserved word' % name)
