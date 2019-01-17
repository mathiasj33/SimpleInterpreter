from src.mytoken import MyToken, TokenType

class Lexer:
    def __init__(self, prog):
        self.prog = prog
        self.index = 0
        self.line = 1
        self.char_to_token_type = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LCURLY,
            '}': TokenType.RCURLY,
            '-': TokenType.MINUS,
            '+': TokenType.PLUS,
            '/': TokenType.DIV,
            '*': TokenType.MUL,
            '^': TokenType.POW,
            '\n': TokenType.EOL
        }
        self.keywords = {
            'print': TokenType.PRINT,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE
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
        return MyToken(TokenType.NUMBER, str(value), value, self.line)

    def match_char(self):
        token_type = self.char_to_token_type[self.current()]
        token = MyToken(token_type, self.current(), None, self.line)
        if token_type == TokenType.EOL:
            token.text = None
            self.line += 1
        return token

    def match_ident_or_keyword(self):
        value = ''
        while self.index < len(self.prog) and not (self.current().isspace() or self.current() in self.char_to_token_type):
            value += self.current()
            self.index += 1
        self.index -= 1
        if value in self.keywords:
            return MyToken(self.keywords[value], value, None, self.line)
        else:
            return MyToken(TokenType.IDENT, value, value, self.line)

    def lex(self):
        tokens = []
        while self.index < len(self.prog):
            c = self.current()
            if c.isnumeric():
                tokens.append(self.match_number())
            else:
                if c in self.char_to_token_type: tokens.append(self.match_char())
                else: tokens.append(self.match_ident_or_keyword())
            self.advance()
        return tokens
