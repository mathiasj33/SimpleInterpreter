class Environment:
    def __init__(self, env, parent=None):
        self.env = env
        self.parent = parent

    def __getitem__(self, item):
        try:
            v = self.env[item]
            return v
        except KeyError:
            return self.parent[item]

    def __setitem__(self, key, value):
        self.env[key] = value

    def __delitem__(self, key):
        del self.env[key]

    def __contains__(self, item):
        return item in self.env or (not self.parent is None and item in self.parent)

    def update(self, other):
        self.env.update(other.env)

    def __len__(self):
        return len(self.env)

    def __repr__(self):
        return repr(self.env)

    def __eq__(self, other):
        if not isinstance(other, Environment):
            return False
        elif self is other:
            return True
        else:
            return self.env == other.env and self.parent == other.parent