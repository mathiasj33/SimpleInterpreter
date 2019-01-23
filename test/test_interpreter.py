from src.syntaxtree import *
from src.mytoken import TokenType
from src.interpreter import Interpreter
from src.environment import Environment
from src.function import Function
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
        interpreter = Interpreter()
        self.assertEqual(394, interpreter.interpret_expr(tree))

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
        interpreter = Interpreter(env)
        self.assertEqual(80, interpreter.interpret_expr(tree))

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
        interpreter = Interpreter()
        self.assertEqual(True, interpreter.interpret_expr(tree))

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
        interpreter = Interpreter()
        self.assertEqual(False, interpreter.interpret_expr(tree))

    def test_assignment(self):
        tree = \
            Program([Assign(Identifier('x'), Literal(5)),
             Assign(Identifier('y'), LogicalBinary(LogicalUnary(TokenType.NOT, Literal(True)), TokenType.OR, Literal(True)))])
        interpreter = Interpreter()
        self.assertEqual(Environment({'x': 5, 'y': True}), interpreter.interpret(tree))

    def test_print(self):
        tree = \
            Program([Print(Identifier('x')), Print(
                LogicalBinary(Identifier('y'), TokenType.AND, Literal(False)))])
        env = {'x': 5, 'y': True}
        interpreter = Interpreter(env)
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            self.assertEqual(env, interpreter.interpret(tree))
            output = out.getvalue().strip()
            self.assertEqual(output, '5\nfalse')
        finally:
            sys.stdout = saved_stdout

    def test_control_structures(self):
        # x := 0\nif 2 < 3 {x := 5}
        tree = \
            Program([Assign(Identifier('x'), Literal(0)), If(Comparison(Literal(2), TokenType.L, Literal(3)),
                                                    Program([Assign(Identifier('x'), Literal(5))]), Program([]))])
        interpreter = Interpreter()
        self.assertEqual(Environment({'x': 5}), interpreter.interpret(tree))

        # x := 0\nif 2 > 3 {x := 5}
        tree = \
            Program([Assign(Identifier('x'), Literal(0)), If(Comparison(Literal(3), TokenType.L, Literal(2)),
                                                    Program([Assign(Identifier('x'), Literal(5))]), Program([]))])
        interpreter = Interpreter()
        self.assertEqual(Environment({'x': 0}), interpreter.interpret(tree))

        # x := 0\nwhile x < 10 {x := x + 1}\nb := x = 10
        tree = \
            Program([Assign(Identifier('x'), Literal(0)), While(Comparison(Identifier('x'), TokenType.L, Literal(10)),
                                                       Program([Assign(Identifier('x'), Binary(Identifier('x'), TokenType.PLUS, Literal(1)))])),
                     Assign(Identifier('b'), Comparison(Identifier('x'), TokenType.EQUAL, Literal(10)))])
        interpreter = Interpreter()
        self.assertEqual(Environment({'x': 10, 'b': True}), interpreter.interpret(tree))

    def test_functions_basics(self):
        # x:=2\nfun f(x) {y:=1\nret x ^ 2\nret x}\nx := f(x + 1)
        tree = \
            Program([Assign(Identifier('x'), Literal(2)), Fun(Identifier('f'), [Identifier('x')], Program([
                Assign(Identifier('y'), Literal(1)),
                Ret(Binary(Identifier('x'), TokenType.POW, Literal(2))), Ret(Identifier('x'))])),
            Assign(Identifier('x'), FunCall(Identifier('f'), [Binary(Identifier('x'), TokenType.PLUS, Literal(1))]))])
        interpreter = Interpreter()
        env = interpreter.interpret(tree)
        self.assertEqual(9, env['x'])
        self.assertEqual(9, env['f'].env['x'])
        self.assertFalse('y' in env)

        # x:=1\nfun f() {ret x}\nx:=2\ny := f()
        tree = \
            Program([Assign(Identifier('x'), Literal(1)),
                     Fun(Identifier('f'), [], Program([Ret(Identifier('x'))])),
                     Assign(Identifier('x'), Literal(2)),
                     Assign(Identifier('y'), FunCall(Identifier('f'), []))])
        interpreter = Interpreter()
        env = interpreter.interpret(tree)
        self.assertEqual(2, env['y'])

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
        interpreter = Interpreter()
        self.assertEqual(5, interpreter.interpret(tree)['x'])

        # fun odd(n) {
        #     if n = 0 {
        #         ret false
        #     }
        #     ret even(n-1)
        # }
        #
        # fun even(n) {
        #     if n = 0 {
        #         ret true
        #     }
        #     ret odd(n-1)
        # }
        #
        # a := even(5)
        # b :=  odd(5)
        # c :=  even(10)
        # d :=  odd(10)
        tree = \
            Program([
                Fun(Identifier('odd'), [Identifier('n')], Program([
                    If(Comparison(Identifier('n'), TokenType.EQUAL, Literal(0)),
                       Program([Ret(Literal(False))]),
                       Program([])),
                    Ret(FunCall(Identifier('even'), [Binary(Identifier('n'), TokenType.MINUS, Literal(1))]))
                ])),
                Fun(Identifier('even'), [Identifier('n')], Program([
                    If(Comparison(Identifier('n'), TokenType.EQUAL, Literal(0)),
                       Program([Ret(Literal(True))]),
                       Program([])),
                    Ret(FunCall(Identifier('odd'), [Binary(Identifier('n'), TokenType.MINUS, Literal(1))]))
                ])),
                Assign(Identifier('a'), FunCall(Identifier('even'), [Literal(5)])),
                Assign(Identifier('b'), FunCall(Identifier('odd'), [Literal(5)])),
                Assign(Identifier('c'), FunCall(Identifier('even'), [Literal(10)])),
                Assign(Identifier('d'), FunCall(Identifier('odd'), [Literal(10)]))
            ])
        interpreter = Interpreter()
        env = interpreter.interpret(tree)
        self.assertEqual(False, env['a'])
        self.assertEqual(True, env['b'])
        self.assertEqual(True, env['c'])
        self.assertEqual(False, env['d'])

    def test_higher_order_functions(self):
        # fun f(g, x) {ret g(g(x))}\nfun g(x) {ret x+1}\ny:=f(g, 3)
        tree = \
            Program([Fun(Identifier('f'), [Identifier('g'), Identifier('x')],
                         Program([Ret(FunCall(Identifier('g'), [FunCall(Identifier('g'), [Identifier('x')])]))])),
                     Fun(Identifier('g'), [Identifier('x')],
                         Program([Ret(Binary(Identifier('x'), TokenType.PLUS, Literal(1)))])),
                     Assign(Identifier('y'), FunCall(Identifier('f'), [Identifier('g'), Literal(3)]))])
        interpreter = Interpreter()
        self.assertEqual(5, interpreter.interpret(tree)['y'])

        # fun f() {fun g() {ret 1}\nret g}\nx := f()()
        tree = \
            Program([Fun(Identifier('f'), [],
                         Program([Fun(Identifier('g'), [], Program([Ret(Literal(1))])), Ret(Identifier('g'))])),
                     Assign(Identifier('x'), FunCall(FunCall(Identifier('f'), []), []))])
        interpreter = Interpreter()
        env = interpreter.interpret(tree)
        self.assertEqual(1, env['x'])
        self.assertFalse('g' in env)

        # fun double(f) {fun g(x) {ret f(f(x))}\n ret g}\nfun g(x) {ret x+1}\nd:= double(g)\na:=d(3)\nb:=d(5)
        tree = \
            Program([Fun(Identifier('double'), [Identifier('f')], Program([Fun(Identifier('g'), [Identifier('x')],
                                                                               Program([Ret(FunCall(Identifier('f'), [
                                                                                   FunCall(Identifier('f'),
                                                                                           [Identifier('x')])]))])),
                                                                           Ret(Identifier('g'))])),
                     Fun(Identifier('g'), [Identifier('x')],
                         Program([Ret(Binary(Identifier('x'), TokenType.PLUS, Literal(1)))])),
                     Assign(Identifier('d'), FunCall(Identifier('double'), [Identifier('g')])),
                     Assign(Identifier('a'), FunCall(Identifier('d'), [Literal(3)])),
                     Assign(Identifier('b'), FunCall(Identifier('d'), [Literal(5)]))])
        interpreter = Interpreter()
        env = interpreter.interpret(tree)
        self.assertEqual(5, env['a'])
        self.assertEqual(7, env['b'])

    def test_expression_statements(self):
        # fun f() {print 5}\n10+4\nf()
        tree = \
            Program([Fun(Identifier('f'), [], Program([Print(Literal(5))])),
                     ExprStmt(Binary(Literal(10), TokenType.PLUS, Literal(4))), ExprStmt(FunCall(Identifier('f'), []))])
        interpreter = Interpreter()
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            interpreter.interpret(tree)
            output = out.getvalue().strip()
            self.assertEqual(output, '5')
        finally:
            sys.stdout = saved_stdout

