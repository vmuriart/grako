# -*- coding: utf-8 -*-

import pytest
from . import parser_base
from grako.exceptions import FailedParse


def test_basic():
    parser = parser_base.SqlParser()
    ast = parser.parse("""-- comment
              SELECT 1 a, 2 b, 3 c, d FROM dual t, triple WHERE 1 = 4""")
    assert isinstance(ast, list)


def test_fail():
    parser = parser_base.SqlParser()
    with pytest.raises(FailedParse):
        parser.parse("""-- comment
              SELECT 1 a, 2 b, 3 c, d FROM dual t, triple WHERE""")
