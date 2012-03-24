import sys
import unittest

if __name__ == '__main__':
    test_names = ['test_lexer', 'test_combinators', 'test_imp_parser', 'test_eval']
    suite = unittest.defaultTestLoader.loadTestsFromNames(test_names)
    result = unittest.TextTestRunner().run(suite)
