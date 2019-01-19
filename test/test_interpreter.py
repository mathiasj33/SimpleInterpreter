from src.syntaxtree import *
from src.mytoken import TokenType
from src.interpreter import Interpreter
from unittest import TestCase
import sys
from io import StringIO

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
        self.assertEqual(394, interpreter.interpret_expr())

    def test_identifiers(self):
        # 5 * x + test123 * (7 - asd)
        tree = \
            Binary(
                Binary(
                    Literal(5),
                    TokenType.MUL,
                    Identifier('x')
                ),
                TokenType.PLUS,
                Binary(
                    Identifier('test123'),
                    TokenType.MUL,
                    Grouping(
                        Binary(
                            Literal(7),
                            TokenType.MINUS,
                            Identifier('asd')
                        )
                    )
                )
            )
        env = {'x': 2, 'test123': 7, 'asd': -3}
        interpreter = Interpreter(tree, env)
        self.assertEqual(80, interpreter.interpret_expr())

    def test_booleans(self):
        # not true and false or not false
        tree = \
            LogicalBinary(
                LogicalBinary(
                    LogicalUnary(
                        TokenType.NOT,
                        Literal(True)
                    ),
                    TokenType.AND,
                    Literal(False)
                ),
                TokenType.OR,
                LogicalUnary(
                    TokenType.NOT,
                    Literal(False)
                )
            )
        interpreter = Interpreter(tree)
        self.assertEqual(True, interpreter.interpret_expr())

        # 5 <= 3 = 7 > 5 - 2
        tree = \
            Comparison(
                Comparison(
                    Literal(5),
                    TokenType.LE,
                    Literal(3)
                ),
                TokenType.EQUAL,
                Comparison(
                    Literal(7),
                    TokenType.G,
                    Binary(
                        Literal(5),
                        TokenType.MINUS,
                        Literal(2)
                    )
                )
            )
        interpreter = Interpreter(tree)
        self.assertEqual(False, interpreter.interpret_expr())

    def test_assignment(self):
        tree = \
            Program([Assign(Identifier('x'), Literal(5)),
             Assign(Identifier('y'), LogicalBinary(LogicalUnary(TokenType.NOT, Literal(True)), TokenType.OR, Literal(True)))])
        interpreter = Interpreter(tree)
        self.assertEqual({'x': 5, 'y': True}, interpreter.interpret())

    def test_print(self):
        tree = \
            Program([Print(Identifier('x')), Print(
                LogicalBinary(Identifier('y'), TokenType.AND, Literal(False)))])
        env = {'x': 5, 'y': True}
        interpreter = Interpreter(tree, env)
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            self.assertEqual(env, interpreter.interpret())
            output = out.getvalue().strip()
            self.assertEqual(output, '5\nfalse')
        finally:
            sys.stdout = saved_stdout

    def test_control_structures(self):
        # x := 0\nif 2 < 3 {x := 5}
        tree = \
            Program([Assign(Identifier('x'), Literal(0)), If(Comparison(Literal(2), TokenType.L, Literal(3)),
                                                    Program([Assign(Identifier('x'), Literal(5))]), Program([]))])
        interpreter = Interpreter(tree)
        self.assertEqual({'x': 5}, interpreter.interpret())

        # x := 0\nif 2 > 3 {x := 5}
        tree = \
            Program([Assign(Identifier('x'), Literal(0)), If(Comparison(Literal(3), TokenType.L, Literal(2)),
                                                    Program([Assign(Identifier('x'), Literal(5))]), Program([]))])
        interpreter = Interpreter(tree)
        self.assertEqual({'x': 0}, interpreter.interpret())

        # x := 0\nwhile x < 10 {x := x + 1}\nb := x = 10
        tree = \
            Program([Assign(Identifier('x'), Literal(0)), While(Comparison(Identifier('x'), TokenType.L, Literal(10)),
                                                       Program([Assign(Identifier('x'), Binary(Identifier('x'), TokenType.PLUS, Literal(1)))])),
                     Assign(Identifier('b'), Comparison(Identifier('x'), TokenType.EQUAL, Literal(10)))])
        interpreter = Interpreter(tree)
        self.assertEqual({'x': 10, 'b': True}, interpreter.interpret())
