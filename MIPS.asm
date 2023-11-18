.data
    newline: .asciiz "\n"    
.text
Factorial:
    li $a0, 4
    li $v0, 9
    syscall
    move $s0, $v0

    li $t0, 0
    sw $t0, 0($s0)

Factorial_factorial:
    sub $sp, $sp, 32
    sw $ra, 0($sp)
    lw $t0, 0($sp)
    li $t1, 0
    li $t0, 0
    sw $t0, 4($sp)
    lw $t0, 0($sp)
    li $t1, 1
    li $t0, 1
    sw $t0, 4($sp)
    lw $t0, 0($sp)
    lw $t1, 0($sp)
    li $t2, 1
    sub $t3, $t1, $t2

    jal Factorial_factorial

    mul $t2, $t0, $t1

    sw $t2, 4($sp)
    lw $ra, 0($sp)
    add $sp, $sp, 32
    move $v0, SP[4]
    jr $ra

Fibonacci:

Fibonacci_fibonacci:
    sub $sp, $sp, 48
    sw $ra, 0($sp)
    lw $t0, 0($sp)
    li $t1, 1
    li $t0, 1
    sw $t0, 4($sp)
    lw $t0, 0($sp)
    li $t1, 2
    li $t0, 1
    sw $t0, 4($sp)
    lw $t0, 0($sp)
    li $t1, 1
    sub $t2, $t0, $t1

    jal Fibonacci_fibonacci

    lw $t1, 0($sp)
    li $t2, 2
    sub $t3, $t1, $t2

    jal Fibonacci_fibonacci

    add $t2, $t0, $t1

    lw $t0, 0($sp)
    li $t1, 3
    sub $t3, $t0, $t1

    jal Fibonacci_fibonacci

    add $t1, $t2, $t0

    sw $t1, 4($sp)
    lw $ra, 0($sp)
    add $sp, $sp, 48
    move $v0, SP[4]
    jr $ra

Main:
    li $a0, 8
    li $v0, 9
    syscall
    move $s0, $v0

    li $t0, 10
    sw $t0, 0($s0)

Main_main:
    sub $sp, $sp, 8
    sw $ra, 0($sp)
    sw $t0, 4($s0)
    sw $t0, 8($s0)
    lw $t0, 8($s0)
    lw $t0, 0($s0)
    jal $t0_fibonacci

    jal IO_out_int

    lw $ra, 0($sp)
    add $sp, $sp, 8
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