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
LineInfo = namedtuple('LineInfo',
                      ['filename', 'line', 'col', 'start', 'end', 'text'])


class Buffer(object):
    def __init__(self,
                 text,
                 filename=None,
                 whitespace=None,
                 tabwidth=None,
                 comments_re=None,
                 eol_comments_re=None,
                 ignorecase=False,
                 trace=False,
                 nameguard=None,
                 comment_recovery=False,
                 namechars='',
                 **kwargs):
        self.original_text = text
        self.text = ustr(text)
        self.filename = filename or ''

        self.whitespace = whitespace

        self.tabwidth = tabwidth
        self.comments_re = comments_re
        self.eol_comments_re = eol_comments_re
        self.ignorecase = ignorecase
        self.trace = True
        self.nameguard = (nameguard
                          if nameguard is not None
                          else bool(self.whitespace_re))
        self.comment_recovery = comment_recovery
        self.namechars = namechars
        self._namechar_set = set(namechars)

        self._pos = 0
        self._len = 0
        self._linecount = 0
        self._line_index = []
        self._comment_index = []
        self._preprocess()
        self._linecache = []
        self._build_line_cache()
        self._comment_index = [[] for _ in self._line_index]
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

    def _preprocess(self, *args, **kwargs):
        lines, index = self._preprocess_block(self.filename, self.text)
        self.text = ''.join(lines)
        self._line_index = index

    def _preprocess_block(self, name, block, **kwargs):
        lines = self.split_block_lines(name, block)
        index = self._block_index(name, len(lines))
        return self.process_block(name, lines, index, **kwargs)

    def _block_index(self, name, n):
        return list(zip(n * [name], range(n)))

    def split_block_lines(self, name, block, **kwargs):
        return block.splitlines(True)

    def process_block(self, name, lines, index, **kwargs):
        return lines, index

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
        return c is not None and c.isalnum() or c in self._namechar_set

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
            if not self.nameguard:
                return token
            else:
                partial_match = (
                    token.isalnum() and
                    token[0].isalpha() and
                    self.is_name_char(self.current())
                )
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
            re = regexp.compile(
                pattern,
                flags
            )
            self._re_cache[pattern] = re
        return re.match(self.text, self.pos + offset)

    def _build_line_cache(self):
        # The line cache holds the position of the last character
        # (counting from 0) in each line (counting from 1).  At the
        # head, we have an imaginary line 0 that ends at -1.
        lines = self.text.splitlines(True)
        i = -1
        n = 0
        cache = []
        for n, s in enumerate(lines):
            cache.append(PosLine(i, n))
            i += len(s)
        n += 1
        if lines and lines[-1][-1] in '\r\n':
            n += 1
        cache.append(PosLine(i, n))
        self._linecache = cache
        self._linecount = n
