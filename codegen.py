from ast_nodes import *

class CodeGen:
    def __init__(self):
        self.code = []
        self.label_count = 0
        self.env = {}

    def new_label(self, prefix):
        self.label_count += 1
        return f"{prefix}{self.label_count}"

    def get_var_addr(self, name):
        if name in self.env:
            return self.env[name]
        return f"{name}"

    def generate(self, programa):
        bss = [".section .bss"]
        for d in programa.decls:
            if isinstance(d, Decl):
                bss.append(f"    {d.name}: .quad 0")
        
        self.code = []

        self.env = {}
        for d in programa.decls:
            if isinstance(d, Decl):
                self.gen_expr(d.expr)
                self.code.append(f"    movq %rax, {d.name}")

        for cmd in programa.cmds:
            self.gen_cmd(cmd)

        self.gen_expr(programa.result)
        main_code = self.code

        funcs_code = []
        for fdecl in programa.decls:
            if isinstance(fdecl, FunDecl):
                self.env = {}
                self.code = []
                
                L = len(fdecl.decls)
                num_params = len(fdecl.params)
                
                for idx, pname in enumerate(fdecl.params):
                    offset = (L * 8) + 16 + (idx * 8)
                    self.env[pname] = f"{offset}(%rbp)"
                
                for idx, vdecl in enumerate(fdecl.decls):
                    offset = idx * 8
                    self.env[vdecl.name] = f"{offset}(%rbp)"

                self.code.append(f"{fdecl.name}:")
                self.code.append(f"    pushq %rbp")
                
                if L > 0:
                    self.code.append(f"    subq ${L * 8}, %rsp")
                    
                self.code.append(f"    movq %rsp, %rbp")
                
                for idx, vdecl in enumerate(fdecl.decls):
                    self.gen_expr(vdecl.expr)
                    addr = self.get_var_addr(vdecl.name)
                    self.code.append(f"    movq %rax, {addr}")
                    
                for cmd in fdecl.cmds:
                    self.gen_cmd(cmd)
                    
                self.gen_expr(fdecl.result)
                
                if L > 0:
                    self.code.append(f"    addq ${L * 8}, %rsp")
                self.code.append(f"    popq %rbp")
                self.code.append(f"    ret")
                
                funcs_code.extend(self.code)

        final_main = "\n".join(main_code)
        final_funcs = "\n".join(funcs_code)
        return "\n".join(bss), final_main, final_funcs

    def gen_cmd(self, node):
        if isinstance(node, Assign):
            self.gen_expr(node.expr)
            addr = self.get_var_addr(node.name)
            self.code.append(f"    movq %rax, {addr}")

        elif isinstance(node, If):
            l_else = self.new_label("Lfalso")
            l_end  = self.new_label("Lfim")

            self.gen_expr(node.cond)
            self.code.append("    cmpq $0, %rax")
            self.code.append(f"    jz {l_else}")

            for c in node.then_cmds: self.gen_cmd(c)
            self.code.append(f"    jmp {l_end}")

            self.code.append(f"{l_else}:")
            for c in node.else_cmds: self.gen_cmd(c)
            self.code.append(f"{l_end}:")

        elif isinstance(node, While):
            l_start = self.new_label("Linicio")
            l_end   = self.new_label("Lfim")

            self.code.append(f"{l_start}:")
            self.gen_expr(node.cond)
            self.code.append("    cmpq $0, %rax")
            self.code.append(f"    jz {l_end}")

            for c in node.cmds: self.gen_cmd(c)
            self.code.append(f"    jmp {l_start}")
            self.code.append(f"{l_end}:")

    def gen_expr(self, node):
        if isinstance(node, Number):
            self.code.append(f"    movq ${node.value}, %rax")

        elif isinstance(node, Var):
            addr = self.get_var_addr(node.name)
            self.code.append(f"    movq {addr}, %rax")
            
        elif isinstance(node, Call):
            for arg in reversed(node.args):
                self.gen_expr(arg)
                self.code.append(f"    pushq %rax")
            
            self.code.append(f"    call {node.name}")
            
            if len(node.args) > 0:
                self.code.append(f"    addq ${len(node.args) * 8}, %rsp")

        elif isinstance(node, BinOp):
            self.gen_expr(node.right)
            self.code.append("    pushq %rax")
            self.gen_expr(node.left)
            self.code.append("    popq %rbx")

            ops = {
                '+': 'addq %rbx, %rax',
                '-': 'subq %rbx, %rax',
                '*': 'imulq %rbx, %rax',
                '/': 'cqto\n    idivq %rbx'
            }
            if node.op == '/':
                self.code.append("    cqto")
                self.code.append("    idivq %rbx")
            else:
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