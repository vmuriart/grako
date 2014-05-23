# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import collections
import sys
import datetime

__all__ = ['simplify_list', 'trim', 'indent']

if sys.version_info[0] >= 3:
    strtype = str  # @ReservedAssignmet
else:
    strtype = basestring


def to_list(o):
    if o is None:
        return []
    elif isinstance(o, list):
        return o
    else:
        return [o]


def ustr(s):
    if sys.version_info[0] >= 3:
        return str(s)
    elif isinstance(s, str):
        return s.decode('utf-8')
    else:
        return unicode(s)


def udecode(s):
    if sys.version_info[0] >= 3:
        return str(s)
    else:
        if not isinstance(s, str):
            s = ustr(s)
        return s.encode('utf-8')


def simplify_list(x):
    if isinstance(x, list) and len(x) == 1:
        return simplify_list(x[0])
    return x


def isiter(value):
    return isinstance(value, collections.Iterable) and not isinstance(value, strtype)


def trim(text, tabwidth=4):
    """
    Trim text of common, leading whitespace.

    Based on the trim algorithm of PEP 257:
        http://www.python.org/dev/peps/pep-0257/
    """
    if not text:
        return ''
    lines = text.expandtabs(tabwidth).splitlines()
    maxindent = len(text)
    indent = maxindent
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    trimmed = [lines[0].strip()] + [line[indent:].rstrip() for line in lines[1:]]
    i = 0
    while i < len(trimmed) and not trimmed[i]:
        i += 1
    return '\n'.join(trimmed[i:])


def indent(text, indent=1, multiplier=4):
    """ Indent the given block of text by indent*4 spaces
    """
    if text is None:
        return ''
    text = ustr(text)
    if indent >= 0:
        sindent = ' ' * multiplier * indent
        text = '\n'.join((sindent + t).rstrip() for t in text.splitlines())
    return text


def format_if(fmt, values):
    return fmt % values if values else ''


def notnone(value, default=None):
    return value if value is not None else default


def timestamp():
    return '.'.join(str(t) for t in datetime.datetime.utcnow().utctimetuple())
