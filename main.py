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
from BuildTable import YAPLVisitorImpl

from utils.utils import CustomErrorListener, beautify_lisp_string

def create_g4():
    texto = T.get("1.0", tk.END)
    arch = "./tests/exampleUser.expr"
    try:
        with open(arch, "w") as archivo:
            archivo.write(texto)
    except IOError as e:
        print("Error al generar el archivo:", e)
        
    #root.after(4000, lambda: T.delete(1.0, tk.END))
    
    grammar = "YAPL.g4" 
    comando = ["antlr4", "-Dlanguage=Python3", "-visitor",str(grammar)]

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
        
        file_name = './tests/exampleUser.expr'
        error_listener = CustomErrorListener(T, tk)
        
        input_stream = FileStream(file_name)
        lexer = YAPLLexer(input_stream)
        
        token_stream = CommonTokenStream(lexer)
        parser = YAPLParser(token_stream)
        parser.removeErrorListeners()
        parser._listeners = [error_listener]
        tree = parser.prog()
        
        YV = YAPLVisitorImpl()
        try:
            YV.visit(tree)
        except TypeError as e:
            print(e);
        treeF = YV.symbolTable.build_Table()
        print(treeF)
        
        if not error_listener.has_error():
            T.insert(tk.END, "\n\nNo se encontraron errores, árbol disponible en consola y GUI desplegada")
            print('Tree:\n')
            lisp_tree_str = tree.toStringTree(recog=parser)
            print(beautify_lisp_string(lisp_tree_str))
            print()
            show_tree()
        else:
            T.delete(1.0, tk.END)
            errors = error_listener.get_errors()
            T.insert(tk.END, "\nSe encontraron errores:\n")
            for error in errors:
                T.insert(tk.END, error + "\n")

def show_tree():
    file_name = './tests/exampleUser.expr'
    command = ["antlr4-parse", "YAPL.g4", "prog", "-gui"]

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    with open(file_name, "r") as file:
        example = file.read()
        
    process.communicate(input=example.encode('utf-8'))
        
    root.after(10000, lambda: T.delete(1.0, tk.END))

def clear():
    T.delete(1.0, tk.END)

root = tk.Tk()
root.title("Not Visual Studio Code")
root.configure(bg="#1e1e1e")  # Color de fondo oscuro

l = tk.Label(root, text="Not Visual Studio Code", fg="white", bg="#1e1e1e", font=("Arial", 13))
l.pack()

T = scrolledtext.ScrolledText(root, height=20, width=100, bg="#2d2d2d", fg="white", insertbackground="white",
                              selectbackground="blue", selectforeground="white", font=("Arial", 12))
T.pack()

space = tk.Label(root, height=1, bg="#1e1e1e")
space.pack()

b2 = tk.Button(root, text="Ingresar expresion y mostrar árbol", command=create_g4, bg="#2d2d2d", fg="white",
               activebackground="#444", activeforeground="white")
b2.pack()

b3 = tk.Button(root, text="Limpiar", command=clear, bg="#2d2d2d", fg="white", activebackground="#444",
               activeforeground="white")
b3.pack()

space2 = tk.Label(root, height=1, bg="#1e1e1e")
space2.pack()

b4 = tk.Button(root, text="Exit", command=root.destroy, bg="#2d2d2d", fg="white", activebackground="#444",
               activeforeground="white")
b4.pack()

T.insert(tk.END, "")
tk.mainloop()

