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
        # 5 ^ x + test123 * (7.2 - asd)
        tree = \
            Binary(
                Binary(
                    Literal(5),
                    TokenType.POW,
                    Identifier('x')
                ),
                TokenType.PLUS,
                Binary(
                    Identifier('test123'),
                    TokenType.MUL,
                    Grouping(
                        Binary(
                            Literal(7.2),
                            TokenType.MINUS,
                            Identifier('asd')
                        )
                    )
                )
            )
        env = {'x': -1, 'test123': 7, 'asd': -3}
        interpreter = Interpreter(env)
        self.assertAlmostEqual(71.6, interpreter.interpret_expr(tree))

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

    def test_strings(self):
        # x # ('test' # '123') # ''
        tree = \
            StringBinary(
                StringBinary(
                    Identifier('x'),
                    TokenType.HASH,
                    Grouping(
                        StringBinary(
                            Literal('test'),
                            TokenType.HASH,
                            Literal('123')
                        )
                    )
                ),
                TokenType.HASH,
                Literal('')
            )
        interpreter = Interpreter(Environment({'x': 'hello'}))
        self.assertEqual('hellotest123', interpreter.interpret_expr(tree))

        # 'asd' # 5 + 3 # true and false # x
        tree = \
            StringBinary(
                StringBinary(
                    StringBinary(
                        Literal('asd'),
                        TokenType.HASH,
                        Binary(
                            Literal(5),
                            TokenType.PLUS,
                            Literal(3)
                        )
                    ),
                    TokenType.HASH,
                    LogicalBinary(
                        Literal(True),
                        TokenType.AND,
                        Literal(False)
                    )
                ),
                TokenType.HASH,
                Identifier('x')
            )
        interpreter = Interpreter(Environment({'x': 'hello'}))
        self.assertEqual('asd8falsehello', interpreter.interpret_expr(tree))

        # 1.2
        tree = \
            StringBinary(Literal(1), TokenType.HASH, Literal(2))
        interpreter = Interpreter()
        self.assertEqual('12', interpreter.interpret_expr(tree))

    def test_assignment(self):
        tree = \
            Program([Assign(Identifier('x'), Literal(5.2)),
                     Assign(Identifier('y'), LogicalBinary(LogicalUnary(TokenType.NOT, Literal(True)), TokenType.OR, Literal(True))),
                     Assign(Identifier('z'), StringBinary(Literal('asd'), TokenType.HASH, Identifier('y')))])
        interpreter = Interpreter()
        env = interpreter.interpret(tree)
        self.assertAlmostEqual(5.2, env['x'])
        self.assertEqual(True, env['y'])
        self.assertEqual('asdtrue', env['z'])

    def test_print(self):
        tree = \
            Program([ExprStmt(FunCall(Identifier('print'), [Identifier('x')])), ExprStmt(FunCall(Identifier('print'),[
                LogicalBinary(Identifier('y'), TokenType.AND, Literal(False))])),
                     ExprStmt(FunCall(Identifier('print'), [Literal('asd')]))])
        env = {'x': 5, 'y': True}
        interpreter = Interpreter(env)
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            self.assertEqual(env, interpreter.interpret(tree))
            output = out.getvalue().strip()
            self.assertEqual(output, '5\nfalse\nasd')
        finally:
            sys.stdout = saved_stdout

    def test_control_structures(self):
        # x := 0\nif 2 < 3 {x := 5}
        tree = \
            Program([Assign(Identifier('x'), Literal(0)), If(Comparison(Literal(2), TokenType.L, Literal(3)),
                                                    Program([Assign(Identifier('x'), Literal(5))]), Program([]))])
        interpreter = Interpreter()
        self.assertEqual(5, interpreter.interpret(tree)['x'])

        # x := 0\nif 2 > 3 {x := 5}
        tree = \
            Program([Assign(Identifier('x'), Literal(0)), If(Comparison(Literal(3), TokenType.L, Literal(2)),
                                                    Program([Assign(Identifier('x'), Literal(5))]), Program([]))])
        interpreter = Interpreter()
        self.assertEqual(0, interpreter.interpret(tree)['x'])

        # x := 0\nwhile x < 10 {x := x + 1}\nb := x = 10
        tree = \
            Program([Assign(Identifier('x'), Literal(0)), While(Comparison(Identifier('x'), TokenType.L, Literal(10)),
                                                       Program([Assign(Identifier('x'), Binary(Identifier('x'), TokenType.PLUS, Literal(1)))])),
                     Assign(Identifier('b'), Comparison(Identifier('x'), TokenType.EQUAL, Literal(10)))])
        interpreter = Interpreter()
        env = interpreter.interpret(tree)
        self.assertEqual(10, env['x'])
        self.assertEqual(True, env['b'])

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

        # x:=1\nfun f() {x := 2}\nf()
        tree = \
            Program([Assign(Identifier('x'), Literal(1)), Fun(Identifier('f'), [], Program([
                Assign(Identifier('x'), Literal(2))
            ])),ExprStmt(FunCall(Identifier('f'), []))])
        interpreter = Interpreter()
        env = interpreter.interpret(tree)
        self.assertEqual(2, env['x'])

        # a := 'global'\nb1 := '1'\n b2 := '2'\nfun outer() {fun showA() {ret a}\nb1 := showA()\na := 'inner'\nb2 := showA()}\nouter()
        tree = \
            Program([Assign(Identifier('a'), Literal(
                'global')), Assign(Identifier('b1'), Literal(
                '1')),Assign(Identifier('b2'), Literal(
                '2')),Fun(Identifier('outer'), [],
                                Program([Fun(Identifier('showA'), [], Program([Ret(Identifier('a'))])),
                                         Assign(Identifier('b1'), FunCall(Identifier('showA'), [])),
                                         Assign(Identifier('a'), Literal('inner')),
                                         Assign(Identifier('b2'), FunCall(Identifier('showA'), []))])),
                     ExprStmt(FunCall(Identifier('outer'), []))])
        interpreter = Interpreter()
        env = interpreter.interpret(tree)
        self.assertEqual('global', env['b1'])
        self.assertEqual('inner', env['b2'])

        # fun f() {print(a)\na:=10}\na:=20\nf()\nprint(a)
        tree = \
            Program([Fun(Identifier('f'), [], Program(
                [ExprStmt(FunCall(Identifier('print'), [Identifier('a')])), Assign(Identifier('a'), Literal(10))])),
                     Assign(Identifier('a'), Literal(20)), ExprStmt(FunCall(Identifier('f'), [])),
                     ExprStmt(FunCall(Identifier('print'), [Identifier('a')]))])
        interpreter = Interpreter()
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            env = interpreter.interpret(tree)
            output = out.getvalue().strip()
            self.assertEqual('20\n10', output)
        finally:
            sys.stdout = saved_stdout

        # fun f(x) {x := 10\nret x}\n x:=5\ny := f(x)
        tree = \
            Program([Fun(Identifier('f'), [Identifier('x')], Program([
                Assign(Identifier('x'), Literal(10)), Ret(Identifier('x'))
            ])), Assign(Identifier('x'), Literal(5)), Assign(Identifier('y'), FunCall(Identifier('f'), [Identifier('x')]))])
        interpreter = Interpreter()
        env = interpreter.interpret(tree)
        self.assertEqual(5, env['x'])
        self.assertEqual(10, env['y'])

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

        # fun counter() {i := 0\nfun count() {i := i+1\nret i}\n ret count}\nc := counter()\na := c()\nb := c()
        tree = \
            Program([Fun(Identifier('counter'), [], Program([Assign(Identifier('i'), Literal(0)),
                                                             Fun(Identifier('count'), [], Program([Assign(
                                                                 Identifier('i'),
                                                                 Binary(Identifier('i'), TokenType.PLUS, Literal(1))),
                                                                                                   Ret(Identifier(
                                                                                                       'i'))])),
                                                             Ret(Identifier('count'))])),
                     Assign(Identifier('c'), FunCall(Identifier('counter'), [])),
                     Assign(Identifier('a'), FunCall(Identifier('c'), [])),
                     Assign(Identifier('b'), FunCall(Identifier('c'), []))])
        interpreter = Interpreter()
        env = interpreter.interpret(tree)
        self.assertEqual(1, env['a'])
        self.assertEqual(2, env['b'])

    def test_expression_statements(self):
        # fun f() {print(5)}\n10+4\nf()
        tree = \
            Program([Fun(Identifier('f'), [], Program([ExprStmt(FunCall(Identifier('print'), [Literal(5)]))])),
                     ExprStmt(Binary(Literal(10), TokenType.PLUS, Literal(4))), ExprStmt(FunCall(Identifier('f'), []))])
        interpreter = Interpreter()
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            interpreter.interpret(tree)
            output = out.getvalue().strip()
            self.assertEqual('5', output)
        finally:
            sys.stdout = saved_stdout

