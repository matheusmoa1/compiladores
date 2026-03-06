from ast_nodes import Number, BinOp

class Parser:
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
        ast = self.expr()
        if self.current() is not None:
            tok = self.current()
            raise SyntaxError(f"Erro sintático na posição {tok[2]}: tokens inesperados após expressão")
        return ast

    def expr(self):
        token = self.current()
        if token is None:
            raise SyntaxError("Erro sintático: expressão incompleta")

        if token[0] == "NUMBER":
            self.eat("NUMBER")
            return Number(token[1])

        elif token[0] == "LPAREN":
            self.eat("LPAREN")
            left = self.expr()
            op_token = self.current()
            if op_token and op_token[0] in ("PLUS", "MINUS", "TIMES", "DIV"):
                op = op_token[1]
                self.pos += 1
            else:
                posicao = op_token[2] if op_token else "?"
                raise SyntaxError(f"Erro sintático na posição {posicao}: operador esperado")
            right = self.expr()
            self.eat("RPAREN")
            return BinOp(left, op, right)

        else:
            raise SyntaxError(f"Erro sintático na posição {token[2]}: expressão inválida")