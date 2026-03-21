from ast_nodes import Number, BinOp, Var, Decl, Programa

def interpret_expr(node, env):
    if isinstance(node, Number):
        return node.value
    elif isinstance(node, Var):
        if node.name not in env:
            raise NameError(f"Variavel nao declarada: '{node.name}'")
        return env[node.name]
    elif isinstance(node, BinOp):
        left_val  = interpret_expr(node.left, env)
        right_val = interpret_expr(node.right, env)
        if node.op == "+":
            return left_val + right_val
        elif node.op == "-":
            return left_val - right_val
        elif node.op == "*":
            return left_val * right_val
        elif node.op == "/":
            if right_val == 0:
                raise ZeroDivisionError("Divisao por zero")
            return left_val // right_val
    raise ValueError(f"No desconhecido: {node}")

def interpret(programa):
    env = {}
    for decl in programa.decls:
        env[decl.name] = interpret_expr(decl.expr, env)
    return interpret_expr(programa.result, env)

if __name__ == "__main__":
    import sys
    from lexer import tokenize
    from parser_ev import ParserEV
    from semantic import verificar

    if len(sys.argv) != 2:
        print("Uso: python interpreter_ev.py entrada.ev")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        source = f.read()

    tokens = tokenize(source)
    programa = ParserEV(tokens).parse()
    verificar(programa)
    print(interpret(programa))
