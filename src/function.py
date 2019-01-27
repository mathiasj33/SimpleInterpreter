from src.syntaxtree import Identifier
from src.environment import Environment

class Function:
    def __init__(self, fun, env):
        self.fun = fun
        self.env = env

    def call(self, interpreter, args):
        tmp = {}
        for i in range(len(self.fun.args)):
            tmp[self.fun.args[i].name] = args[i].accept(interpreter)  # eager evaluation
        new_env = Environment(tmp, parent=self.env)
        try:
            interpreter.interpret(self.fun.body, env=new_env)
        except RetError as r:
            return r.value
        return None

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False
        elif self is other:
            return True
        else:
            return True and self.fun == other.fun and self.env == other.env

class RetError(Exception):
    def __init__(self, value):
        self.value = value