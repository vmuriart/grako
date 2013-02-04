#!/usr/env/bin python
# -*- coding: utf-8 -*-
#
# CAVEAT UTILITOR
# This file was automatically generated by Grako.
#    https://bitbucket.org/apalala/grako/
# Any changes you make to it will be overwritten the
# next time the file is generated.
#

from __future__ import print_function, division, absolute_import, unicode_literals
from grako.parsing import * # @UnusedWildImport
from grako.exceptions import * # @UnusedWildImport

__version__ = '13.035.15.25.50'

class RegexParserRoot(Parser):
    def _START_(self):
        _e = None
        _e = self._call('EXPRE')
        self.ast.add('expre', _e)
        self._check_eof()
        
    def _EXPRE_(self):
        _e = None
        def choice2():
            _e = None
            with self._option():
                _e = self._call('CHOICE')
                return _e
            with self._option():
                _e = self._call('SEQUENCE')
                return _e
            self.error('no available options')
        _e = choice2()
        
    def _CHOICE_(self):
        _e = None
        _e = self._call('SEQUENCE')
        self.ast.add('opts', _e, force_list=True)
        def repeat4():
            _e = self._token('|')
            self._cut()
            _e = self._call('SEQUENCE')
            self.ast.add('opts', _e, force_list=True)
            return _e
        _e = self._repeat(repeat4, plus=True)
        
    def _SEQUENCE_(self):
        _e = None
        def repeat16():
            _e = self._call('TERM')
            return _e
        _e = self._repeat(repeat16, plus=True)
        self.ast.add('terms', _e)
        
    def _TERM_(self):
        _e = None
        def choice17():
            _e = None
            with self._option():
                _e = self._call('CLOSURE')
                return _e
            with self._option():
                _e = self._call('ATOM')
                return _e
            self.error('no available options')
        _e = choice17()
        
    def _CLOSURE_(self):
        _e = None
        _e = self._call('ATOM')
        self.ast.add('atom', _e)
        _e = self._token('*')
        self._cut()
        
    def _ATOM_(self):
        _e = None
        def choice20():
            _e = None
            with self._option():
                _e = self._call('SUBEXP')
                return _e
            with self._option():
                _e = self._call('LITERAL')
                return _e
            self.error('no available options')
        _e = choice20()
        
    def _SUBEXP_(self):
        _e = None
        _e = self._token('(')
        self._cut()
        _e = self._call('EXPRE')
        self.ast.add('expre', _e)
        _e = self._token(')')
        
    def _LITERAL_(self):
        _e = None
        _e = self._pattern('(?:\\\\.|[^|*\\\\()])+')
        
    


class AbstractRegexParser(AbstractParserMixin, RegexParserRoot):
    pass


class RegexParserBase(RegexParserRoot):
    def START(self, ast):
        return ast
    
    def EXPRE(self, ast):
        return ast
    
    def CHOICE(self, ast):
        return ast
    
    def SEQUENCE(self, ast):
        return ast
    
    def TERM(self, ast):
        return ast
    
    def CLOSURE(self, ast):
        return ast
    
    def ATOM(self, ast):
        return ast
    
    def SUBEXP(self, ast):
        return ast
    
    def LITERAL(self, ast):
        return ast
    

def main(filename, startrule):
    import json
    with open(filename) as f:
        text = f.read()
    parser = RegexParserBase(text, simple=True)
    ast = parser.parse(startrule)
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()

if __name__ == '__main__':
    import sys
    if '-l' in sys.argv:
        print('Rules:')
        for r in RegexParserBase.rule_list():
            print(r)
        print()
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print('Usage:')
        program = sys.argv[0].split('/')[-1]
        print(program, ' <filename> <startrule>')
        print(program, ' -l') # list rules
        print(program, ' -h')

