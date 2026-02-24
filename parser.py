
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
        raise SyntaxError(f"Esperado {token_type}, encontrado {token}")

    def parse(self):
        return self.expr()

    def expr(self):
        token = self.current()

        if token[0] == "NUMBER":
            self.eat("NUMBER")
            return Number(token[1])

        elif token[0] == "LPAREN":
            self.eat("LPAREN")
            left = self.expr()
            op_token = self.current()
            if op_token[0] in ("PLUS", "MINUS", "TIMES", "DIV"):
                op = op_token[1]
                self.pos += 1
            else:
                raise SyntaxError("Operador esperado")
            right = self.expr()
            self.eat("RPAREN")
            return BinOp(left, op, right)

        else:
            raise SyntaxError("Expressão inválida")
