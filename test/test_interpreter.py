from src.syntaxtree import *
from src.mytoken import TokenType
from src.interpreter import Interpreter
from unittest import TestCase

class TestInterpreter(TestCase):
    def test_arithmetic(self):
        # 5 * 2 + 3 * 8 ^ 2 * 2 - (10 / 5 - 2)
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
                                Literal(2)
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
                            Literal(10),
                            TokenType.DIV,
                            Literal(5)
                        ),
                        TokenType.MINUS,
                        Literal(2)
                    )
                )
            )
        interpreter = Interpreter(tree)
        self.assertEqual(394, interpreter.interpret())