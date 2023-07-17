'''
    Universidad del Valle de Guatemala
    Construcción de Compiladores
    Christopher García 20541
    Ma. Isabel Solano 20504
    Laboratorio#0
'''

# Interfaz
import tkinter as tk
import subprocess
import os

from tkinter import scrolledtext, Label, Button
from antlr4 import *

from utils.utils import CustomErrorListener, beautify_lisp_string

def create_g4():
    texto = T.get("1.0", tk.END)
    arch = "test1.expr"
    try:
        with open(arch, "w") as archivo:
            archivo.write(texto)
    except IOError as e:
        print("Error al generar el archivo:", e)
        
    #root.after(4000, lambda: T.delete(1.0, tk.END))
    
    grammar = "YAPL.g4" 
    comando = ["antlr4", "-Dlanguage=Python3", str(grammar)]

    try:
        subprocess.run(comando, check=True)
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar el comando:", e)
    
    # Crear archivo para imprimir arbol
    archP = f"{grammar[:-3]}Parser.py"
    archL = f"{grammar[:-3]}Lexer.py"
            
    treeA = "Tree.py"
    
    if os.path.exists(archP) and os.path.exists(archL):
        from YAPLParser import YAPLParser
        from YAPLLexer import YAPLLexer
        
        file_name = 'test1.expr'
        error_listener = CustomErrorListener(T, tk)
        
        input_stream = FileStream(file_name)
        lexer = YAPLLexer(input_stream)
        
        token_stream = CommonTokenStream(lexer)
        parser = YAPLParser(token_stream)
        parser.removeErrorListeners()
        parser._listeners = [error_listener]
        tree = parser.prog()
        
        if not error_listener.has_error():
            T.insert(tk.END, "\nNo se encontraron errores, árbol disponible en consola y GUI desplegada")
            print('Tree:\n')
            lisp_tree_str = tree.toStringTree(recog=parser)
            print(beautify_lisp_string(lisp_tree_str))
            print()
            
            show_tree()

def show_tree():
    file_name = 'test1.expr'
    command = ["antlr4-parse", "YAPL.g4", "prog", "-gui"]

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    with open(file_name, "r") as file:
        example = file.read()
        
    process.communicate(input=example.encode('utf-8'))
        
    #root.after(10000, lambda: T.delete(1.0, tk.END))

root = tk.Tk()

T = scrolledtext.ScrolledText(root, height=20, width=100)
l = Label(root, text="Not Visual Studio Code")
l.config(font=("Arial", 13))

space = Label(root, height=1)
space2 = Label(root, height=1)
b2 = Button(root, text="Ingresar expresion y mostrar árbol", command=create_g4)
b4 = Button(root, text="Exit", command=root.destroy)

l.pack()
T.pack()
space.pack()
b2.pack()
space2.pack()
b4.pack()

T.insert(tk.END, "")
tk.mainloop()

