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
        self.headers = ['Name', 'Value', 'Type', 'Env', 'Line']
        self.columns = []
        self.prettyT = PrettyTable()
        
    def getCell(self, type, name=None, value=None):
        # Buscar la celda que coincida con los valores dados
        if type is not None and name is not None and value is not None:
            for row in self.columns:
                if row[2] == type and row[0] == name and row[1] == value:
                    print(self.prettyCell(row, type, name, value))
                    return row
                else:
                    print(self.prettyCell(None, type, name, value))
                    return None

        # Si no se encuentra ninguna celda que coincida, se devuelve None
        return None
    
    def prettyCell(self, row, type=None, name=None, value=None):
        if row == None:
            return f"Value with parameters ({type}, {name}, {value}) is not present"
        else:
            return f"(Type: {row[2]}) {row[0]} = {row[1]} in line {row[4]}"
        
    def add_column(self, column):
        self.columns.append(column)
        self.build_Table()

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
        print(self.prettyT)
       