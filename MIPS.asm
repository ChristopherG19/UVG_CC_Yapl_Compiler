.data
    newline: .asciiz "\n"
    
.text
.globl Main_main
Main:
    sub $sp, $sp, 8
    sw $ra, 0($sp)
    la $s0, 0($sp)
    la $s1, 4($sp)


Main_main:
    jal $t0(Object)_type_name
    li $t0(Int), 4
    li $t1(Int), 1
    jal $t0(Object)_substr
    jal IO_out_string
    jal $t0(Object)_type_name
    li $t0(Int), 1
    li $t0(Int), 3
    jal $t0(Object)_substr
    jal $t1(Object)_out_string
    li $t0(String), "\n"
    jal IO_out_string
    j exit

IO_out_string:
    move $a0, $t0
    li $v0, 4
    syscall
    la $a0, newline
    li $v0, 4
    syscall
    jr $ra

exit:
    li $v0, 10
    syscall