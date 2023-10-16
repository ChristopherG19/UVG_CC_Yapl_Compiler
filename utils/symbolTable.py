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
        self.show_contains = False  # Un indicador para mostrar o no la columna 'Contains' al imprimir

    def toggle_show_contains(self, show_contains):
        # Este método te permite cambiar si deseas mostrar la columna 'Contains' o no.
        self.show_contains = show_contains

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
    def get_cell(self, id, addType=None, addParent=None, addFunctionP=None, addScope=None):
        for row in self.columns:
            if row[0] == id and (not addType or row[1] == addType) and (not addParent or row[4] == addParent) and (not addFunctionP or row[5] == addFunctionP) and (not addScope or row[5] == addScope):
                return row
        return None
        
    def containsKey(self, id, addType=None, addParent=None, addFunctionP=None):
        if self.get_cell(id, addType, addParent, addFunctionP) is not None:
            return True
        return False
    
    def checkCanUse(self, id, addType=None, addParent=None):
        for row in self.columns:
            row_id, row_add_type, row_add_parent, row_add_function_p = row[0], row[1], row[4], row[5]
            if row_id == id and (addType is None or row_add_type == addType):
                return True
            elif addParent is not None and row_add_parent == addParent:
                return True      
        return False
    
    def get_parameters(self, par_fun, parent=None):
        params = []
        for row in self.columns:
            if row[2] == "Param" and row[5] == par_fun:
                if parent is not None and str(parent) == row[4]:
                    params.append(row)
                elif parent is None:
                    params.append(row)
        return params

    
    def get_method(self, name, parent):
        for row in self.columns:
            if row[0] == name and row[2] == "Method" and row[4] == parent:
                return row
        return None 
    
    def get_method2(self, name, parent):
        ret = None
        for row in self.columns:
            if row[0] == name and row[2] == "Method" and row[4] == parent:
                ret = row

        if ret is not None:
            return ret 
        
        else:
            #probar con el padre
            if (self.get_cell(parent))[3] is not None:
                parent = self.get_cell(parent)[3]

                for row in self.columns:
                    if row[0] == name and row[2] == "Method" and row[4] == parent:
                        ret = row

                if ret is not None:
                    return ret 

            # else, ya no se puede hacer nada

        return ret

    def get_inherited(self, name, parent):
        for row in self.columns:
            if row[0] == name and row[4] == parent:
                return row[3]
        return None
    
    def get_coincidences(self, id):
        matches = []
        for row in self.columns:
            if row[0] == id:
                matches.append(row)
        return matches
        
    def add_info_to_cell(self, name, column_name, value, func=None, classF=None):
        print("------->",name, column_name, value, func, classF)
        # Iterate through the symbol table to find the appropriate cell
        for row in self.columns:
            if row[0] == name:
                if row[5] == func and row[4] == classF:
                    # Check if the column name exists in the headers
                    if column_name in self.headers:
                        index = self.headers.index(column_name)
                        if index < len(row):
                            # Update the cell with the new value
                            row[index] = value
                            print("RR", row)
                            self.build_Table()
                            return True
                    else:
                        print(f"Column '{column_name}' does not exist in the table.")
                        return False
                elif row[5] != func and row[4] != classF:
                    continue
                else:
                    #print("-->>>",row[4], row[5], row[5] == func, row[4] == classF)
                    if column_name in self.headers:
                        index = self.headers.index(column_name)
                        if index < len(row):
                            row[index] = value
                            print("RR2", row)
                            self.build_Table()
                            return True
                    else:
                        print(f"Column '{column_name}' does not exist in the table.")
                        return False
        print(f"Row with name '{name}' does not exist in the table.")
        return False
    
    def getAllfromClass(self, classname):
        ret = []
        for row in self.columns:
            if row[4] == classname and row[2] != "Class":
                ret.append(row)

        return ret

    def build_Table(self):
        # Limpiar tabla
        self.prettyT = PrettyTable()

        # Establecer los encabezados (incluir o excluir 'Contains' según show_contains)
        headers_to_show = self.headers if self.show_contains else [header for header in self.headers if header != 'Contains']
        self.prettyT.field_names = headers_to_show

        # Agregar las filas a la tabla (incluir o excluir 'Contains' según show_contains)
        for row in self.columns:
            row_to_show = row if self.show_contains else row[:6] + row[7:]  # Incluye o excluye la columna 'Contains'
            self.prettyT.add_row(row_to_show)

        # Centrar todo, agregar título e imprimir tabla
        self.prettyT.align = "c"
        self.prettyT.title = "Symbols Table"
        return self.prettyT
    
    def get_displacement(self, id, addType=None, addParent=None, addFunctionP=None):
        for row in self.columns:
            if row[0] == id and (not addType or row[1] == addType) and (not addParent or row[4] == addParent) and (not addFunctionP or row[5] == addFunctionP):
                return row[7]
        return None
    
    def get_cell_Value(self, addType=None, addParent=None, addFunctionP=None, Value=None):
        for row in self.columns:
            if (not addType or row[1] == addType) and (not addParent or row[4] == addParent) and (not addFunctionP or row[5] == addFunctionP) and (not Value or row[-1] == Value):
                return row
        return None