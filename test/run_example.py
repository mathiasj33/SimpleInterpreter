from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

with open('example.si') as f:
    program = f.read()

env = Interpreter(Parser(Lexer(program).lex()).parse()).interpret()