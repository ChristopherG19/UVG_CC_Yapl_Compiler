.data
    newline: .asciiz "\n"
    str_0: .asciiz "Object"
    str_1: .asciiz "Int"
    str_2: .asciiz "5"    
.text

Main:
    li $a0, 56
    li $v0, 9
    syscall
    move $s0, $v0

Main_main:
    sub $sp, $sp, 40
    sw $ra, 0($sp)

    la $t0, str_0
    move $a2, $t0
    li $t0, 3
    li $t1, 2
    move $a0, $t0
    move $a1, $t1
    jal String_substr
    move $t0, $v0
    move $a0, $t0
    jal IO_out_string

    la $t0, str_1
    move $a2, $t0
    li $t0, 0
    li $t1, 3
    move $a0, $t0
    move $a1, $t1
    jal String_substr
    move $t0, $v0
    move $a0, $t0
    jal IO_out_string
    li $t4, 0

    la $t0, str_2
    move $a0, $t0
    jal IO_out_string
    li $t4, 0

    lw $ra, 0($sp)
    add $sp, $sp, 40
    j exit

String_substr:
    move $t2, $a2
    move $t0, $a0
    move $t1, $a1
    add $t2, $t2, $t0
    add $t4, $sp, $zero
    add $t5, $t2, $t1
loop:
    bge $t2, $t5, end
    lb $t3, ($t2)
    sb $t3, ($t4)
    addi $t2, $t2, 1
    addi $t4, $t4, 1
    j loop

end:
    move $v0, $sp
    jr $ra

IO_out_string:
    li $v0, 4
    syscall
    la $a0, newline
    li $v0, 4
    syscall
    jr $ra

exit:
    li $v0, 10
    syscall