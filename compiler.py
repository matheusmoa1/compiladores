import sys
from lexer import Lexer
from parser import Parser
from semantic import verificar
from codegen import CodeGen

TEMPLATE = """\
{bss}

.section .text
.globl _start

_start:
{code}
    # O resultado final do programa (que está em %rax) é impresso aqui
    call imprime_num
    call sair

# Esse arquivo precisa estar na mesma pasta pra o 'as' e 'ld' funcionarem
.include "runtime.s"
"""

def compile_cmd(source_code):
    # O grande fluxo: Transforma texto puro em Assembly x86-64.
    # 1. Análise Léxica e Sintática (Transforma texto em árvore/AST)
    parser = Parser(source_code)
    ast = parser.parse()

    # 2. Análise Semântica (checa se as variáveis existem)
    verificar(ast)

    # 3. Geração de Código (Transforma a árvore em Assembly real)
    generator = CodeGen()
    bss_part, code_part = generator.generate(ast)

    # 4. Monta o arquivo final usando nosso template
    return TEMPLATE.format(bss=bss_part, code=code_part)

if __name__ == "__main__":
    # Checa se o usuário passou os arquivos de entrada e saída no terminal
    if len(sys.argv) != 3:
        print("Uso: python compiler.py entrada.cmd saida.s")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2]

    try:
        # Lê o seu código na linguagem Cmd
        with open(entrada, "r") as f:
            source = f.read()

        # Faz a mágica acontecer
        output_assembly = compile_cmd(source)

        # Salva o resultado no arquivo .s
        with open(saida, "w") as f:
            f.write(output_assembly)
        
        print(f"Sucesso! Código Assembly gerado em: {saida}")

    except Exception as e:
        # Se der erro de sintaxe ou semântica, a gente avisa aqui
        print(f"❌ Erro durante a compilação: {e}")
        sys.exit(1)