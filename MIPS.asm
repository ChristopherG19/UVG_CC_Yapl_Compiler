.data
    newline: .asciiz "\n"    
.text

Main:
    li $a0, 72
    li $v0, 9
    syscall
    move $s0, $v0
    li $t0, 10
    sw $t0, 0($s0)
    li $t0, 2
    sw $t0, 4($s0)
    jal Main_main

Main_retA:
    sub $sp, $sp, 16
    sw $ra, 0($sp)

    lw $t0, 0($s0)
    move $v0, $t0
    lw $ra, 0($sp)
    add $sp, $sp, 16
    jr $ra
Main_retB:
    sub $sp, $sp, 16
    sw $ra, 0($sp)

    lw $t1, 4($s0)
    move $v0, $t1
    lw $ra, 0($sp)
    add $sp, $sp, 16
    jr $ra
Main_main:
    sub $sp, $sp, 8
    sw $ra, 0($sp)

    jal Main_retA
    move $t2, $v0
    jal Main_retB
    move $t3, $v0
    add $t4, $t2, $t3

    move $a0, $t4
    jal IO_out_int

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