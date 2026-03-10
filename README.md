> **Equipe:** Alisson Gabriel, Cassio Vittori, Hiago Galdino e Matheus Oliveira

# Compilador EC1 + EC2

Compilador completo para **EC1** (Atividades 04, 05, 07) e **EC2** (Atividade 08).

## EC1 vs EC2

| Característica | EC1 | EC2 |
|---|---|---|
| **Parênteses** | Obrigatórios | Opcionais — precedência `* /` > `+ -` |
| **Associatividade** | N/A | Todos à esquerda |
| **Exemplo** | `(33 + (912 * 11))` | `33 + 912 * 11` = 10065 |

## Exemplos

### EC1
```
333
(6 * 7)
(3 + (4 + (11 + 7)))
```

### EC2
```
7 + 5 * 3        # = 22
10 - 8 - 2       # = 0
(7 + 5) * 3      # = 36
```

## Estrutura do projeto

```
├── ast_nodes.py       # AST (Number, BinOp)
├── lexer.py           # Análise léxica (EC1 + EC2)
├── parser.py          # Parser EC1
├── parser_ec2.py      # Parser EC2 (precedência)
├── codegen.py         # Assembly x86-64
├── compiler.py        # Compilador EC1
├── compiler_ec2.py    # Compilador EC2
├── interpreter.py     # Interpretador
├── print_tree.py      # Impressão AST
└── tests/
    ├── ec1/           # .ec1 (com parênteses)
    └── ec2/           # .ec2 (sem parênteses)
```

## Pré-requisitos

**Apenas Python 3.8+** — usa só biblioteca padrão (`re`, `sys`).

## Como usar

### EC1
```bash
python lexer.py tests/ec1/exemplo_pdf.ec1
python interpreter.py tests/ec1/exemplo_pdf.ec1
python compiler.py tests/ec1/exemplo_pdf.ec1 saida.s
```

### EC2
```bash
python interpreter.py tests/ec2/soma_mult.ec2
python compiler_ec2.py tests/ec2/soma_mult.ec2 saida.s
cat saida.s
```

## Testes manuais

### EC1
```bash
python interpreter.py tests/ec1/exemplo_pdf.ec1    # 10065
python interpreter.py tests/ec1/complexo.ec1       # 2657
```

### EC2
```bash
python interpreter.py tests/ec2/soma_mult.ec2      # 22
python interpreter.py tests/ec2/sub_esquerda.ec2   # 0
python interpreter.py tests/ec2/complexo.ec2       # 13
```

## Erros detectados

| Tipo | Exemplo | Mensagem |
|------|---------|----------|
| Léxico | `7 + @ 3` | `Erro léxico na posição 4` |
| Sintático | `7 +` | `Erro sintático: esperado número ou '('` |
| Semântico | `10 / 0` | `Divisão por zero` |

## Montagem (Linux/WSL)

```bash
as saida.s -o saida.o
ld saida.o -o saida
./saida
```

> **Assembly x86-64 Linux.** Precisa do `runtime.s`.