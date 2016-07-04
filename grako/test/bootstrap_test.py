# -*- coding: utf-8 -*-
"""
This awkward set of tests tries to make Grako bang its head against iself.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import os
import pickle
import shutil
import sys
import unittest

from grako.model import DepthFirstWalker
from grako.parser import GrakoGrammarGenerator, GrakoParser
from grako.semantics import GrakoSemantics
from grako.grammars import COMMENTS_RE, EOL_COMMENTS_RE
from grako.codegen import codegen

TEST_DIR_PATH = os.path.dirname(__file__)
GRAKO_DIR_PATH = os.path.dirname(TEST_DIR_PATH)
REPO_DIR_PATH = os.path.dirname(GRAKO_DIR_PATH)

ETC_DIR_PATH = os.path.join(REPO_DIR_PATH, 'etc/')
TMP_DIR_PATH = os.path.join(REPO_DIR_PATH, 'tmp/')
sys.path.append(TMP_DIR_PATH)

class BootstrapTests(unittest.TestCase):

    def test_bootstrap(self):
        print()

        if os.path.isfile(TMP_DIR_PATH + '00.ast'):
            shutil.rmtree(TMP_DIR_PATH)
        if not os.path.isdir(TMP_DIR_PATH):
            os.mkdir(TMP_DIR_PATH)
        print('-' * 20, 'phase 00 - parse using the bootstrap grammar')
        with open(ETC_DIR_PATH + 'grako.ebnf') as f:
            text = str(f.read())
        g = GrakoParser('GrakoBootstrap')
        grammar0 = g.parse(text)
        ast0 = json.dumps(grammar0, indent=2)
        with open(TMP_DIR_PATH + '00.ast', 'w') as f:
            f.write(ast0)

        print('-' * 20, 'phase 01 - parse with parser generator')
        with open(ETC_DIR_PATH + 'grako.ebnf') as f:
            text = str(f.read())
        g = GrakoGrammarGenerator('GrakoBootstrap')
        g.parse(text, trace=False)

        generated_grammar1 = str(g.ast['start'])
        with open(TMP_DIR_PATH + '01.ebnf', 'w') as f:
            f.write(generated_grammar1)

        print('-' * 20, 'phase 02 - parse previous output with the parser generator')
        with open(TMP_DIR_PATH + '01.ebnf', 'r') as f:
            text = str(f.read())
        g = GrakoGrammarGenerator('GrakoBootstrap')
        g.parse(text, trace=False)
        generated_grammar2 = str(g.ast['start'])
        with open(TMP_DIR_PATH + '02.ebnf', 'w') as f:
            f.write(generated_grammar2)
        self.assertEqual(generated_grammar2, generated_grammar1)

        print('-' * 20, 'phase 03 - repeat')
        with open(TMP_DIR_PATH + '02.ebnf') as f:
            text = f.read()
        g = GrakoParser('GrakoBootstrap')
        ast3 = g.parse(text)
        with open(TMP_DIR_PATH + '03.ast', 'w') as f:
            f.write(json.dumps(ast3, indent=2))

        print('-' * 20, 'phase 04 - repeat')
        with open(TMP_DIR_PATH + '02.ebnf') as f:
            text = f.read()
        g = GrakoGrammarGenerator('GrakoBootstrap')
        g.parse(text)
        parser = g.ast['start']
        # pprint(parser.first_sets, indent=2, depth=3)
        generated_grammar4 = str(parser)
        with open(TMP_DIR_PATH + '04.ebnf', 'w') as f:
            f.write(generated_grammar4)
        self.assertEqual(generated_grammar4, generated_grammar2)

        print('-' * 20, 'phase 05 - parse using the grammar model')
        with open(TMP_DIR_PATH + '04.ebnf') as f:
            text = f.read()
        ast5 = parser.parse(text)
        with open(TMP_DIR_PATH + '05.ast', 'w') as f:
            f.write(json.dumps(ast5, indent=2))

        print('-' * 20, 'phase 06 - generate parser code')
        gencode6 = codegen(parser)
        with open(TMP_DIR_PATH + 'g06.py', 'w') as f:
            f.write(gencode6)

        print('-' * 20, 'phase 07 - import generated code')
        from g06 import GrakoBootstrapParser as GenParser  # @UnresolvedImport

        print('-' * 20, 'phase 08 - compile using generated code')
        parser = GenParser(trace=False)
        result = parser.parse(
            text,
            'start',
            comments_re=COMMENTS_RE,
            eol_comments_re=EOL_COMMENTS_RE
        )
        self.assertEqual(result, parser.ast['start'])
        ast8 = parser.ast['start']
        json8 = json.dumps(ast8, indent=2)
        open(TMP_DIR_PATH + '08.ast', 'w').write(json8)
        self.assertEqual(ast5, ast8)

        print('-' * 20, 'phase 09 - Generate parser with semantics')
        with open(ETC_DIR_PATH + 'grako.ebnf') as f:
            text = f.read()
        parser = GrakoGrammarGenerator('GrakoBootstrap')
        g9 = parser.parse(text)
        generated_grammar9 = str(g9)
        with open(TMP_DIR_PATH + '09.ebnf', 'w') as f:
            f.write(generated_grammar9)
        self.assertEqual(generated_grammar9, generated_grammar1)

        print('-' * 20, 'phase 10 - Parse with a model using a semantics')
        g10 = g9.parse(
            text,
            start_rule='start',
            semantics=GrakoSemantics('GrakoBootstrap')
        )
        generated_grammar10 = str(g10)
        with open(TMP_DIR_PATH + '10.ebnf', 'w') as f:
            f.write(generated_grammar10)
        gencode10 = codegen(g10)
        with open(TMP_DIR_PATH + 'g10.py', 'w') as f:
            f.write(gencode10)

        print('-' * 20, 'phase 11 - Pickle the model and try again.')
        with open(TMP_DIR_PATH + '11.grako', 'wb') as f:
            pickle.dump(g10, f, protocol=2)
        with open(TMP_DIR_PATH + '11.grako', 'rb') as f:
            g11 = pickle.load(f)
        r11 = g11.parse(
            text,
            start_rule='start',
            semantics=GrakoSemantics('GrakoBootstrap')
        )
        with open(TMP_DIR_PATH + '11.ebnf', 'w') as f:
            f.write(str(g11))
        gencode11 = codegen(r11)
        with open(TMP_DIR_PATH + 'g11.py', 'w') as f:
            f.write(gencode11)

        print('-' * 20, 'phase 12 - Walker')

        class PrintNameWalker(DepthFirstWalker):
            def __init__(self):
                self.walked = []

            def walk_default(self, o, children):
                self.walked.append(o.__class__.__name__)

        v = PrintNameWalker()
        v.walk(g11)
        with open(TMP_DIR_PATH + '12.txt', 'w') as f:
            f.write('\n'.join(v.walked))

        print('-' * 20, 'phase 13 - Graphics')
        try:
            from grako.diagrams import draw
        except ImportError:
            print('PyGraphViz not found!')
        else:
            draw('tmp/13.png', g11)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(BootstrapTests)


def main():
    unittest.TextTestRunner(verbosity=2).run(suite())

if __name__ == '__main__':
    main()
