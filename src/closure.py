class Closure:
    def __init__(self, name, args, body, env):
        self.name = name
        self.args = args
        self.body = body
        self.env = env

    def __eq__(self, other):
        if not isinstance(other, Closure):
            return False
        elif self is other:
            return True
        else:
            return True and self.name == other.name and self.args == other.args and self.body == other.body and self.env == other.env

    def __str__(self):
        return '<{}({}) -> {}, {}>'.format(self.name, self.args, self.body, self.env)

    def __repr__(self):
        return str(self)
