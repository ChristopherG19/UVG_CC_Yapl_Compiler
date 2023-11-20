.data
    newline: .asciiz "\n"
    str_0: .asciiz "Hello World.\n"    
.text

Main:
    li $a0, 360
    li $v0, 9
    syscall
    move $s0, $v0

Main_main:
    sub $sp, $sp, 120
    sw $ra, 0($sp)

    la $t0, str_0
    move $a0, $t0
    jal IO_out_string

    lw $ra, 0($sp)
    add $sp, $sp, 120
    j exit

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