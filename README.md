# Compilador EC1

Este é um compilador didático que converte expressões matemáticas simples para a linguagem de montagem (Assembly x86_64).

##  Como testar o projeto

Possui duas opções principais para testar o funcionamento do compilador:

### 1. Testes Rápidos (Via Terminal)
O projeto inclui um arquivo `tests.py` que contém testes pré-definidos (como `42`, `(7 + 11)`). Ao rodá-lo, o compilador irá processar essas expressões e exibir no terminal o código Assembly gerado para cada caso.

**Para verificar os casos testes existentes, execute:**
```bash
python3 tests.py
```
*(Não depende de um processador ou arquitetura específica para validar o Assembly via terminal, ideal para testar a gramática no macOS/Windows).*

### 2. Testando e Montando um Arquivo Completo
Você pode criar o seu próprio arquivo de código origem e realizar a transcrição completa para compilar um executável.

**Passo 1:** Crie um arquivo texto qualquer e escreva uma expressão na sintaxe EC1 (ex: `entrada.ec1`).

**Passo 2:** Rode o compilador para transformar esse arquivo num código fonte Assembly (`saida.s`):
```bash
python3 compiler.py entrada.ec1 saida.s
```

**Passo 3:** Converta o arquivo fonte Assembly em um arquivo Objeto (.o) e o use para Linkar (ld) o programa:
```bash
as -o saida.o saida.s
ld -o programa saida.o
```
*(Certifique-se de possuir o arquivo `runtime.s` contendo a diretiva final de sistema para que ele seja linkado corretamente).*

**Passo 4:** Rode o arquivo gerado:
```bash
./programa
```
