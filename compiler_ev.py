from lexer import tokenize
from parser_ev import ParserEV
from semantic import verificar
from codegen import generate
import sys

TEMPLATE = """\
{bss}
.section .text
.globl _start
_start:
{code}
    call imprime_num
    call sair
.include "runtime.s"
"""

def compile_ev(source):
    tokens = tokenize(source)
    parser = ParserEV(tokens)
    programa = parser.parse()
    verificar(programa)
    bss, code = generate(programa)
    return TEMPLATE.format(bss=bss, code=code)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python compiler_ev.py entrada.ev saida.s")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        source = f.read()

    output = compile_ev(source)

    with open(sys.argv[2], "w") as f:
        f.write(output)
