from lexer import tokenize
from parser_ec2 import ParserEC2
from codegen import generate
import sys

TEMPLATE = """
.section .text
.globl _start
_start:
{code}
call imprime_num
call sair
.include "runtime.s"
"""

def compile_ec2(source):
    tokens = tokenize(source)
    parser = ParserEC2(tokens)
    ast = parser.parse()
    asm_code = generate(ast)
    return TEMPLATE.format(code=asm_code)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python compiler_ec2.py entrada.ec2 saida.s")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        source = f.read()

    output = compile_ec2(source)

    with open(sys.argv[2], "w") as f:
        f.write(output)
