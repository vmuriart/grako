# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

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

if PY3:
    strtype = str
    basestring = None
    unicode = None
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


def notnone(value, default=None):
    return value if value is not None else default


def prune_dict(d, predicate):
    """Remove all items x where predicate(x, d[x])"""

    keys = [k for k, v in d.items() if predicate(k, v)]
    for k in keys:
        del d[k]
