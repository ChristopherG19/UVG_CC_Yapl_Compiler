'''
    Universidad del Valle de Guatemala
    Construcción de Compiladores
    Christopher García 20541
    Laboratorio#0
'''

# Interfaz
import tkinter as tk
from tkinter import ttk, Text, Label, Button

def obtener_texto():
    # Texto completo
    texto = T.get("1.0", tk.END)
    print(texto)  
    
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
b3 = Button(root, text="Obtener Texto", command=obtener_texto)

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

