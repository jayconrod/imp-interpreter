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
from combinators import *

id = Tag(ID)
integer = Tag(INT)
def keyword(s):
    return Reserved(s, RESERVED)

class TestCombinators(unittest.TestCase):
    def combinator_test(self, code, parser, expected):
        tokens = imp_lex(code)
        result = parser(tokens, 0)
        self.assertNotEquals(None, result)
        self.assertEquals(expected, result.value)

    def test_tag(self):
        self.combinator_test('if', Tag(RESERVED), 'if')

    def test_reserved(self):
        self.combinator_test('if', Reserved('if', RESERVED), 'if')

    def test_concat(self):
        parser = Concat(id, id)
        self.combinator_test('x y', parser, ('x', 'y'))

    def test_concat_sugar(self):
        parser = id + id
        self.combinator_test('x y', parser, ('x', 'y'))

    def test_concat_associativity(self):
        parser = id + id + id
        self.combinator_test('x y z', parser, (('x', 'y'), 'z'))

    def test_exp(self):
        separator = keyword('+') ^ (lambda x: lambda l, r: l + r)
        parser = Exp(id, separator)
        self.combinator_test('x', parser, 'x')
        self.combinator_test('x + y', parser, 'xy')
        self.combinator_test('x + y + z', parser, 'xyz')

    def test_exp_sugar(self):
        separator = keyword('+') ^ (lambda x: lambda l, r: l + r)
        parser = id * separator
        self.combinator_test('x + y + z', parser, 'xyz')

    def test_alternate(self):
        parser = Alternate(id, integer)
        self.combinator_test('x', parser, 'x')
        self.combinator_test('12', parser, '12')

    def test_alternate_sugar(self):
        parser = id | integer
        self.combinator_test('x', parser, 'x')

    def test_opt(self):
        parser = Opt(id)
        self.combinator_test('x', parser, 'x')
        self.combinator_test('12', parser, None)

    def test_rep(self):
        parser = Rep(id)
        self.combinator_test('', parser, [])
        self.combinator_test('x y z', parser, ['x', 'y', 'z'])

    def test_process(self):
        parser = Process(integer, int)
        self.combinator_test('12', parser, 12)

    def test_process_sugar(self):
        parser = integer ^ int
        self.combinator_test('12', parser, 12)

    def test_lazy(self):
        def get_parser():
            return id
        parser = Lazy(get_parser)
        self.combinator_test('x', parser, 'x')

    def test_phrase(self):
        parser = Phrase(id)
        self.combinator_test('x', parser, 'x')

