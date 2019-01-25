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
            TokenType.STRING: self.parse_literal,
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
            TokenType.GE: (self.parse_comparison, Precedences.L, Associativity.LEFT),
            TokenType.DOT: (self.parse_infix_string_operator, Precedences.DOT, Associativity.LEFT),
            TokenType.LPAREN: (self.parse_call, Precedences.CALL, Associativity.LEFT)
        }

    def consume(self):
        token = self.tokens[self.index]
        self.index += 1
        return token

    def consume_token(self, token_type, skip_newline=False):
        if skip_newline:
            while self.peek().token_type == TokenType.EOL:
                self.consume()
        if self.peek().token_type != token_type: raise ParseError(self.peek().line, 'Expected {}.'.format(token_type))
        return self.consume()

    def peek(self):
        return self.lookahead(1)

    def lookahead(self, num):
        return self.tokens[self.index + num - 1]

    def is_at_expr_end(self):
        return self.is_at_end() or self.peek().token_type == TokenType.EOL

    def is_at_end(self):
        return self.index >= len(self.tokens)

    def parse(self):
        program = Program([])
        while True:
            token_type = self.peek().token_type
            if token_type == TokenType.IDENT and self.lookahead(2).token_type == TokenType.ASSIGN:
                program.stmts.append(self.parse_assignment())
            elif token_type == TokenType.FUN:
                program.stmts.append(self.parse_function())
            elif token_type == TokenType.RET:
                program.stmts.append(self.parse_ret())
            elif token_type == TokenType.IF:
                program.stmts.append(self.parse_if())
            elif token_type == TokenType.WHILE:
                program.stmts.append(self.parse_while())
            elif token_type == TokenType.EOL:
                self.consume()
            else:
                try:
                    program.stmts.append(ExprStmt(self.parse_expr()))
                except ParseError:
                    return program

            if self.is_at_end():
                return program

    def parse_assignment(self):
        token = self.consume()
        self.consume_token(TokenType.ASSIGN)
        return Assign(self.parse_identifier(token), self.parse_expr())

    def parse_function(self):
        self.consume_token(TokenType.FUN)
        token = self.consume()
        self.consume_token(TokenType.LPAREN)
        args = []
        if self.peek().token_type != TokenType.RPAREN:
            while True:
                arg = self.consume_token(TokenType.IDENT)
                args.append(self.parse_identifier(arg))
                if self.peek().token_type == TokenType.RPAREN: break
                self.consume_token(TokenType.COMMA)
        self.consume_token(TokenType.RPAREN)
        self.consume_token(TokenType.LBRACE, skip_newline=True)
        body = self.parse()
        self.consume_token(TokenType.RBRACE, skip_newline=True)
        return Fun(self.parse_identifier(token), args, body)

    def parse_ret(self):
        self.consume_token(TokenType.RET)
        return Ret(self.parse_expr())

    def parse_if(self):
        self.consume_token(TokenType.IF)
        condition = self.parse_expr()
        self.consume_token(TokenType.LBRACE, skip_newline=True)
        left = self.parse()
        self.consume_token(TokenType.RBRACE, skip_newline=True)
        if self.is_at_end():
            return If(condition, left, Program([]))

        if self.peek().token_type != TokenType.ELSE:
            return If(condition, left, Program([]))
        self.consume()
        if self.peek().token_type == TokenType.IF:
            right = Program([self.parse_if()])
        else:
            self.consume_token(TokenType.LBRACE, skip_newline=True)
            right = self.parse()
            self.consume_token(TokenType.RBRACE, skip_newline=True)
        return If(condition, left, right)

    def parse_while(self):
        self.consume_token(TokenType.WHILE)
        condition = self.parse_expr()
        self.consume_token(TokenType.LBRACE, skip_newline=True)
        stmts = self.parse()
        self.consume_token(TokenType.RBRACE, skip_newline=True)
        return While(condition, stmts)

    def parse_expr(self, precedence=0):
        token = self.consume()
        try:
            prefix_function = self.prefix_functions[token.token_type]
        except KeyError:
            self.index -= 1  # undo the consume
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

    def get_precedence(self):
        token = self.peek()
        try:
            _, precedence, _ = self.not_prefix_functions[token.token_type]
            return precedence
        except KeyError:
            return 0

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

    def parse_infix_string_operator(self, left, token, precedence, associativity):
        precedence = precedence - (1 if associativity == Associativity.RIGHT else 0)
        right = self.parse_expr(precedence)
        return StringBinary(left, token.token_type, right)

    def parse_comparison(self, left, token, precedence, associativity):
        precedence = precedence - (1 if associativity == Associativity.RIGHT else 0)
        right = self.parse_expr(precedence)
        return Comparison(left, token.token_type, right)

    def parse_call(self, left, token, precedence, associativity):
        args = []
        if self.peek().token_type != TokenType.RPAREN:
            while True:
                arg = self.parse_expr()
                args.append(arg)
                if self.peek().token_type == TokenType.RPAREN: break
                self.consume_token(TokenType.COMMA)
        self.consume_token(TokenType.RPAREN)
        return FunCall(left, args)

class Precedences:
    DOT = 1
    OR = 2
    AND = 3
    EQUAL = 4
    L = 5
    PLUS = 6
    MUL = 7
    POW = 8
    PREFIX = 9
    CALL = 10

Associativity = Enum('Associativity', 'LEFT RIGHT')

class ParseError(Exception):
    def __init__(self, line, msg):
        self.line = line
        self.msg = msg
