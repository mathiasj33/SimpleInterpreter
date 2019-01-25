from function import Function

class PrintFunction(Function):
    def __init__(self):
        super().__init__(None, None)

    def call(self, interpreter, args):
        value = args[0].accept(interpreter)
        print(interpreter.to_string(value))