from src.mytoken import MyToken, TokenType

class Lexer:
    def __init__(self, prog):
        self.prog = prog
        self.index = 0
        self.line = 1
        self.char_to_token_type = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '-': TokenType.MINUS,
            '+': TokenType.PLUS,
            '/': TokenType.DIV,
            '*': TokenType.MUL,
            '^': TokenType.POW,
            '=': TokenType.EQUAL,
            ':': None,  # only needed for :=
            '<': TokenType.L,
            '>': TokenType.G,
            ',': TokenType.COMMA,
            '#': TokenType.HASH,
            '\n': TokenType.EOL
        }
        self.keywords = {
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'or': TokenType.OR,
            'and': TokenType.AND,
            'not': TokenType.NOT,
            'fun': TokenType.FUN,
            'ret': TokenType.RET
        }

    def current(self):
        return self.prog[self.index]

    def peek(self):
        return self.prog[self.index + 1]

    def advance(self):
        self.index += 1
        while self.index < len(self.prog) and self.prog[self.index] in ['\t', ' ']:
            self.index += 1

    def match_number(self):
        number_string = ''
        while self.index < len(self.prog) and (self.current().isnumeric() or self.current() == '.'):
            number_string += self.current()
            self.index += 1
        self.index -= 1
        value = float(number_string) if '.' in number_string else int(number_string)
        return MyToken(TokenType.NUMBER, number_string, value, self.line)

    def match_char(self):
        if self.index < len(self.prog) - 1 and self.peek() == '=':
            if self.current() == ':':
                self.advance()
                return MyToken(TokenType.ASSIGN, ':=', None, self.line)
            elif self.current() == '<':
                self.advance()
                return MyToken(TokenType.LE, '<=', None, self.line)
            elif self.current() == '>':
                self.advance()
                return MyToken(TokenType.GE, '>=', None, self.line)

        token_type = self.char_to_token_type[self.current()]
        token = MyToken(token_type, self.current(), None, self.line)
        if token_type == TokenType.EOL:
            token.text = None
            self.line += 1
        return token

    def match_string(self):
        text = ''
        self.index += 1
        while self.index < len(self.prog) and self.current() != '\'':
            text += self.current()
            self.index += 1
        return MyToken(TokenType.STRING, text, text, self.line)

    def match_ident_or_keyword(self):
        text = ''
        while self.index < len(self.prog) and self.is_valid_ident_char():
            text += self.current()
            self.index += 1
        self.index -= 1
        if text in self.keywords:
            token_type = self.keywords[text]
            value = None
            if token_type == TokenType.TRUE: value = True
            elif token_type == TokenType.FALSE: value = False
            return MyToken(self.keywords[text], text, value, self.line)
        else:
            return MyToken(TokenType.IDENT, text, text, self.line)

    def lex(self):
        tokens = []
        while self.index < len(self.prog):
            c = self.current()
            if c.isnumeric() or c == '.':
                tokens.append(self.match_number())
            elif c in self.char_to_token_type:
                tokens.append(self.match_char())
            elif c == '\'':
                tokens.append(self.match_string())
            else:
                tokens.append(self.match_ident_or_keyword())
            self.advance()
        return tokens

    def is_valid_ident_char(self):
        c = ord(self.current())
        return 48 <= c <= 57 or 65 <= c <= 90 or 97 <= c <= 122 or c == 95