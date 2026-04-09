# Compilador Fun

Este projeto é um compilador modular capaz de transformar código de alto nível (Linguagem Fun) em binários executáveis nativos. Ele foi projetado com suporte otimizado para Windows (via MinGW/GCC).

## Capacidades do Compilador

O projeto evoluiu para a linguagem **Fun**, que suporta as seguintes funcionalidades:

- **Funções e Recursão**: Declaração de funções com múltiplos parâmetros e suporte total a chamadas recursivas.
- **Variáveis Locais**: Escopo léxico estrito para variáveis dentro de funções e parâmetros.
- **Variáveis Globais**: Armazenadas na seção `.bss` e acessíveis por todas as funções.
- **Aritmética**: Suporte a soma, subtração, multiplicação e divisão com precedência.
- **Estruturas de Controle**:
  - `if / else`: Execução condicional de blocos de código.
  - `while`: Laços de repetição baseados em condições.
- **Geração de Assembly**: Produz código x86-64 puro em sintaxe AT&T, utilizando o registrador `RBP` para gerenciamento de frames de pilha.

## Casos de Uso (Pasta tests/fun/)

### 1. Funções Recursivas (fib.fun)
O exemplo máximo de poder da linguagem: cálculo de Fibonacci usando recursão profunda.
```javascript
fun fib(n) {
  var res = 0;
  if n < 2 {
    res = n;
  } else {
    res = fib(n - 1) + fib(n - 2);
  }
  return res;
}

main {
  return fib(10);
}
```

### 2. Algoritmo de Euclides - MDC (mdc.fun)
Encontra o Máximo Divisor Comum utilizando a nova estrutura de blocos e funções.
```javascript
var a = 18;
var b = 12;

main {
  var r = a;
  while r + 1 > b { r = r - b; }
  
  while r > 0 {
    a = b; b = r; r = a;
    while r + 1 > b { r = r - b; }
  }
  return b;
}
```

## Como Rodar (Windows / Git Bash)

O compilador agora gera código compatível com o ponto de entrada `main` do C, o que facilita a ligação no Windows.

1. **Gerar Assembly**:
   ```bash
   python compiler.py tests/fun/fib.fun fib.s
   ```

2. **Montar e Ligar (Compilar)**:
   ```bash
   gcc fib.s -o fib.exe
   ```

3. **Executar**:
   ```bash
   ./fib.exe
   ```

## Estrutura de Funcionamento

O projeto segue a arquitetura clássica de compiladores:

1. **Lexer** (`lexer.py`): Tokenização com suporte a novas palavras-chave (`fun`, `main`, `var`).
2. **Parser** (`parser.py`): Gera uma AST complexa suportando o nó mestre `Programa` e declarações de funções.
3. **Semântico** (`semantic.py`): Valida escopos, declarações de variáveis e aridade de funções.
4. **CodeGen** (`codegen.py`): Implementa o protocolo de chamada x64, gerenciando a pilha e offsets de memória.
5. **Runtime** (`runtime.s`): Interface entre o assembly gerado e o Sistema Operacional através do C Runtime.

## Equipe
- Alisson Gabriel
- Cassio Vittori
- Hiago Galdino
- Matheus Oliveira