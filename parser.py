from lexer import *
from ast_nodes import *


class Parser:
    def __init__(self, text):
        self.lexer = Lexer(text)
        self.tok   = self.lexer.next_token()

    def error(self, msg):
        raise SyntaxError(f"Erro de sintaxe: {msg}. Encontrei {self.tok.type} ({self.tok.value})")

    def eat(self, ttype):
        """Confere se o token atual é o esperado e pula pro próximo"""
        if self.tok.type == ttype:
            val = self.tok.value
            self.tok = self.lexer.next_token()
            return val
        self.error(f"Esperava {ttype}")

    def parse(self):
        """
        <programa> ::= <decl>* '{' <cmd>* 'return' <exp> ';' '}'
        """
        # 1. Declarações no topo (opcionais, mas vêm antes das chaves)
        decls = []
        while self.tok.type == TK_ID and self.lexer.peek() == '=':
            # Se é um ID seguido de '=', é uma declaração global
            name = self.eat(TK_ID)
            self.eat(TK_ASSIGN)
            expr = self.parse_expr()
            self.eat(TK_SEMI)
            decls.append(Decl(name, expr))

        # 2. O corpo do programa começa com '{' 
        self.eat(TK_LBRACE)
        
        # 3. Lista de comandos (if, while, atribuição) 
        cmds = []
        while self.tok.type in (TK_ID, 'IF', 'WHILE'):
            cmds.append(self.parse_cmd())

        # 4. O retorno obrigatório 
        self.eat('RETURN')
        result = self.parse_expr()
        self.eat(TK_SEMI)
        
        # 5. Fecha o programa
        self.eat(TK_RBRACE)
        
        return Programa(decls, cmds, result)

    def parse_cmd(self):
        # <cmd> ::= <if> | <while> | <atrib>
        if self.tok.type == 'IF':
            return self.parse_if()
        elif self.tok.type == 'WHILE':
            return self.parse_while()
        else:
            return self.parse_assign()

    def parse_assign(self):
        # <atrib> ::= <var> '=' <exp> ';'
        name = self.eat(TK_ID)
        self.eat(TK_ASSIGN)
        expr = self.parse_expr()
        self.eat(TK_SEMI)
        return Assign(name, expr)

    def parse_if(self):
        # 'if' <exp> '{' <cmd>* '}' 'else' '{' <cmd>* '}'
        self.eat('IF')
        cond = self.parse_expr()
        
        self.eat(TK_LBRACE)
        then_cmds = []
        while self.tok.type in (TK_ID, 'IF', 'WHILE'):
            then_cmds.append(self.parse_cmd())
        self.eat(TK_RBRACE)

        self.eat('ELSE')
        self.eat(TK_LBRACE)
        else_cmds = []
        while self.tok.type in (TK_ID, 'IF', 'WHILE'):
            else_cmds.append(self.parse_cmd())
        self.eat(TK_RBRACE)

        return If(cond, then_cmds, else_cmds)

    def parse_while(self):
        # 'while' <exp> '{' <cmd>* '}'
        self.eat('WHILE')
        cond = self.parse_expr()
        
        self.eat(TK_LBRACE)
        cmds = []
        while self.tok.type in (TK_ID, 'IF', 'WHILE'):
            cmds.append(self.parse_cmd())
        self.eat(TK_RBRACE)
        
        return While(cond, cmds)


    def parse_expr(self):
        # Nível mais baixo: Comparações (<, >, ==)
        node = self.parse_arith()
        op_map = {TK_LT: '<', TK_GT: '>', TK_EQ: '=='}
        
        if self.tok.type in op_map:
            op = op_map[self.tok.type]
            self.eat(self.tok.type)
            # Compara o que veio antes com a próxima expressão aritmética
            node = Compare(node, op, self.parse_arith())
        return node

    def parse_arith(self):
        # Soma e Subtração (+, -)
        node = self.parse_term()
        while self.tok.type in (TK_PLUS, TK_MINUS):
            op = self.tok.value
            self.eat(self.tok.type)
            node = BinOp(node, op, self.parse_term())
        return node

    def parse_term(self):
        # Multiplicação e Divisão (*, /) 
        node = self.parse_factor()
        while self.tok.type in (TK_MUL, TK_DIV):
            op = self.tok.value
            self.eat(self.tok.type)
            node = BinOp(node, op, self.parse_factor())
        return node

    def parse_factor(self):
        # Números, Variáveis ou parênteses 
        if self.tok.type == TK_NUM:
            return Number(self.eat(TK_NUM))
        elif self.tok.type == TK_ID:
            return Var(self.eat(TK_ID))
        elif self.tok.type == TK_LPAREN:
            self.eat(TK_LPAREN)
            node = self.parse_expr()
            self.eat(TK_RPAREN)
            return node
        self.error("Esperava número, variável ou '('")