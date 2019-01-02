from unittest import TestCase
from src.lexer import Lexer
from src.mytoken import MyToken, TokenType


class TestLexer(TestCase):

    def setUp(self):
        self.lexer = Lexer()

    def test_arithmetic(self):
        expected = [MyToken(TokenType.NUMBER, 5, 1), MyToken(TokenType.MUL, None, 1), MyToken(TokenType.NUMBER, 341, 1),
                    MyToken(TokenType.MINUS, None, 1), MyToken(TokenType.NUMBER, 4, 1), MyToken(TokenType.DIV, None, 1),
                    MyToken(TokenType.NUMBER, 81, 1), MyToken(TokenType.MUL, None, 1), MyToken(TokenType.LPAREN, None, 1),
                    MyToken(TokenType.NUMBER, 532, 1), MyToken(TokenType.PLUS, None, 1), MyToken(TokenType.NUMBER, 7, 1),
                    MyToken(TokenType.RPAREN, None, 1)]
        self.assertEqual(expected, self.lexer.lex('5 * 341 - 4 / 81 * (532 + 7)'))
