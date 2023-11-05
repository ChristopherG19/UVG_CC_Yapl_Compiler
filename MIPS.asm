.data
    newline: .asciiz "\n"
.text
.globl Main_main
Main:
    sub $sp, $sp, 40
    sw $ra, 0($sp)
    la $s0, 0($sp)
    la $s1, 4($sp)

    li $t0, 10
    sw $t0, 0($s0)

    li $t0, 2
    sw $t0, 4($s0)

    lw $t0, 0($s0)
    lw $t1, 4($s0)
    add $t2, $t0, $t1

    sw $t2, 8($s0)
    lw $t0, 0($s0)
    lw $t1, 4($s0)
    add $t2, $t0, $t1

    sw $t2, 12($s0)

Main_main:
    li $t0, 5
    sw $t0, 0($s1)

    lw $t0, 0($s0)
    lw $t1, 0($s1)
    add $t2, $t0, $t1

    sw $t2, 8($s0)
    lw $t0, 8($s0)
    jal IO_out_int
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