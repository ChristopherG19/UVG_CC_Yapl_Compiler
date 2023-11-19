.data
    newline: .asciiz "\n"
    
.text
.globl Main_main
A:
    sub $sp, $sp, 4
    sw $ra, 0($sp)
    la $s0, 0($sp)
    la $s1, 4($sp)

    li $t0(Int), 5
    sw $t0(Int), 0($s0)

Main:
    sub $sp, $sp, 32
    sw $ra, 0($sp)
    la $s0, 0($sp)
    la $s1, 4($sp)


Main_a:
    li $t0(Int), 3
    sw $t1(A), 0($s0)

Main_main:
    jal Main_a
    jal IO_out_int
    lw $t1(A), 0($s0)
    jal $t1(A)_GP[0]
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