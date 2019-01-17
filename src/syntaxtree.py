class Binary:
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

	def __eq__(self, other):
		if not isinstance(other, Binary): return False
		elif self is other: return True
		else:
			return True and self.left == other.left and self.op == other.op and self.right == other.right

	def __str__(self):
		return 'Binary({}, {}, {})'.format(str(self.left), str(self.op), str(self.right))

	def __repr__(self):
		return str(self)

class Unary:
	def __init__(self, op, expr):
		self.op = op
		self.expr = expr

	def __eq__(self, other):
		if not isinstance(other, Unary): return False
		elif self is other: return True
		else:
			return True and self.op == other.op and self.expr == other.expr

	def __str__(self):
		return 'Unary({}, {})'.format(str(self.op), str(self.expr))

	def __repr__(self):
		return str(self)

class Grouping:
	def __init__(self, expr):
		self.expr = expr

	def __eq__(self, other):
		if not isinstance(other, Grouping): return False
		elif self is other: return True
		else:
			return True and self.expr == other.expr

	def __str__(self):
		return 'Grouping({})'.format(str(self.expr))

	def __repr__(self):
		return str(self)

class Literal:
	def __init__(self, value):
		self.value = value

	def __eq__(self, other):
		if not isinstance(other, Literal): return False
		elif self is other: return True
		else:
			return True and self.value == other.value

	def __str__(self):
		return 'Literal({})'.format(str(self.value))

	def __repr__(self):
		return str(self)

class Identifier:
	def __init__(self, name):
		self.name = name

	def __eq__(self, other):
		if not isinstance(other, Identifier): return False
		elif self is other: return True
		else:
			return True and self.name == other.name

	def __str__(self):
		return 'Identifier({})'.format(str(self.name))

	def __repr__(self):
		return str(self)

