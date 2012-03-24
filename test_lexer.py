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
from lexer import *

KEYWORD = 'KEYWORD'
INT = 'INT'
ID = 'ID'
token_exprs = [
    (r'[ \t\n]+', None),
    (r'#[^\n]*', None),
    (r'keyword', KEYWORD),
    (r'[0-9]+', INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID)
]

class TestLexer(unittest.TestCase):
    def lexer_test(self, code, expected):
        actual = lex(code, token_exprs)
        self.assertEquals(expected, actual)

    def test_empty(self):
        self.lexer_test('', [])

    def test_id(self):
        self.lexer_test('abc', [('abc', ID)])

    def test_keyword_first(self):
        self.lexer_test('keyword', [('keyword', KEYWORD)])

    def test_space(self):
        self.lexer_test(' ', [])

    def test_id_space(self):
        self.lexer_test('abc def', [('abc', ID), ('def', ID)])

        
    
    
