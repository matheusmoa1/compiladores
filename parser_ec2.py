from ast_nodes import Number, BinOp

class ParserEC2:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token_type):
        token = self.current()
        if token and token[0] == token_type:
            self.pos += 1
            return token
        posicao = token[2] if token else "?"
        raise SyntaxError(f"Erro sintático na posição {posicao}: esperado {token_type}, encontrado {token}")

    def parse(self):
        # <programa> ::= <exp_a>
        ast = self.exp_a()
        if self.current() is not None:
            tok = self.current()
            raise SyntaxError(f"Erro sintático na posição {tok[2]}: tokens inesperados após expressão")
        return ast

    def exp_a(self):
        # <exp_a> ::= <exp_m> (('+' | '-') <exp_m>)*
        left = self.exp_m()
        while True:
            tok = self.current()
            if tok and tok[0] in ("PLUS", "MINUS"):
                op = tok[1]
                self.pos += 1
                right = self.exp_m()
                left = BinOp(left, op, right)
            else:
                break
        return left

    def exp_m(self):
        # <exp_m> ::= <prim> (('*' | '/') <prim>)*
        left = self.prim()
        while True:
            tok = self.current()
            if tok and tok[0] in ("TIMES", "DIV"):
                op = tok[1]
                self.pos += 1
                right = self.prim()
                left = BinOp(left, op, right)
            else:
                break
        return left

    def prim(self):
        # <prim> ::= <num> | '(' <exp_a> ')'
        tok = self.current()
        if tok and tok[0] == "NUMBER":
            self.eat("NUMBER")
            return Number(tok[1])
        elif tok and tok[0] == "LPAREN":
            self.eat("LPAREN")
            expr = self.exp_a()
            self.eat("RPAREN")
            return expr
        else:
            raise SyntaxError(f"Erro sintático na posição {tok[2]}: esperado número ou '(', encontrado {tok}")
