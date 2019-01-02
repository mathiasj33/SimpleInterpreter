from enum import Enum


TokenType = Enum('Token', 'PLUS MINUS MUL DIV POW NUMBER LPAREN RPAREN EOL')


class MyToken:

    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __eq__(self, other):
        if isinstance(other, MyToken):
            return self.type == other.type and self.value == other.value and self.line == other.line
        return False

    def __str__(self):
        if self.value is not None:
            return '{}({})'.format(self.type, self.value)
        return '{}'.format(self.type)

    def __repr__(self):
        return str(self)