# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import functools
import sys
import re

RE_FLAGS = re.UNICODE | re.MULTILINE

PY3 = sys.version_info[0] == 3
if PY3:
    def ustr(s):
        return str(s)

else:
    def ustr(s):
        if isinstance(s, unicode):
            return s
        elif isinstance(s, str):
            return unicode(s, 'utf-8')


# decorator for rule implementation methods
def graken(func_rule):
    @functools.wraps(func_rule)
    def wrapper(self):
        # remove the leading and trailing underscore the parser generator added
        name = func_rule.__name__[1:-1]
        return self._call(func_rule, name)

    return wrapper
