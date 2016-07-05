# -*- coding: utf-8 -*-

import pytest
from . import parser_base
from grako.ast import AST
from grako.exceptions import FailedParse

def test_basic():
    parser = parser_base.SqlParser(parseinfo=True)
    ast = parser.parse("""-- comment
              SELECT 1 a, 2 b, 3 c, d FROM dual t, triple WHERE 1 = 4
            """, rule_name='start')
    assert isinstance(ast, AST)


def test_fail():
    parser = parser_base.SqlParser(parseinfo=True)
    with pytest.raises(FailedParse):
        parser.parse("""-- comment
              SELECT 1 a, 2 b, 3 c, d FROM dual t, triple WHERE
            """, rule_name='start')

