# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from contextlib import contextmanager
import functools

from grako.buffering import Buffer
from grako.exceptions import FailedLeftRecursion, FailedParse, OptionSucceeded


@contextmanager
def suppress(*exceptions):
    try:
        yield
    except exceptions:
        pass


# decorator for rule implementation methods
def graken(func_rule):
    @functools.wraps(func_rule)
    def wrapper(self):
        # remove the leading and trailing underscore the parser generator added
        name = func_rule.__name__[1:-1]
        return self._call(func_rule, name)

    return wrapper


class Parser(object):
    def __init__(self, eol_comments_re=None, keywords=None):

        self.eol_comments_re = eol_comments_re
        self.keywords = set(keywords)

        self._concrete_stack = [None]
        self._memoization_cache = dict()
        self._buffer = None

    def _reset(self, text=None):
        self._concrete_stack = [None]
        self._memoization_cache = dict()
        self._buffer = Buffer(text, eol_comments_re=self.eol_comments_re)

    def parse(self, text, rule_name='start'):
        self._reset(text=text)
        rule = getattr(self, '_' + rule_name + '_', None)
        return rule()

    def _add_cst_node(self, node):
        # node can be list, unicode, or none
        if node is None:
            return
        previous = self._concrete_stack[-1]
        if previous is None:
            self._concrete_stack[-1] = node
        elif isinstance(previous, list):
            previous.append(node)
        else:
            # previous is unicode
            self._concrete_stack[-1] = [previous, node]

    def _extend_cst(self, node):
        if node is None:
            return
        previous = self._concrete_stack[-1]
        if previous is None:
            self._concrete_stack[-1] = node
        elif isinstance(previous, list) and isinstance(previous, list):
            previous.extend(node)
        else:
            # previous is unicode
            self._concrete_stack[-1] = [previous, node]

    @staticmethod
    def _error(item, etype=FailedParse):
        raise etype(item)

    def _call(self, rule, name):
        pos = self._buffer.pos
        try:
            node, newpos = self._invoke_rule(rule, name)
        except FailedParse:
            self._buffer.goto(pos)
            raise
        else:
            self._buffer.goto(newpos)
            self._add_cst_node(node)
            return node

    def _invoke_rule(self, rule, name):
        if name[0].islower():
            self._buffer.next_token()
        key = self._buffer.pos, rule
        if key in self._memoization_cache:
            memo = self._memoization_cache[key]
            if isinstance(memo, Exception):
                raise memo
            return memo

        self._memoization_cache[key] = FailedLeftRecursion(name)  # left rc grd
        self._concrete_stack.append(None)
        try:
            rule(self)
        except FailedParse as e:
            self._memoization_cache[key] = e
            raise
        finally:
            node = self._concrete_stack.pop()

        result = node, self._buffer.pos
        self._memoization_cache[key] = result
        return result

    def _token(self, token):
        self._buffer.next_token()
        if self._buffer.match(token) is None:
            self._error(token)
        self._add_cst_node(token)
        return token

    def _pattern(self, pattern):
        token = self._buffer.matchre(pattern)
        if token is None:
            self._error(pattern)
        self._add_cst_node(token)
        return token

    def _check_eof(self):
        self._buffer.next_token()
        if not self._buffer.at_end():
            self._error('Expecting end of text.')

    @contextmanager
    def _try(self):
        pos = self._buffer.pos
        self._concrete_stack.append(None)
        try:
            yield
        except Exception:
            self._buffer.goto(pos)
            raise
        finally:
            node = self._concrete_stack.pop()
        self._extend_cst(node)

    @contextmanager
    def _option(self):
        with suppress(FailedParse):
            with self._try():
                yield
            raise OptionSucceeded()

    @contextmanager
    def _choice(self):
        with self._try():
            with suppress(OptionSucceeded):
                yield

    @contextmanager
    def _optional(self):
        with self._choice():
            with self._option():
                yield

    @contextmanager
    def _group(self):
        self._concrete_stack.append(None)
        try:
            yield
        finally:
            node = self._concrete_stack.pop()
        self._extend_cst(node)

    def _repeater(self, block, prefix=None):
        while True:
            self._concrete_stack.append(None)
            try:
                with self._try():
                    if prefix:
                        prefix()
                    block()
            except FailedParse:
                break
            finally:
                node = self._concrete_stack.pop()
            self._extend_cst(node)

    def _positive_closure(self, block, prefix=None):
        self._concrete_stack.append(None)
        try:
            with self._try():
                block()
            self._concrete_stack[-1] = [self._concrete_stack[-1]]
            self._repeater(block, prefix=prefix)
        finally:
            node = self._concrete_stack.pop()
        self._extend_cst(node)

    def _check_name(self, token):
        name = token.upper()  # bcuz ignorecase == True
        if name in self.keywords:
            raise FailedParse('"{name}" is a reserved word'.format(name=name))
