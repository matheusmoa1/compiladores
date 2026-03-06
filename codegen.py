def generate(node):
    if node.__class__.__name__ == "Number":
        return f"    mov ${node.value}, %rax\n"

    elif node.__class__.__name__ == "BinOp":
        code = ""
        code += generate(node.right)
        code += "    push %rax\n"
        code += generate(node.left)
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
