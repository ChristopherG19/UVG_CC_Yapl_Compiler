'''
    Universidad del Valle de Guatemala
    Construcción de Compiladores
    Christopher García 20541
    Ma. Isabel Solano 20504
    Laboratorio#1
'''

from prettytable import PrettyTable

class Table():
    def __init__(self):
        self.headers = ['Name', 'Value', 'Type']
        self.columns = []
        self.prettyT = PrettyTable()
    
    def prettyCell(self, row, type=None, name=None, value=None):
        if row == None:
            return f"Value with parameters ({type}, {name}, {value}) is not present"
        else:
            return f"(Type: {row[2]}) {row[0]} = {row[1]}"
        
    def add_column(self, column):
        self.columns.append(column)
        self.build_Table()
        
    def get_cell(self, id):
        for row in self.columns:
            if row[0] == id:
                return row[2]
            return None
        
    def containsKey(self, id):
        if self.get_cell(id) is not None:
            return True
        return False

    def build_Table(self):
        # Limpiar tabla
        self.prettyT = PrettyTable()
        
        # Establecer los encabezados
        self.prettyT.field_names = self.headers
        
        # Agregar las filas a la tabla
        for row in self.columns:
            self.prettyT.add_row(row)
        
        # Centrar todo, agregar título e imprimir tabla
        self.prettyT.align = "c"
        self.prettyT.title = "Symbols Table"
        return self.prettyT
       