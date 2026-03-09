> Equipe: Alisson Gabriel, Cassio Vittori, Hiago Galdino e Matheus Oliveira

# Compilador EC1


Compilador para a linguagem **EC1 (Expressões Constantes 1)**, desenvolvido na disciplina de Compiladores.  
Traduz expressões aritméticas com operandos constantes para código Assembly x86-64.

## Exemplos de programas EC1 válidos

```
333
(6 * 7)
(3 + (4 + (11 + 7)))
((427 / 7) + (11 * (231 + 5)))
```

## Estrutura do projeto

```
compiladores/
├── ast_nodes.py       # Nós da árvore sintática (Number, BinOp)
├── lexer.py           # Análise léxica — gera tokens com posição
├── parser.py          # Análise sintática — produz a AST
├── interpreter.py     # Interpretador por varredura da árvore
├── print_tree.py      # Impressão da AST no formato EC1
├── codegen.py         # Geração de código Assembly x86-64
├── compiler.py        # Pipeline completo: EC1 → arquivo .s
├── test_ec1.py        # Testes automatizados (pytest)
├── requirements.txt   # Dependências do projeto
├── tests/             # Programas EC1 usados nos testes
│   ├── constante.ec1
│   ├── soma_simples.ec1
│   ├── exemplo_pdf.ec1
│   ├── complexo.ec1
│   ├── erro_lexico.ec1
│   └── ...
└── runtime.s          # Sub-rotinas de impressão e saída (Assembly)
```

## Pré-requisitos

- Python 3.8+

## Como usar

### Analisador léxico (Atividade 04)
Imprime a sequência de tokens do programa de entrada:
```bash
python lexer.py tests/exemplo_pdf.ec1
```
Saída:
```
<LPAREN, "(", 0>
<NUMBER, "33", 1>
<PLUS, "+", 4>
...
```

### Interpretador (Atividade 05)
Executa o programa EC1 e imprime o resultado:
```bash
python interpreter.py tests/exemplo_pdf.ec1
```
Saída:
```
10065
```

### Compilador completo (Atividade 07)
Compila um programa EC1 para Assembly x86-64:
```bash
python compiler.py tests/exemplo_pdf.ec1 saida.s
cat saida.s
```

## Erros detectados

O compilador detecta e reporta erros com a posição no arquivo:

| Tipo | Exemplo | Mensagem |
|------|---------|----------|
| Léxico | `(3 @ 4)` | `Erro léxico na posição 3: caractere inesperado '@'` |
| Sintático | `(3 4)` | `Erro sintático na posição 3: operador esperado` |
| Semântico | `(5 / 0)` | `Divisão por zero na expressão EC1` |

## Montando e executando o assembly (Linux/WSL)

Para montar o arquivo `.s` gerado e criar um executável, é necessário o arquivo `runtime.s` e o GNU Assembler:

```bash
as saida.s -o saida.o
ld saida.o -o saida
./saida
```

> O assembly gerado é x86-64 Linux e requer WSL ou Linux para ser executado.
