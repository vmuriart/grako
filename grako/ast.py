# -*- coding: utf-8 -*-
"""
Define the AST class, a direct descendant of dict that's used during parsing
to store the values of named elements of grammar rules.
"""
from __future__ import absolute_import, division, unicode_literals

from grako.util import strtype, is_list, PY3


class AST(dict):
    _closed = False

    def __init__(self, *args, **kwargs):
        super(AST, self).__init__()
        self._order = []
        self._parseinfo = None

        self.update(*args, **kwargs)
        self._closed = True

    def iteritems(self):
        return ((k, self[k]) for k in self)

    def items(self):
        items = self.iteritems()
        return items if PY3 else list(items)

    def update(self, *args, **kwargs):
        def upairs(d):
            for k, v in d:
                self[k] = v

        for d in args:
            upairs(d)
        upairs(kwargs.items())

    def set(self, key, value):
        key = self._safekey(key)

        previous = self.get(key, None)
        if previous is None:
            super(AST, self).__setitem__(key, value)
            self._order.append(key)
        elif is_list(previous):
            previous.append(value)
        else:
            super(AST, self).__setitem__(key, [previous, value])
        return self

    def copy(self):
        return AST((k, v[:] if is_list(v) else v) for k, v in self.items())

    def __iter__(self):
        return iter(self._order)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __setattr__(self, name, value):
        super(AST, self).__setattr__(name, value)

    def __hasattribute__(self, name):
        if not isinstance(name, strtype):
            return False
        try:
            super(AST, self).__getattribute__(name)
            return True
        except AttributeError:
            return False

    def _safekey(self, key):
        while self.__hasattribute__(key):
            key += '_'
        return key
