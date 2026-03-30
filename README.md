# Compilador Cmd

Este projeto e um compilador modular capaz de transformar codigo de alto nivel (Linguagem Cmd) em binarios executaveis nativos para macOS, Linux e Windows (x86-64).

## Capacidades do Compilador

O projeto suporta uma linguagem completa (Cmd) com as seguintes funcionalidades:

- Variaveis Dinamicas: Declaracao e atribuicao de valores.
- Arithmetica: Suporte a soma, subtracao e multiplicacao com precedencia.
- Estruturas de Controle:
  - if / else: Execucao condicional de blocos de codigo.
  - while: Lacos de repeticao baseados em condicoes.
- Comparacoes: Operadores relacionais igual, menor que e maior que.
- Blocos de Escopo: Agrupamento de comandos usando chaves.
- Geracao de Assembly: Produz codigo x86-64 puro em sintaxe AT&T.

---

## Casos de Uso (Exemplos)

Os exemplos a seguir estao disponiveis na pasta tests/cmd/ e demonstram a versatilidade do compilador:

### 1. Operacoes Simples (simples.cmd)
Realiza um calculo aritmetico direto e retorna o resultado.
```c
{
  return 7 * 6;
}
```

### 2. Condicionais e Valor Absoluto (if_else.cmd)
Demonstra o uso de variaveis e a estrutura if/else para calcular o valor absoluto da diferenca entre dois numeros.
```c
a = 10;
b = 20;
delta = 0;
{
  delta = a - b;
  if delta < 0 {
    delta = 0 - delta;
  } else {
    delta = delta;
  }
  return delta;
}
```

### 3. Calculo de Resto (resto.cmd)
Utiliza um laco while para calcular o resto de uma divisao atraves de subtracoes sucessivas.
```c
m = 10;
n = 4;
{
  while m + 1 > n {
    m = m - n;
  }
  return m;
}
```

### 4. Algoritmo de Euclides - MDC (mdc.cmd)
Implementacao completa do algoritmo de Euclides para encontrar o Maximo Divisor Comum entre dois numeros, utilizando loops aninhados e variaveis auxiliares.
```c
a = 18;
b = 12;
r = 0;
{
  r = a;
  while r + 1 > b {
    r = r - b;
  }
  
  while r > 0 {
    a = b;
    b = r;
    r = a;
    while r + 1 > b {
      r = r - b;
    }
  }
  return b;
}
```

---

## Como Rodar (Por Plataforma)

O processo de transformar o arquivo .s gerado em um programa varia conforme o sistema operacional:

### macOS (x86-64)
No Mac, sao usadas as ferramentas nativas do CommandLineTools.

1. Gerar Assembly:
   python3 compiler.py entrada.cmd saida.s

2. Montar e Ligar:
   as saida.s -o saida.o
   ld saida.o -o programa -lSystem -L/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/lib

3. Executar:
   ./programa

### Linux / WSL (Ubuntu/Debian)
No Linux, o processo e direto devido ao linking estatico por padrao.

1. Gerar Assembly:
   python3 compiler.py entrada.cmd saida.s

2. Montar e Ligar:
   as saida.s -o saida.o
   ld saida.o -o programa

3. Executar:
   ./programa

### Windows (x64 via MinGW)
No Windows, recomenda-se o uso do ambiente MinGW-w64 (GCC).

1. Gerar Assembly:
   python compiler.py entrada.cmd saida.s

2. Montar e Ligar:
   as saida.s -o saida.o
   gcc saida.o -o programa.exe

3. Executar:
   programa.exe

Diferenca de Runtime: Para Windows e Linux, e necessario ajustar as chamadas de sistema no arquivo runtime.s para usar as syscalls corretas de cada kernel ou chamar funcoes da biblioteca C (libc).

---

## Estrutura de Funcionamento

O projeto segue a arquitetura de compiladores:

1. Lexer (lexer.py): Transforma o texto em uma sequencia de tokens.
2. Parser (parser.py): Organiza os tokens em uma Arvore de Sintaxe Abstrata (AST).
3. Semantico (semantic.py): Garante que variaveis usadas foram declaradas.
4. CodeGen (codegen.py): Traduz a AST em instrucoes Assembly.
5. Runtime (runtime.s): Fornece as funcoes de suporte para impressao e encerramento.

## Equipe
- Alisson Gabriel, Cassio Vittori, Hiago Galdino e Matheus Oliveira
