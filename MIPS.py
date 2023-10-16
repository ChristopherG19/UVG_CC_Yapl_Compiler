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
        # Abre el archivo de entrada en modo lectura
        with open(self.CI, 'r') as file:
            # Lee el contenido del archivo
            input_code = file.read()
            
        if(input_code != None):
            mips_code = ""
            mips_code += ".data\n.text"

            # Divide el código intermedio en líneas
            lines = input_code.split('\n')

            Act_class = None
            Act_func = None
            Count_Param = 0
            for line in lines:
                # Divide cada línea en palabras (instrucciones y argumentos)
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
                        
                    elif (Act_class+".") in words[0]:
                        call_func = words[0].replace('.', '_')
                        self.etiquetas.append(call_func)
                        Count_Param = 0
                        mips_code += f"\n{call_func}:\n"
                    
                    elif words[0] == "LW":
                        match = re.match(r'(\w+)\[(\d+)\]', words[1])

                        if match:
                            env = match.group(1)
                            disp = match.group(2)
                            mips_code += f"    lw {words[2]}, {disp}(${env.lower()})\n"
                        else:
                            if words[2] == "R":
                                mips_code += f"    lw {words[1]}, $v0\n"
                                
                            
                    elif words[0] == "SW":
                        match = re.match(r'(\w+)\[(\d+)\]', words[1])

                        if match:
                            env = match.group(1)
                            disp = match.group(2)
                            mips_code += f"    lw {words[2]}, {disp}(${env.lower()})\n"
                    
                    elif words[0] == "PARAM":
                        match = re.match(r'(\w+)\[(\d+)\]', words[1])

                        if match:
                            env = match.group(1)
                            disp = match.group(2)

                            mips_code += f"    lw $a{Count_Param}, {disp}(${env.lower()})\n"
                            Count_Param += 1
                            
                    elif words[0] == "CALL":
                        func = words[1].replace('.', '_')
                        if(func not in self.etiquetas):
                            mips_code += f"    jal {func}\n"
                            self.tempBlock += f"{func}:\n    li $v0, 4\n    syscall\n    jr $ra\n"
                        else:    
                            mips_code += f"    jal {func}\n"
                    
                    elif words[0] == "ADD":
                        mips_code += f"    add {words[1]}, {words[2]}, {words[3]}\n"
                        
                    elif words[0] == "RETURN":
                        if len(words) == 1:
                            if Act_class == "Main" and Act_func == "main":
                                mips_code += "    j exit\n"
                            else:
                                mips_code += "    move $t0, $v0\n    jr $ra\n"
                        
                    elif words[0] == "EOC":
                        mips_code += ""
                        
                    elif words[0] == "END":
                        if self.tempBlock != "":
                            mips_code += "\n"+self.tempBlock
                        mips_code += ""
                        self.tempBlock = ""
                   
                    elif words[0] == "EOF":
                        mips_code += "\nexit:"
                        return mips_code

            return mips_code
        else:
            print("Ocurrio un error leyendo el archivo del CI")
            return None            
            
            