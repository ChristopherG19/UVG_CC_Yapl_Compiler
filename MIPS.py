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
            mips_code = mips_code.replace("(Int)", "")
            mips_code = mips_code.replace("(Bool)", "")
            mips_code = mips_code.replace("(String)", "")
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
        self.end_B = ""
        self.current_eti = ""
        self.objects = []
        self.recursive = False
        self.strings_creados = []
        self.last_Result = None
        self.last_obj = None
        self.param = 0
        
        # Abre el archivo de entrada en modo lectura
        with open(self.CI, 'r') as file:
            # Lee el contenido del archivo
            input_code = file.read()
            
        if(input_code != None):
            mips_code = ""
            self.dataBlock += '    newline: .asciiz "\\n"'
            mips_code += '    \n.text\n'

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
                    
                    #print(words)
                    # Traducción de instrucciones
                    if words[0] == "CLASS":
                        Act_func = None
                        Count_Param = 0
                        Act_class = words[1]
                        self.etiquetas.append(Act_class)
                        mips_code += f"\n{Act_class}:\n"
                        if words[2] != '0':
                            mips_code += f"    li $a0, {int(words[2])*2}\n"
                            mips_code += f"    li $v0, 9\n"
                            mips_code += f"    syscall\n"
                            mips_code += f"    move $s0, $v0\n"
                        
                    elif (Act_class+".") in words[0]:    
                        self.param = 0                
                        if(self.end_B != ""):
                            mips_code += self.end_B
                            
                        call_func = words[0].replace('.', '_')
                        self.etiquetas.append(call_func)
                        self.current_eti = call_func
                        Count_Param = 0
                        
                        mips_code += f"\n{call_func}:\n"
                        mips_code += f"    sub $sp, $sp, {int(words[1])*2}\n"
                        mips_code += f"    sw $ra, 0($sp)\n\n"

                        self.end_B = f"    lw $ra, 0($sp)\n    add $sp, $sp, {words[1]}\n"
                    
                    elif words[0] == "LW":
                        match = re.match(r'(\w+)\[(\d+)\]', words[2])
                        print("LW words", words)
                        if match:
                            env = match.group(1)
                            disp = match.group(2)
                            if env == "GP":
                                mips_code += f"    lw {words[1]}, {disp}($s0)\n"
                            elif env == "SP":
                                mips_code += f"    lw {words[1]}, {disp}($sp)\n"
                                
                        else:
                            if words[2] == "RET":
                                # Aquí se analizan los diferentes tipos de retorno
                                if(self.last_Result != ""):
                                    if(self.last_Result[0] == "Str"):
                                        mips_code += f"    la {words[1]}, {self.last_Result[1]}\n"   
                                        mips_code += f"    move $a2, {words[1]}\n"
                                        self.last_obj = (words[1], self.last_Result[1])
                                    
                            elif words[2] in self.etiquetas:
                                self.objects.append((words[1].replace('$', ''), words[2]))
                            
                            elif('$' in words[1]):

                                print("$ ", words)
                            
                                get_temp = re.search(r'\$t\d+', words[1])
                                temp = get_temp.group()
                                get_type = re.search(r'\((.*?)\)', words[1])
                                type_T = get_type.group(1)

                                eti = f"str_{self.etis}"
                                mips_code += f"    la {words[1]}, {eti}\n"
                                
                                if(not ' '.join(words[2:]).startswith('"') and not ' '.join(words[2:]).endswith('"')):
                                    n_type_T = '"'+' '.join(words[2:])+'"'
                                else:
                                    n_type_T = ' '.join(words[2:])
                                
                                if(n_type_T not in self.strings_creados):
                                    eti = f"str_{self.etis}"
                                    self.dataBlock += f"\n    {eti}: .asciiz {n_type_T}"
                                    self.strings_creados.append(n_type_T)
                                    self.etis += 1  
                                    self.last_Result = ("Str",eti)
                            
                            else:
                                match = re.match(r'(\w+)\[(\d+)\]', words[1])
                                match2 = re.match(r'P\d+', words[2])
                                if match and match2:
                                    0#print(words)
                    
                    elif words[0] == "LA":
                        mips_code += f"    la {words[1]}, {words[2]}\n"              
                    
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
                                mips_code += f"    sw $t0, {disp}($sp)\n\n"  
                        else:
                            if words[2] == "RET":
                                mips_code += f"    li {words[1]}, $v0\n"

                            else:
                                get_temp = re.search(r'\$t\d+', words[1])
                                temp = get_temp.group()
                                get_type = re.search(r'\((.*?)\)', words[1])
                                type_T = get_type.group(1)
                                mips_code += f"    li {temp}, {words[2]}\n"          
                            
                    elif words[0] == "SW":
                        match = re.match(r'(\w+)\[(\d+)\]', words[1])

                        if match:
                            env = match.group(1)
                            disp = match.group(2)
                            if env == "GP":
                                mips_code += f"    sw {words[2]}, {disp}($s0)\n"
                            elif env == "SP":
                                mips_code += f"    sw {words[2]}, {disp}($sp)\n"
                    
                    elif words[0] == "PARAM":
                        match = re.match(r'(\w+)\[(\d+)\]', words[1])
                        if match:
                            env = match.group(1)
                            disp = match.group(2)

                            mips_code += f"    lw $a{Count_Param}, {disp}(${env.lower()})\n    move $a0, $t0\n"
                            Count_Param += 1
                            
                        # elif(type(words[1]) == str and "$" not in words[1]):
                            
                        #     #TODO revisar creación de strings repetidos
                        #     eti = f"str_{self.etis}"
                        #     mips_code += f"    la $t0, {eti}\n    move $a0, $t0\n"
                            
                        #     if(words[1] not in self.strings_creados):
                        #         self.etis += 1
                        #         eti = f"str_{self.etis}"
                        #         self.dataBlock += f"\n    {eti}: .asciiz {words[1]}"
                        #         self.strings_creados.append(words[1])
                            
                        else:
                            get_temp = re.search(r'\$t\d+', words[1])
                            temp = get_temp.group()
                            get_type = re.search(r'\((.*?)\)', words[1])
                            type_T = get_type.group(1)
                            
                            if temp:
                                mips_code += f"    move $a{self.param}, {temp}\n"
                                self.param += 1
                                
                            
                    elif words[0] == "CALL":
                        self.param = 0    
                        func = words[1].replace('.', '_')
                        temp_exist = func.split('_', 1)
                        #print(words, temp_exist)
                        #self.tempBlock = ""
                        
                        #TODO
                        if('$t' in temp_exist[0]):
                            get_temp = re.search(r'\$t\d+', words[1])
                            temp = get_temp.group()
                            get_type = re.search(r'\((.*?)\)', words[1])
                            type_T = get_type.group(1)
                            
                            #Cargar info de tn
                            if(temp_exist[1] == 'type_name'):
                                n_type_T = '"'+type_T+'"'
                                if(n_type_T not in self.strings_creados):
                                    self.etis += 1
                                    eti = f"str_{self.etis}"
                                    self.dataBlock += f"\n    {eti}: .asciiz {n_type_T}"
                                    self.strings_creados.append(n_type_T)
                                    self.last_Result = ("Str",eti)
                                
                            elif(temp_exist[1] == 'substr'):
                                # t2 = cadena, t0 = inicio, t1 = longitud
                                self.tempBlock += f"String_substr:\n    la $t2, {self.last_obj[1]}\n    move $t0, $a0\n    move $t1, $a1\n    add $t2, $t2, $t0\n    sub $sp, $sp, $t1\n"
                                self.tempBlock += "\n    loop:\n        lb $t3, ($t2)\n        sb $t3, ($sp)\n        addi $t2, $t2, 1\n        addi $sp, $sp, 1\n        addi $t1, $t1, -1\n        bnez $t1, loop\n    move $v0, $sp\n    jr $ra\n\n"

                                self.etiquetas.append("String_substr")
                                self.last_Result = ""
                                mips_code += "    jal String_substr\n    move $t0, $v0\n"

                            elif (temp_exist[1] == 'abort'):
                                print("abort temp ", temp)
                                mips_code += f"\n    la $a0, ({temp})\n"
                                mips_code += f"    jal abort\n\n"
                                self.tempBlock += "abort:\n    li $v0, 4\n    syscall\n    li $v0, 10\n    syscall\n"
                                
                                self.etiquetas.append("abort")

                        elif('"' in temp_exist[0]):
                            get_f = [x.strip() for x in temp_exist[1].split(',')]
                            if(get_f[0] == 'abort'):
                                0
                            elif(get_f[0] == 'concat'):
                                0
                            elif(get_f[0] == 'substr'):
                                0
                            elif(get_f[0] == 'length'):
                                0
                        else:        
                            if func == self.current_eti:
                                self.recursive = True
                            
                            print("\nfunc ", func)

                            if(func not in self.etiquetas):
                                print("in func", func)
                                if("out_int" in func):
                                    self.tempBlock += f"{func}:\n    li $v0, 1\n    syscall\n    la $a0, newline\n    li $v0, 4\n    syscall\n    jr $ra\n\n"
                                elif("out_string" in func):
                                    self.tempBlock += f"{func}:\n    li $v0, 4\n    syscall\n    la $a0, newline\n    li $v0, 4\n    syscall\n    jr $ra\n\n"
                                elif("Object_abort"):
                                    func = "abort"
                                    self.tempBlock += "abort:\n    li $v0, 4\n    syscall\n    li $v0, 10\n    syscall\n"
                                mips_code += f"    jal {func}\n\n"
                                self.etiquetas.append(func)
                                    
                            else:    
                                print("in func else")
                                mips_code += f"    jal {func}\n\n"
                        

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
                            
                        matchB = re.match(r'(\w+)\[(\d+)\]', words[3])

                        if matchB:
                            envB = matchB.group(1)
                            dispB = matchB.group(2)
                            if envB == "GP":
                                mips_code += f"    lw {words[3]}, {dispB}($s0)\n"
                            elif envB == "SP":
                                mips_code += f"    lw {words[3]}, {dispB}($s1)\n"
                                
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
                                mips_code += f"    lw {words[3]}, {dispB}($s0)\n"
                            elif envB == "SP":
                                mips_code += f"    lw {words[3]}, {dispB}($s1)\n"
                        
                        mips_code += f"    {words[0].lower()} {words[1]}, {words[2]}, {words[3]}\n"

                    
                    elif words[0] == "GOTO":
                        mips_code += f"    j {words[1]}\n"

                    elif words[0][:7] == "L_LOOP_":
                        mips_code += f"\n{words[0]}\n"

                    elif words[0] == "IF":
                        # print("if")
                        if "LOOP" in words[len(words) - 1]:
                            mips_code += f"    beqz {words[1]}, {words[5]}\n"
                        else:
                            mips_code += f"    bnez {words[1]}, {words[5]}\n"

                    elif words[0][:6] == "L_TRUE" or words[0][:7] == "L_FALSE":
                        mips_code += f"\n{words[0]}\n"

                    elif words[0][:5] == "L_IF_":
                        mips_code += f"\n{words[0]}\n"
                        
                    elif words[0] == "RETURN":
                        if(self.end_B != ""):
                            mips_code += self.end_B
                            self.end_B = ""
                            
                        if(len(words) == 1):
                            continue
                            
                        match = re.match(r'(\w+)\[(\d+)\]', words[1])
                        
                        if match:
                            env = match.group(1)
                            disp = match.group(2)

                            if Act_class != "Main" and Act_func != "main":
                                mips_code += f"    lw $v0, {disp}(${env.lower()})\n    jr $ra\n"

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
                    
            mips_code = self.dataBlock + mips_code
            return mips_code
        else:
            print("Ocurrio un error leyendo el archivo del CI")
            return None            
            