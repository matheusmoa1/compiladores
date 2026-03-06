from ast_nodes import Number, BinOp

def interpret(node):
    if isinstance(node, Number):
        return node.value
    elif isinstance(node, BinOp):
        left_val  = interpret(node.left)
        right_val = interpret(node.right)
        if node.op == "+":
            return left_val + right_val
        elif node.op == "-":
            return left_val - right_val
        elif node.op == "*":
            return left_val * right_val
        elif node.op == "/":
            if right_val == 0:
                raise ZeroDivisionError("Divisão por zero na expressão EC1")
            return left_val // right_val
    raise ValueError(f"Nó desconhecido: {node}")

if __name__ == "__main__":
    import sys
    from lexer import tokenize
    from parser import Parser

    if len(sys.argv) != 2:
        print("Uso: python interpreter.py entrada.ec1")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        source = f.read()
    tokens = tokenize(source)
    ast = Parser(tokens).parse()
    print(interpret(ast))