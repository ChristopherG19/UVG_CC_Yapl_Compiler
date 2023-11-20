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

from tkinter import scrolledtext, filedialog
from PIL import Image, ImageTk
from antlr4 import *

from BuildTable import YAPLVisitorImpl
from CI import *
from MIPS import *

from utils.utils import CustomErrorListener, beautify_lisp_string

arch = "./tests/exampleUser.cl"
grammar = "YAPL.g4" 
current = "code" # possible values ["code", "CI", "tokens", "Mips"]
code = ""

def init_program():

    comando = ["antlr4", "-Dlanguage=Python3", "-visitor", str(grammar)]

    try:
        subprocess.run(comando, check=True)
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar el comando:", e)
    
    # Crear archivo para imprimir arbol
    archP = f"{grammar[:-3]}Parser.py"
    archL = f"{grammar[:-3]}Lexer.py"
            
    treeA = "Tree.py"

def create_g4():

    global current
    global code

    if (current != "code"):
        texto = code

    else: 
        texto = T.get("1.0", tk.END)
    
    try:
        with open(arch, "w") as archivo:
            archivo.write(texto)
    except IOError as e:
        print("Error al generar el archivo:", e)
        
    #root.after(4000, lambda: T.delete(1.0, tk.END))
    
    
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
        
        file_name = './tests/exampleUser.cl'
        error_listener = CustomErrorListener(T, tk)
        
        input_stream = FileStream(file_name)
        lexer = YAPLLexer(input_stream)
        
        token_stream = CommonTokenStream(lexer)
        parser = YAPLParser(token_stream)
        parser.removeErrorListeners()
        parser._listeners = [error_listener]
        tree = parser.prog()
        
        if not error_listener.has_error():
            Terminal.delete(1.0, tk.END)
            Terminal.insert(tk.END, "\n\nNo se encontraron errores, árbol disponible en consola y GUI desplegada")

            show_tree()

            try:
                YV = YAPLVisitorImpl()
                res = YV.visit(tree)
                Terminal.delete(1.0, tk.END)
                if(str(res) == "Error" or len (YV.customErrors) > 0):
                    Terminal.insert(tk.END, "\nResultado Lectura: Errores semánticos encontrados\n")
                    for err in YV.customErrors:
                        Terminal.insert(tk.END, f"-> {err}\n")
                    print()

                else:
                    Terminal.insert(tk.END, "\nResultado Lectura: Todo está semánticamente correcto\n")
                    CI = CodigoIntermedio("CI.txt", YV.symbolTable)
                    resCI = CI.visit(tree)

                    MIPS_ = MIPS("CI.txt")
                    MIPS_.get_MIPS_Code()

                    treeF = YV.symbolTable.build_Table()
                    with open("SymbolTable.txt", 'w', encoding="utf-8") as f:
                        f.write(treeF.get_string())

            except TypeError as e:
                print(e);

        else:
            Terminal.delete(1.0, tk.END)
            errors = error_listener.get_errors()
            
            Terminal.insert(tk.END, "\n========================================================")
            Terminal.insert(tk.END, "\nSe encontraron errores:\n")
            for error in errors:
                Terminal.insert(tk.END, error + "\n")

def show_tree():
    file_name = './tests/exampleUser.cl'
    command = ["antlr4-parse", "YAPL.g4", "prog", "-gui"]

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    with open(file_name, "r") as file:
        example = file.read()
        
    process.communicate(input=example.encode('utf-8'))
        
    #root.after(10000, lambda: T.delete(1.0, tk.END))

# HEADER =================================================

def clear():
    T.delete(1.0, tk.END)

def clear_terminal():
    Terminal.delete(1.0, tk.END)

# FILE ===================================================
def on_new():
    T.delete(1.0, tk.END)
    Terminal.delete(1.0, tk.END)

def on_open():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("All Files", "*.*")])
    if file_path:
        print("Selected File:", file_path)

def on_save():
    texto = T.get("1.0", tk.END)
    arch = "./tests/exampleUser.cl"
    try:
        with open(arch, "w") as archivo:
            archivo.write(texto)
    except IOError as e:
        print("Error al generar el archivo:", e)

def on_save_as():
    file_path = filedialog.asksaveasfilename(title="Select Where to save it", filetypes=[("All Files", "*.*")])
    if file_path:
        print("Selected File:", file_path)

# EDIT ===================================================

def on_undo():
    try:
        T.edit_undo()
    except tk.TclError:
        pass

def on_redo():
    try:
        T.edit_redo()
    except tk.TclError:
        pass

def on_copy():
    selected_text = T.get("sel.first", "sel.last")
    root.clipboard_clear()
    root.clipboard_append(selected_text)

def on_paste():
    clipboard_text = root.clipboard_get()
    T.insert(tk.END, clipboard_text)

def on_cut():
    selected_text = T.get("sel.first", "sel.last")
    root.clipboard_clear()
    root.clipboard_append(selected_text)
    T.delete("sel.first", "sel.last")

# RUN ==========================================================

def on_select_grammar():
    file_path_g = filedialog.askopenfilename(title="Select a File", filetypes=[("All Files", "*.*")])
    if file_path_g:
        # grammar = file_path_g
        print("Nueva gramática obtenida a partir de:", file_path_g)
        with open(file_path_g) as new_Grammar:
            content = new_Grammar.read()

        with open('YAPL.g4', "w") as old_Grammar:
            old_Grammar.write(content)

        # reinizializar el programa
        init_program()


def on_change_to_codigo():
    global current
    global code
    if (current != "code"):
        
        T.delete(1.0, tk.END)    
        T.insert(tk.END, code)

    # change current
    current = "code"

def on_change_to_tokens():
    global current
    global code
    if (current == "code"):
        # save code
        code = T.get("1.0", tk.END)

    # change current
    current = "tokens"

    # Clear
    T.delete(1.0, tk.END)

    # get text from file
    try:
        with open("YAPL.tokens", 'r') as file:
            text_ = str(file.read())

            # change text to the one on 
            T.insert(tk.END, text_)

    except:
        print("Error leyendo YAPL.token") 

def on_change_to_CI():
    global current
    global code
    if (current == "code"):
        # save code
        code = T.get("1.0", tk.END)

    # change current
    current = "CI"

    # Clear
    T.delete(1.0, tk.END)

    # get text from file
    try:
        with open("CI.txt", 'r') as file:
            text_ = str(file.read())

            # change text to the one on 
            T.insert(tk.END, text_)

    except:
        print("Error leyendo Código Intermedio") 
    

def on_change_to_MIPS():
    global current
    global code
    if (current == "code"):
        # save code
        code = T.get("1.0", tk.END)

    # change current
    current = "MIPS"

    # Clear
    T.delete(1.0, tk.END)

    # get text from file
    try:
        with open("MIPS.asm", 'r') as file:
            text_ = str(file.read())

            # change text to the one on 
            T.insert(tk.END, text_)

    except:
        print("Error leyendo MIPS") 

# UID ==========================================================

root = tk.Tk()
root.title("Not Visual Studio Code")
root.configure(bg="#1e1e1e")  # Color de fondo oscuro


l = tk.Label(root, text="Not Visual Studio Code", fg="white", bg="#1e1e1e", font=("Arial", 13))
l.pack()

# Upper options
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

IDE_opts = tk.Menu(menu_bar)
root.config(menu=IDE_opts)

btn_File = tk.Menu(menu_bar, tearoff=0)
IDE_opts.add_cascade(label="Archivo", menu=btn_File)
btn_File.add_command(label="Nuevo Archivo", command=on_new)
btn_File.add_command(label="Abrir", command=on_open)
btn_File.add_separator()
btn_File.add_command(label="Guardar", command=on_save)
btn_File.add_command(label="Guardar como", command=on_save_as)
btn_File.add_separator()
btn_File.add_command(label="Salir", command=root.quit)

btn_Edit = tk.Menu(menu_bar, tearoff=0)
IDE_opts.add_cascade(label="Editar", menu=btn_Edit)
btn_Edit.add_command(label="Deshacer", command=on_undo)
btn_Edit.add_command(label="Rehacer", command=on_redo)
btn_Edit.add_separator()
btn_Edit.add_command(label="Copiar", command=on_copy)
btn_Edit.add_command(label="Pegar", command=on_paste)
btn_Edit.add_command(label="Cortar", command=on_cut)

btn_Exec = tk.Menu(menu_bar, tearoff=0)
IDE_opts.add_cascade(label="Ejecución", menu=btn_Exec)
btn_Exec.add_command(label="Correr", command=create_g4)
btn_Exec.add_separator()
btn_Exec.add_command(label="Definir gramática", command=on_select_grammar)


IDE_opts.add_separator()

# Header 
header_frame = tk.Frame(root, bg="#1e1e1e")
header_frame.pack(side=tk.TOP, fill=tk.X)

# Botones 

emtpy_spc_0 = tk.Frame(header_frame, width=10, bg="#1e1e1e")
emtpy_spc_0.pack(side=tk.RIGHT, fill="y")

btn_exe = tk.Button(header_frame, text="Ejecutar", command=create_g4, bg="#2d2d2d", fg="white",
               activebackground="#444", activeforeground="white")
btn_exe.pack(side=tk.RIGHT)

emtpy_spc_1 = tk.Frame(header_frame, width=10, bg="#1e1e1e")
emtpy_spc_1.pack(side=tk.RIGHT, fill="y")

btn_Clean_terminal = tk.Button(header_frame, text="Limpiar Terminal", command=clear_terminal, bg="#2d2d2d", fg="white", activebackground="#444",
               activeforeground="white")
btn_Clean_terminal.pack(side=tk.RIGHT)

btn_Clean_space = tk.Button(header_frame, text="Limpiar", command=clear, bg="#2d2d2d", fg="white", activebackground="#444",
               activeforeground="white")
btn_Clean_space.pack(side=tk.RIGHT)

btn_Code = tk.Button(header_frame, text="Código", command=on_change_to_codigo, bg="#2d2d2d", fg="white", activebackground="#444",
               activeforeground="white")
btn_Code.pack(side=tk.LEFT)

btn_Tokens = tk.Button(header_frame, text="Tokens", command=on_change_to_tokens, bg="#2d2d2d", fg="white", activebackground="#444",
               activeforeground="white")
btn_Tokens.pack(side=tk.LEFT)

btn_CI = tk.Button(header_frame, text="Código Intermedio", command=on_change_to_CI, bg="#2d2d2d", fg="white", activebackground="#444",
               activeforeground="white")
btn_CI.pack(side=tk.LEFT)

btn_Mips = tk.Button(header_frame, text="Mips", command=on_change_to_MIPS, bg="#2d2d2d", fg="white", activebackground="#444",
               activeforeground="white")
btn_Mips.pack(side=tk.LEFT)


# Área de escritura de texto 
T = scrolledtext.ScrolledText(root, height=20, bg="#2d2d2d", fg="white", insertbackground="white",
                              selectbackground="#444649", selectforeground="white", font=("Arial", 12),)
T.pack(fill="both")

emtpy_spc_3 = tk.Frame(root, height=5, bg="#1e1e1e")
emtpy_spc_3.pack(fill="x")

# Terminal 
Terminal = scrolledtext.ScrolledText(root, height=10, bg="#2d2d2d", fg="white", insertbackground="white",
                              selectbackground="#444649", selectforeground="white", font=("Arial", 12),
                              )
Terminal.pack(fill="x")


space = tk.Label(root, height=1, bg="#1e1e1e")
space.pack()


T.insert(tk.END, "")


# inicialización del programa y la gramática
init_program()

tk.mainloop()

