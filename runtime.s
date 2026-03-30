.section __TEXT,__text

# Função para imprimir o número que está em %rax
.globl _imprime_num
_imprime_num:
    pushq %rbp
    movq %rsp, %rbp
    
    # Espaço para string (máximo 20 dígitos + sinal + \n)
    subq $32, %rsp
    
    movq %rax, %rdi    # rdi = número a converter
    leaq 30(%rsp), %rsi # rsi = fim do buffer
    movb $10, (%rsi)   # coloca \n no final
    
    movq $10, %rcx     # divisor
    movq %rdi, %rax
    
    # Lida com números negativos
    testq %rax, %rax
    jge .L_positivo
    negq %rax

.L_positivo:
.L_loop:
    xorq %rdx, %rdx
    divq %rcx
    addb $48, %dl      # converte dígito para ASCII
    decq %rsi
    movb %dl, (%rsi)
    testq %rax, %rax
    jnz .L_loop

    # Se era negativo, coloca o sinal de '-'
    testq %rdi, %rdi
    jge .L_imprime
    decq %rsi
    movb $45, (%rsi)

.L_imprime:
    # Syscall write(1, buffer, len) no macOS x86_64
    # rdi=1 (stdout), rsi=buffer, rdx=len
    movq %rsp, %rdx
    addq $31, %rdx
    subq %rsi, %rdx    # calcula o tamanho
    
    movq $0x2000004, %rax # syscall write
    movq $1, %rdi
    syscall

    addq $32, %rsp
    popq %rbp
    ret

# Função para sair do programa corretamente
.globl _sair
_sair:
    movq $0x2000001, %rax # syscall exit no Mac
    xorq %rdi, %rdi
    syscall