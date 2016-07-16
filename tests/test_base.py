# -*- coding: utf-8 -*-

import pytest
from . import parser_base2003 as parser_base
from . import simple_parser_base as bse
from grako.exceptions import FailedParse


def test_simple():
    parser = bse.SqlParser()
    parser.parse('1=1+1')

def test_basic():
    parser = parser_base.SqlParser()
    ast = parser.parse("""\
        -- comment
        SELECT a a,dual.b, triple.c as r, 2 b, 3 c, d
        FROM dual t, triple WHERE 1 = 4""")
    assert isinstance(ast, list)
    ast = parser.parse("""SELECT a, 1 , b FROM dual WHERE 1 = 4;
select 1 from dual
""")
    print ast

def test_fail():
    parser = parser_base.SqlParser()
    with pytest.raises(FailedParse):
        parser.parse("""\
            -- comment
            SELECT 1 a, 2 b, 3 c, d FROM dual t, triple WHERE""")
