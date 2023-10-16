.data
.text
Main:
    lw 0, 0($gp)
    lw 2, 4($gp)
    add $t0, GP[0], GP[4]
    lw $t0, 8($gp)

Main_main:
    lw $a0, 12($gp)
    jal IO_out_string
    j exit

IO_out_string:
    li $v0, 4
    syscall
    jr $ra

exit: