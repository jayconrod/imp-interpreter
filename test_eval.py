import unittest
from imp_lexer import *
from imp_parser import *

class TestEvaluation(unittest.TestCase):
    def program_test(self, code, expected_env):
        tokens = imp_lex(code)
        result = imp_parse(tokens)
        self.assertNotEquals(None, result)
        program = result.value
        env = {}
        program.eval(env)
        self.assertEquals(expected_env, env)

    def test_assign(self):
        self.program_test('x := 1', {'x': 1})

    def test_compound(self):
        self.program_test('x := 1; y := 2', {'x': 1, 'y': 2})

    def test_if(self):
        self.program_test('if 1 < 2 then x := 1 else x := 2 end', {'x': 1})

    # def test_while(self):
    #     self.program_test('x := 10; y := 0; while x > 0 do y := y + 1 end', {'x': 0, 'y': 10})
