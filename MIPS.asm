.data
.text
.globl Main_main
Main:
	sub $sp, $sp, 20
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

Main_main:
    lw 5, 0($s1)
    lw $t0, 0($s0)
    lw $t1, 0($s1)

    add $t2, $t0, $t1

    lw $t0, 8($s0)
	j exit

exit:
	li $v0, 10
	syscall