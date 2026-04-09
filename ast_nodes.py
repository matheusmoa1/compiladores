class Number:
    def __init__(self, value):
        self.value = int(value)

class BinOp:
    def __init__(self, left, op, right):
        self.left  = left   
        self.op    = op     
        self.right = right  

class Compare:
    def __init__(self, left, op, right):
        self.left  = left   
        self.op    = op     
        self.right = right  

class Var:
    def __init__(self, name):
        self.name = name    

class Decl:
    def __init__(self, name, expr):
        self.name = name    
        self.expr = expr    

class Assign:
    def __init__(self, name, expr):
        self.name = name    
        self.expr = expr    

class If:
    def __init__(self, cond, then_cmds, else_cmds):
        self.cond      = cond        
        self.then_cmds = then_cmds   
        self.else_cmds = else_cmds   

class While:
    def __init__(self, cond, cmds):
        self.cond = cond    
        self.cmds = cmds    

class Programa:
    def __init__(self, decls, cmds):
        self.decls  = decls   
        self.cmds   = cmds    

class FunDecl:
    def __init__(self, name, params, decls, cmds):
        self.name = name
        self.params = params
        self.decls = decls
        self.cmds = cmds

class Call:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Return:
    def __init__(self, expr):
        self.expr = expr