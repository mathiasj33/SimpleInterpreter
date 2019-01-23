from src.syntaxtree import *
from src.mytoken import TokenType
from src.interpreter import Interpreter
from src.closure import Closure
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

    def test_functions_basics(self):
        # y:=1\nfun f(x) {ret x}
        tree = \
            Program([Assign(Identifier('y'),  Literal(1)), Fun(Identifier('f'), [Identifier('x')], Program([Ret(Identifier('x'))]))])
        interpreter = Interpreter(tree)
        self.assertEqual({'f': Closure(Identifier('f'), [Identifier('x')], Program([Ret(Identifier('x'))]), {'y': 1,
                         'f': Closure(Identifier('f'), [Identifier('x')], Program([Ret(Identifier('x'))]), {'y': 1})}), 'y': 1}, interpreter.interpret())

        # x:=2\nfun f(x) {y:=1\nret x ^ 2\nret x}\nx := f(x + 1)
        tree = \
            Program([Assign(Identifier('x'), Literal(2)), Fun(Identifier('f'), [Identifier('x')], Program([
                Assign(Identifier('y'), Literal(1)),
                Ret(Binary(Identifier('x'), TokenType.POW, Literal(2))), Ret(Identifier('x'))])),
            Assign(Identifier('x'), FunCall(Identifier('f'), [Binary(Identifier('x'), TokenType.PLUS, Literal(1))]))])
        interpreter = Interpreter(tree)
        self.assertEqual({'x': 9, 'f': Closure(Identifier('f'), [Identifier('x')], Program([
                Assign(Identifier('y'), Literal(1)),
                Ret(Binary(Identifier('x'), TokenType.POW, Literal(2))), Ret(Identifier('x'))]), {'x': 2,
              'f': Closure(Identifier('f'), [Identifier('x')], Program([
                Assign(Identifier('y'), Literal(1)),
                Ret(Binary(Identifier('x'), TokenType.POW, Literal(2))), Ret(Identifier('x'))]), {'x': 2})})}, interpreter.interpret())

        # x:=1\nfun f() {ret x}\nx:=2\ny := f()
        tree = \
            Program([Assign(Identifier('x'), Literal(1)),
                     Fun(Identifier('f'), [], Program([Ret(Identifier('x'))])),
                     Assign(Identifier('x'), Literal(2)),
                     Assign(Identifier('y'), FunCall(Identifier('f'), []))])
        interpreter = Interpreter(tree)
        self.assertEqual({'x': 2, 'f': Closure(Identifier('f'), [], Program([Ret(Identifier('x'))]), {'x': 1,
                          'f': Closure(Identifier('f'), [], Program([Ret(Identifier('x'))]), {'x': 1})}), 'y': 1}, interpreter.interpret())

    def test_functions_recursion(self):
        # fun f(a,b) {if a = 0 {ret b} else {ret f(a-1,b+1)}}\nx:=f(5,0)
        tree = \
            Program([
                Fun(Identifier('f'), [Identifier('a'), Identifier('b')], Program([
                    If(Comparison(Identifier('a'), TokenType.EQUAL, Literal(0)),
                       Program([Ret(Identifier('b'))]),
                       Program([Ret(FunCall(Identifier('f'),
                                            [Binary(Identifier('a'), TokenType.MINUS, Literal(1)),
                                             Binary(Identifier('b'), TokenType.PLUS, Literal(1))]))])
                       )
                ])),
                Assign(Identifier('x'), FunCall(Identifier('f'), [Literal(5), Literal(0)]))
            ])
        interpreter = Interpreter(tree)
        self.assertEqual(5, interpreter.interpret()['x'])
