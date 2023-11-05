.data
.text
A:
    add $t0, 452, 9
    lw $t0, 0($gp)
    lw $t2, 4($gp)
    lw $t0, 8($gp)
    lw 5, 9($gp)

A_returnVar:
    add $t1, $t0, 7

B:
    add $t0, 452, 9
    lw $t0, 0($gp)
    lw $t2, 4($gp)
    lw $t0, 8($gp)
    lw 5, 9($gp)

B_returnVar:
    add $t1, $t0, 7

B_setVar1:
    lw P0, 0($sp)
    lw $t0, 13($gp)

Main:
    lw $t0, 21($gp)
    add $t0, 5, 4
    lw $t0, 42($gp)

Main_meth1:
    lw P0, 0($sp)
    lw $t0, 38($gp)

Main_meth2:
    lw P0, 0($sp)
    lw $t0, 4($gp)

Main_main:
    lw $t0, 0($gp)
    lw "igual", 4($gp)
    lw "mayor", 4($gp)
    lw "menor", 4($gp)
    jal IO_out_string
    jal IO_out_string
    add $t3, 1, $t2
    lw $t2, 0($gp)
    lw "hehe", 34($sp)
    lw $t0, 36($sp)
    lw 5, 40($sp)
    lw $t0, 44($sp)
    lw False, 48($sp)
    lw True, 48($sp)
    jal IO_out_string
    add $t0, $t2, $t3
    lw $t0, 10($gp)
    jal IO_out_string
    jal IO_out_string
    add $t0, 5, 6
    jal Main_meth1
    jal $t0_abort
    jal $t0_returnVar
    lw $t0, 14($gp)
    jal $t0_GP[4]
    lw $t3, 14($gp)
    add $t3, 10, $t0
    jal IO_out_int
    jal IO_out_string
    lw $t4, 20($gp)
    j exit

IO_out_string:
    li $v0, 4
    syscall
    jr $ra
IO_out_string:
    li $v0, 4
    syscall
    jr $ra
IO_out_string:
    li $v0, 4
    syscall
    jr $ra
IO_out_string:
    li $v0, 4
    syscall
    jr $ra
IO_out_string:
    li $v0, 4
    syscall
    jr $ra
$t0_abort:
    li $v0, 4
    syscall
    jr $ra
$t0_returnVar:
    li $v0, 4
    syscall
    jr $ra
$t0_GP[4]:
    li $v0, 4
    syscall
    jr $ra
IO_out_int:
    li $v0, 4
    syscall
    jr $ra
IO_out_string:
    li $v0, 4
    syscall
    jr $ra

exit: