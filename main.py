'''
    Universidad del Valle de Guatemala
    Construcción de Compiladores
    Christopher García 20541
    Laboratorio#0
'''

# Interfaz
import tkinter as tk
import subprocess
import os

from tkinter import ttk, Text, Label, Button

def create_g4():
    # Texto completo
    texto = T.get("1.0", tk.END)
    arch = "Expr.g4"
    try:
        with open(arch, "w") as archivo:
            archivo.write(texto)
    except IOError as e:
        print("Error al generar el archivo:", e)
        
    comando = ["antlr4", "-Dlanguage=Python3", str(arch)]

    try:
        subprocess.run(comando, check=True)
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar el comando:", e)
    
    # Crear archivo para imprimir arbol
    archP = f"{arch[:-3]}Parser.py"
    archL = f"{arch[:-3]}Lexer.py"
    
    treeA = "Tree.py"
    
    if os.path.exists(archP) and os.path.exists(archL):
        with open(treeA, "w") as archi:
            archi.write("from antlr4 import *\n")
            archi.write(f"from {archP[:-3]} import {archP[:-3]}\n")
            archi.write(f"from {archL[:-3]} import {archL[:-3]}\n\n")
            archi.write("def beautify_lisp_string(in_string):\n")
            archi.write("   indent_size = 4\n")
            archi.write("   add_indent = ' '*indent_size\n")
            archi.write("   out_string = in_string[0]\n")
            archi.write("   indent = ''\n")
            archi.write("   for i in range(1, len(in_string)):\n")
            archi.write("       if in_string[i] == '(' and in_string[i+1] != ' ':\n")
            archi.write("           indent += add_indent\n")
            archi.write("           out_string += '\\n' + indent + '(' \n")
            archi.write("       elif in_string[i] == ')':\n")
            archi.write("           out_string += ')'\n")
            archi.write("           if len(indent) > 0:\n")
            archi.write("               indent = indent.replace(add_indent, '', 1)\n")
            archi.write("       else:\n")
            archi.write("           out_string += in_string[i]\n")
            archi.write("   return out_string\n\n")
            archi.write("file_name = 'test1.expr'\n")
            archi.write("input_stream = FileStream(file_name)\n")
            archi.write(f"lexer = {archL[:-3]}(input_stream)\n")
            archi.write("token_stream = CommonTokenStream(lexer)\n")
            archi.write(f"parser = {archP[:-3]}(token_stream)\n")
            archi.write("tree = parser.prog()\n\n")
            archi.write("print('Tree:')\n")
            archi.write("lisp_tree_str = tree.toStringTree(recog=parser)\n")
            archi.write("print(beautify_lisp_string(lisp_tree_str))\n")
            archi.write("print()\n")

    # Texto por líneas
    # texto = T.get("1.0", "end-1c")  # Obtener el texto línea por línea
    # lineas = texto.split("\n")  # Dividir el texto en líneas separadas
    
    #for linea in lineas:
    #    print(linea)  # Imprimir cada línea en la consola

root = tk.Tk()

# Create text widget and specify size.
T = Text(root, height=15, width=55)

# Create label
l = Label(root, text="Cheap Studio Code")
l.config(font=("Arial", 13))

space = Label(root, height=1)
space2 = Label(root, height=1)

# Create an Exit button.
b2 = Button(root, text="Exit", command=root.destroy)
b3 = Button(root, text="Obtener Texto", command=create_g4)

l.pack()
T.pack()
space.pack()
b3.pack()
space2.pack()
b2.pack()

# Insert The Fact.
T.insert(tk.END, "")

tk.mainloop()

# Manipulación de resultado


# Presentación de árbol

