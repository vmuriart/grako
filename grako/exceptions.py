# -*- coding: utf-8 -*-
"""
Exceptions used in Grako parser generation and in generated parsers.

The parameters of the Failed... hierarchy of exceptions are the ones required
to be able to report accurate error messages as late as possible with the aid
of the .buffering.Buffer class, and with as little overhead as possible for
exceptions that will not be parsing errors (remember that Grako uses the
exception system to backtrack).
"""
from __future__ import absolute_import, division, unicode_literals


class GrakoException(Exception):
    pass


class OptionSucceeded(GrakoException):
    pass


class GrammarError(GrakoException):
    pass


class SemanticError(GrakoException):
    pass


class CodegenError(GrakoException):
    pass


class MissingSemanticFor(SemanticError):
    pass


class ParseError(GrakoException):
    pass


class FailedSemantics(ParseError):
    pass


class FailedKeywordSemantics(FailedSemantics):
    pass


class FailedParseBase(ParseError):
    def __init__(self, buf, stack, item):
        self.buf = buf
        self.stack = stack
        self.pos = buf.pos
        self.item = item


class FailedParse(FailedParseBase):
    pass


class FailedToken(FailedParse):
    def __init__(self, buf, stack, token):
        super(FailedToken, self).__init__(buf, stack, token)
        self.token = token


class FailedPattern(FailedParse):
    def __init__(self, buf, stack, pattern):
        super(FailedPattern, self).__init__(buf, stack, pattern)
        self.pattern = pattern


class FailedMatch(FailedParse):
    def __init__(self, buf, name, item):
        super(FailedMatch, self).__init__(buf, item)
        self.name = name


class FailedRef(FailedParseBase):
    def __init__(self, buf, stack, name):
        super(FailedRef, self).__init__(buf, stack, name)
        self.name = name


class FailedCut(FailedParse):
    def __init__(self, nested):
        super(FailedCut, self).__init__(nested.buf, nested.stack, nested.item)
        self.pos = nested.pos
        self.nested = nested


class FailedChoice(FailedParse):
    pass


class FailedLookahead(FailedParse):
    pass


class FailedLeftRecursion(FailedParse):
    pass
