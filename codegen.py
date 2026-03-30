from ast_nodes import *

class CodeGen:
    def __init__(self):
        self.code = []
        self.label_count = 0

    def new_label(self, prefix):
        # Cria nomes de rótulos únicos (ex: Lfim1, Lfim2) pra não dar conflito
        self.label_count += 1
        return f"{prefix}{self.label_count}"

    def generate(self, programa):
        # 1. Seção .bss: Reservamos 8 bytes (64 bits) para cada variável declarada
        bss = [".section .bss"]
        for d in programa.decls:
            bss.append(f"{d.name}: .quad 0")
        
        # 2. Seção .text: Onde o código de verdade acontece
        self.code = [
            ".section .text", 
            ".globl _start", 
            "_start:"
        ]

        # Inicializa as variáveis com os valores definidos nas declarações do topo
        for d in programa.decls:
            self.gen_expr(d.expr)
            self.code.append(f"    movq %rax, {d.name}  # Inicializa {d.name}")

        # Gera o código para cada comando (if, while, atribuição) no corpo do programa
        for cmd in programa.cmds:
            self.gen_cmd(cmd)

        # Gera a expressão final de retorno (o resultado vai pra %rax)
        self.gen_expr(programa.result)

        return "\n".join(bss), "\n".join(self.code)

    def gen_cmd(self, node):
        # Transforma comandos em instruções de salto e memória.
        if isinstance(node, Assign):
            # Calcula a conta e salva o resultado no endereço da variável
            self.gen_expr(node.expr)
            self.code.append(f"    movq %rax, {node.name}  # {node.name} = valor")

        elif isinstance(node, If):
            # Lógica do IF/ELSE usando saltos
            l_else = self.new_label("Lfalso")
            l_end  = self.new_label("Lfim")

            self.gen_expr(node.cond)           # Resultado da condição em RAX
            self.code.append("    cmpq $0, %rax")   # Compara com zero (falso)
            self.code.append(f"    jz {l_else}")   # Se for 0, pula pro ELSE

            for c in node.then_cmds: self.gen_cmd(c)
            self.code.append(f"    jmp {l_end}")   # Pula o ELSE pra não executar os dois

            self.code.append(f"{l_else}:")
            for c in node.else_cmds: self.gen_cmd(c)
            self.code.append(f"{l_end}:")

        elif isinstance(node, While):
            # Lógica do WHILE (volta pro início até a condição falhar)
            l_start = self.new_label("Linicio")
            l_end   = self.new_label("Lfim")

            self.code.append(f"{l_start}:")
            self.gen_expr(node.cond)
            self.code.append("    cmpq $0, %rax")   # Testa se ainda é verdadeiro
            self.code.append(f"    jz {l_end}")     # Se for zero (falso), sai do loop

            for c in node.cmds: self.gen_cmd(c)
            self.code.append(f"    jmp {l_start}") # Volta e testa de novo
            self.code.append(f"{l_end}:")

    def gen_expr(self, node):
        # Transforma contas e comparações em assembly.
        if isinstance(node, Number):
            self.code.append(f"    movq ${node.value}, %rax")

        elif isinstance(node, Var):
            self.code.append(f"    movq {node.name}, %rax")

        elif isinstance(node, BinOp):
            # Resolve a direita, guarda na pilha, resolve a esquerda, tira da pilha e opera
            self.gen_expr(node.right)
            self.code.append("    pushq %rax")
            self.gen_expr(node.left)
            self.code.append("    popq %rbx")

            ops = {
                '+': 'addq %rbx, %rax',
                '-': 'subq %rbx, %rax',
                '*': 'imulq %rbx, %rax'
            }
            self.code.append(f"    {ops[node.op]}")

        elif isinstance(node, Compare):
            self.gen_expr(node.right)
            self.code.append("    pushq %rax")
            self.gen_expr(node.left)
            self.code.append("    popq %rbx")
            
            self.code.append("    xorq %rcx, %rcx")
            self.code.append("    cmpq %rax, %rbx") 
            
            set_op = {'==': 'setz', '<': 'setg', '>': 'setl'}[node.op]
            self.code.append(f"    {set_op} %cl")
            self.code.append("    movq %rcx, %rax")