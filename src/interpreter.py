from src.syntaxtree import *
from src.function import *
from src.mytoken import TokenType
from src.environment import Environment
from operator import add, sub, truediv, mul, pow, or_, and_, not_, lt, le, gt, ge, eq

class Interpreter:
    def __init__(self, globals=None):
        self.globals = globals
        if self.globals is None:
            self.globals = Environment({})
        self.environment = self.globals

    def begin_scope(self):
        self.environment = Environment({}, self.environment)
        return self.environment

    def end_scope(self):
        self.environment = self.environment.parent

    def interpret(self, program):
        program.accept(self)
        return self.environment

    def visit_program(self, program):
        for stmt in program.stmts:
            stmt.accept(self)

    def visit_assign(self, assign_stmt):
        right = assign_stmt.right.accept(self)
        self.environment[assign_stmt.left.name] = right

    def visit_fun(self, fun):
        function = Function(fun, self.environment)
        self.environment[fun.name.name] = function

    def visit_funcall(self, funcall):
        function = funcall.callee.accept(self)
        return function.call(self, funcall.args)

    def visit_ret(self, ret):
        raise RetError(ret.expr.accept(self))

    def visit_print(self, print_stmt):
        value = print_stmt.expr.accept(self)
        if value is False:
            print('false')
        elif value is True:
            print('true')
        else:
            print(value)

    def visit_if(self, if_stmt):
        cond_value = if_stmt.cond.accept(self)
        if cond_value:
            if_stmt.left.accept(self)
        else:
            if_stmt.right.accept(self)

    def visit_while(self, while_stmt):
        while while_stmt.cond.accept(self):
            while_stmt.body.accept(self)

    def interpret_expr(self, expr):
        return expr.accept(self)

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
