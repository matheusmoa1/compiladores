from parser import Parser
from codegen import CodeGen
from semantic import verificar
import sys

TEMPLATE = """
{bss}

.section .text
.globl _start
_start:
{main}
    call imprime_num
    call sair

{funcs}

.include "runtime.s"
"""

def compile_ec1(source):
    # Análise Sintática e Léxica
    parser = Parser(source)
    ast = parser.parse()
    
    # Análise Semântica
    verificar(ast)
    
    # Geração de Código
    codegen = CodeGen()
    bss, main_code, funcs_code = codegen.generate(ast)
    
    return TEMPLATE.format(bss=bss, main=main_code, funcs=funcs_code)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python compiler.py entrada.ec1 saida.s")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2]

    try:
        with open(entrada, "r") as f:
            source = f.read()

        output_assembly = compile_ec1(source)

        with open(saida, "w") as f:
            f.write(output_assembly)
        
        print(f"Sucesso! Código Assembly gerado em: {saida}")

    except Exception as e:
        print(f"Erro durante a compilação: {e}")
        sys.exit(1)