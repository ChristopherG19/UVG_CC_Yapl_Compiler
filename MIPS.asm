.data
    newline: .asciiz "\n"
    str_0: .asciiz "2 is trivially prime.\n"
    str_1: .asciiz " is prime.\n"    
.text
Main:
    li $a0, 184
    li $v0, 9
    syscall
    move $s0, $v0
    la $t0, str_0
    move $a0, $t0
    jal IO_out_string

    li $t0, 2
    sw $t0, 92($s0)
    lw $t0, 92($s0)
    sw $t0, 96($s0)
    li $t0, 500
    sw $t0, 104($s0)

Main_main:
    sub $sp, $sp, 64
    sw $ra, 0($sp)

    j L_LOOP_0

L_LOOP_0:
    bnez true, L_LOOP_END_0
    lw $t0, 96($s0)
    li $t1, 1
    add $t2, $t0, $t1

    sw $t2, 96($s0)
    li $t0, 2
    sw $t0, 100($s0)
    j L_LOOP_1

L_LOOP_1:
    lw $t0, 96($s0)
    lw $t1, 100($s0)
    lw $t2, 100($s0)
    mul $t3, $t1, $t2

    slt $t1, $t0, $t3
    bnez $t1, L_TRUE_0
    j L_FALSE_0

L_TRUE_0:
    j L_IF_END_0

L_FALSE_0:
    lw $t0, 96($s0)
    lw $t1, 100($s0)
    lw $t2, 96($s0)
    lw $t3, 100($s0)
    div $t4, $t2, $t3
    mfhi $s1

    mul $t2, $t1, $t4

    sub $t1, $t0, $t2

    li $t0, 0
    seq $t2, $t1, $t0
    bnez $t2, L_TRUE_1
    j L_FALSE_1

L_TRUE_1:
    j L_IF_END_1

L_FALSE_1:
    j L_IF_END_1

L_IF_END_1:
    j L_IF_END_0

L_IF_END_0:
    bnez true, L_LOOP_END_1
    lw $t0, 100($s0)
    li $t1, 1
    add $t2, $t0, $t1

    sw $t2, 100($s0)
    j L_LOOP_1

L_LOOP_END_1:
    lw $t0, 96($s0)
    lw $t1, 100($s0)
    lw $t2, 100($s0)
    mul $t3, $t1, $t2

    slt $t1, $t0, $t3
    bnez $t1, L_TRUE_2
    j L_FALSE_2

L_TRUE_2:
    lw $t0, 96($s0)
    sw $t0, 92($s0)
    lw $t0, 92($s0)
    move $a0, $t0
    jal IO_out_int

    la $t0, str_1
    move $a0, $t0
    jal IO_out_string

    j L_IF_END_2

L_FALSE_2:
    li $t0, 0
    j L_IF_END_2

L_IF_END_2:
    lw $t1, 104($s0)
    lw $t2, 96($s0)
    sle $t3, $t1, $t2
    bnez $t3, L_TRUE_3
    j L_FALSE_3

L_TRUE_3:
    j L_IF_END_3

L_FALSE_3:
    j L_IF_END_3

L_IF_END_3:
    j L_LOOP_0

L_LOOP_END_0:
    lw $ra, 0($sp)
    add $sp, $sp, 64
    j exit

exit:
    li $v0, 10
    syscall