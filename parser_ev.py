from ast_nodes import Number, BinOp, Var, Decl, Programa

class ParserEV:
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
        raise SyntaxError(f"Erro sintatico na posicao {posicao}: esperado {token_type}, encontrado {token}")

    def parse(self):
        node = self.programa()
        if self.current() is not None:
            tok = self.current()
            raise SyntaxError(f"Erro sintatico na posicao {tok[2]}: tokens inesperados apos expressao")
        return node

    def programa(self):
        decls = []
        tok = self.current()
        while tok and tok[0] == "IDENT":
            decls.append(self.decl())
            tok = self.current()
        if tok is None or tok[0] != "ASSIGN":
            posicao = tok[2] if tok else "?"
            raise SyntaxError(f"Erro sintatico na posicao {posicao}: esperado '=' para expressao de resultado")
        self.eat("ASSIGN")
        result = self.exp_a()
        return Programa(decls, result)

    def decl(self):
        tok = self.eat("IDENT")
        name = tok[1]
        self.eat("ASSIGN")
        expr = self.exp_a()
        self.eat("SEMICOLON")
        return Decl(name, expr)

    def exp_a(self):
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
        tok = self.current()
        if tok and tok[0] == "NUMBER":
            self.eat("NUMBER")
            return Number(tok[1])
        elif tok and tok[0] == "IDENT":
            self.eat("IDENT")
            return Var(tok[1])
        elif tok and tok[0] == "LPAREN":
            self.eat("LPAREN")
            expr = self.exp_a()
            self.eat("RPAREN")
            return expr
        else:
            posicao = tok[2] if tok else "?"
            raise SyntaxError(f"Erro sintatico na posicao {posicao}: esperado numero, identificador ou '(', encontrado {tok}")
