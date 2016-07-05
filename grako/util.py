# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import codecs
import collections
import itertools
import sys

try:
    import regex as re

    WHITESPACE_RE = re.compile(r'\p{IsPattern_White_Space}+', re.UNICODE)
except ImportError:
    import re

    WHITESPACE_RE = re.compile(r'\s+', re.UNICODE)
RE_FLAGS = re.UNICODE | re.MULTILINE

PY3 = sys.version_info[0] >= 3
PY33 = PY3 and sys.version_info[1] >= 3

if PY3:
    strtype = str
    basestring = None
    unicode = None
    if PY33:
        from collections import abc

        Mapping = abc.Mapping
    else:
        Mapping = collections.Mapping
    zip_longest = itertools.zip_longest
    import builtins
else:
    strtype = basestring  # noqa
    Mapping = collections.Mapping
    zip_longest = itertools.izip_longest
    import __builtin__ as builtins
assert builtins


def is_list(o):
    return type(o) == list


def ustr(s):
    if PY3:
        return str(s)
    elif isinstance(s, unicode):
        return s
    elif isinstance(s, str):
        return unicode(s, 'utf-8')
    else:
        # FIXME: last case resource!  We don't know unicode, period.
        return ustr(s.__str__())


ESCAPE_SEQUENCE_RE = re.compile(
    r'''
    ( \\U........      # 8-digit Unicode escapes
    | \\u....          # 4-digit Unicode escapes
    | \\x..            # 2-digit Unicode escapes
    | \\[0-7]{1,3}     # Octal character escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''',
    re.UNICODE | re.VERBOSE
)


def eval_escapes(s):
    """
    Given a string, evaluate escape sequences starting with backslashes as
    they would be evaluated in Python source code. For a list of these
    sequences, see: https://docs.python.org/3/reference/lexical_analysis.html

    This is not the same as decoding the whole string with the 'unicode-escape'
    codec, because that provides no way to handle non-ASCII characters that are
    literally present in the string.
    """

    # by Rob Speer

    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)


def simplify_list(x):
    if isinstance(x, list) and len(x) == 1:
        return simplify_list(x[0])
    return x


def isiter(value):
    return (isinstance(value, collections.Iterable) and
            not isinstance(value, strtype))


def format_if(fmt, values):
    return fmt % values if values else ''


def notnone(value, default=None):
    return value if value is not None else default


def prune_dict(d, predicate):
    """Remove all items x where predicate(x, d[x])"""

    keys = [k for k, v in d.items() if predicate(k, v)]
    for k in keys:
        del d[k]
