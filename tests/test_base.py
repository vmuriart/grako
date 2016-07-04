# -*- coding: utf-8 -*-

import pytest
from . import parser_base
from grako.ast import AST

def test_basic():
    parser = parser_base.UnknownParser(parseinfo=True)
    ast = parser.parse('select 1 from dual', rule_name='start')
    assert isinstance(ast, AST)
    assert str(ast) == "AST({u'select': [u'SELECT', [u'1'], [u'FROM', [u'dual']]]})"
