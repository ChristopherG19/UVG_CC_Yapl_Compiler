.data
    newline: .asciiz "\n"
    str_0: .asciiz "Stop"    
.text

Main:
    jal Main_main

Main_main:
    sub $sp, $sp, 0
    sw $ra, 0($sp)

    j L_LOOP_0

L_LOOP_0:
    li $t0, 1
    beqz $t0, L_LOOP_END_0
    la $t0, str_0

    la $a0, ($t0)
    jal abort

    j L_LOOP_0

L_LOOP_END_0:
    j exit

abort:
    li $v0, 4
    syscall
    li $v0, 10
    syscall
exit:
    li $v0, 10
    syscall