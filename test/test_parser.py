from unittest import TestCase
from src.syntaxtree import *
from src.parser import Parser
from src.mytoken import MyToken, TokenType

class TestParser(TestCase):
    def test_arithmetic(self):
        # 5 * 2 + 3 * 8 ^ 4 ^ - 2 * 2 - (1 / 3 - 2)
        tokens = [MyToken(TokenType.NUMBER, '5', 5, 1), MyToken(TokenType.MUL, '*', None, 1),
                  MyToken(TokenType.NUMBER, '2', 2, 1), MyToken(TokenType.PLUS, '+', None, 1),
                  MyToken(TokenType.NUMBER, '3', 3, 1), MyToken(TokenType.MUL, '*', None, 1),
                  MyToken(TokenType.NUMBER, '8', 8, 1), MyToken(TokenType.POW, '^', None, 1),
                  MyToken(TokenType.NUMBER, '4', 4, 1), MyToken(TokenType.POW, '^', None, 1),
                  MyToken(TokenType.MINUS, '-', None, 1), MyToken(TokenType.NUMBER, '2', 2, 1),
                  MyToken(TokenType.MUL, '*', None, 1), MyToken(TokenType.NUMBER, '2', 2, 1),
                  MyToken(TokenType.MINUS, '-', None, 1), MyToken(TokenType.LPAREN, '(', None, 1),
                  MyToken(TokenType.NUMBER, '1', 1, 1), MyToken(TokenType.DIV, '/', None, 1),
                  MyToken(TokenType.NUMBER, '3', 3, 1), MyToken(TokenType.MINUS, '-', None, 1),
                  MyToken(TokenType.NUMBER, '2', 2, 1), MyToken(TokenType.RPAREN, ')', None, 1)]
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

        self.assertEqual(tree, parser.parse_expr())

    def test_identifiers(self):
        # 5 * x + test123 * (7 - asd)
        tokens = [MyToken(TokenType.NUMBER, '5', 5, 1), MyToken(TokenType.MUL, '*', None, 1),
                  MyToken(TokenType.IDENT, 'x', 'x', 1), MyToken(TokenType.PLUS, '+', None, 1),
                  MyToken(TokenType.IDENT, 'test123', 'test123', 1), MyToken(TokenType.MUL, '*', None, 1),
                  MyToken(TokenType.LPAREN, '(', None, 1),
                  MyToken(TokenType.NUMBER, '7', 7, 1), MyToken(TokenType.MINUS, '-', None, 1),
                  MyToken(TokenType.IDENT, 'asd', 'asd', 1), MyToken(TokenType.RPAREN, ')', None, 1)]
        parser = Parser(tokens)
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

        self.assertEqual(tree, parser.parse_expr())

    def test_booleans(self):
        # (x or true and false) and not y or not z = 7 > 5 - 2 and y < 5 and t or 5 + 1 >= 10
        tokens = \
            [MyToken(TokenType.LPAREN, '(', None, 1), MyToken(TokenType.IDENT, 'x', 'x', 1),
             MyToken(TokenType.OR, 'or', None, 1), MyToken(TokenType.TRUE, 'true', True, 1),
             MyToken(TokenType.AND, 'and', None, 1), MyToken(TokenType.FALSE, 'false', False, 1),
             MyToken(TokenType.RPAREN, ')', None, 1), MyToken(TokenType.AND, 'and', None, 1),
             MyToken(TokenType.NOT, 'not', None, 1), MyToken(TokenType.IDENT, 'y', 'y', 1),
             MyToken(TokenType.OR, 'or', None, 1), MyToken(TokenType.NOT, 'not', None, 1),
             MyToken(TokenType.IDENT, 'z', 'z', 1), MyToken(TokenType.EQUAL, '=', None, 1),
             MyToken(TokenType.NUMBER, '7', 7, 1), MyToken(TokenType.G, '>', None, 1),
             MyToken(TokenType.NUMBER, '5', 5, 1), MyToken(TokenType.MINUS, '-', None, 1),
             MyToken(TokenType.NUMBER, '2', 2, 1), MyToken(TokenType.AND, 'and', None, 1),
             MyToken(TokenType.IDENT, 'y', 'y', 1), MyToken(TokenType.L, '<', None, 1),
             MyToken(TokenType.NUMBER, '5', 5, 1), MyToken(TokenType.AND, 'and', None, 1),
             MyToken(TokenType.IDENT, 't', 't', 1), MyToken(TokenType.OR, 'or', None, 1),
             MyToken(TokenType.NUMBER, '5', 5, 1), MyToken(TokenType.PLUS, '+', None, 1),
             MyToken(TokenType.NUMBER, '1', 1, 1), MyToken(TokenType.GE, '>=', None, 1),
             MyToken(TokenType.NUMBER, '10', 10, 1)]
        parser = Parser(tokens)
        tree = \
        LogicalBinary(
            LogicalBinary(
                LogicalBinary(
                    Grouping(
                        LogicalBinary(
                            Identifier('x'),
                            TokenType.OR,
                            LogicalBinary(
                                Literal(True),
                                TokenType.AND,
                                Literal(False)
                            )
                        )
                    ),
                    TokenType.AND,
                    LogicalUnary(
                        TokenType.NOT,
                        Identifier('y')
                    )
                ),
                TokenType.OR,
                LogicalBinary(
                    LogicalBinary(
                        Comparison(
                            LogicalUnary(
                                TokenType.NOT,
                                Identifier('z')
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
                        ),
                        TokenType.AND,
                        Comparison(
                            Identifier('y'),
                            TokenType.L,
                            Literal(5)
                        )
                    ),
                    TokenType.AND,
                    Identifier('t')
                )
            ),
            TokenType.OR,
            Comparison(
                Binary(
                    Literal(5),
                    TokenType.PLUS,
                    Literal(1)
                ),
                TokenType.GE,
                Literal(10)
            )
        )
        self.assertEqual(tree, parser.parse_expr())

        # 5 <= 3 = 7 > 5 - 2
        tokens = [MyToken(TokenType.NUMBER, '5', 5, 1), MyToken(TokenType.LE, '<=', None, 1), MyToken(TokenType.NUMBER, '3', 3, 1),
                     MyToken(TokenType.EQUAL, '=', None, 1), MyToken(TokenType.NUMBER, '7', 7, 1), MyToken(TokenType.G, '>', None, 1),
                     MyToken(TokenType.NUMBER, '5', 5, 1), MyToken(TokenType.MINUS, '-', None, 1), MyToken(TokenType.NUMBER, '2', 2, 1)]
        parser = Parser(tokens)
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
        self.assertEqual(tree, parser.parse_expr())

    def test_strings(self):
        # x . ('test' . '123') . ''
        tokens = [MyToken(TokenType.IDENT, 'x', 'x', 1), MyToken(TokenType.DOT, '.', None, 1),
                  MyToken(TokenType.LPAREN, '(', '(', 1), MyToken(TokenType.STRING, 'test', 'test', 1),
                  MyToken(TokenType.DOT, '.', None, 1), MyToken(TokenType.STRING, '123', '123', 1),
                  MyToken(TokenType.RPAREN, ')', ')', 1), MyToken(TokenType.DOT, '.', None, 1),
                  MyToken(TokenType.STRING, '', '', 1)]
        parser = Parser(tokens)
        tree = \
            StringBinary(
                StringBinary(
                    Identifier('x'),
                    TokenType.DOT,
                    Grouping(
                        StringBinary(
                            Literal('test'),
                            TokenType.DOT,
                            Literal('123')
                        )
                    )
                ),
                TokenType.DOT,
                Literal('')
            )
        self.assertEqual(tree, parser.parse_expr())

        # 'asd' . 5 + 3 . true and false . x
        tokens = \
            [MyToken(TokenType.STRING, 'asd', 'asd', 1), MyToken(TokenType.DOT, '.', None, 1),
             MyToken(TokenType.NUMBER, '5', 5, 1), MyToken(TokenType.PLUS, '+', None, 1),
             MyToken(TokenType.NUMBER, '3', 3, 1), MyToken(TokenType.DOT, '.', None, 1),
             MyToken(TokenType.TRUE, 'true', True, 1), MyToken(TokenType.AND, 'and', None, 1),
             MyToken(TokenType.FALSE, 'false', False, 1), MyToken(TokenType.DOT, '.', None, 1),
             MyToken(TokenType.IDENT, 'x', 'x', 1)]
        tree = \
            StringBinary(
                StringBinary(
                    StringBinary(
                        Literal('asd'),
                        TokenType.DOT,
                        Binary(
                            Literal(5),
                            TokenType.PLUS,
                            Literal(3)
                        )
                    ),
                    TokenType.DOT,
                    LogicalBinary(
                        Literal(True),
                        TokenType.AND,
                        Literal(False)
                    )
                ),
                TokenType.DOT,
                Identifier('x')
            )
        parser = Parser(tokens)
        self.assertEqual(tree, parser.parse_expr())

    def test_assignment(self):
        # x := 5\ny := not b + 7\ny := 'asd'.'123'
        tokens = [MyToken(TokenType.IDENT, 'x', 'x', 1), MyToken(TokenType.ASSIGN, ':=', None, 1), MyToken(TokenType.NUMBER, '5', 5, 1),
                  MyToken(TokenType.EOL, 'None', None, 1), MyToken(TokenType.IDENT, 'y', 'y', 2), MyToken(TokenType.ASSIGN, ':=', None, 2),
                  MyToken(TokenType.NOT, 'not', None, 2), MyToken(TokenType.IDENT, 'b', 'b', 2), MyToken(TokenType.PLUS, '+', None, 2),
                  MyToken(TokenType.NUMBER, '7', 7, 2), MyToken(TokenType.EOL, 'None', None, 2),
                  MyToken(TokenType.IDENT, 'y', 'y', 3), MyToken(TokenType.ASSIGN, ':=', None, 3),
                  MyToken(TokenType.STRING, 'asd', 'asd', 3), MyToken(TokenType.DOT, '.', None, 3), MyToken(TokenType.STRING, '123', '123', 3)]
        parser = Parser(tokens)
        tree = \
        Program([Assign(Identifier('x'), Literal(5)),
         Assign(Identifier('y'), Binary(LogicalUnary(TokenType.NOT, Identifier('b')), TokenType.PLUS, Literal(7))),
         Assign(Identifier('y'), StringBinary(Literal('asd'), TokenType.DOT, Literal('123')))])
        self.assertEqual(tree, parser.parse())

    def test_expr_stmt(self):
        # 5 = 7\n x 3 + 2
        tokens = \
            [MyToken(TokenType.NUMBER, '5', 5, 1), MyToken(TokenType.EQUAL, '=', None, 1),
             MyToken(TokenType.NUMBER, '7', 7, 1), MyToken(TokenType.EOL, 'None', None, 1), MyToken(TokenType.IDENT, 'x', 'x', 2),
             MyToken(TokenType.NUMBER, '3', 3, 2), MyToken(TokenType.PLUS, '+', None, 2),
             MyToken(TokenType.NUMBER, '2', 2, 2)]
        parser = Parser(tokens)
        tree = \
        Program([ExprStmt(Comparison(Literal(5), TokenType.EQUAL, Literal(7))),
                 ExprStmt(Identifier('x')),
                 ExprStmt(Binary(Literal(3), TokenType.PLUS, Literal(2)))])
        self.assertEqual(tree, parser.parse())

    def test_control_structures(self):
        # if x {y\nx := 6}\nif x < 3 {\nx := 3\n} else if t {\nx := 7\n} else \n{t\n}\nwhile not (x + y = 3) {x\nt\n}\n
        tokens = [MyToken(TokenType.IF, 'if', None, 1), MyToken(TokenType.IDENT, 'x', 'x', 1),
                  MyToken(TokenType.LBRACE,'{', None, 1),
                  MyToken(TokenType.IDENT, 'y', 'y', 1), MyToken(TokenType.EOL, 'None', None, 1),
                  MyToken(TokenType.IDENT, 'x', 'x', 2), MyToken(TokenType.ASSIGN, ':=', None, 2),
                  MyToken(TokenType.NUMBER, '6', 6, 2), MyToken(TokenType.RBRACE, '}', None, 2),
                  MyToken(TokenType.EOL, 'None', None, 2), MyToken(TokenType.IF, 'if', None, 3),
                  MyToken(TokenType.IDENT, 'x', 'x', 3), MyToken(TokenType.L, '<', None, 3),
                  MyToken(TokenType.NUMBER, '3', 3, 3), MyToken(TokenType.LBRACE, '{', None, 3),
                  MyToken(TokenType.EOL, 'None', None, 3), MyToken(TokenType.IDENT, 'x', 'x', 4),
                  MyToken(TokenType.ASSIGN, ':=', None, 4), MyToken(TokenType.NUMBER, '3', 3, 4),
                  MyToken(TokenType.EOL, 'None', None, 4), MyToken(TokenType.RBRACE, '}', None, 5),
                  MyToken(TokenType.ELSE, 'else', None, 5), MyToken(TokenType.IF, 'if', None, 5),
                  MyToken(TokenType.IDENT, 't', 't', 5), MyToken(TokenType.LBRACE, '{', None, 5),
                  MyToken(TokenType.EOL, 'None', None, 5), MyToken(TokenType.IDENT, 'x', 'x', 6),
                  MyToken(TokenType.ASSIGN, ':=', None, 6), MyToken(TokenType.NUMBER, '7', 7, 6),
                  MyToken(TokenType.EOL, 'None', None, 6), MyToken(TokenType.RBRACE, '}', None, 7),
                  MyToken(TokenType.ELSE, 'else', None, 7), MyToken(TokenType.EOL, 'None', None, 7),
                  MyToken(TokenType.LBRACE, '{', None, 8),
                  MyToken(TokenType.IDENT, 't', 't', 8), MyToken(TokenType.EOL, 'None', None, 8),
                  MyToken(TokenType.RBRACE, '}', None, 9), MyToken(TokenType.EOL, 'None', None, 9),
                  MyToken(TokenType.WHILE, 'while', None, 10), MyToken(TokenType.NOT, 'not', None, 10),
                  MyToken(TokenType.LPAREN, '(', None, 10), MyToken(TokenType.IDENT, 'x', 'x', 10),
                  MyToken(TokenType.PLUS, '+', None, 10), MyToken(TokenType.IDENT, 'y', 'y', 10),
                  MyToken(TokenType.EQUAL, '=', None, 10), MyToken(TokenType.NUMBER, '3', 3, 10),
                  MyToken(TokenType.RPAREN, ')', None, 10), MyToken(TokenType.LBRACE, '{', None, 10),
                   MyToken(TokenType.IDENT, 'x', 'x', 10),
                  MyToken(TokenType.EOL, 'None', None, 10),
                  MyToken(TokenType.IDENT, 't', 't', 11), MyToken(TokenType.EOL, 'None', None, 11),
                  MyToken(TokenType.RBRACE, '}', None, 12), MyToken(TokenType.EOL, 'None', None, 12)]
        parser = Parser(tokens)
        tree = \
        Program([
            If(
                Identifier('x'),
                Program([ExprStmt(Identifier('y')), Assign(Identifier('x'), Literal(6))]),
                Program([])
            ),
            If(
                Comparison(Identifier('x'), TokenType.L, Literal(3)),
                Program([Assign(Identifier('x'), Literal(3))]),
                Program([If(Identifier('t'), Program([Assign(Identifier('x'), Literal(7))]), Program([ExprStmt(Identifier('t'))]))])
            ),
            While(
                LogicalUnary(TokenType.NOT, Grouping(Comparison(Binary(Identifier('x'), TokenType.PLUS, Identifier('y')), TokenType.EQUAL, Literal(3)))),
                Program([ExprStmt(Identifier('x')), ExprStmt(Identifier('t'))])
            )
        ])
        self.assertEqual(tree, parser.parse())

    def test_functions(self):
        # fun f(x) {ret x}\nfun f2(x,y,z) {\nprint(x - y)\nx\n}x := -f() + 3 - g(x + 2, y)(3) y := (g(f))(x)\nf()
        tokens = \
            [MyToken(TokenType.FUN, 'fun', None, 1), MyToken(TokenType.IDENT, 'f', 'f', 1),
             MyToken(TokenType.LPAREN, '(', None, 1), MyToken(TokenType.IDENT, 'x', 'x', 1),
             MyToken(TokenType.RPAREN, ')', None, 1), MyToken(TokenType.LBRACE, '{', None, 1),
             MyToken(TokenType.RET, 'ret', None, 1), MyToken(TokenType.IDENT, 'x', 'x', 1),
             MyToken(TokenType.RBRACE, '}', None, 1), MyToken(TokenType.EOL, None, None, 1),
             MyToken(TokenType.FUN, 'fun', None, 2), MyToken(TokenType.IDENT, 'f2', 'f2', 2),
             MyToken(TokenType.LPAREN, '(', None, 2), MyToken(TokenType.IDENT, 'x', 'x', 2),
             MyToken(TokenType.COMMA, ',', None, 2), MyToken(TokenType.IDENT, 'y', 'y', 2),
             MyToken(TokenType.COMMA, ',', None, 2), MyToken(TokenType.IDENT, 'z', 'z', 2),
             MyToken(TokenType.RPAREN, ')', None, 2), MyToken(TokenType.LBRACE, '{', None, 2),
             MyToken(TokenType.EOL, None, None, 2), MyToken(TokenType.IDENT, 'print', 'print', 3),
             MyToken(TokenType.LPAREN, '(', None, 3),
             MyToken(TokenType.IDENT, 'x', 'x', 3), MyToken(TokenType.MINUS, '-', None, 3),
             MyToken(TokenType.IDENT, 'y', 'y', 3), MyToken(TokenType.RPAREN, ')', None, 3),
             MyToken(TokenType.EOL, None, None, 3), MyToken(TokenType.IDENT, 'x', 'x', 4),
             MyToken(TokenType.EOL, None, None, 4), MyToken(TokenType.RBRACE, '}', None, 5),
             MyToken(TokenType.IDENT, 'x', 'x', 5), MyToken(TokenType.ASSIGN, ':=', None, 5),
             MyToken(TokenType.MINUS, '-', None, 5),
             MyToken(TokenType.IDENT, 'f', 'f', 5), MyToken(TokenType.LPAREN, '(', None, 5),
             MyToken(TokenType.RPAREN, ')', None, 5), MyToken(TokenType.PLUS, '+', None, 5),
             MyToken(TokenType.NUMBER, '3', 3, 5), MyToken(TokenType.MINUS, '-', None, 5),
             MyToken(TokenType.IDENT, 'g', 'g', 5), MyToken(TokenType.LPAREN, '(', None, 5),
             MyToken(TokenType.IDENT, 'x', 'x', 5), MyToken(TokenType.PLUS, '+', None, 5),
             MyToken(TokenType.NUMBER, '2', 2, 5), MyToken(TokenType.COMMA, ',', None, 5),
             MyToken(TokenType.IDENT, 'y', 'y', 5), MyToken(TokenType.RPAREN, ')', None, 5),
             MyToken(TokenType.LPAREN, '(', None, 5), MyToken(TokenType.NUMBER, '3', 3, 5),
             MyToken(TokenType.RPAREN, ')', None, 5), MyToken(TokenType.IDENT, 'y', 'y', 5),
             MyToken(TokenType.ASSIGN, ':=', None, 5), MyToken(TokenType.LPAREN, '(', None, 5),
             MyToken(TokenType.IDENT, 'g', 'g', 5), MyToken(TokenType.LPAREN, '(', None, 5),
             MyToken(TokenType.IDENT, 'f', 'f', 5), MyToken(TokenType.RPAREN, ')', None, 5),
             MyToken(TokenType.RPAREN, ')', None, 5), MyToken(TokenType.LPAREN, '(', None, 5),
             MyToken(TokenType.IDENT, 'x', 'x', 5), MyToken(TokenType.RPAREN, ')', None, 5),
             MyToken(TokenType.EOL, None, None, 5), MyToken(TokenType.IDENT, 'f', 'f', 6),
             MyToken(TokenType.LPAREN, '(', None, 6), MyToken(TokenType.RPAREN, ')', None, 6)
            ]
        parser = Parser(tokens)
        tree = \
        Program(
            [Fun(Identifier('f'), [Identifier('x')], Program([Ret(Identifier('x'))])),
             Fun(Identifier('f2'), [Identifier('x'), Identifier('y'), Identifier('z')], Program([
                 ExprStmt(FunCall(Identifier('print'), [Binary(Identifier('x'), TokenType.MINUS, Identifier('y'))])),
                                                 ExprStmt(Identifier('x'))])),
             Assign(Identifier('x'),
                    Binary(
                        Binary(
                            Unary(
                                TokenType.MINUS,
                                FunCall(Identifier('f'), [])
                            ),
                            TokenType.PLUS,
                            Literal(3)
                        ),
                        TokenType.MINUS,
                        FunCall(FunCall(Identifier('g'), [Binary(Identifier('x'), TokenType.PLUS, Literal(2)), Identifier('y')]), [Literal(3)])
                    )),
             Assign(Identifier('y'),
                    FunCall(
                        Grouping(
                            FunCall(
                                Identifier('g'),
                                [Identifier('f')]
                            )
                        ),
                        [Identifier('x')]
                    )),
             ExprStmt(FunCall(Identifier('f'), []))
             ]
        )
        self.assertEqual(tree, parser.parse())

