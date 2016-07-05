# -*- coding: utf-8 -*-
"""
The Buffer class provides the functionality required by a parser-driven lexer.

Line analysis and caching are done so the parser can freely move with goto(p)
to any position in the parsed text, and still recover accurate information
about source lines and content.
"""
from __future__ import absolute_import, unicode_literals

import sys
import re as regexp

RE_FLAGS = regexp.UNICODE | regexp.MULTILINE
RETYPE = type(regexp.compile('.'))

PY3 = sys.version_info[0] == 3
if PY3:
    unicode = None

    def ustr(s):
        return str(s)
else:
    unicode = unicode

    def ustr(s):
        if isinstance(s, unicode):
            return s
        elif isinstance(s, str):
            return unicode(s, 'utf-8')


class Buffer(object):
    def __init__(self, text, whitespace=None, eol_comments_re=None):
        self.text = ustr(text)
        self.whitespace_re = whitespace
        self.eol_comments_re = eol_comments_re

        self._pos = 0
        self._len = len(self.text)
        self._re_cache = {}

    @property
    def pos(self):
        return self._pos

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
        while self.matchre(self.whitespace_re):
            pass

    def eat_eol_comments(self):
        while self.matchre(self.eol_comments_re):
            pass

    def next_token(self):
        p = None
        while self._pos != p:
            p = self._pos
            self.eat_eol_comments()
            self.eat_whitespace()

    def is_name_char(self, c):
        return c is not None and c.isalnum()

    def match(self, token):
        p = self.pos
        # ignorecase == True
        result = self.text[p:p + len(token)].lower() == token.lower()

        if result:
            self.move(len(token))
            partial_match = (self.is_name_char(self.current()) and
                             token.isalnum() and token[0].isalpha())
            if not partial_match:
                return token
        self.goto(p)

    def matchre(self, pattern):
        matched = self._scanre(pattern)
        if matched:
            token = matched.group()
            self.move(len(token))
            return token

    def _scanre(self, pattern):
        if isinstance(pattern, RETYPE):
            re = pattern
        elif pattern in self._re_cache:
            re = self._re_cache[pattern]
        else:
            flags = RE_FLAGS | regexp.IGNORECASE
            re = regexp.compile(pattern, flags)
            self._re_cache[pattern] = re
        return re.match(self.text, self.pos)
