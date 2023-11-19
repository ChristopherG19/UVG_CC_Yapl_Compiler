.data
    newline: .asciiz "\n"
    str_0: .asciiz "11 is trivially prime.\n"
    str_1: .asciiz " is prime.\n"
    str_2: .asciiz "halt"
    str_3: .asciiz "continue"    
.text

Main:
    li $a0, 368
    li $v0, 9
    syscall
    move $s0, $v0
    la $t0, str_0
    move $a0, $t0
    jal IO_out_string

    li $t0, 11
    sw $t0, 96($s0)
    lw $t0, 96($s0)
    sw $t0, 100($s0)
    li $t0, 500
    sw $t0, 108($s0)

Main_main:
    sub $sp, $sp, 128
    sw $ra, 0($sp)

    j L_LOOP_0

L_LOOP_0:
    li $t0, 1
    bnez $t0, L_LOOP_END_0
    lw $t0, 100($s0)
    li $t1, 1
    add $t2, $t0, $t1

    sw $t2, 100($s0)
    li $t0, 2
    sw $t0, 104($s0)
    j L_LOOP_1

L_LOOP_1:
    lw $t0, 100($s0)
    lw $t1, 104($s0)
    lw $t2, 104($s0)
    mul $t3, $t1, $t2

    slt $t1, $t0, $t3
    bnez $t1, L_TRUE_0
    j L_FALSE_0

L_TRUE_0:
    li $t0, 0
    j L_IF_END_0

L_FALSE_0:
    lw $t1, 100($s0)
    lw $t2, 104($s0)
    lw $t3, 100($s0)
    lw $t4, 104($s0)
    div $t5, $t3, $t4
    mfhi $s1

    mul $t3, $t2, $t5

    sub $t2, $t1, $t3

    li $t1, 0
    seq $t3, $t2, $t1
    bnez $t3, L_TRUE_1
    j L_FALSE_1

L_TRUE_1:
    li $t1, 0
    j L_IF_END_1

L_FALSE_1:
    li $t2, 1
    j L_IF_END_1

L_IF_END_1:
    j L_IF_END_0

L_IF_END_0:
    bnez $t2, L_LOOP_END_1
    lw $t2, 104($s0)
    li $t3, 1
    add $t4, $t2, $t3

    sw $t4, 104($s0)
    j L_LOOP_1

L_LOOP_END_1:
    lw $t2, 100($s0)
    lw $t3, 104($s0)
    lw $t4, 104($s0)
    mul $t5, $t3, $t4

    slt $t3, $t2, $t5
    bnez $t3, L_TRUE_2
    j L_FALSE_2

L_TRUE_2:
    lw $t2, 100($s0)
    sw $t2, 96($s0)
    lw $t2, 96($s0)
    move $a0, $t2
    jal IO_out_int

    la $t0, str_1
    move $a0, $t2
    jal IO_out_string

    j L_IF_END_2

L_FALSE_2:
    li $t2, 0
    j L_IF_END_2

L_IF_END_2:
    lw $t3, 108($s0)
    lw $t4, 100($s0)
    sle $t5, $t3, $t4
    bnez $t5, L_TRUE_3
    j L_FALSE_3

L_TRUE_3:
    la $t0, str_2
    jal abort

    j L_IF_END_3

L_FALSE_3:
    la $t0, str_3
    j L_IF_END_3

L_IF_END_3:
    j L_LOOP_0

L_LOOP_END_0:
    lw $ra, 0($sp)
    add $sp, $sp, 64
    j exit

IO_out_string:
    li $v0, 4
    syscall
    la $a0, newline
    li $v0, 4
    syscall
    jr $ra

IO_out_int:
    li $v0, 1
    syscall
    la $a0, newline
    li $v0, 4
    syscall
    jr $ra

abort:
    li $v0, 10
    syscall

exit:
    li $v0, 10
    syscall