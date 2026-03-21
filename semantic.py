from ast_nodes import Number, BinOp, Var, Decl, Programa

def verificar_expr(node, declaradas):
    if isinstance(node, Number):
        return
    elif isinstance(node, Var):
        if node.name not in declaradas:
            raise NameError(f"Erro semantico: variavel '{node.name}' nao foi declarada")
    elif isinstance(node, BinOp):
        verificar_expr(node.left, declaradas)
        verificar_expr(node.right, declaradas)
    else:
        raise ValueError(f"No desconhecido na analise semantica: {node}")

def verificar(programa):
    declaradas = set()
    for decl in programa.decls:
        verificar_expr(decl.expr, declaradas)
        declaradas.add(decl.name)
    verificar_expr(programa.result, declaradas)
