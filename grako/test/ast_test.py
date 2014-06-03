# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from grako.ast import AST


class ASTTests(unittest.TestCase):
    def test_ast(self):
        ast = AST()
        self.assertEquals([], list(ast.items()))
        self.assertTrue(hasattr(ast, '__json__'))

    def test_empty(self):
        ast = AST()
        self.assertIsNone(ast.name)

    def test_add(self):
        ast = AST()
        ast.name = 'hello'
        self.assertIsNotNone(ast.name)
        self.assertEqual('hello', ast.name)

        ast.name = 'world'
        self.assertEqual(['hello', 'world'], ast.name)
        self.assertEqual(['hello', 'world'], ast['name'])

        ast.value = 1
        self.assertEqual(1, ast.value)
        print(AST)

    def test_iter(self):
        ast = AST()
        ast.name = 'hello'
        ast.name = 'world'
        ast.value = 1
        self.assertEqual(['name', 'value'], list(ast))
        self.assertEqual([['hello', 'world'], 1], list(ast.values()))

