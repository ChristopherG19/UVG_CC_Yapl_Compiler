'''
    Universidad del Valle de Guatemala
    Construcción de Compiladores
    Christopher García 20541
    Ma. Isabel Solano 20504
    Laboratorio#0
'''

import sys
from antlr4.error.ErrorListener import ErrorListener

class CustomErrorListener(ErrorListener):    
    def __init__(self, text_widget, tk_module):
        self.T = text_widget
        self.tk = tk_module
        self.errors = []  # Lista para almacenar los mensajes de error
        self.error_occurred = False
        
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_msg = f"Error en línea {line}, columna {column}\nDescripcion: {msg}\n"
        self.errors.append(error_msg)
        self.error_occurred = True
        
    def has_error(self):
        return self.error_occurred

    def get_errors(self):
        return self.errors

# Función proveniente de https://github.com/AkiraHakuta/antlr4_Python3_examples
def beautify_lisp_string(in_string):
   indent_size = 4
   add_indent = ' '*indent_size
   out_string = in_string[0]
   indent = ''
   for i in range(1, len(in_string)):
       if in_string[i] == '(' and in_string[i+1] != ' ':
           indent += add_indent
           out_string += '\n' + indent + '(' 
       elif in_string[i] == ')':
           out_string += ')'
           if len(indent) > 0:
               indent = indent.replace(add_indent, '', 1)
       else:
           out_string += in_string[i]
   return out_string