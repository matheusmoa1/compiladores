# Documentação Histórico de Desenvolvimento

Esta seção documenta toda a estruturação técnica percorrida pelo grupo ao longo das fases da disciplina, culminando no estado atual do **Compilador Fun x64**.

---

## 1. Análise Léxica [EC1 - Ativ. 04]
O marco incial do compilador se deu na tokenização (transição crua do arquivo texto para sequências amarradas conhecidas da linguagem). O arquivo central estrutural criado foi o `lexer.py`, e incialmente focado no isolamento e tratamento cego na limpeza de espaços em branco, separando identificadores orgânicos de caracteres de quebra (`(`, `)`, Operadores Numéricos).

## 2. AST, Padrões Analíticos e Primeira Geração [EC1 - Ativ. 05 & 07]
Estabelecimento do núcleo do compilador. 
- Criamos os nós centrais via manipulação na árvore de `ast_nodes.py` e formatamos a varredura atrelada aos tokens sob o escopo estrito de **Análise Descendente Recursiva** do Parser: A verificação atômica de nós que prioriza e isola o que calcula primeiro (ex: multiplicação ante da soma) usando o peso limitante e exaustivo guiado por parênteses obrigatórios.
- A Geração inicial à máquina foi elaborada de modo cru lendo essa árvore, mantendo instruções virtuais de empilhamento AT&T na memória da RAM que resgata imediatamente cálculos (`push` e `pop` atrelado fortemente à salvação dos estados do barramento `%rbx`).

## 3. Precedência Ativa [EC2 - Ativ. 08]
Re-elaboração pesada das construções do `parser.py` para anular a ambiguidade de compilação eliminando a obrigatoriedade restrita do usuário de inserir parênteses. Resolvemos o inferno acadêmico da "Recursividade à Esquerda" adotando com sucesso a decomposição em 3 blocos hierárquicos: expressões aditivas em `<exp_a>`, multiplicativas em `<exp_m>` e os literais primitivos na frente em `<prim>`. O uso dessa fragmentação nos legou a **Precedência Canônica** de forma orgânica à nossa AST!

## 4. Nascimento de Variáveis e Semântica [EV - Ativ. 09]
Evolução para a Expressão com Variáveis (`Linguagem EV`):
- O compilador abandonou o seu núcleo inicial imediatista para testar e abraçar a base profunda da "Análise Semântica" (Criação de nossa primeira **Tabela de Símbolos**). Aqui, na raiz criamos bloqueios precoces nas Árvores identificando inconsistências lógicas de usuário, proibindo as chamadas de "Variáveis Fantasmas" antes de virarem dor de cabeça de código máquina.
- Expandimos de vez o Output em `codegen.py` obrigando o compilador a declarar blocos `.BSS` declarando espaços puros (como as diretiva de quadword `.lcomm x, 8`) alocando os estados permanentes na máquina.

## 5. Salto Turing-Completo e Loops [Cmd - Ativ. 10]
Controle real de arquitetura base em Rótulos!
- Essa fase evoluiu para a **Linguagem Cmd**, englobando as estruturas lógicas como os laços de controle sub-rotineiros (`If / Else`, `While`, `Assign`).
- A nossa equipe amarrou os pulos e limites matemáticos traduzindo as variáveis lendo e atacando diretamente o pacote RFLAGS da Unidade Central. Operamos Condicionais nativos testando os sub-registradores booleanos `cl`, e gerenciando saltos reais entre os Rótulos assembly (Jumps flexíveis como `Linicio0` e `Lfim0`) - gerando na mão um dos loops nativos mais polidos das camadas atreladas ao Python.

## 6. Funções, Chamadas e Conveção Microsoft x64 [Fun - Ativ. 11]
Aqui o código abandonou a formatação linear amarrada do Cmd e entramos na **Linguagem Fun**.
- A inserção de "Múltiplas Funções com Parâmetros" exigiu a re-alocação dos escopos em `semantic.py`, criando barricadas limpas para lidar o mundo "Local" e impedir sobreposição e poluição aos ambientes do bloco Global. 
- Todo nosso *Back-End* e Geração final se inclinou rigorosamente a atender o Padrão do **Calling Convention** das bibliotecas C baseadas nas normativas das máquinas Microsoft x64.
- Instanciamos *Offsets dinâmicos virtuais* baseados em Base Pointers rigorosos (`pushq %rbp`), viabilizando com precisão o cálculo complexo e as manutenções perigosas em matemática de sub-chamadas, culminando no funcionamento assustador da Máscara Recursiva em que nosso Compilador chama execuções de repetição matemática (ex: Fibonacci de 10) ativamente sem derreter a RAM.

## 7. O Projeto Final [Extensões de Complexidade Simples]
O projeto acadêmico finalizou validando e aplicando total destreza matemática à máquina, atestando todo controle flexível e robustez estrutural das pipelines criadas durante os semestres.
- Eliminamos os macro-modelos falhos abraçando os duplos comparadores lógicos (`!=`, `<=`, `>=`), atrelando as capturas sintáticas purificando as instruções reversas AT&T estritas (`setge`, `setnz`).
- Re-adequação ao submundo do mapeamento atômico das diretivas extraindo ativamente os restos residuais modulares da idivq pescando o restolho do comando em `%rdx`.
- Ruptura completa do controle amarrado em roda-pé validando nativamente os saltos interceptadores dinâmicos preventivos (`Early Returns`). Nossa compilação agora caça internamente epílogos criados com a injeção em código, e desce o nível efetuando quebras em comandos e loops para forçar os expurgo das bases (`popq %rbp`), contendo os limites e validando o sistema à prova de erros não mapeados em qualquer laço existente.
