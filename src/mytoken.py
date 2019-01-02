from enum import Enum


TokenType = Enum('Token', 'PLUS MINUS MUL DIV POW NUMBER LPAREN RPAREN')


class MyToken:

    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __str__(self):
        if self.value is not None:
            return '{}({})'.format(self.type, self.value)
        return '{}'.format(self.type)
