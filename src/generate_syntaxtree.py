nodes = [
    'Binary left op right',
    'Unary op expr',
    'Grouping expr',
    'Literal value',
    'Identifier name',
    'LogicalBinary left op right',
    'LogicalUnary op expr',
    'Comparison left op right',
    'StringBinary left op right',
    'FunCall callee args',
    'Fun name args body',
    'Assign left right',
    'ExprStmt expr',
    'Ret expr',
    'If cond left right',
    'While cond body',
    'Program stmts'
]

with open('syntaxtree.py', 'w') as f:
    for node in nodes:
        arr = node.split(' ')
        f.write('class {}:\n'.format(arr[0]))
        f.write('\tdef __init__(self')
        for arg in arr[1:]:
            f.write(', {}'.format(arg))
        f.write('):\n')
        for arg in arr[1:]:
            f.write('\t\tself.{} = {}\n'.format(arg, arg))
        f.write('\n')
        f.write('\tdef accept(self, visitor):\n')
        f.write('\t\treturn visitor.visit_{}(self)\n'.format(arr[0].lower()))
        f.write('\n')
        f.write('\tdef __eq__(self, other):\n')
        f.write('\t\tif not isinstance(other, {}): return False\n'.format(arr[0]))
        f.write('\t\telif self is other: return True\n')
        f.write('\t\telse:\n')
        f.write('\t\t\treturn True')
        for arg in arr[1:]:
            f.write(' and self.{} == other.{}'.format(arg, arg))
        f.write('\n\n')
        f.write('\tdef __str__(self):\n')
        f.write('\t\treturn \'{}('.format(arr[0]))
        f.write(', '.join(['{}'] * len(arr[1:])))
        f.write(')\'.format(')
        f.write(', '.join(['str(self.{})'.format(arg) for arg in arr[1:]]))
        f.write(')')
        f.write('\n\n')
        f.write('\tdef __repr__(self):\n')
        f.write('\t\treturn str(self)')
        f.write('\n\n')

