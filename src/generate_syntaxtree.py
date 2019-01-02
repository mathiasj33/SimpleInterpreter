nodes = [
    'Binary left op right',
    'Unary op expr',
    'Grouping expr',
    'Literal value'
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

