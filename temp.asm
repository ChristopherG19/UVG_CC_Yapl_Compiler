.data
    newline: .asciiz "\n"
    str_0: .asciiz "Object"

.text

Main:
    li $a0, 72
    li $v0, 9
    syscall
    move $s0, $v0

Main_main:
    sub $sp, $sp, 40
    sw $ra, 0($sp)

    la $t0, str_0  # Cargar la dirección del literal de la cadena en el registro $t0
    move $a2, $t0
    li $t0, 3  # Índice de inicio del substring "Object"
    li $t1, 3  # Longitud del substring
    move $a0, $t0
    move $a1, $t1
    jal String_substr
    move $t0, $v0  # Posición inicial del substring
    move $a0, $t0
    jal IO_out_string  # Imprimir la posición inicial

    lw $ra, 0($sp)
    add $sp, $sp, 40
    j exit

String_substr:
    la $t2, str_0      # Puntero al inicio de la cadena
    move $t0, $a0      # Índice de inicio del substring
    move $t1, $a1      # Longitud del substring
    add $t2, $t2, $t0  # Puntero a la posición inicial del substring

    add $t4, $sp, $zero  # Puntero al inicio del área reservada en la pila
    add $t5, $t2, $t1    # Puntero al final del substring

copy_loop:
    bge $t2, $t5, end_substring  # Verificar si se llegó al final del substring

    lb $t3, ($t2)      # Cargar el carácter del substring
    sb $t3, ($t4)      # Almacenar el carácter en la pila
    addi $t2, $t2, 1   # Mover al siguiente carácter del substring
    addi $t4, $t4, 1   # Mover al siguiente espacio en la pila
    j copy_loop

end_substring:
    move $v0, $sp      # Devolver el puntero al inicio del área copiada en la pila
    jr $ra

IO_out_string:
    move $a0, $a0  # Cargar la dirección del substring
    li $v0, 4
    syscall
    la $a0, newline  # Cargar el carácter de nueva línea
    li $v0, 4
    syscall
    jr $ra

exit:
    li $v0, 10
    syscall
