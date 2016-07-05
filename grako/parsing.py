# -*- coding: utf-8 -*-
"""
Parser is the base class for generated parsers and for the bootstrap parser
(the parser that parses Grako grammars).

Parser does memoization at the rule invocation level, and provides the
decorators, context managers, and iterators needed to make generated parsers
simple.

Parser is also in charge of dealing with comments, with the help of
the .buffering module.

Parser.parse() will take the text to parse directly, or an instance of the
.buffering.Buffer class.
"""
from __future__ import absolute_import, unicode_literals

import functools

from grako.contexts import ParseContext


# decorator for rule implementation methods
def graken(func_rule):
    @functools.wraps(func_rule)
    def wrapper(self):
        name = func_rule.__name__
        # remove the leading and trailing underscore the parser generator added
        name = name[1:-1]
        return self._call(func_rule, name)

    return wrapper


Parser = ParseContext
