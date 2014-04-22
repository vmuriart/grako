# -*- coding: utf-8 -*-
"""
Define the AST class, a direct descendant of dict that's used during parsing
to store the values of named elements of grammar rules.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

__all__ = ['AST']


class AST(dict):
    """
    A dictionary with attribute-style access. It maps attribute access to
    the real dictionary.
    """
    # ActiveState Recipe:
    # http://code.activestate.com/recipes/473786-dictionary-with-attribute-style-access/

    def __getstate__(self):
        return self.__dict__.items()

    def __setstate__(self, items):
        for key, val in items:
            self.__dict__[key] = val

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, super(AST, self).__repr__())

    def __setitem__(self, key, value):
        self._add(key, value)

    def __getitem__(self, name):
        if name in self:
            return super(AST, self).__getitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def __getattribute__(self, name):
        if name in self:
            return self[name]
        return super(AST, self).__getattribute__(name)

    def _define(self, keys):
        return
        for key in keys:
            if not self.__contains__(key):
                super(AST, self).__setitem__(key, None)

    def _copy(self):
        haslists = any(isinstance(v, list) for v in self.values())
        if not haslists:
            return AST(self)
        return AST(
            (k, v[:] if isinstance(v, list) else v)
            for k, v in self.items()
        )

    def _add(self, key, value, force_list=False):
        previous = self[key]
        if previous is None:
            if force_list:
                super(AST, self).__setitem__(key, [value])
            else:
                super(AST, self).__setitem__(key, value)
        elif isinstance(previous, list):
            previous.append(value)
        else:
            super(AST, self).__setitem__(key, [previous, value])
        return self

    def _append(self, key, value):
        return self._add(key, value, force_list=True)

    @property
    def parseinfo(self):
        """ Make the special attribute `_parseinfo` be available
            as a property without an underscore in the name.
            This patch helps with backwards compatibility.
        """
        return self._parseinfo
