from src.mytoken import TokenType
from src.syntaxtree import *
from enum import Enum

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.prefix_functions = {
            TokenType.NUMBER: self.parse_literal,
            TokenType.TRUE: self.parse_literal,
            TokenType.FALSE: self.parse_literal,
            TokenType.IDENT: self.parse_identifier,
            TokenType.PLUS: self.parse_prefix_operator,
            TokenType.MINUS: self.parse_prefix_operator,
            TokenType.NOT: self.parse_prefix_logical_operator,
            TokenType.LPAREN: self.parse_grouping
        }
        self.not_prefix_functions = {
            TokenType.PLUS: (self.parse_infix_operator, Precedences.PLUS, Associativity.LEFT),
            TokenType.MINUS: (self.parse_infix_operator, Precedences.PLUS, Associativity.LEFT),
            TokenType.MUL: (self.parse_infix_operator, Precedences.MUL, Associativity.LEFT),
            TokenType.DIV: (self.parse_infix_operator, Precedences.MUL, Associativity.LEFT),
            TokenType.POW: (self.parse_infix_operator, Precedences.POW, Associativity.RIGHT),
            TokenType.OR: (self.parse_infix_logical_operator, Precedences.OR, Associativity.LEFT),
            TokenType.AND: (self.parse_infix_logical_operator, Precedences.AND, Associativity.LEFT),
            TokenType.EQUAL: (self.parse_comparison, Precedences.EQUAL, Associativity.LEFT),
            TokenType.L: (self.parse_comparison, Precedences.L, Associativity.LEFT),
            TokenType.LE: (self.parse_comparison, Precedences.L, Associativity.LEFT),
            TokenType.G: (self.parse_comparison, Precedences.L, Associativity.LEFT),
            TokenType.GE: (self.parse_comparison, Precedences.L, Associativity.LEFT)
        }

    def consume(self):
        token = self.tokens[self.index]
        self.index += 1
        return token

    def consume_token(self, token_type):
        if self.peek().token_type != token_type: raise ParseError(self.peek().line, 'Expected {}.'.format(token_type))
        self.consume()

    def peek(self):
        return self.tokens[self.index]

    def is_at_expr_end(self):
        return self.is_at_end() or self.peek().token_type == TokenType.EOL

    def is_at_end(self):
        return self.index >= len(self.tokens)

    def get_precedence(self):
        token = self.peek()
        try:
            _, precedence, _ = self.not_prefix_functions[token.token_type]
            return precedence
        except KeyError:
            return 0

    def parse(self):
        program = []
        while True:
            if self.peek().token_type == TokenType.IDENT:
                program.append(self.parse_assignment())
            elif self.peek().token_type == TokenType.EOL:
                self.consume()

            if self.is_at_end():
                return program

    def parse_assignment(self):
        token = self.consume()
        self.consume_token(TokenType.ASSIGN)
        return Assign(self.parse_identifier(token), self.parse_expr())

    def parse_expr(self, precedence=0):
        token = self.consume()
        try:
            prefix_function = self.prefix_functions[token.token_type]
        except KeyError:
            raise ParseError(token.line, 'Could not parse {}.'.format(token.text))
        left = prefix_function(token)
        if self.is_at_expr_end():
            return left
        else:
            while precedence < self.get_precedence():
                token = self.consume()
                not_prefix_function, function_precedence, associativity = self.not_prefix_functions[token.token_type]
                left = not_prefix_function(left, token, function_precedence, associativity)
                if self.is_at_expr_end():
                    return left
            return left

    # Pratt parsing functions ('parselets')
    def parse_identifier(self, token):
        return Identifier(token.value)

    def parse_literal(self, token):
        return Literal(token.value)

    def parse_prefix_operator(self, token):
        arg = self.parse_expr(Precedences.PREFIX)
        return Unary(token.token_type, arg)

    def parse_prefix_logical_operator(self, token):
        arg = self.parse_expr(Precedences.PREFIX)
        return LogicalUnary(token.token_type, arg)

    def parse_grouping(self, token):
        expr = self.parse_expr()
        if self.consume().token_type != TokenType.RPAREN:
            raise ParseError(token.line, 'Missing \')\'.')
        return Grouping(expr)

    def parse_infix_operator(self, left, token, precedence, associativity):
        precedence = precedence - (1 if associativity == Associativity.RIGHT else 0)
        right = self.parse_expr(precedence)
        return Binary(left, token.token_type, right)

    def parse_infix_logical_operator(self, left, token, precedence, associativity):
        precedence = precedence - (1 if associativity == Associativity.RIGHT else 0)
        right = self.parse_expr(precedence)
        return LogicalBinary(left, token.token_type, right)

    def parse_comparison(self, left, token, precedence, associativity):
        precedence = precedence - (1 if associativity == Associativity.RIGHT else 0)
        right = self.parse_expr(precedence)
        return Comparison(left, token.token_type, right)

class Precedences:
    OR = 1
    AND = 2
    EQUAL = 3
    L = 4
    PLUS = 5
    MUL = 6
    POW = 7
    PREFIX = 8

Associativity = Enum('Associativity', 'LEFT RIGHT')

class ParseError(Exception):
    def __init__(self, line, msg):
        self.line = line
        self.msg = msg