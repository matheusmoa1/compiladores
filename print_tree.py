from ast_nodes import Number, BinOp

def print_tree(node):
    """Reconstrói a expressão EC1 a partir da árvore (formato original)."""
    if isinstance(node, Number):
        return str(node.value)
    elif isinstance(node, BinOp):
        left  = print_tree(node.left)
        right = print_tree(node.right)
        return f"({left} {node.op} {right})"
    raise ValueError(f"Nó desconhecido: {node}")