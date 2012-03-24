# Copyright (c) 2011, Jay Conrod.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Jay Conrod nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL JAY CONROD BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest
from imp_lexer import *
from imp_parser import *

class TestImpParser(unittest.TestCase):
    def parser_test(self, code, parser, expected):
        tokens = imp_lex(code)
        result = parser(tokens, 0)
        self.assertNotEquals(None, result)
        self.assertEquals(expected, result.value)

    def test_precedence(self):
        def combine(op):
            if op == '*':
                return lambda l, r: int(l) * int(r)
            else:
                return lambda l, r: int(l) + int(r)
        levels = [['*'], ['+']]
        parser = precedence(num, levels, combine)
        self.parser_test('2 * 3 + 4', parser, 10)
        self.parser_test('2 + 3 * 4', parser, 14)

    def test_aexp_num(self):
        self.parser_test('12', aexp(), IntAexp(12))

    def test_aexp_var(self):
        self.parser_test('x', aexp(), VarAexp('x'))

    def test_aexp_group(self):
        self.parser_test('(12)', aexp(), IntAexp(12))

    def test_aexp_binop(self):
        code = '2 * 3 + 4'
        expected = BinopAexp('+', BinopAexp('*', IntAexp(2), IntAexp(3)), IntAexp(4))
        self.parser_test('2 * 3 + 4', aexp(), expected)

    def test_aexp_binop_group(self):
        code = '2 * (3 + 4)'
        expected = BinopAexp('*', IntAexp(2), BinopAexp('+', IntAexp(3), IntAexp(4)))
        self.parser_test(code, aexp(), expected)

    def test_bexp_relop(self):
        self.parser_test('2 < 3', bexp(), RelopBexp('<', IntAexp(2), IntAexp(3)))

    def test_bexp_not(self):
        self.parser_test('not 2 < 3', bexp(), NotBexp(RelopBexp('<', IntAexp(2), IntAexp(3))))

    def test_bexp_and(self):
        expected = AndBexp(RelopBexp('<', IntAexp(2), IntAexp(3)), RelopBexp('<', IntAexp(3), IntAexp(4)))
        self.parser_test('2 < 3 and 3 < 4', bexp(), expected)

    def test_bexp_logic(self):
        code = '1 < 2 and 3 < 4 or 5 < 6'
        expected = OrBexp(AndBexp(RelopBexp('<', IntAexp(1), IntAexp(2)), 
                                  RelopBexp('<', IntAexp(3), IntAexp(4))),
                          RelopBexp('<', IntAexp(5), IntAexp(6)))
        self.parser_test(code, bexp(), expected)

    def test_bexp_logic_group(self):
        code = '1 < 2 and (3 < 4 or 5 < 6)'
        expected = AndBexp(RelopBexp('<', IntAexp(1), IntAexp(2)),
                           OrBexp(RelopBexp('<', IntAexp(3), IntAexp(4)),
                                  RelopBexp('<', IntAexp(5), IntAexp(6))))
        self.parser_test(code, bexp(), expected)

    def test_bexp_not_precedence(self):
        code = 'not 1 < 2 and 3 < 4'
        expected = AndBexp(NotBexp(RelopBexp('<', IntAexp(1), IntAexp(2))), 
                           RelopBexp('<', IntAexp(3), IntAexp(4)))
        self.parser_test(code, bexp(), expected)

    def test_assign_stmt(self):
        self.parser_test('x := 1', stmt_list(), AssignStatement('x', IntAexp(1)))

    def test_if_stmt(self):
        code = 'if 1 < 2 then x := 3 else x := 4 end'
        expected = IfStatement(RelopBexp('<', IntAexp(1), IntAexp(2)),
                               AssignStatement('x', IntAexp(3)),
                               AssignStatement('x', IntAexp(4)))
        self.parser_test(code, stmt_list(), expected)

    def test_while_stmt(self):
        code = 'while 1 < 2 do x := 3 end'
        expected = WhileStatement(RelopBexp('<', IntAexp(1), IntAexp(2)),
                                  AssignStatement('x', IntAexp(3)))
        self.parser_test(code, stmt_list(), expected)

    def test_compound_stmt(self):
        code = 'x := 1; y := 2'
        expected = CompoundStatement(AssignStatement('x', IntAexp(1)),
                                     AssignStatement('y', IntAexp(2)))
        self.parser_test(code, stmt_list(), expected)
