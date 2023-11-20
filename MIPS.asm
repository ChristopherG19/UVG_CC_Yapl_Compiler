.data
    newline: .asciiz "\n"
    str_0: .asciiz "2 is trivially prime.\n"
    str_1: .asciiz "halt mmmm"    
.text

Main:
    li $a0, 496
    li $v0, 9
    syscall
    move $s0, $v0
    la $t0, str_0
    move $a0, $t0
    jal IO_out_string

    li $t0, 2
    sw $t0, 92($s0)
    la $t0, str_1
    sw $t0, 96($s0)
    lw $t0, 92($s0)
    sw $t0, 132($s0)
    li $t0, 500
    sw $t0, 140($s0)

Main_main:
    sub $sp, $sp, 8
    sw $ra, 0($sp)

    j L_LOOP_0

L_LOOP_0:
    li $t0, 1
    beqz $t0, L_LOOP_END_0
    lw $t0, 96($s0)

    la $a0, ($t0)
    jal abort

    j L_LOOP_0

L_LOOP_END_0:
    li $t0, 10
    li $t1, 20
    add $t2, $t0, $t1

    move $a0, $t2
    jal IO_out_int

    lw $ra, 0($sp)
    add $sp, $sp, 4
    j exit

IO_out_string:
    li $v0, 4
    syscall
    la $a0, newline
    li $v0, 4
    syscall
    jr $ra

abort:
    li $v0, 4
    syscall
    li $v0, 10
    syscall
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