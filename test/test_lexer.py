from unittest import TestCase
from src.lexer import Lexer
from src.mytoken import MyToken, TokenType

class TestLexer(TestCase):
    def test_arithmetic(self):
        lexer = Lexer('5 *  341 - 4 / 81*(532 + -7)   51  \n  ^   423 12')
        expected = [MyToken(TokenType.NUMBER, '5', 5, 1), MyToken(TokenType.MUL, '*', None, 1),
                    MyToken(TokenType.NUMBER, '341', 341, 1),
                    MyToken(TokenType.MINUS, '-', None, 1), MyToken(TokenType.NUMBER, '4', 4, 1),
                    MyToken(TokenType.DIV, '/', None, 1),
                    MyToken(TokenType.NUMBER, '81', 81, 1), MyToken(TokenType.MUL, '*', None, 1),
                    MyToken(TokenType.LPAREN, '(', None, 1),
                    MyToken(TokenType.NUMBER, '532', 532, 1), MyToken(TokenType.PLUS, '+', None, 1),
                    MyToken(TokenType.MINUS, '-', None, 1),
                    MyToken(TokenType.NUMBER, '7', 7, 1), MyToken(TokenType.RPAREN, ')', None, 1),
                    MyToken(TokenType.NUMBER, '51', 51, 1),
                    MyToken(TokenType.EOL, None, None, 1), MyToken(TokenType.POW, '^', None, 2),
                    MyToken(TokenType.NUMBER, '423', 423, 2),
                    MyToken(TokenType.NUMBER, '12', 12, 2)]
        self.assertEqual(expected, lexer.lex())

    def test_identifiers(self):
        lexer = Lexer('x + 7 - test123( 18 x x18 /_try-')
        expected = [MyToken(TokenType.IDENT, 'x', 'x', 1), MyToken(TokenType.PLUS, '+', None, 1),
                    MyToken(TokenType.NUMBER, '7', 7, 1), MyToken(TokenType.MINUS, '-', None, 1),
                    MyToken(TokenType.IDENT, 'test123', 'test123', 1), MyToken(TokenType.LPAREN, '(', None, 1),
                    MyToken(TokenType.NUMBER, '18', 18, 1), MyToken(TokenType.IDENT, 'x', 'x', 1),
                    MyToken(TokenType.IDENT, 'x18', 'x18', 1), MyToken(TokenType.DIV, '/', None, 1),
                    MyToken(TokenType.IDENT, '_try', '_try', 1), MyToken(TokenType.MINUS, '-', None, 1)]
        self.assertEqual(expected, lexer.lex())

    def test_keyword(self):
        lexer = Lexer('if x {}\nelse elses i ifs} while{ print printx _print')
        expected = \
        [MyToken(TokenType.IF, 'if', None, 1), MyToken(TokenType.IDENT, 'x', 'x', 1), MyToken(TokenType.LCURLY, '{', None, 1),
         MyToken(TokenType.RCURLY, '}', None, 1), MyToken(TokenType.EOL, None, None, 1), MyToken(TokenType.ELSE, 'else', None, 2),
         MyToken(TokenType.IDENT, 'elses', 'elses', 2), MyToken(TokenType.IDENT, 'i', 'i', 2), MyToken(TokenType.IDENT, 'ifs', 'ifs', 2),
         MyToken(TokenType.RCURLY, '}', None, 2), MyToken(TokenType.WHILE, 'while', None, 2), MyToken(TokenType.LCURLY, '{', None, 2),
         MyToken(TokenType.PRINT, 'print', None, 2), MyToken(TokenType.IDENT, 'printx', 'printx', 2), MyToken(TokenType.IDENT, '_print', '_print', 2)]
        self.assertEqual(expected, lexer.lex())

    def test_assignment(self):
        lexer = Lexer('x:= 7\nx = 7')
        expected = [MyToken(TokenType.IDENT, 'x', 'x', 1), MyToken(TokenType.ASSIGN, ':=', None, 1), MyToken(TokenType.NUMBER, '7', 7, 1),
                    MyToken(TokenType.EOL, None, None, 1), MyToken(TokenType.IDENT, 'x', 'x', 2), MyToken(TokenType.EQUAL, '=', None, 2),
                    MyToken(TokenType.NUMBER, '7', 7, 2)]
        self.assertEqual(expected, lexer.lex())

    def test_booleans(self):
        lexer = Lexer('true false trues = true 7 < 12 <= > y>=x or xor and not_ < not true')
        expected = \
        [MyToken(TokenType.TRUE, 'true', True, 1), MyToken(TokenType.FALSE, 'false', False, 1), MyToken(TokenType.IDENT, 'trues', 'trues', 1),
         MyToken(TokenType.EQUAL, '=', None, 1), MyToken(TokenType.TRUE, 'true', True, 1), MyToken(TokenType.NUMBER, '7', 7, 1),
         MyToken(TokenType.L, '<', None, 1), MyToken(TokenType.NUMBER, '12', 12, 1), MyToken(TokenType.LE, '<=', None, 1),
         MyToken(TokenType.G, '>', None, 1), MyToken(TokenType.IDENT, 'y', 'y', 1), MyToken(TokenType.GE, '>=', None, 1), MyToken(TokenType.IDENT, 'x', 'x', 1),
         MyToken(TokenType.OR, 'or', None, 1), MyToken(TokenType.IDENT, 'xor', 'xor', 1), MyToken(TokenType.AND, 'and', None, 1),
         MyToken(TokenType.IDENT, 'not_', 'not_', 1), MyToken(TokenType.L, '<', None, 1), MyToken(TokenType.NOT, 'not', None, 1),
         MyToken(TokenType.TRUE, 'true', True, 1)]
        self.assertEqual(expected, lexer.lex())