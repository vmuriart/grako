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
def graken():
    def decorator(rule):
        @functools.wraps(rule)
        def wrapper(self):
            name = rule.__name__
            # remove the single leading and trailing underscore
            # that the parser generator added
            name = name[1:-1]
            return self._call(rule, name)

        return wrapper

    return decorator


class Parser(ParseContext):
    def _find_rule(self, name):
        rule = getattr(self, '_' + name + '_', None)
        if isinstance(rule, type(self._find_rule)):
            return rule
