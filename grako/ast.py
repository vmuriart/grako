# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
from collections import OrderedDict, Mapping
import json

__all__ = ['AST']

class AST(dict):
    """
    A dictionary with attribute-style access. It maps attribute access to
    the real dictionary.
    """
    # ActiveState Recipe:
    # http://code.activestate.com/recipes/473786-dictionary-with-attribute-style-access/

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __getstate__(self):
        return self.__dict__.items()

    def __setstate__(self, items):
        for key, val in items:
            self.__dict__[key] = val

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, dict.__repr__(self))

    def __setitem__(self, key, value):
        self.add(key, value)

    def __getitem__(self, name):
        if name in self:
            return super(AST, self).__getitem__(name)

    def __delitem__(self, name):
        return super(AST, self).__delitem__(name)

    __getattr__ = __getitem__
    __setattr__ = __setitem__

    def copy(self):
        ch = AST(self)
        return ch

    def add(self, key, value, force_list=False):
        previous = self[key]
        if previous is None:
            if force_list:
                return super(AST, self).__setitem__(key, [value])
            else:
                return super(AST, self).__setitem__(key, value)
        elif isinstance(previous, list):
            previous.append(value)
        else:
            return super(AST, self).__setitem__(key, [previous, value])

    def jsons(self, indent=2, **kwargs):
        return json.dumps(self, indent=indent, **kwargs)
