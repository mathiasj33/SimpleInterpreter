class Binary:
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

	def accept(self, visitor):
		return visitor.visit_binary(self)

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

	def accept(self, visitor):
		return visitor.visit_unary(self)

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

	def accept(self, visitor):
		return visitor.visit_grouping(self)

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

	def accept(self, visitor):
		return visitor.visit_literal(self)

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

	def accept(self, visitor):
		return visitor.visit_identifier(self)

	def __eq__(self, other):
		if not isinstance(other, Identifier): return False
		elif self is other: return True
		else:
			return True and self.name == other.name

	def __str__(self):
		return 'Identifier({})'.format(str(self.name))

	def __repr__(self):
		return str(self)

class LogicalBinary:
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

	def accept(self, visitor):
		return visitor.visit_logicalbinary(self)

	def __eq__(self, other):
		if not isinstance(other, LogicalBinary): return False
		elif self is other: return True
		else:
			return True and self.left == other.left and self.op == other.op and self.right == other.right

	def __str__(self):
		return 'LogicalBinary({}, {}, {})'.format(str(self.left), str(self.op), str(self.right))

	def __repr__(self):
		return str(self)

class LogicalUnary:
	def __init__(self, op, expr):
		self.op = op
		self.expr = expr

	def accept(self, visitor):
		return visitor.visit_logicalunary(self)

	def __eq__(self, other):
		if not isinstance(other, LogicalUnary): return False
		elif self is other: return True
		else:
			return True and self.op == other.op and self.expr == other.expr

	def __str__(self):
		return 'LogicalUnary({}, {})'.format(str(self.op), str(self.expr))

	def __repr__(self):
		return str(self)

class Comparison:
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

	def accept(self, visitor):
		return visitor.visit_comparison(self)

	def __eq__(self, other):
		if not isinstance(other, Comparison): return False
		elif self is other: return True
		else:
			return True and self.left == other.left and self.op == other.op and self.right == other.right

	def __str__(self):
		return 'Comparison({}, {}, {})'.format(str(self.left), str(self.op), str(self.right))

	def __repr__(self):
		return str(self)

class StringBinary:
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

	def accept(self, visitor):
		return visitor.visit_stringbinary(self)

	def __eq__(self, other):
		if not isinstance(other, StringBinary): return False
		elif self is other: return True
		else:
			return True and self.left == other.left and self.op == other.op and self.right == other.right

	def __str__(self):
		return 'StringBinary({}, {}, {})'.format(str(self.left), str(self.op), str(self.right))

	def __repr__(self):
		return str(self)

class FunCall:
	def __init__(self, callee, args):
		self.callee = callee
		self.args = args

	def accept(self, visitor):
		return visitor.visit_funcall(self)

	def __eq__(self, other):
		if not isinstance(other, FunCall): return False
		elif self is other: return True
		else:
			return True and self.callee == other.callee and self.args == other.args

	def __str__(self):
		return 'FunCall({}, {})'.format(str(self.callee), str(self.args))

	def __repr__(self):
		return str(self)

class Fun:
	def __init__(self, name, args, body):
		self.name = name
		self.args = args
		self.body = body

	def accept(self, visitor):
		return visitor.visit_fun(self)

	def __eq__(self, other):
		if not isinstance(other, Fun): return False
		elif self is other: return True
		else:
			return True and self.name == other.name and self.args == other.args and self.body == other.body

	def __str__(self):
		return 'Fun({}, {}, {})'.format(str(self.name), str(self.args), str(self.body))

	def __repr__(self):
		return str(self)

class Assign:
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def accept(self, visitor):
		return visitor.visit_assign(self)

	def __eq__(self, other):
		if not isinstance(other, Assign): return False
		elif self is other: return True
		else:
			return True and self.left == other.left and self.right == other.right

	def __str__(self):
		return 'Assign({}, {})'.format(str(self.left), str(self.right))

	def __repr__(self):
		return str(self)

class ExprStmt:
	def __init__(self, expr):
		self.expr = expr

	def accept(self, visitor):
		return visitor.visit_exprstmt(self)

	def __eq__(self, other):
		if not isinstance(other, ExprStmt): return False
		elif self is other: return True
		else:
			return True and self.expr == other.expr

	def __str__(self):
		return 'ExprStmt({})'.format(str(self.expr))

	def __repr__(self):
		return str(self)

class Ret:
	def __init__(self, expr):
		self.expr = expr

	def accept(self, visitor):
		return visitor.visit_ret(self)

	def __eq__(self, other):
		if not isinstance(other, Ret): return False
		elif self is other: return True
		else:
			return True and self.expr == other.expr

	def __str__(self):
		return 'Ret({})'.format(str(self.expr))

	def __repr__(self):
		return str(self)

class If:
	def __init__(self, cond, left, right):
		self.cond = cond
		self.left = left
		self.right = right

	def accept(self, visitor):
		return visitor.visit_if(self)

	def __eq__(self, other):
		if not isinstance(other, If): return False
		elif self is other: return True
		else:
			return True and self.cond == other.cond and self.left == other.left and self.right == other.right

	def __str__(self):
		return 'If({}, {}, {})'.format(str(self.cond), str(self.left), str(self.right))

	def __repr__(self):
		return str(self)

class While:
	def __init__(self, cond, body):
		self.cond = cond
		self.body = body

	def accept(self, visitor):
		return visitor.visit_while(self)

	def __eq__(self, other):
		if not isinstance(other, While): return False
		elif self is other: return True
		else:
			return True and self.cond == other.cond and self.body == other.body

	def __str__(self):
		return 'While({}, {})'.format(str(self.cond), str(self.body))

	def __repr__(self):
		return str(self)

class Program:
	def __init__(self, stmts):
		self.stmts = stmts

	def accept(self, visitor):
		return visitor.visit_program(self)

	def __eq__(self, other):
		if not isinstance(other, Program): return False
		elif self is other: return True
		else:
			return True and self.stmts == other.stmts

	def __str__(self):
		return 'Program({})'.format(str(self.stmts))

	def __repr__(self):
		return str(self)

