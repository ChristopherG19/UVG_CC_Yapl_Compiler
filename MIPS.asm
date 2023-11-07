.data
    newline: .asciiz "\n"
    
.text
.globl Main_main
Main:
    sub $sp, $sp, 42
    sw $ra, 0($sp)
    la $s0, 0($sp)
    la $s1, 4($sp)

    li $t0, 10
    sw $t0, 0($s0)
    li $t0, 2
    sw $t0, 20($s0)
    lw $t0, 0($s0)
    lw $t1, 20($s0)
    add $t2, $t0, $t1

    sw $t2, 8($s0)
    li $t0, 4
    sw $t0, 12($s0)
    li $t0, 5
    sw $t0, 16($s0)

Main_main:
    sub $sp, $sp, 12
    sw $ra, 0($sp)
    la $s0, 0($sp)
    la $s1, 4($sp)

    lw $t0, 12($s0)
    li $t1, 4
    li $t0, 1
    jal IO_out_int
    li $t0, 0
    jal IO_out_int
    lw $t0, 0($s0)
    j exit

IO_out_int:
    move $a0, $t0
    li $v0, 1
    syscall
    la $a0, newline
    li $v0, 4
    syscall
    jr $ra
    sw False, 20($s0)
    lw $t1, 0($s0)
    lw $t2, 20($s0)
    sw $t3, 21($s0)

exit:
    li $v0, 10
    syscall