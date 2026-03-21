from ast_nodes import Number, BinOp, Var, Decl, Programa

def generate_expr(node):
    if isinstance(node, Number):
        return f"    mov ${node.value}, %rax\n"

    elif isinstance(node, Var):
        return f"    mov {node.name}(%rip), %rax\n"

    elif isinstance(node, BinOp):
        code = ""
        code += generate_expr(node.right)
        code += "    push %rax\n"
        code += generate_expr(node.left)
        code += "    pop %rbx\n"
        if node.op == "+":
            code += "    add %rbx, %rax\n"
        elif node.op == "-":
            code += "    sub %rbx, %rax\n"
        elif node.op == "*":
            code += "    imul %rbx, %rax\n"
        elif node.op == "/":
            code += "    cqo\n"
            code += "    idiv %rbx\n"
        return code

    else:
        raise ValueError(f"No desconhecido em generate_expr: {node}")

def generate(programa):
    bss = ".section .bss\n"
    for decl in programa.decls:
        bss += f"    .lcomm {decl.name}, 8\n"

    code = ""
    for decl in programa.decls:
        code += generate_expr(decl.expr)
        code += f"    mov %rax, {decl.name}(%rip)\n"

    code += generate_expr(programa.result)
    return bss, code
