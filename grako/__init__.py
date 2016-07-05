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

from grako.parsing import Parser, graken
from grako.buffering import RE_FLAGS, regexp

__version__ = '3.9.1'
__all__ = ['Parser', 'graken', 'RE_FLAGS', 'regexp']
