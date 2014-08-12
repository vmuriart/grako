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
from grako.parsing import graken, Parser


__version__ = (2014, 8, 12, 2, 36, 41, 1)

__all__ = [
    'GrakoBootstrapParser',
    'GrakoBootstrapSemantics',
    'main'
]


class GrakoBootstrapParser(Parser):
    def __init__(self, whitespace=None, nameguard=None, **kwargs):
        super(GrakoBootstrapParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            **kwargs
        )

    @graken('Grammar')
    def _grammar_(self):

        def block1():
            self._rule_()
        self._positive_closure(block1)

        self.ast['rules'] = self.last_node
        self._check_eof()

        self.ast._define(
            ['rules'],
            []
        )

    @graken()
    def _paramdef_(self):
        with self._choice():
            with self._option():
                self._token('::')
                self._cut()
                self._params_only_()
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

    @graken('Rule')
    def _rule_(self):
        self._new_name_()
        self.ast['name'] = self.last_node
        self._cut()
        with self._optional():
            with self._choice():
                with self._option():
                    self._token('::')
                    self._cut()
                    self._params_only_()
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
        self.ast['exp'] = self.last_node
        self._token(';')
        self._cut()

        self.ast._define(
            ['name', 'params', 'kwparams', 'base', 'exp'],
            []
        )

    @graken()
    def _params_(self):
        self._literal_()
        self.ast.setlist('@', self.last_node)

        def block1():
            self._token(',')
            self._literal_()
            self.ast.setlist('@', self.last_node)
            with self._ifnot():
                self._token('=')
        self._closure(block1)

    @graken()
    def _params_only_(self):
        self._literal_()
        self.ast.setlist('@', self.last_node)

        def block1():
            self._token(',')
            self._literal_()
            self.ast.setlist('@', self.last_node)
        self._closure(block1)

    @graken()
    def _kwparams_(self):
        self._pair_()
        self.ast.setlist('@', self.last_node)

        def block1():
            self._token(',')
            self._cut()
            self._pair_()
            self.ast.setlist('@', self.last_node)
        self._closure(block1)

    @graken()
    def _pair_(self):
        self._word_()
        self.ast.setlist('@', self.last_node)
        self._token('=')
        self._cut()
        self._literal_()
        self.ast.setlist('@', self.last_node)

    @graken()
    def _expre_(self):
        with self._choice():
            with self._option():
                self._choice_()
            with self._option():
                self._sequence_()
            self._error('no available options')

    @graken('Choice')
    def _choice_(self):
        self._sequence_()
        self.ast.setlist('@', self.last_node)

        def block1():
            self._token('|')
            self._cut()
            self._sequence_()
            self.ast.setlist('@', self.last_node)
        self._positive_closure(block1)

    @graken('Sequence')
    def _sequence_(self):

        def block1():
            self._element_()
        self._positive_closure(block1)

        self.ast['sequence'] = self.last_node

        self.ast._define(
            ['sequence'],
            []
        )

    @graken()
    def _element_(self):
        with self._choice():
            with self._option():
                self._rule_include_()
            with self._option():
                self._named_()
            with self._option():
                self._override_()
            with self._option():
                self._term_()
            self._error('no available options')

    @graken('RuleInclude')
    def _rule_include_(self):
        self._token('>')
        self._cut()
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

    @graken('NamedList')
    def _named_list_(self):
        self._name_()
        self.ast['name'] = self.last_node
        self._token('+:')
        self._cut()
        self._element_()
        self.ast['exp'] = self.last_node

        self.ast._define(
            ['name', 'exp'],
            []
        )

    @graken('Named')
    def _named_single_(self):
        self._name_()
        self.ast['name'] = self.last_node
        self._token(':')
        self._cut()
        self._element_()
        self.ast['exp'] = self.last_node

        self.ast._define(
            ['name', 'exp'],
            []
        )

    @graken()
    def _override_(self):
        with self._choice():
            with self._option():
                self._override_list_()
            with self._option():
                self._override_single_()
            with self._option():
                self._override_single_deprecated_()
            self._error('no available options')

    @graken('OverrideList')
    def _override_list_(self):
        self._token('@+:')
        self._cut()
        self._element_()
        self.ast['@'] = self.last_node

    @graken('Override')
    def _override_single_(self):
        self._token('@:')
        self._cut()
        self._element_()
        self.ast['@'] = self.last_node

    @graken('Override')
    def _override_single_deprecated_(self):
        self._token('@')
        self._cut()
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

    @graken('Group')
    def _group_(self):
        self._token('(')
        self._cut()
        self._expre_()
        self.ast['exp'] = self.last_node
        self._token(')')
        self._cut()

        self.ast._define(
            ['exp'],
            []
        )

    @graken('PositiveClosure')
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

    @graken('Closure')
    def _closure_(self):
        self._token('{')
        self._expre_()
        self.ast['@'] = self.last_node
        self._token('}')
        with self._optional():
            self._token('*')
        self._cut()

    @graken('Optional')
    def _optional_(self):
        self._token('[')
        self._cut()
        self._expre_()
        self.ast['@'] = self.last_node
        self._token(']')
        self._cut()

    @graken('Special')
    def _special_(self):
        self._token('?(')
        self._cut()
        self._pattern(r'.*?(?!\)\?)')
        self.ast['@'] = self.last_node
        self._token(')?')
        self._cut()

    @graken('Lookahead')
    def _kif_(self):
        self._token('&')
        self._cut()
        self._term_()
        self.ast['@'] = self.last_node

    @graken('NegativeLookahead')
    def _knot_(self):
        self._token('!')
        self._cut()
        self._term_()
        self.ast['@'] = self.last_node

    @graken()
    def _atom_(self):
        with self._choice():
            with self._option():
                self._cut_()
            with self._option():
                self._cut_deprecated_()
            with self._option():
                self._token_()
            with self._option():
                self._call_()
            with self._option():
                self._pattern_()
            with self._option():
                self._eof_()
            self._error('no available options')

    @graken('RuleRef')
    def _call_(self):
        self._word_()

    @graken('Void')
    def _void_(self):
        self._token('()')
        self._cut()

    @graken('Cut')
    def _cut_(self):
        self._token('~')
        self._cut()

    @graken('Cut')
    def _cut_deprecated_(self):
        self._token('>>')
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
                self._string_()
            with self._option():
                self._word_()
            with self._option():
                self._hex_()
            with self._option():
                self._float_()
            with self._option():
                self._int_()
            self._error('no available options')

    @graken('Token')
    def _token_(self):
        self._string_()

    @graken()
    def _string_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('"')
                    self._cut()
                    self._pattern(r'([^"\n]|\\"|\\\\)*')
                    self.ast['@'] = self.last_node
                    self._token('"')
                with self._option():
                    self._token("'")
                    self._cut()
                    self._pattern(r"([^'\n]|\\'|\\\\)*")
                    self.ast['@'] = self.last_node
                    self._token("'")
                self._error('expecting one of: " \'')
        self._cut()

    @graken()
    def _hex_(self):
        self._pattern(r'0[xX](\d|[a-fA-F])+')

    @graken()
    def _float_(self):
        with self._choice():
            with self._option():
                self._pattern(r'[-+]?\d+\.(?:\d*)?(?:[Ee][-+]?\d+)?')
            with self._option():
                self._pattern(r'[-+]?\d*\.\d+(?:[Ee][-+]?\d+)?')
            self._error('expecting one of: [-+]?\\d*\\.\\d+(?:[Ee][-+]?\\d+)? [-+]?\\d+\\.(?:\\d*)?(?:[Ee][-+]?\\d+)?')

    @graken()
    def _int_(self):
        self._pattern(r'[-+]?\d+')

    @graken()
    def _word_(self):
        self._pattern(r'(?!\d)\w+')

    @graken('Pattern')
    def _pattern_(self):
        with self._choice():
            with self._option():
                self._token('?/')
                self._cut()
                self._pattern(r'(.|\n)+?(?=/\?)')
                self.ast['@'] = self.last_node
                self._pattern(r'/\?+')
                self._cut()
            with self._option():
                self._token('/')
                self._cut()
                self._pattern(r'(.|\n)+?(?=/)')
                self.ast['@'] = self.last_node
                self._token('/')
                self._cut()
            self._error('expecting one of: / ?/')

    @graken('EOF')
    def _eof_(self):
        self._token('$')
        self._cut()


class GrakoBootstrapSemantics(object):
    def grammar(self, ast):
        return ast

    def paramdef(self, ast):
        return ast

    def rule(self, ast):
        return ast

    def params(self, ast):
        return ast

    def params_only(self, ast):
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

    def override(self, ast):
        return ast

    def override_list(self, ast):
        return ast

    def override_single(self, ast):
        return ast

    def override_single_deprecated(self, ast):
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

    def cut_deprecated(self, ast):
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

    def string(self, ast):
        return ast

    def hex(self, ast):
        return ast

    def float(self, ast):
        return ast

    def int(self, ast):
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

    main(
        args.file,
        args.startrule,
        trace=args.trace,
        whitespace=args.whitespace
    )
