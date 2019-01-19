from src.syntaxtree import *
from src.mytoken import TokenType
from operator import add, sub, truediv, mul, pow

class Interpreter:
    def __init__(self, ast):
        self.ast = ast

    def interpret(self):
        return self.ast.accept(self)

    def visit_binary(self, binary):
        left = binary.left.accept(self)
        right = binary.right.accept(self)
        return {
            TokenType.PLUS: add,
            TokenType.MINUS: sub,
            TokenType.DIV: truediv,
            TokenType.MUL: mul,
            TokenType.POW: pow
        }[binary.op](left, right)

    def visit_unary(self, unary):
        value = unary.expr.accept(self)
        return {
            TokenType.PLUS: lambda x: x,
            TokenType.MINUS: lambda x: -x
        }[unary.op](value)

    def visit_grouping(self, grouping):
        return grouping.expr.accept(self)

    def visit_literal(self, literal):
        return literal.value
