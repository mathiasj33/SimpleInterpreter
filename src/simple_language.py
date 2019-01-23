from src.interpreter import Interpreter
from src.parser import Parser
from src.lexer import Lexer

class SimpleLanguage:
    @staticmethod
    def interpret_file(path):
        with open(path) as f:
            program = f.read()
        tokens = Lexer(program).lex()
        ast = Parser(tokens).parse()
        Interpreter().interpret(ast)