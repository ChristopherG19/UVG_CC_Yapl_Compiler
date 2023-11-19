.data
    newline: .asciiz "\n"
    
.text
.globl Main_main
Main:
    sub $sp, $sp, 16
    sw $ra, 0($sp)
    la $s0, 0($sp)
    la $s1, 4($sp)

    li $t0, 10
    sw $t0, 0($s0)
    li $t0, 2
    sw $t0, 4($s0)
    li $t0, 1
    sw $t0, 8($s0)
    li $t0, 0
    sw $t0, 12($s0)

Main_main:
    lw $t0, 12($s0)
    lw $t1, 12($s0)
    or $t2, $t0, $t1

    bnez $t2, L_TRUE_0
    j L_FALSE_0
L_TRUE_0:
    li $t0, 100
    jal IO_out_int
    j L_IF_END_0
L_FALSE_0:
    li $t0, 0
    jal IO_out_int
    j L_IF_END_0
L_IF_END_0:
    j exit

IO_out_int:
    move $a0, $t0
    li $v0, 1
    syscall
    la $a0, newline
    li $v0, 4
    syscall
    jr $ra

exit:
    li $v0, 10
    syscall