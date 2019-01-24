from function import Function

class PrintFunction(Function):
    def __init__(self):
        super().__init__(None, None)

    def call(self, interpreter, args):
        value = args[0].accept(interpreter)
        if value is False:
            print('false')
        elif value is True:
            print('true')
        else:
            print(value)