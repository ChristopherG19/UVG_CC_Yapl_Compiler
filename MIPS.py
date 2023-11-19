"""
    Universidad del Valle de Guatemala
    Construcción de Compiladores
    Christopher García 20541
    Ma. Isabel Solano 20504
"""
import re

class MIPS():
    def __init__(self, CI_txt):
        self.CI = CI_txt
        self.etiquetas = []
        
    def get_MIPS_Code(self):
        # Realiza la traducción a MIPS
        mips_code = self.translate()

        if(mips_code != None):
            output_file = "MIPS.asm"
            # Abre el archivo de salida en modo escritura
            with open(output_file, 'w') as file:
                # Escribe el código MIPS traducido en el archivo de salida
                file.write(mips_code)
        else:
            print("Lo sentimos, la generación de código MIPS salió mal\n")
            
    def translate(self):
        input_code = None
        self.tempBlock = ""
        self.dataBlock = ".data\n"
        self.etis = 0
        # Abre el archivo de entrada en modo lectura
        with open(self.CI, 'r') as file:
            # Lee el contenido del archivo
            input_code = file.read()
            
        if(input_code != None):
            mips_code = ""
            self.dataBlock += '    newline: .asciiz "\\n"\n'
            mips_code += '    \n.text\n.globl Main_main'

            # Divide el código intermedio en líneas
            lines = input_code.split('\n')

            Act_class = None
            Act_func = None
            Count_Param = 0
            for line in lines:
                # Divide cada línea en palabras (instrucciones y argumentos)
                words = line.split(None, 1)
                
                if(len(words) > 1):
                    if(words[1].startswith('"')):
                        pass
                    else:
                        words = line.split()
                        words = [("$" + word.replace(",", "")) if re.match(r't\d', word) else word.replace(",", "") for word in words]

                if words:    
                    try:
                        funcs = words[0].split('.')
                        if funcs[0] == Act_class:
                            Act_func = funcs[1]
                    except:
                        continue
                    
                    # Traducción de instrucciones
                    if words[0] == "CLASS":
                        Act_func = None
                        Count_Param = 0
                        Act_class = words[1]
                        self.etiquetas.append(Act_class)
                        mips_code += f"\n{Act_class}:\n"
                        mips_code += f"    sub $sp, $sp, {words[2]}\n"
                        mips_code += f"    sw $ra, 0($sp)\n"
                        mips_code += f"    la $s0, 0($sp)\n"
                        mips_code += f"    la $s1, 4($sp)\n\n"
                        
                    elif (Act_class+".") in words[0]:
                        call_func = words[0].replace('.', '_')
                        self.etiquetas.append(call_func)
                        Count_Param = 0
                        mips_code += f"\n{call_func}:\n"
                        # mips_code += f"    sub $sp, $sp, {words[1]}\n"
                        # mips_code += f"    sw $ra, 0($sp)\n"
                        # mips_code += f"    la $s0, 0($sp)\n"
                        # mips_code += f"    la $s1, 4($sp)\n\n"
                    
                    elif words[0] == "LW":
                        match = re.match(r'(\w+)\[(\d+)\]', words[2])

                        if match:
                            env = match.group(1)
                            disp = match.group(2)
                            if env == "GP":
                                mips_code += f"    lw {words[1]}, {disp}($s0)\n"
                            elif env == "SP":
                                mips_code += f"    lw {words[1]}, {disp}($s1)\n"
                                
                        else:
                            if words[2] == "R":
                                mips_code += f"    lw {words[1]}, $v0\n"
                    
                    elif words[0] == "LI":
                        match = re.match(r'(\w+)\[(\d+)\]', words[1])

                        if match:
                            env = match.group(1)
                            disp = match.group(2)
                            if env == "GP":
                                mips_code += f"    li $t0, {words[2]}\n"
                                mips_code += f"    sw $t0, {disp}($s0)\n\n"
                            elif env == "SP":
                                mips_code += f"    li $t0, {words[2]}\n"
                                mips_code += f"    sw $t0, {disp}($s1)\n\n"  
                        else:
                            if words[2] == "R":
                                mips_code += f"    li {words[1]}, $v0\n"

                            else:
                                mips_code += f"    li {words[1]}, {words[2]}\n"          
                            
                    elif words[0] == "SW":
                        match = re.match(r'(\w+)\[(\d+)\]', words[1])

                        if match:
                            env = match.group(1)
                            disp = match.group(2)
                            if env == "GP":
                                mips_code += f"    sw {words[2]}, {disp}($s0)\n"
                            elif env == "SP":
                                mips_code += f"    sw {words[2]}, {disp}($s1)\n"

                    elif words[0] == "PARAM":
                        match = re.match(r'(\w+)\[(\d+)\]', words[1])

                        if match:
                            env = match.group(1)
                            disp = match.group(2)

                            mips_code += f"    lw $a{Count_Param}, {disp}(${env.lower()})\n"
                            Count_Param += 1
                            
                        elif(type(words[1]) == str and "$" not in words[1]):
                            
                            eti = f"str_{self.etis}"
                            self.dataBlock += f"    {eti}: .asciiz {words[1]}\n"
                            mips_code += f"    la $t0, {eti}\n"
                            self.etis += 1
                            
                    elif words[0] == "CALL":
                        func = words[1].replace('.', '_')
                        self.tempBlock = ""
                        if(func not in self.etiquetas):
                            mips_code += f"    jal {func}\n"
                            if("out_int" in func):
                                self.tempBlock += f"{func}:\n    move $a0, $t0\n    li $v0, 1\n    syscall\n    la $a0, newline\n    li $v0, 4\n    syscall\n    jr $ra\n"
                            elif("out_string" in func):
                                self.tempBlock += f"{func}:\n    move $a0, $t0\n    li $v0, 4\n    syscall\n    la $a0, newline\n    li $v0, 4\n    syscall\n    jr $ra\n"
                                
                        else:    
                            mips_code += f"    jal {func}\n"
                        #self.etiquetas.append(func)

                    elif words[0] == "DIV":

                        matchA = re.match(r'(\w+)\[(\d+)\]', words[2])

                        # div $t1, $t2  # Divide $t1 por $t2, almacenando el cociente en $LO y el residuo en $HI
                        if matchA:
                            envA = matchA.group(1)
                            dispA = matchA.group(2)
                            if envA == "GP":
                                mips_code += f"    lw {words[2]}, {dispA}($s0)\n"
                            elif envA == "SP":
                                mips_code += f"    lw {words[2]}, {dispA}($s1)\n"

                        else:
                            print("no match div A")
                            
                        matchB = re.match(r'(\w+)\[(\d+)\]', words[3])

                        if matchB:
                            envB = matchB.group(1)
                            dispB = matchB.group(2)
                            if envB == "GP":
                                mips_code += f"    lw {words[3]}, {dispB}($s0)\n"
                            elif envB == "SP":
                                mips_code += f"    lw {words[3]}, {dispB}($s1)\n"
                        
                        else:
                            print("no match div B")
                                
                        mips_code += f"    div {words[1]}, {words[2]}, {words[3]}\n"
                        mips_code += f"    mfhi $s1\n\n"

                    elif words[0] == "MULT":
                        matchA = re.match(r'(\w+)\[(\d+)\]', words[2])

                        if matchA:
                            envA = matchA.group(1)
                            dispA = matchA.group(2)
                            if envA == "GP":
                                mips_code += f"    lw {words[2]}, {dispA}($s0)\n"
                            elif envA == "SP":
                                mips_code += f"    lw {words[2]}, {dispA}($s1)\n"
                            
                        matchB = re.match(r'(\w+)\[(\d+)\]', words[3])

                        if matchB:
                            envB = matchB.group(1)
                            dispB = matchB.group(2)
                            if envB == "GP":
                                mips_code += f"    lw {words[3]}, {dispB}($s0)\n"
                            elif envB == "SP":
                                mips_code += f"    lw {words[3]}, {dispB}($s1)\n"
                                
                        mips_code += f"    mul {words[1]}, {words[2]}, {words[3]}\n\n"

                    
                    elif words[0] == "ADD":
                        
                        matchA = re.match(r'(\w+)\[(\d+)\]', words[2])

                        if matchA:
                            envA = matchA.group(1)
                            dispA = matchA.group(2)
                            if envA == "GP":
                                mips_code += f"    lw {words[2]}, {dispA}($s0)\n"
                            elif envA == "SP":
                                mips_code += f"    lw {words[2]}, {dispA}($s1)\n"
                            
                        matchB = re.match(r'(\w+)\[(\d+)\]', words[3])

                        if matchB:
                            envB = matchB.group(1)
                            dispB = matchB.group(2)
                            if envB == "GP":
                                mips_code += f"    lw {words[3]}, {dispB}($s0)\n"
                            elif envB == "SP":
                                mips_code += f"    lw {words[3]}, {dispB}($s1)\n"
                                
                        mips_code += f"    add {words[1]}, {words[2]}, {words[3]}\n\n"
                        
                    elif words[0] == "SUB":
                        
                        matchA = re.match(r'(\w+)\[(\d+)\]', words[2])

                        if matchA:
                            envA = matchA.group(1)
                            dispA = matchA.group(2)
                            if envA == "GP":
                                mips_code += f"    lw {words[2]}, {dispA}($s0)\n"
                            elif envA == "SP":
                                mips_code += f"    lw {words[2]}, {dispA}($s1)\n"
                            
                        matchB = re.match(r'(\w+)\[(\d+)\]', words[3])

                        if matchB:
                            envB = matchB.group(1)
                            dispB = matchB.group(2)
                            if envB == "GP":
                                mips_code += f"    lw {words[3]}, {dispB}($s0)\n"
                            elif envB == "SP":
                                mips_code += f"    lw {words[3]}, {dispB}($s1)\n"
                                
                        mips_code += f"    sub {words[1]}, {words[2]}, {words[3]}\n\n"

                    elif words[0] == "AND" or words[0] == "OR":

                        matchA = re.match(r'(\w+)\[(\d+)\]', words[2])

                        if matchA:
                            envA = matchA.group(1)
                            dispA = matchA.group(2)
                            if envA == "GP":
                                mips_code += f"    lw {words[2]}, {dispA}($s0)\n"
                            elif envA == "SP":
                                mips_code += f"    lw {words[2]}, {dispA}($s1)\n"
                            
                        matchB = re.match(r'(\w+)\[(\d+)\]', words[3])

                        if matchB:
                            envB = matchB.group(1)
                            dispB = matchB.group(2)
                            if envB == "GP":
                                #TODO si se arreglan los temporales, este arreglo se eliminaria
                                mips_code += f"    lw {words[3]}, {dispB}($s0)\n"
                            elif envB == "SP":
                                mips_code += f"    lw {words[3]}, {dispB}($s1)\n"
                                
                        
                        mips_code += f"    {words[0].lower()} {words[1]}, {words[2]}, {words[3]}\n\n"

                    elif (words[0] == "SLT" or words[0] == "SEQ" or words[0] == "SLE" or
                          words[0] == "SGT" or words[0] == "SGE"):

                        matchA = re.match(r'(\w+)\[(\d+)\]', words[2])

                        if matchA:
                            envA = matchA.group(1)
                            dispA = matchA.group(2)
                            if envA == "GP":
                                mips_code += f"    lw {words[2]}, {dispA}($s0)\n"
                            elif envA == "SP":
                                mips_code += f"    lw {words[2]}, {dispA}($s1)\n"
                            
                        matchB = re.match(r'(\w+)\[(\d+)\]', words[3])

                        if matchB:
                            envB = matchB.group(1)
                            dispB = matchB.group(2)
                            if envB == "GP":
                                #TODO si se arreglan los temporales, este arreglo se eliminaria
                                mips_code += f"    lw {words[3]}, {dispB}($s0)\n"
                            elif envB == "SP":
                                mips_code += f"    lw {words[3]}, {dispB}($s1)\n"
                        
                        mips_code += f"    {words[0].lower()} {words[1]}, {words[2]}, {words[3]}\n"

                    
                    elif words[0] == "GOTO":
                        mips_code += f"    j {words[1]}\n"

                    elif words[0][:7] == "L_LOOP_":
                        mips_code += f"{words[0]}\n"

                    elif words[0] == "IF":
                        print("if")
                        mips_code += f"    bnez {words[1]}, {words[5]}\n"

                    elif words[0][:6] == "L_TRUE" or words[0][:7] == "L_FALSE":
                        mips_code += f"{words[0]}\n"

                    elif words[0][:5] == "L_IF_":
                        mips_code += f"{words[0]}\n"
                        
                    elif words[0] == "RETURN":
                        if Act_class != "Main" and Act_func != "main":
                            mips_code += f"    move $v0, {words[1]}\n    jr $ra\n"
                        # else:
                        #     if len(words) > 1:
                        #         mips_code += "    move $t0, $v0\n    jr $ra\n"
                        
                    elif words[0] == "EOC":
                        mips_code += ""
                        
                    elif words[0] == "END":
                        if(words[2] == "main"):
                            mips_code += "    j exit\n"
                            
                        if self.tempBlock != "":
                            mips_code += "\n"+self.tempBlock
                        mips_code += ""
                        self.tempBlock = ""
                   
                    elif words[0] == "EOF":
                        mips_code += "\nexit:\n    li $v0, 10\n    syscall"
                        mips_code = self.dataBlock + mips_code
                        return mips_code
                    
                    else:
                        print(words)
                    
            mips_code = self.dataBlock + mips_code
            return mips_code
        else:
            print("Ocurrio un error leyendo el archivo del CI")
            return None 