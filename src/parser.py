from src.mytoken import TokenType
from src.syntaxtree import *
from enum import Enum

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.prefix_functions = {
            TokenType.NUMBER: self.parse_number,
            TokenType.IDENT: self.parse_identifier,
            TokenType.PLUS: self.parse_prefix_operator,
            TokenType.MINUS: self.parse_prefix_operator,
            TokenType.LPAREN: self.parse_grouping
        }
        self.not_prefix_functions = {
            TokenType.PLUS: (self.parse_infix_operator, Precedences.PLUS, Associativity.LEFT),
            TokenType.MINUS: (self.parse_infix_operator, Precedences.PLUS, Associativity.LEFT),
            TokenType.MUL: (self.parse_infix_operator, Precedences.MUL, Associativity.LEFT),
            TokenType.DIV: (self.parse_infix_operator, Precedences.MUL, Associativity.LEFT),
            TokenType.POW: (self.parse_infix_operator, Precedences.POW, Associativity.RIGHT)
        }

    def consume(self):
        token = self.tokens[self.index]
        self.index += 1
        return token

    def peek(self):
        return self.tokens[self.index]

    def is_at_end(self):
        return self.index >= len(self.tokens)

    def get_precedence(self):
        token = self.peek()
        try:
            _, precedence, _ = self.not_prefix_functions[token.token_type]
            return precedence
        except KeyError:
            return 0

    def parse_expr(self, precedence=0):
        token = self.consume()
        try:
            prefix_function = self.prefix_functions[token.token_type]
        except KeyError:
            raise ParseError(token.line, 'Could not parse {}.'.format(token.text))
        left = prefix_function(token)
        if self.is_at_end():
            return left
        else:
            while precedence < self.get_precedence():
                token = self.consume()
                not_prefix_function, function_precedence, associativity = self.not_prefix_functions[token.token_type]
                left = not_prefix_function(left, token, function_precedence, associativity)
                if self.is_at_end():
                    return left
            return left

    # Pratt parsing functions ('parselets')
    def parse_identifier(self, token):
        return Identifier(token.value)

    def parse_number(self, token):
        return Literal(token.value)

    def parse_prefix_operator(self, token):
        arg = self.parse_expr(Precedences.PREFIX)
        return Unary(token.token_type, arg)

    def parse_grouping(self, token):
        expr = self.parse_expr()
        if self.consume().token_type != TokenType.RPAREN:
            raise ParseError(token.line, 'Missing \')\'.')
        return Grouping(expr)

    def parse_infix_operator(self, left, token, precedence, associativity):
        precedence = precedence - (1 if associativity == Associativity.RIGHT else 0)
        right = self.parse_expr(precedence)
        return Binary(left, token.token_type, right)

class Precedences:
    PLUS = 1
    MUL = 2
    POW = 3
    PREFIX = 4

Associativity = Enum('Associativity', 'LEFT RIGHT')

class ParseError(Exception):
    def __init__(self, line, msg):
        self.line = line
        self.msg = msg