# Compilador Fun

Este projeto é um compilador modular capaz de transformar código de alto nível (Linguagem Fun) em binários executáveis nativos. Ele foi projetado com suporte otimizado para Windows (via MinGW/GCC).

## Capacidades do Compilador

O projeto evoluiu para a linguagem **Fun**, que suporta as seguintes funcionalidades:

- **Funções e Recursão**: Declaração de funções com múltiplos parâmetros e suporte total a chamadas recursivas.
- **Variáveis Locais**: Escopo léxico estrito para variáveis dentro de funções e parâmetros.
- **Variáveis Globais**: Armazenadas na seção `.bss` e acessíveis por todas as funções.
- **Aritmética e Módulos**: Suporte a soma, subtração, multiplicação, divisão e resto da divisão (`%`) com precedência.
- **Operadores Relacionais**: Validações estritas usando `>`, `<`, `==`, `>=`, `<=` e `!=`.
- **Estruturas de Controle e Retorno Prévio**:
  - `if / else`: Execução condicional de blocos de código.
  - `while`: Laços de repetição baseados em condições.
  - `return`: Controle flexível com encerramento forçado de funções em qualquer ponto lógico (early-return) tratando os resíduos de pilha ativamente.
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

### 3. Validação de Módulo e Early-Return (mod.fun)
Calcula se um número é par usando o operador de resto (`%`) e utiliza o conceito de retorno forçado (early return).
```javascript
var x = 0;

fun par(n) {
  if (n % 2) == 0 {
     return 1;
  } else { }
  return 0;
}

main {
  x = par(10);
  if x != 0 {
      return 99;
  } else { }
  return x;
}
```

### 4. Avaliação de Comparadores Lógicos (comp.fun)
Valida a precisão da estrutura de controle utilizando múltiplas portas de desigualdade complexas (`<=`, `>=`, `!=`).
```javascript
var global = 100;
var x = 0;

main {
  x = 10;
  if x <= 10 { x = 5; } else { }
  if x >= 5 { x = x + 1; } else { }
  if x != 100 { return x; } else { }
  return 0;
}
```

## Como Rodar (Windows / Git Bash)

O compilador gera código x64 compatível com o ponto de entrada `main` do C, o que requer o uso do compilador nativo para a ligação estrita da máquina (como o `gcc` do MinGW-w64). O arquivo `runtime.s` injerirá o print e encerramento para cada arquivo alvo rodado!

### Compilando e Executando (Passo-a-Passo)
Substitua `fib` ou `mod` dependendo de qual caso de teste você quiser rodar no prompt de comandos:

1. **Converter `.fun` para Assembly (`.s`)**:
   ```bash
   python compiler.py tests/fun/mod.fun mod.s
   ```
   *(Caso não esteja na pasta atrelada global, invoque usando `venv`: `.\venv\Scripts\python.exe compiler.py ...`)*

2. **Compilação Nativa (Via GCC)**:
   ```bash
   gcc mod.s -o aplicativo.exe
   ```

3. **Visualizar o Resultado**:
   ```bash
   ./aplicativo.exe
   ```
   *(Ele exibirá imediatamente o valor computacional exato do teste. O de fibonacci imprimirá 55, o do módulo imprimirá 99).*

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