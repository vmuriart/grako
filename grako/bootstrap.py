#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals
from grako.parsing import graken, Parser, CheckSemanticsMixin
from grako.exceptions import *  # noqa


__version__ = '2014.06.08.17.44.12.06'

__all__ = [
    'GrakoBootstrapParser',
    'GrakoBootstrapSemanticParser',
    'GrakoBootstrapSemantics',
    'main'
]


class GrakoBootstrapParser(Parser):
    def __init__(self, whitespace=None, **kwargs):
        super(GrakoBootstrapParser, self).__init__(whitespace=whitespace, **kwargs)

    @graken()
    def _grammar_(self):

        def block1():
            self._rule_()
        self._positive_closure(block1)

        self.ast['@'] = self.last_node
        self._check_eof()

    @graken()
    def _paramdef_(self):
        with self._choice():
            with self._option():
                self._token('::')
                self._cut()
                self._params_()
                self.ast['params'] = self.last_node
            with self._option():
                self._token('(')
                self._cut()
                with self._group():
                    with self._choice():
                        with self._option():
                            self._kwparams_()
                            self.ast['kwparams'] = self.last_node
                        with self._option():
                            self._params_()
                            self.ast['params'] = self.last_node
                            self._token(',')
                            self._cut()
                            self._kwparams_()
                            self.ast['kwparams'] = self.last_node
                        with self._option():
                            self._params_()
                            self.ast['params'] = self.last_node
                        self._error('no available options')
                self._token(')')
            self._error('no available options')

        self.ast._define(
            ['params', 'kwparams'],
            []
        )

    @graken()
    def _rule_(self):
        self._new_name_()
        self.ast['name'] = self.last_node
        self._cut()
        with self._optional():
            with self._choice():
                with self._option():
                    self._token('::')
                    self._cut()
                    self._params_()
                    self.ast['params'] = self.last_node
                with self._option():
                    self._token('(')
                    self._cut()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._kwparams_()
                                self.ast['kwparams'] = self.last_node
                            with self._option():
                                self._params_()
                                self.ast['params'] = self.last_node
                                self._token(',')
                                self._cut()
                                self._kwparams_()
                                self.ast['kwparams'] = self.last_node
                            with self._option():
                                self._params_()
                                self.ast['params'] = self.last_node
                            self._error('no available options')
                    self._token(')')
                self._error('no available options')
        with self._optional():
            self._token('<')
            self._cut()
            self._known_name_()
            self.ast['base'] = self.last_node
        self._token('=')
        self._cut()
        self._expre_()
        self.ast['rhs'] = self.last_node
        self._token(';')
        self._cut()

        self.ast._define(
            ['name', 'params', 'kwparams', 'base', 'rhs'],
            []
        )

    @graken()
    def _params_(self):
        self._literal_()
        self.ast._append('@', self.last_node)

        def block1():
            self._token(',')
            self._literal_()
            self.ast._append('@', self.last_node)
        self._closure(block1)

    @graken()
    def _kwparams_(self):
        self._pair_()
        self.ast._append('@', self.last_node)

        def block1():
            self._token(',')
            self._pair_()
            self.ast._append('@', self.last_node)
        self._closure(block1)

    @graken()
    def _pair_(self):
        self._word_()
        self.ast._append('@', self.last_node)
        self._token('=')
        self._literal_()
        self.ast._append('@', self.last_node)

    @graken()
    def _expre_(self):
        with self._choice():
            with self._option():
                self._choice_()
            with self._option():
                self._sequence_()
            self._error('no available options')

    @graken()
    def _choice_(self):
        self._sequence_()
        self.ast._append('@', self.last_node)

        def block1():
            self._token('|')
            self._sequence_()
            self.ast._append('@', self.last_node)
        self._positive_closure(block1)

    @graken()
    def _sequence_(self):

        def block0():
            self._element_()
        self._positive_closure(block0)

    @graken()
    def _element_(self):
        with self._choice():
            with self._option():
                self._rule_include_()
            with self._option():
                self._named_()
            with self._option():
                self._override_list_()
            with self._option():
                self._override_()
            with self._option():
                self._term_()
            self._error('no available options')

    @graken()
    def _rule_include_(self):
        self._token('>')
        self._known_name_()
        self.ast['@'] = self.last_node

    @graken()
    def _named_(self):
        with self._choice():
            with self._option():
                self._named_list_()
            with self._option():
                self._named_single_()
            self._error('no available options')

    @graken()
    def _named_list_(self):
        self._name_()
        self.ast['name'] = self.last_node
        self._token('+:')
        self._element_()
        self.ast['value'] = self.last_node

        self.ast._define(
            ['name', 'value'],
            []
        )

    @graken()
    def _named_single_(self):
        self._name_()
        self.ast['name'] = self.last_node
        self._token(':')
        self._element_()
        self.ast['value'] = self.last_node

        self.ast._define(
            ['name', 'value'],
            []
        )

    @graken()
    def _override_list_(self):
        self._token('@+:')
        self._element_()
        self.ast['@'] = self.last_node

    @graken()
    def _override_(self):
        self._token('@:')
        self._element_()
        self.ast['@'] = self.last_node

    @graken()
    def _term_(self):
        with self._choice():
            with self._option():
                self._void_()
            with self._option():
                self._group_()
            with self._option():
                self._positive_closure_()
            with self._option():
                self._closure_()
            with self._option():
                self._optional_()
            with self._option():
                self._special_()
            with self._option():
                self._kif_()
            with self._option():
                self._knot_()
            with self._option():
                self._atom_()
            self._error('no available options')

    @graken()
    def _group_(self):
        self._token('(')
        self._expre_()
        self.ast['@'] = self.last_node
        self._token(')')
        self._cut()

    @graken()
    def _positive_closure_(self):
        self._token('{')
        self._expre_()
        self.ast['@'] = self.last_node
        self._token('}')
        with self._group():
            with self._choice():
                with self._option():
                    self._token('-')
                with self._option():
                    self._token('+')
                self._error('expecting one of: + -')
        self._cut()

    @graken()
    def _closure_(self):
        self._token('{')
        self._expre_()
        self.ast['@'] = self.last_node
        self._token('}')
        with self._optional():
            self._token('*')
        self._cut()

    @graken()
    def _optional_(self):
        self._token('[')
        self._expre_()
        self.ast['@'] = self.last_node
        self._token(']')
        self._cut()

    @graken()
    def _special_(self):
        self._token('?(')
        self._pattern(r'(.*)')
        self.ast['@'] = self.last_node
        self._token(')?')
        self._cut()

    @graken()
    def _kif_(self):
        self._token('&')
        self._term_()
        self.ast['@'] = self.last_node

    @graken()
    def _knot_(self):
        self._token('!')
        self._term_()
        self.ast['@'] = self.last_node

    @graken()
    def _atom_(self):
        with self._choice():
            with self._option():
                self._cut_()
            with self._option():
                self._token_()
            with self._option():
                self._call_()
            with self._option():
                self._pattern_()
            with self._option():
                self._eof_()
            self._error('no available options')

    @graken()
    def _call_(self):
        self._word_()

    @graken()
    def _void_(self):
        self._token('()')
        self._cut()

    @graken()
    def _cut_(self):
        self._token('~')
        self._cut()

    @graken()
    def _new_name_(self):
        self._name_()
        self._cut()

    @graken()
    def _known_name_(self):
        self._name_()
        self._cut()

    @graken()
    def _name_(self):
        self._word_()

    @graken()
    def _literal_(self):
        with self._choice():
            with self._option():
                self._token_()
            with self._option():
                self._number_()
            with self._option():
                self._word_()
            self._error('no available options')

    @graken()
    def _token_(self):
        with self._choice():
            with self._option():
                self._token('"')
                self._pattern(r'([^"\n]|\\"|\\\\)*')
                self.ast['@'] = self.last_node
                self._token('"')
            with self._option():
                self._token("'")
                self._pattern(r"([^'\n]|\\'|\\\\)*")
                self.ast['@'] = self.last_node
                self._token("'")
            self._error('expecting one of: " \'')

    @graken()
    def _number_(self):
        self._pattern(r'[0-9]+')

    @graken()
    def _word_(self):
        self._pattern(r'[-_A-Za-z0-9]+')

    @graken()
    def _pattern_(self):
        self._token('?/')
        self._pattern(r'(.*?)(?=/\?)')
        self.ast['@'] = self.last_node
        self._pattern(r'/\?+')
        self._cut()

    @graken()
    def _eof_(self):
        self._token('$')
        self._cut()


class GrakoBootstrapSemanticsCheck(CheckSemanticsMixin):
    pass


class GrakoBootstrapSemantics(object):
    def grammar(self, ast):
        return ast

    def paramdef(self, ast):
        return ast

    def rule(self, ast):
        return ast

    def params(self, ast):
        return ast

    def kwparams(self, ast):
        return ast

    def pair(self, ast):
        return ast

    def expre(self, ast):
        return ast

    def choice(self, ast):
        return ast

    def sequence(self, ast):
        return ast

    def element(self, ast):
        return ast

    def rule_include(self, ast):
        return ast

    def named(self, ast):
        return ast

    def named_list(self, ast):
        return ast

    def named_single(self, ast):
        return ast

    def override_list(self, ast):
        return ast

    def override(self, ast):
        return ast

    def term(self, ast):
        return ast

    def group(self, ast):
        return ast

    def positive_closure(self, ast):
        return ast

    def closure(self, ast):
        return ast

    def optional(self, ast):
        return ast

    def special(self, ast):
        return ast

    def kif(self, ast):
        return ast

    def knot(self, ast):
        return ast

    def atom(self, ast):
        return ast

    def call(self, ast):
        return ast

    def void(self, ast):
        return ast

    def cut(self, ast):
        return ast

    def new_name(self, ast):
        return ast

    def known_name(self, ast):
        return ast

    def name(self, ast):
        return ast

    def literal(self, ast):
        return ast

    def token(self, ast):
        return ast

    def number(self, ast):
        return ast

    def word(self, ast):
        return ast

    def pattern(self, ast):
        return ast

    def eof(self, ast):
        return ast


def main(filename, startrule, trace=False, whitespace=None):
    import json
    with open(filename) as f:
        text = f.read()
    parser = GrakoBootstrapParser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        whitespace=whitespace)
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()

if __name__ == '__main__':
    import argparse
    import string
    import sys

    class ListRules(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            print('Rules:')
            for r in GrakoBootstrapParser.rule_list():
                print(r)
            print()
            sys.exit(0)

    parser = argparse.ArgumentParser(description="Simple parser for GrakoBootstrap.")
    parser.add_argument('-l', '--list', action=ListRules, nargs=0,
                        help="list all rules and exit")
    parser.add_argument('-t', '--trace', action='store_true',
                        help="output trace information")
    parser.add_argument('-w', '--whitespace', type=str, default=string.whitespace,
                        help="whitespace specification")
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    parser.add_argument('startrule', metavar="STARTRULE",
                        help="the start rule for parsing")
    args = parser.parse_args()

    main(args.file, args.startrule, trace=args.trace, whitespace=args.whitespace)
