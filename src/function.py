class Function:
    def __init__(self, fun, env):
        self.fun = fun
        self.env = env

    def call(self, interpreter, args):
        new_env = interpreter.begin_scope()
        new_env.update(self.env)
        for i in range(len(self.fun.args)):
            new_env[self.fun.args[i].name] = args[i].accept(interpreter)  # eager evaluation
        try:
            interpreter.interpret(self.fun.body)
        except RetError as r:
            return r.value
        finally:
            interpreter.end_scope()
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