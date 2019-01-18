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

    def test_assignment(self):
        # x := 5\ny := not b + 7
        tokens = [MyToken(TokenType.IDENT, 'x', 'x', 1), MyToken(TokenType.ASSIGN, ':=', None, 1), MyToken(TokenType.NUMBER, '5', 5, 1),
                  MyToken(TokenType.EOL, 'None', None, 1), MyToken(TokenType.IDENT, 'y', 'y', 2), MyToken(TokenType.ASSIGN, ':=', None, 2),
                  MyToken(TokenType.NOT, 'not', None, 2), MyToken(TokenType.IDENT, 'b', 'b', 2), MyToken(TokenType.PLUS, '+', None, 2),
                  MyToken(TokenType.NUMBER, '7', 7, 2)]
        parser = Parser(tokens)
        tree = \
        [Assign(Identifier('x'), Literal(5)),
         Assign(Identifier('y'), Binary(LogicalUnary(TokenType.NOT, Identifier('b')), TokenType.PLUS, Literal(7)))]
        self.assertEqual(tree, parser.parse())

    def test_print(self):
        # print x\nprint y and 7 - 2
        tokens = [MyToken(TokenType.PRINT, 'print', None, 1), MyToken(TokenType.IDENT, 'x', 'x', 1),
                  MyToken(TokenType.EOL, 'None', None, 1), MyToken(TokenType.PRINT, 'print', None, 2),
                  MyToken(TokenType.IDENT, 'y', 'y', 2), MyToken(TokenType.AND, 'and', None, 2),
                  MyToken(TokenType.NUMBER, '7', 7, 2), MyToken(TokenType.MINUS, '-', None, 2),
                  MyToken(TokenType.NUMBER, '2', 2, 2)]
        parser = Parser(tokens)
        tree = \
        [Print(Identifier('x')), Print(LogicalBinary(Identifier('y'), TokenType.AND, Binary(Literal(7), TokenType.MINUS, Literal(2))))]
        self.assertEqual(tree, parser.parse())

