# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from contextlib import contextmanager

from grako.buffering import Buffer
from grako.exceptions import (
    FailedLeftRecursion, FailedParse, FailedPattern, FailedToken,
    FailedSemantics, FailedKeywordSemantics, OptionSucceeded)


class Parser(object):
    def __init__(self, eol_comments_re=None, whitespace=None, keywords=None):

        self.eol_comments_re = eol_comments_re
        self.whitespace = whitespace
        self.keywords = set(keywords)

        self._buffer = None

        self._concrete_stack = [None]
        self._memoization_cache = dict()
        self._recursive_results = dict()

        self.last_node = None
        self._state = None

    def _reset(self, text=None):
        self._buffer = Buffer(text, whitespace=self.whitespace,
                              eol_comments_re=self.eol_comments_re)

        self._concrete_stack = [None]
        self._memoization_cache = dict()
        self._recursive_results = dict()

        self.last_node = None
        self._state = None

    def parse(self, text, rule_name='start'):
        self._reset(text=text)
        rule = self._find_rule(rule_name)
        result = rule()
        return result

    def goto(self, pos):
        self._buffer.goto(pos)

    @property
    def _pos(self):
        return self._buffer.pos

    def _next_token(self):
        self._buffer.next_token()

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
        if isinstance(node, list):
            return list(node)
        else:
            return node

    def _find_rule(self, name):
        return getattr(self, '_' + name + '_', None)

    def _error(self, item, etype=FailedParse):
        raise etype(item)

    def _call(self, rule, name):
        pos = self._pos
        try:
            self.last_node = None
            node, newpos, newstate = self._invoke_rule(rule, name)
            self.goto(newpos)
            self._state = newstate
            self._add_cst_node(node)
            self.last_node = node
            return node
        except FailedPattern:
            self._error('Expecting <%s>' % name)
        except FailedParse:
            self.goto(pos)
            raise

    def _invoke_rule(self, rule, name):
        cache = self._memoization_cache
        pos = self._pos

        key = (pos, rule, self._state)
        if key in cache:
            memo = cache[key]
            if isinstance(memo, Exception):
                raise memo
            return memo

        self._memoization_cache[key] = FailedLeftRecursion(name)  #left rec grd
        self._push_cst()
        try:
            if name[0].islower():
                self._next_token()
            try:
                rule(self)

                node = {}  # used to be ast get
                if not node:
                    node = self.cst

                result = (node, self._pos, self._state)
                self._recursive_results[key] = result

                cache[key] = result
                return result
            except FailedSemantics as e:
                self._error(str(e))
        except FailedParse as e:
            cache[key] = e
            raise
        finally:
            self._pop_cst()

    def _token(self, token):
        self._next_token()
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
        self._next_token()
        if not self._buffer.at_end():
            self._error('Expecting end of text.')

    @contextmanager
    def _try(self):
        p = self._pos
        s = self._state
        self._push_cst()
        self.last_node = None
        try:
            yield
            cst = self.cst
        except:
            self.goto(p)
            self._state = s
            raise
        finally:
            self._pop_cst()
        self._extend_cst(cst)
        self.last_node = cst

    @contextmanager
    def _option(self):
        self.last_node = None
        try:
            with self._try():
                yield
            raise OptionSucceeded()
        except FailedParse:
            pass

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
            self._push_cst()
            try:
                p = self._pos
                with self._try():
                    if prefix:
                        with self._ignore():
                            prefix()

                    block()
                    cst = self.cst

                    if self._pos == p:
                        self._error('empty closure')
            except FailedParse:
                break
            finally:
                self._pop_cst()
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
