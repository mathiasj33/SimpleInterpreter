from src.syntaxtree import *
from src.mytoken import TokenType
from operator import add, sub, truediv, mul, pow, or_, and_, not_, lt, le, gt, ge, eq

class Interpreter:
    def __init__(self, ast, environment=None):
        self.ast = ast
        self.environment = environment
        if self.environment is None:
            self.environment = {}

    def interpret(self):
        self.ast.accept(self)
        return self.environment

    def visit_program(self, program):
        for stmt in program.stmts:
            stmt.accept(self)

    def visit_assign(self, assign):
        right = assign.right.accept(self)
        self.environment[assign.left.name] = right

    def visit_print(self, print_stmt):
        value = print_stmt.expr.accept(self)
        if value is False:
            print('false')
        elif value is True:
            print('true')
        else:
            print(value)

    def interpret_expr(self):
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

    def visit_identifier(self, identifier):
        return self.environment[identifier.name]

    def visit_logicalbinary(self, logicalbinary):
        left = logicalbinary.left.accept(self)
        right = logicalbinary.right.accept(self)
        return {
            TokenType.OR: or_,
            TokenType.AND: and_
        }[logicalbinary.op](left, right)

    def visit_logicalunary(self, logicalunary):
        value = logicalunary.expr.accept(self)
        return {
            TokenType.NOT: not_
        }[logicalunary.op](value)

    def visit_comparison(self, comparison):
        left = comparison.left.accept(self)
        right = comparison.right.accept(self)
        return {
            TokenType.L: lt,
            TokenType.LE: le,
            TokenType.G: gt,
            TokenType.GE: ge,
            TokenType.EQUAL: eq
        }[comparison.op](left, right)
