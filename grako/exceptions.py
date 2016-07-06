# -*- coding: utf-8 -*-
"""
Exceptions used in Grako parser generation and in generated parsers.

The parameters of the Failed... hierarchy of exceptions are the ones required
to be able to report accurate error messages as late as possible with the aid
of the .buffering.Buffer class, and with as little overhead as possible for
exceptions that will not be parsing errors (remember that Grako uses the
exception system to backtrack).
"""
from __future__ import absolute_import, unicode_literals


class GrakoException(Exception):
    pass


class OptionSucceeded(GrakoException):
    pass


class FailedParse(GrakoException):
    def __init__(self, item):
        self.item = item


class FailedLeftRecursion(FailedParse):
    pass
