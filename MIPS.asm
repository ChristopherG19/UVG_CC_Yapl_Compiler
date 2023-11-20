.data
    newline: .asciiz "\n"    
.text

Main:
    li $a0, 64
    li $v0, 9
    syscall
    move $s0, $v0
    li $t0, 0
    sw $t0, 0($s0)

Main_main:
    sub $sp, $sp, 40
    sw $ra, 0($sp)

    j L_LOOP_0

L_LOOP_0:
    lw $t0, 0($s0)
    li $t1, 10
    slt $t2, $t0, $t1
    beqz $t2, L_LOOP_END_0
    lw $t0, 0($s0)
    move $a0, $t0
    jal IO_out_int

    lw $t0, 0($s0)
    li $t1, 1
    add $t2, $t0, $t1

    sw $t2, 0($s0)
    j L_LOOP_0

L_LOOP_END_0:
    li $t0, 0
    bnez $t0, L_TRUE_0
    j L_FALSE_0

L_TRUE_0:
    li $t0, 100
    move $a0, $t0
    jal IO_out_int

    j L_IF_END_0

L_FALSE_0:
    li $t0, 0
    move $a0, $t0
    jal IO_out_int

    j L_IF_END_0

L_IF_END_0:
    lw $ra, 0($sp)
    add $sp, $sp, 20
    j exit

IO_out_int:
    li $v0, 1
    syscall
    la $a0, newline
    li $v0, 4
    syscall
    jr $ra


exit:
    li $v0, 10
    syscall