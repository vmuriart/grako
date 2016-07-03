# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from grako.tool import genmodel


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(DiagramTests)


def main():
    unittest.TextTestRunner(verbosity=2).run(suite())


if __name__ == '__main__':
    main()
