# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import copyreg

from ..model import synth


__registry = dict()


def register_nodetype(nodetype):
    __registry[nodetype.__name__] = nodetype
    setattr(synth, nodetype.__name__, nodetype)


def find_nodetype(typename):
    return __registry.get(typename, None)


def _synthetize_type(typename, baseType):
    nodetype = type(typename, (baseType,), {})

    def pickle_nodetype(n):
        return nodetype, (), n.__init__
    copyreg.pickle(nodetype, pickle_nodetype)

    register_nodetype(nodetype)
    return nodetype


def get_nodetype(typename, baseType):
    typename = str(typename)
    nodetype = find_nodetype(typename)
    if nodetype is not None:
        return nodetype

    nodetype = _synthetize_type(typename, baseType)
    print('SYNTHNAME', typename, nodetype.__name__, nodetype.__module__)
    return nodetype
