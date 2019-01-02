from unittest import TestCase
from src.lexer import Lexer
from src.mytoken import MyToken, TokenType


class TestLexer(TestCase):
    def test_arithmetic(self):
        lexer = Lexer('5 *  341 - 4 / 81*(532 + -7)   51  \n     423 12')
        expected = [MyToken(TokenType.NUMBER, 5, 1), MyToken(TokenType.MUL, None, 1), MyToken(TokenType.NUMBER, 341, 1),
                    MyToken(TokenType.MINUS, None, 1), MyToken(TokenType.NUMBER, 4, 1), MyToken(TokenType.DIV, None, 1),
                    MyToken(TokenType.NUMBER, 81, 1), MyToken(TokenType.MUL, None, 1), MyToken(TokenType.LPAREN, None, 1),
                    MyToken(TokenType.NUMBER, 532, 1), MyToken(TokenType.PLUS, None, 1), MyToken(TokenType.MINUS, None, 1),
                    MyToken(TokenType.NUMBER, 7, 1), MyToken(TokenType.RPAREN, None, 1), MyToken(TokenType.NUMBER, 51, 1),
                    MyToken(TokenType.EOL, None, 1), MyToken(TokenType.NUMBER, 423, 2), MyToken(TokenType.NUMBER, 12, 2)]
        self.assertEqual(expected, lexer.lex())
