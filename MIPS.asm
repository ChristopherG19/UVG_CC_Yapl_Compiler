.data
    newline: .asciiz "\n"
    str_0: .asciiz "retA"
    str_1: .asciiz "retB"    
.text

Main:
    li $a0, 144
    li $v0, 9
    syscall
    move $s0, $v0
    li $t0, 10
    sw $t0, 0($s0)
    li $t0, 2
    sw $t0, 4($s0)
    li $t0, 5
    sw $t0, 8($s0)

Main_retA:
    sub $sp, $sp, 16
    sw $ra, 0($sp)

    lw $t0, 0($s0)
    lw $ra, 0($sp)
    add $sp, $sp, 16

Main_retB:
    sub $sp, $sp, 16
    sw $ra, 0($sp)

    lw $t1, 4($s0)
    lw $ra, 0($sp)
    add $sp, $sp, 16

Main_main:
    sub $sp, $sp, 64
    sw $ra, 0($sp)

    lw $t2, 0($s0)
    move $a0, $t2
    jal IO_out_int

    lw $t2, 4($s0)
    move $a0, $t2
    jal IO_out_int
    li $t4, 0

    lw $t2, 8($s0)
    move $a0, $t2
    jal IO_out_int
    li $t4, 0

    lw $t2, 0($s0)
    lw $t3, 4($s0)
    lw $t4, 8($s0)
    sub $t5, $t3, $t4

    add $t3, $t2, $t5

    sw $t3, 12($s0)
    lw $t2, 12($s0)
    move $a0, $t2
    jal IO_out_int
    li $t4, 0

    lw $t2, 0($s0)
    lw $t3, 4($s0)
    mul $t4, $t2, $t3

    lw $t2, 8($s0)
    div $t3, $t4, $t2
    mfhi $s1

    sw $t3, 12($s0)
    lw $t2, 12($s0)
    move $a0, $t2
    jal IO_out_int
    li $t4, 0

    lw $t2, 0($s0)
    li $t3, 8
    sub $t4, $t2, $t3

    move $a0, $t4
    jal IO_out_int
    li $t4, 0

    li $t2, 100
    li $t3, 5
    div $t4, $t2, $t3
    mfhi $s1

    move $a0, $t4
    jal IO_out_int
    li $t4, 0

    la $t2, str_0
    la $t3, str_1
    mul $t4, $t2, $t3

    sw $t4, 12($s0)
    lw $t2, 12($s0)
    move $a0, $t2
    jal IO_out_int
    li $t4, 0

    lw $ra, 0($sp)
    add $sp, $sp, 64
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