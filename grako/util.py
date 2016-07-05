# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import sys
import re

RE_FLAGS = re.UNICODE | re.MULTILINE

PY3 = sys.version_info[0] == 3
if PY3:
    def ustr(s):
        return str(s)

    unicode = None

else:
    def ustr(s):
        if isinstance(s, unicode):
            return s
        elif isinstance(s, str):
            return unicode(s, 'utf-8')

    unicode = unicode
