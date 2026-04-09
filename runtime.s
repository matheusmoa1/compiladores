.section .text

.globl imprime_num
imprime_num:
    pushq %rbp
    movq %rsp, %rbp
    subq $48, %rsp          # Espaço para sombra (32 bytes) + alinhamento
    
    movq %rax, %rdx         # 2º argumento: o número em RAX
    leaq .Lfmt(%rip), %rcx  # 1º argumento: a string de formato
    call printf
    
    addq $48, %rsp
    popq %rbp
    ret

.Lfmt:
    .ascii "%lld\12\0"      # %lld seguido de \n (12 em octal) e nulo (0)

.globl sair
sair:
    movq $0, %rcx           # status de saída 0
    call exit
