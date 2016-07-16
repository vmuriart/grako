from __future__ import absolute_import, unicode_literals

from grako import graken, Parser

KEYWORDS = {'SELECT',
            'FROM',
            'WHERE',
            }


class SqlParser(Parser):
    def __init__(self):
        super(SqlParser, self).__init__(eol_comments_re='--.*?$',
                                        keywords=KEYWORDS)

    @graken
    def _start_(self):
        self._equation_()
        self._check_eof()

    @graken
    def _integer_(self):
        self._pattern(r'\d+')

    @graken
    def _sign_(self):
        with self._choice():
            with self._option():
                self._token('+')
            with self._option():
                self._token('-')
            self._error('expecting one of: + -')

    @graken
    def _variable_(self):
        self._token('x')

    @graken
    def _comparison_(self):
        with self._choice():
            with self._option():
                self._token('=')
            with self._option():
                self._token('<')
            with self._option():
                self._token('>')
            self._error('expecting one of: < = >')

    @graken
    def _operation_(self):
        self._integer_()
        self._sign_()
        self._variable_()

    @graken
    def _term_(self):
        with self._choice():
            with self._option():
                self._integer_()
            with self._option():
                self._operation_()
            self._error('no available options')

    @graken
    def _equation_(self):
        self._term_()
        self._comparison_()
        self._term_()
