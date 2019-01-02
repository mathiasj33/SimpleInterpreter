from src.mytoken import MyToken, TokenType


class Lexer:

    def __init__(self, prog):
        self.prog = prog
        self.index = 0
        self.line = 1
        self.char_to_token_type = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '-': TokenType.MINUS,
            '+': TokenType.PLUS,
            '/': TokenType.DIV,
            '*': TokenType.MUL,
            '^': TokenType.POW,
            '\n': TokenType.EOL
        }

    def current(self):
        return self.prog[self.index]

    def advance(self):
        self.index += 1
        while self.index < len(self.prog) and self.prog[self.index] in ['\t', ' ']:
            self.index += 1

    def match_number(self):
        value = 0
        while self.index < len(self.prog) and self.current().isnumeric():
            value *= 10
            value += int(self.current())
            self.index += 1
        self.index -= 1
        return MyToken(TokenType.NUMBER, value, self.line)

    def match_char(self):
        type = self.char_to_token_type[self.current()]
        token = MyToken(type, None, self.line)
        if type == TokenType.EOL:
            self.line += 1
        return token

    def lex(self):
        tokens = []
        while self.index < len(self.prog):
            c = self.current()
            if c.isnumeric():
                tokens.append(self.match_number())
            else:
                tokens.append(self.match_char())
            self.advance()
        return tokens
