> **Equipe:** Alisson Gabriel, Cassio Vittori, Hiago Galdino e Matheus Oliveira

# Compilador EC1 + EC2 + EV

Compilador completo para **EC1** (Atividades 04, 05, 07), **EC2** (Atividade 08) e **EV** (Atividade 09).

## EC1 vs EC2 vs EV

| Característica | EC1 | EC2 | EV |
|---|---|---|---|
| **Parênteses** | Obrigatórios | Opcionais — precedência `* /` > `+ -` | Opcionais — precedência `* /` > `+ -` |
| **Associatividade** | N/A | Todos à esquerda | Todos à esquerda |
| **Variáveis** | Não | Não | Sim |
| **Exemplo** | `(33 + (912 * 11))` | `33 + 912 * 11` = 10065 | `x = 10; = x * 2` = 20 |

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

### EV
```
l = 30;
c = 40;
= l + l + c + c  # = 140
```

```
x = (7 + 4) * 12;
y = x * 3 + 11;
= (x * y) + (x * 11) + (y * 13)  # = 60467
```

## Estrutura do projeto

```
├── ast_nodes.py       # AST (Number, BinOp, Var, Decl, Programa)
├── lexer.py           # Análise léxica (EC1 + EC2 + EV)
├── parser.py          # Parser EC1
├── parser_ec2.py      # Parser EC2 (precedência)
├── parser_ev.py       # Parser EV (declarações e variáveis)
├── semantic.py        # Análise semântica EV
├── codegen.py         # Assembly x86-64
├── compiler.py        # Compilador EC1
├── compiler_ec2.py    # Compilador EC2
├── compiler_ev.py     # Compilador EV
├── interpreter.py     # Interpretador EC1/EC2
├── interpreter_ev.py  # Interpretador EV
├── print_tree.py      # Impressão AST
└── tests/
    ├── ec1/           # .ec1 (com parênteses)
    ├── ec2/           # .ec2 (sem parênteses)
    └── ev/            # .ev (com variáveis)
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

### EV
```bash
python interpreter_ev.py tests/ev/complexo.ev
python compiler_ev.py tests/ev/complexo.ev saida.s
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

### EV
```bash
python interpreter_ev.py tests/ev/perimetro.ev     # 140
python interpreter_ev.py tests/ev/simples.ev       # 18172
python interpreter_ev.py tests/ev/complexo.ev      # 60467
python interpreter_ev.py tests/ev/so_resultado.ev  # 11
```

## Erros detectados

| Tipo | Exemplo | Mensagem |
|------|---------|----------|
| Léxico | `7 + @ 3` | `Erro léxico na posição 4` |
| Sintático | `7 +` | `Erro sintático: esperado número ou '('` |
| Semântico (EC1/EC2) | `10 / 0` | `Divisão por zero` |
| Semântico (EV) | `= x + 1` | `Erro semantico: variavel 'x' nao foi declarada` |

## Montagem (Linux/WSL)

```bash
as saida.s -o saida.o
ld saida.o -o saida
./saida
```

> **Assembly x86-64 Linux.** Precisa do `runtime.s`.
