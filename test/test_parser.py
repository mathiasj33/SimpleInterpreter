from unittest import TestCase
from src.syntaxtree import *
from src.parser import Parser
from src.mytoken import MyToken, TokenType


class TestParser(TestCase):
    def test_arithmetic(self):
        # 5 * 2 + 3 * 8 ^ 4 ^ - 2 * 2 - (1 / 3 - 2)
        tokens = [MyToken(TokenType.NUMBER, 5, 1), MyToken(TokenType.MUL, None, 1), MyToken(TokenType.NUMBER, 2, 1),
                  MyToken(TokenType.PLUS, None, 1), MyToken(TokenType.NUMBER, 3, 1), MyToken(TokenType.MUL, None, 1),
                  MyToken(TokenType.NUMBER, 8, 1), MyToken(TokenType.POW, None, 1), MyToken(TokenType.NUMBER, 4, 1),
                  MyToken(TokenType.POW, None, 1), MyToken(TokenType.MINUS, None, 1), MyToken(TokenType.NUMBER, 2, 1),
                  MyToken(TokenType.MUL, None, 1), MyToken(TokenType.NUMBER, 2, 1), MyToken(TokenType.MINUS, None, 1),
                  MyToken(TokenType.LPAREN, None, 1), MyToken(TokenType.NUMBER, 1, 1), MyToken(TokenType.DIV, None, 1),
                  MyToken(TokenType.NUMBER, 3, 1), MyToken(TokenType.MINUS, None, 1), MyToken(TokenType.NUMBER, 2, 1),
                  MyToken(TokenType.RPAREN, None, 1)]
        parser = Parser(tokens)

        tree = \
            Binary(
                Binary(
                    Binary(
                        Literal(5),
                        TokenType.MUL,
                        Literal(2)
                    ),
                    TokenType.PLUS,
                    Binary(
                        Binary(
                            Literal(3),
                            TokenType.MUL,
                            Binary(
                                Literal(8),
                                TokenType.POW,
                                Binary(
                                    Literal(4),
                                    TokenType.POW,
                                    Unary(
                                        TokenType.MINUS,
                                        Literal(2)
                                    )
                                )
                            )
                        ),
                        TokenType.MUL,
                        Literal(2)
                    )
                ),
                TokenType.MINUS,
                Grouping(
                    Binary(
                        Binary(
                            Literal(1),
                            TokenType.DIV,
                            Literal(3)
                        ),
                        TokenType.MINUS,
                        Literal(2)
                    )
                )
            )

        self.assertEqual(tree, parser.parse())
