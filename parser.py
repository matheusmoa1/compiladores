from lexer import *
from ast_nodes import *

class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.tok   = self.lexer.next_token()

    def error(self, msg):
        raise SyntaxError(f"Erro de sintaxe: {msg}. Encontrei {self.tok.type} ({self.tok.value})")

    def eat(self, ttype):
        if self.tok.type == ttype:
            val = self.tok.value
            self.tok = self.lexer.next_token()
            return val
        self.error(f"Esperava {ttype}")

    def parse(self):
        decls = []
        while self.tok.type in ('VAR', 'FUN'):
            if self.tok.type == 'VAR':
                self.eat('VAR')
                name = self.eat(TK_ID)
                self.eat(TK_ASSIGN)
                expr = self.parse_expr()
                self.eat(TK_SEMI)
                decls.append(Decl(name, expr))
            else:
                decls.append(self.parse_fundecl())

        self.eat('MAIN')
        self.eat(TK_LBRACE)
        
        cmds = []
        while self.tok.type in (TK_ID, 'IF', 'WHILE', 'RETURN'):
            cmds.append(self.parse_cmd())

        self.eat(TK_RBRACE)
        return Programa(decls, cmds)

    def parse_fundecl(self):
        self.eat('FUN')
        name = self.eat(TK_ID)
        self.eat(TK_LPAREN)
        
        params = []
        if self.tok.type == TK_ID:
            params.append(self.eat(TK_ID))
            while self.tok.type == TK_COMMA:
                self.eat(TK_COMMA)
                params.append(self.eat(TK_ID))
        self.eat(TK_RPAREN)
        self.eat(TK_LBRACE)
        
        decls = []
        while self.tok.type == 'VAR':
            self.eat('VAR')
            vname = self.eat(TK_ID)
            self.eat(TK_ASSIGN)
            vexpr = self.parse_expr()
            self.eat(TK_SEMI)
            decls.append(Decl(vname, vexpr))
            
        cmds = []
        while self.tok.type in (TK_ID, 'IF', 'WHILE', 'RETURN'):
            cmds.append(self.parse_cmd())
            
        self.eat(TK_RBRACE)
        return FunDecl(name, params, decls, cmds)

    def parse_cmd(self):
        if self.tok.type == 'IF':
            return self.parse_if()
        elif self.tok.type == 'WHILE':
            return self.parse_while()
        elif self.tok.type == 'RETURN':
            self.eat('RETURN')
            expr = self.parse_expr()
            self.eat(TK_SEMI)
            return Return(expr)
        else:
            return self.parse_assign()

    def parse_assign(self):
        name = self.eat(TK_ID)
        self.eat(TK_ASSIGN)
        expr = self.parse_expr()
        self.eat(TK_SEMI)
        return Assign(name, expr)

    def parse_if(self):
        self.eat('IF')
        cond = self.parse_expr()
        
        self.eat(TK_LBRACE)
        then_cmds = []
        while self.tok.type in (TK_ID, 'IF', 'WHILE', 'RETURN'):
            then_cmds.append(self.parse_cmd())
        self.eat(TK_RBRACE)

        self.eat('ELSE')
        self.eat(TK_LBRACE)
        else_cmds = []
        while self.tok.type in (TK_ID, 'IF', 'WHILE', 'RETURN'):
            else_cmds.append(self.parse_cmd())
        self.eat(TK_RBRACE)

        return If(cond, then_cmds, else_cmds)

    def parse_while(self):
        self.eat('WHILE')
        cond = self.parse_expr()
        
        self.eat(TK_LBRACE)
        cmds = []
        while self.tok.type in (TK_ID, 'IF', 'WHILE', 'RETURN'):
            cmds.append(self.parse_cmd())
        self.eat(TK_RBRACE)
        
        return While(cond, cmds)


    def parse_expr(self):
        node = self.parse_arith()
        op_map = {
            TK_LT: '<', TK_GT: '>', TK_EQ: '==', 
            TK_LE: '<=', TK_GE: '>=', TK_NE: '!='
        }
        
        if self.tok.type in op_map:
            op = op_map[self.tok.type]
            self.eat(self.tok.type)
            node = Compare(node, op, self.parse_arith())
        return node

    def parse_arith(self):
        node = self.parse_term()
        while self.tok.type in (TK_PLUS, TK_MINUS):
            op = self.tok.value
            self.eat(self.tok.type)
            node = BinOp(node, op, self.parse_term())
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.tok.type in (TK_MUL, TK_DIV, TK_MOD):
            op = self.tok.value
            self.eat(self.tok.type)
            node = BinOp(node, op, self.parse_factor())
        return node

    def parse_factor(self):
        if self.tok.type == TK_NUM:
            return Number(self.eat(TK_NUM))
        elif self.tok.type == TK_ID:
            name = self.eat(TK_ID)
            if self.tok.type == TK_LPAREN:
                self.eat(TK_LPAREN)
                args = []
                if self.tok.type != TK_RPAREN:
                    args.append(self.parse_expr())
                    while self.tok.type == TK_COMMA:
                        self.eat(TK_COMMA)
                        args.append(self.parse_expr())
                self.eat(TK_RPAREN)
                return Call(name, args)
            return Var(name)
        elif self.tok.type == TK_LPAREN:
            self.eat(TK_LPAREN)
            node = self.parse_expr()
            self.eat(TK_RPAREN)
            return node
        self.error("Esperava numero, variavel ou '('")