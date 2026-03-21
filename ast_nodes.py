class Number:
    def __init__(self, value):
        self.value = int(value)

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Var:
    def __init__(self, name):
        self.name = name

class Decl:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Programa:
    def __init__(self, decls, result):
        self.decls = decls
        self.result = result
