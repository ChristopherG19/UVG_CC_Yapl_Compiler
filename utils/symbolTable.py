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
        self.headers = ['Name', 'Type_Value', 'Type', 'Inherits', 'Parent_Cl', 'Parent_Fun', 'Contains', 'Displacement', 'Scope', 'Space', 'Value']
        self.columns = []
        self.prettyT = PrettyTable()
    
    def prettyCell(self, row, type=None, name=None):
        if row == None:
            return f"Value with parameters ({type}, {name}) is not present"
        else:
            return f"(Type: {row[1]}) {row[0]}"
        
    def row_exists_with_attributes(self, attributes):
        for row in self.columns:
            if all(row[i] == attr for i, attr in enumerate(attributes)):
                return True
        return False
    
    def is_attribute_declared(self, attribute_name, class_name):
        for row in self.columns:
            if row[0] == attribute_name and row[3] == class_name and row[6] != "Parameter":
                return True
        return False

    def add_column(self, column):
        if not self.row_exists_with_attributes(column):
            self.columns.append(column)
            self.build_Table()
            return True
        return False
        
    # Revisa id, tipo (method, class, etc.), clase parent
    def get_cell(self, id, addType=None, addParent=None):
        for row in self.columns:
            if row[0] == id and (not addType or row[1] == addType) and (not addParent or row[4] == addParent):
                return row
        return None
        
    def containsKey(self, id, addType=None, addParent=None):
        if self.get_cell(id, addType, addParent) is not None:
            return True
        return False
    
    def add_info_to_cell(self, name, column_name, value):
        for row in self.columns:
            if row[0] == name:
                if column_name in self.headers:
                    index = self.headers.index(column_name)
                    if index < len(row):
                        row[index] = value
                        self.build_Table()
                        return True
                else:
                    print(f"Column '{column_name}' does not exist in the table.")
                    return False
        print(f"Row with name '{name}' does not exist in the table.")
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
       