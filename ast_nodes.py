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
        # Novo na área! Serve pros testes de <, > e == que o If e o While pedem
        self.left  = left   
        self.op    = op     
        self.right = right  

class Var:
    def __init__(self, name):
        # Só pra quando a gente "chama" a variável no meio da conta
        self.name = name    

class Decl:
    def __init__(self, name, expr):
        # Usado APENAS no topo do programa. Aqui é onde a variável nasce
        self.name = name    
        self.expr = expr    

class Assign:
    def __init__(self, name, expr):
        # Importante: atribuição NÃO cria variável nova. Só muda o valor de uma que já existe
        self.name = name    
        self.expr = expr    

class If:
    def __init__(self, cond, then_cmds, else_cmds):
        # A lógica do "e se...". O PDF exige que tenha o bloco else, mesmo que vazio
        self.cond      = cond        
        self.then_cmds = then_cmds   
        self.else_cmds = else_cmds   

class While:
    def __init__(self, cond, cmds):
        # Onde a mágica (e os loops infinitos) acontecem
        self.cond = cond    
        self.cmds = cmds    

class Programa:
    def __init__(self, decls, cmds, result):
        # O nó mestre. Um programa agora é: Declarações -> Comandos -> Retorno
        self.decls  = decls   
        self.cmds   = cmds    
        self.result = result