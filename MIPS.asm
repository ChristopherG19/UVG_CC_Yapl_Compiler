.data
    newline: .asciiz "\n"
    
.text
.globl Main_main
Main:
    sub $sp, $sp, 64
    sw $ra, 0($sp)
    la $s0, 0($sp)
    la $s1, 4($sp)

    li $t0(Int), 10
    sw $t0(Int), 0($s0)
    li $t0(Int), 2
    sw $t0(Int), 4($s0)
    lw $t0(Int), 0($s0)
    lw $t1(Int), 4($s0)
    add $t2(Int), $t0(Int), $t1(Int)

    sw $t2(Int), 8($s0)
    li $t0(Int), 5
    sw $t0(Int), 12($s0)
    li $t0(Int), 5
    sw $t0(Int), 16($s0)
    li $t0(Bool), 1
    sw $t0(Bool), 20($s0)

Main_main:
    lw $t0(Int), 12($s0)
    li $t1(Int), 4
    seq $t2(Int), $t0(Int), $t1(Int)
    bnez $t2, L_TRUE_0
    j L_FALSE_0
L_TRUE_0:
    li $t0(Int), 1
    jal IO_out_int
    j L_IF_END_0
L_FALSE_0:
    li $t0(Int), 0
    jal IO_out_int
    j L_IF_END_0
L_IF_END_0:
    li $t0(Bool), 1
    sw $t0(Bool), 20($s0)
    li $t0(Bool), 0
    sw $t0(Bool), 24($s0)
    lw $t0(Bool), 20($s0)
    lw $t1(Bool), 24($s0)
    and $t2(Bool), $t0(Bool), $t1(Bool)

    lw $t0(Bool), 24($s0)
    li $t1(Bool), 1
    seq $t2(Bool), $t0(Bool), $t1(Bool)
    bnez $t2, L_TRUE_1
    j L_FALSE_1
L_TRUE_1:
    li $t0(Int), 1
    jal IO_out_int
    j L_IF_END_1
L_FALSE_1:
    li $t0(Int), 0
    jal IO_out_int
    j L_IF_END_1
L_IF_END_1:
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