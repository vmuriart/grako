# -*- coding: utf-8 -*-
"""
The Buffer class provides the functionality required by a parser-driven lexer.

Line analysis and caching are done so the parser can freely move with goto(p)
to any position in the parsed text, and still recover accurate information
about source lines and content.
"""
from __future__ import absolute_import, division, unicode_literals

from collections import namedtuple

from grako.util import ustr, re as regexp, WHITESPACE_RE, RE_FLAGS

__all__ = ['Buffer']

RETYPE = type(regexp.compile('.'))

PosLine = namedtuple('PosLine', ['pos', 'line'])
LineInfo = namedtuple(
    'LineInfo', ['filename', 'line', 'col', 'start', 'end', 'text'])


class Buffer(object):
    def __init__(self, text, whitespace=None, eol_comments_re=None,
                 ignorecase=False):
        self.text = ustr(text)
        self.whitespace = whitespace
        self.eol_comments_re = eol_comments_re
        self.ignorecase = ignorecase

        self._pos = 0
        self._len = len(self.text)
        self._re_cache = {}

    @property
    def whitespace(self):
        return self._whitespace

    @whitespace.setter
    def whitespace(self, value):
        self._whitespace = value
        self.whitespace_re = self.build_whitespace_re(value)

    @staticmethod
    def build_whitespace_re(whitespace):
        if whitespace is None:
            return WHITESPACE_RE
        elif isinstance(whitespace, RETYPE):
            return whitespace
        else:
            return None

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, p):
        self.goto(p)

    def at_end(self):
        return self._pos >= self._len

    def current(self):
        if self._pos >= self._len:
            return None
        return self.text[self._pos]

    def goto(self, p):
        self._pos = max(0, min(len(self.text), p))

    def move(self, n):
        self.goto(self.pos + n)

    def eat_whitespace(self):
        if self.whitespace_re is not None:
            while self.matchre(self.whitespace_re):
                pass

    def eat_eol_comments(self):
        if self.eol_comments_re is not None:
            while True:
                comment = self.matchre(self.eol_comments_re)
                if not comment:
                    break

    def next_token(self):
        p = None
        while self._pos != p:
            p = self._pos
            self.eat_eol_comments()
            self.eat_whitespace()

    def is_name_char(self, c):
        return c is not None and c.isalnum()

    def match(self, token, ignorecase=None):
        ignorecase = ignorecase if ignorecase is not None else self.ignorecase

        if token is None:
            return self.at_end()

        p = self.pos
        if ignorecase:
            result = self.text[p:p + len(token)].lower() == token.lower()
        else:
            result = self.text[p:p + len(token)] == token

        if result:
            self.move(len(token))
            partial_match = (self.is_name_char(self.current()) and
                             token.isalnum() and token[0].isalpha())
            if not partial_match:
                return token
        self.goto(p)

    def matchre(self, pattern, ignorecase=None):
        matched = self._scanre(pattern, ignorecase=ignorecase)
        if matched:
            token = matched.group()
            self.move(len(token))
            return token

    def _scanre(self, pattern, ignorecase=None, offset=0):
        ignorecase = ignorecase if ignorecase is not None else self.ignorecase

        if isinstance(pattern, RETYPE):
            re = pattern
        elif pattern in self._re_cache:
            re = self._re_cache[pattern]
        else:
            flags = RE_FLAGS | (regexp.IGNORECASE if ignorecase else 0)
            re = regexp.compile(pattern, flags)
            self._re_cache[pattern] = re
        return re.match(self.text, self.pos + offset)
