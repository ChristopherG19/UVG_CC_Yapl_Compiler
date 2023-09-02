"""
    Universidad del Valle de Guatemala
    Construcción de Compiladores
    Christopher García 20541
    Ma. Isabel Solano 20504
    Laboratorio#1
"""

from antlr4 import *
from YAPLLexer import YAPLLexer
from YAPLParser import YAPLParser
from YAPLVisitor import YAPLVisitor
from utils.node import *
from utils.symbolTable import *
from utils.utils import clean_errors, get_space_vars

class YAPLVisitorImpl(YAPLVisitor):
    def __init__(self):
        self.symbolTable = Table()
        self.class_methods = {}
        self.methods_parameters = {}
        self.current_class = None
        self.current_function = None
        self.customErrors = []
        self.add_other_classes()
        
    def add_other_classes(self):
        self.symbolTable.add_column(["Int", "Int", "Declaration", None, "Int", None, None, None, "Global", 8, 0])
        self.symbolTable.add_column(["Bool", "Bool", "Declaration", None, "Bool", None, None, None, "Global", 1, False])
        self.symbolTable.add_column([False, "Bool", "Declaration", None, "Bool", None, None, None, "Global", 1, 0])
        self.symbolTable.add_column([True, "Bool", "Declaration", None, "Bool", None, None, None, "Global", 1, 1])
        self.symbolTable.add_column(["Void", "Void", "Declaration", None, "Void", None, None, None, "Global", 8, None])
        self.symbolTable.add_column(["Object", "Object", "Class", None, "Object", None, ["abort", "type_name", "copy"], None, "Global", None, None])
        self.symbolTable.add_column(["String", "String", "Declaration", None, "String", None, ["lenght", "concat", "substr"], None, "Global", 8, ""])
        self.symbolTable.add_column(["abort", "Object", "Declaration", None, "Object", None, None, None, "Global", None, "Error"])
        self.symbolTable.add_column(["type_name", "String", "Declaration", None, "Object", None, None, None, "Global", None, None])
        self.symbolTable.add_column(["copy", "SELF_TYPE", "Declaration", None, "Object", None, None, None, "Global", None, None])
        
    def add_special_class_IO(self):
        self.symbolTable.add_column(["out_string", "SELF_TYPE", "Method", None, "IO", None, ["x"], None, "Global", None, None])
        self.symbolTable.add_column(["xPar", "String", "Param", None, "IO", "out_string", None, None, "Local", None, None])
        
        self.symbolTable.add_column(["out_int", "SELF_TYPE", "Method", None, "IO", None, ["x"], None, "Global", None, None])
        self.symbolTable.add_column(["xPar", "Int", "Param", None, "IO", "out_int", None, None, "Local", None, None])
        
        self.symbolTable.add_column(["in_string", "String", "Method", None, "IO", None, None, None, "Global", None, None])
        self.symbolTable.add_column(["int_int", "Int", "Method", None, "IO", None, None, None, "Global", None, None])
        
        self.symbolTable.add_column(["lenght", "String", "Method", None, "String", None, None, None, "Global", None, None])
        self.symbolTable.add_column(["concat", "String", "Method", None, "String", None, ["s"], None, "Global", None, None])
        self.symbolTable.add_column(["sPar", "String", "Param", None, "String", "concat", None, None, "Local", None, None])
        
        self.symbolTable.add_column(["substr", "String", "Method", None, "String", None, ["i", "l"], None, "Global", None, None])
        self.symbolTable.add_column(["iPar", "Int", "Param", None, "String", "substr", None, None, "Local", None, None])
        self.symbolTable.add_column(["lPar", "Int", "Param", None, "String", "substr", None, None, "Local", None, None])
        
    def visitStart(self, ctx:YAPLParser.StartContext):
        #print("Start")
        final_type = None
        stages = ctx.class_def()
        for stage in stages:
            stage_type = self.visit(stage)
            final_type = stage_type
          
        if(self.symbolTable.containsKey("Main")):
            if(not self.symbolTable.containsKey("main", None, "Main")):
                self.customErrors.append("Clase Main no cuenta con método main")
                return "Error"
            
            cell_Main = self.symbolTable.get_cell("Main")
            if(cell_Main[2] != None):
                value_inh = self.symbolTable.get_cell(cell_Main[2])
                
                if(value_inh != None):
                    if(value_inh[1] == "class"):
                        if(value_inh[0] != "IO"):
                            self.customErrors.append("Clase Main no puede heredar de otra clase")
                            return "Error"
                    self.customErrors.append(f"Clase Main no puede heredar de este elemento ({value_inh[1]})")
                    return "Error"            
        else:
            self.customErrors.append("No contiene clase Main")
            return "Error"

        return final_type
    
    def visitDefClass(self, ctx: YAPLParser.DefClassContext):
        # print("defClass")
        id = ctx.TYPE(0).getText()
        type_id = ctx.CLASS_N().__str__()
        self.current_class = id
        if ctx.INHERITS():
            inherits = ctx.TYPE(1).getText()
            
            if(inherits == "IO"):
                self.add_special_class_IO()
            
            if(inherits.lower() in ["string", "int", "bool"]):
                self.customErrors.append(f"Clase {self.current_class} no puede heredar de esta clase ({inherits})")
                return "Error"
            elif (not self.symbolTable.containsKey(inherits) and inherits != "IO"):
                self.customErrors.append(f"Clase {self.current_class} no puede heredar de esta clase ({inherits}) porque no está definida")
                return "Error"
            else:
                self.symbolTable.add_column([id, None, "Class", inherits, self.current_class, self.current_function, None, None, "Global", None, None])
    
    
        else:
            self.symbolTable.add_column([id, None, "Class", "Object", self.current_class, self.current_function, None, None, "Global", None, None])
        
        self.class_methods[id] = []
        
        type_class = None
        for step in ctx.feature():
            type_step = self.visit(step)
            if type_step == "Error":
                return "Error"
            else:
                if type_step != None:
                    type_class = type_step
        
        return type_class
    
    def visitDefFunc(self, ctx: YAPLParser.DefFuncContext):
        #print("visitDefFunc")
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        parent_class = ctx.parentCtx.TYPE(0).getText() if ctx.parentCtx.TYPE(0) else None
        self.current_class = parent_class
        self.current_function = id
        formal_parameters = ctx.formal()
        if formal_parameters:
            if(id == "main"):
                self.customErrors.append(f"Método main no puede tener parámetros formales")
                return "Error"
            
            for formal_param in formal_parameters:
                param_name = formal_param.ID().getText()
                param_type = formal_param.TYPE().getText()
                space = get_space_vars(param_type.lower())
                self.symbolTable.add_column([param_name, param_type, "Param", None, parent_class, self.current_function, None, None, "Local", space, None])
                if parent_class in self.class_methods:
                    self.class_methods[parent_class].append(param_name)
                else:
                    self.class_methods[parent_class] = [param_name]

                self.visit(formal_param)    
        
        if(self.symbolTable.containsKey(id)):
            temp = self.symbolTable.get_cell(id)
            if temp[1] != type_id:
                parentV = self.symbolTable.get_cell(parent_class)
                if(temp[4] == parentV[3]):
                    self.customErrors.append(f"Intento de override del método '{temp[0]}' en clase {parent_class} que hereda de {temp[4]}")
                    return "Error"
        
        if parent_class in self.class_methods:
            self.class_methods[parent_class].append(id)
            if(self.current_function != id):
                self.symbolTable.add_column([id, type_id, "Method", None, parent_class, self.current_function, None, None, "Local", None, None])
            else:
                self.symbolTable.add_column([id, type_id, "Method", None, parent_class, None, None, None, "Global", None, None])
                
        else:
            self.class_methods[parent_class] = [id]

        self.symbolTable.add_info_to_cell(parent_class, "Contains", self.class_methods[parent_class])
        
        type_id_b = self.visit(ctx.expr())

        if type_id_b == "Error":
            return "Error"
        
        if (type(type_id_b) == tuple):
            if type_id_b[0] == 'Self':
                return type_id_b

            if type_id_b[0] != type_id:
                self.customErrors.append(f"Función {id} definida como {type_id} pero se encontró {type_id_b[0]}")
                return "Error"
            
            return type_id_b


        if type_id_b is None:
        
            if type_id == "SELF_TYPE":
                return "SELF_TYPE"
        
            elif type_id == "Object":
                return "Object"
        
            else:
                self.customErrors.append(f"Función definida como {type_id} pero se encontró None")
                return "Error"
        
        if type_id_b != type_id:

            self.customErrors.append(f"Función definida como {type_id} pero se encontró {type_id_b}")
            return "Error"

        return type_id_b
    
    def visitDefAssign(self, ctx: YAPLParser.DefAssignContext):
        #print("visitDefAssign")
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        space = get_space_vars(type_id.lower())
        
        parent_class = ctx.parentCtx.TYPE(0).getText() if ctx.parentCtx.TYPE(0) else None
        self.current_class = parent_class
        
        if(type_id == "Error"):
            return "Error"
        
        type_id_res = None
        val = None
        if(ctx.expr()):
            type_id_res = self.visit(ctx.expr())
            
            if(type_id_res == "Error"):
                return "Error"
            
            if(type_id_res == "SELF_TYPE"):
                return type_id
                
            if(type_id != type_id_res):
                if not ((type_id == 'Int' and type_id_res == 'Bool') or (type_id == 'Bool' and type_id_res == 'Int')):
                    self.customErrors.append(f"Mismatch entre tipos de datos en asignacion ({id}: {type_id} <- {type_id_res})")
                    return "Error"

        else:
            if (self.symbolTable.get_cell(type_id, "Declaration") != None):
                val = self.symbolTable.get_cell(type_id, "Declaration")[-1]
        
        if parent_class in self.class_methods:
            if(self.symbolTable.containsKey(id, None, parent_class, self.current_function)):
                self.customErrors.append(f"El identificador '{id}' ya fue definido en este ámbito")
                return "Error"
            else:
                if(val == None):
                    val = self.symbolTable.get_cell(type_id)[-1]
                self.class_methods[parent_class].append(id)
                self.symbolTable.add_column([id, type_id, "Instance", None, parent_class, self.current_function, None, None, "Global", space, val])
        else:
            self.class_methods[parent_class] = [id]
            
        self.symbolTable.add_info_to_cell(parent_class, "Contains", self.class_methods[parent_class])
        
        return type_id
    
    def visitFormalAssign(self, ctx:YAPLParser.FormalAssignContext):
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        return type_id
        
    def visitAssignment(self, ctx: YAPLParser.AssignmentContext):
        # print("visitAssignment")
        id = ctx.ID().getText()
        result = self.visit(ctx.expr())

        if isinstance(result, tuple):
            type_id, val = result
        else:
            type_id = result
            val = None
            
        if(self.symbolTable.containsKey(id)):
            if(val != None):
                self.symbolTable.add_info_to_cell(id, "Value", val)

        if type_id == 'Error':
            return 'Error'
        
        row = self.symbolTable.get_cell(id, addParent=self.current_class)

        if(type_id != row[1]):
            if not ((type_id == 'Int' and row[1] == 'Bool') or (type_id == 'Bool' and row[1] == 'Int')):
                self.customErrors.append(f"Mismatch entre tipos de datos en asignacion ({id}: {type_id} <- {row[1]})")
                return "Error"

        return type_id
    
    def visitDispatchExplicit(self, ctx: YAPLParser.DispatchExplicitContext):
        # print("visitDispatchExplicit")
        obj_expr_type = self.visit(ctx.expr(0))
        method_name = ctx.ID().getText()
        type_ = ctx.TYPE()
        # print(ctx.getText())

        id_ = str(ctx.ID().getText())

        otra_clase = self.visit(ctx.expr(0))

        if otra_clase == 'Error':
            return 'Error'

        ## Revisar que exista
        if (not self.symbolTable.containsKey(id_, addParent=otra_clase)):
            self.customErrors.append(f"{id_} no existe en {otra_clase}")
            return 'Error'
        
        row = self.symbolTable.get_cell(id_, addParent=otra_clase)
        type__ = row[1]

        # parametros del actual 
        n = 1
        params_acc = []
        while(ctx.expr(n) is not None):
            params_acc.append(ctx.expr(n))
            n += 1

        # parámetros que debería tener
        params_def = self.symbolTable.get_parameters(method_name)

        # verificar cantidad de parámetros
        if (len(params_def) != len(params_acc)):
            self.customErrors.append(f"{method_name} requiere {len(params_def)} pero se le dieron {len(params_acc)}")
            return "Error"

        
        # verificar tipo de parámetros 
        for par in range(len(params_def)):
            vis = self.visit(params_acc[par])
            
            if vis == "Error":
                return "Error"

            if (type(vis) == tuple):
                # print("tupla ex")
                if (vis[0] != params_def[par][1]):
                    self.customErrors.append(f"En {method_name} el parámetro {params_def[par][0]} require ser {params_def[par][1]} pero se encontró {vis[0]}")
                    # print("print")
                    return "Error"

            else:
                if (vis != params_def[par][1]):
                    self.customErrors.append(f"En {method_name} el parámetro {params_def[par][0]} require ser {params_def[par][1]} pero se encontró {vis}")
                    return "Error"  
                
        if (ctx.TYPE()):
            if ctx.TYPE().getText() != type__:
                self.customErrors.append(f"El TYPE definido no es el mismo al type que retorna: {ctx.TYPE().getText()}, {type__}")
                return 'Error'

        return type__

    def visitDispatchImplicit(self, ctx: YAPLParser.DispatchImplicitContext):
        # print("visitDispatchImplicit")

        method_name = ctx.ID().getText()

        # verificar existencia en la tabla
        met = self.symbolTable.get_cell(method_name)
        if met is None:
            self.customErrors.append(f"Método {method_name} no está definido")
            return "Error"
        else:
            if met[4] != self.current_class:
                # verificar padre
                # print("m", met[4])
                inh = self.symbolTable.get_cell(self.current_class)
                # print("i", inh[3])
                if (met[4] != inh[3]):
                    self.customErrors.append(f"Método {method_name} no está definido")
                    return "Error"
                
        # parametros del actual 
        n = 0
        params_acc = []
        while(ctx.expr(n) is not None):
            params_acc.append(ctx.expr(n))
            n += 1

        # parámetros que debería tener
        params_def = self.symbolTable.get_parameters(method_name)

        # verificar cantidad de parámetros
        if (len(params_def) != len(params_acc)):
            self.customErrors.append(f"{method_name} requiere {len(params_def)} pero se le dieron {len(params_acc)}")
            return "Error"

        # verificar tipo de parámetros 
        for par in range(len(params_def)):
            vis = self.visit(params_acc[par])
            
            if vis == "Error":
                return "Error"

            if (type(vis) == tuple):
                if (vis[0] != params_def[par][1]):
                    self.customErrors.append(f"En {method_name} el parámetro {params_def[par][0]} require ser {params_def[par][1]} pero se encontró {vis[0]}")
                    return "Error"

            else:
                if (vis != params_def[par][1]):
                    self.customErrors.append(f"En {method_name} el parámetro {params_def[par][0]} require ser {params_def[par][1]} pero se encontró {vis}")
                    return "Error"

        c = self.visitChildren(ctx)

        x = self.symbolTable.get_method2(method_name, self.current_class)

        return x[1]
    
    def visitDispatchAttribute(self, ctx: YAPLParser.DispatchAttributeContext):
        # print("\nDispatchAttribute")
        # print(ctx.getText())
        iz = ctx.expr().getText()
        der = ctx.ID()

        temp = self.current_class
        
        otra_clase = self.visit(ctx.expr())

        # print(iz," ", der, " -> ", otra_clase)

        # print("Clase izquierda ", otra_clase)

        # revisar que exista la variable
        if (not self.symbolTable.containsKey(str(der), addParent=otra_clase)):
            self.customErrors.append(f"{str(der)} no existe en {otra_clase}")
            return 'Error'
        
        row = self.symbolTable.get_cell(str(der), addParent=otra_clase)
        # print(row[1])
        return row[1]

    def visitIf(self, ctx: YAPLParser.IfContext):
        #print("visitIf")
        self.visitChildren(ctx)
        condition_expr = self.visit(ctx.expr(0))
        if condition_expr != 'Bool':
        # Handle the type mismatch error here
            self.customErrors.append("La condición dentro del if debe de retornar bool")
            return "Error"

        # return self.visitChildren(ctx)s
        return "Bool"
    
    def visitWhile(self, ctx: YAPLParser.WhileContext):
        #print("visitWhile")
        self.visitChildren(ctx)

        val = None
        condition_expr = self.visit(ctx.expr(0))

        if type(condition_expr) == tuple:
            condition_expr, val = condition_expr
            
        if condition_expr != 'Bool':
        # Handle the type mismatch error here
            self.customErrors.append(f"La condición dentro del while debe de retornar bool pero se encontró {condition_expr}")
            return "Error"

        return "Bool"
    
    def visitBlock(self, ctx: YAPLParser.BlockContext):
        #print("visitBlock")
        n = ctx.getChildCount()  # Get the number of child expressions in the block
        last_expr = None
        
        for i in range(n):
            child_expr_ctx = ctx.expr(i)
            if child_expr_ctx is not None:
                child_expr = self.visit(child_expr_ctx)
                last_expr = child_expr  # Keep track of the last expression's value
        
        return last_expr  # Return the value of the last expression
    
    def visitLetId(self, ctx: YAPLParser.LetIdContext):
        #print("visitLetId")
        for i in range(len(ctx.ID())):
            id = ctx.ID(i).getText()
            _type = ctx.TYPE(i).getText()
            space = get_space_vars(_type.lower())
            if self.current_class in self.class_methods:
                self.class_methods[self.current_class].append(id)
                self.symbolTable.add_column([id, _type, "Variable", None, self.current_class, self.current_function, None, None, "Local", space, None])
            else:
                self.symbolTable.add_column([id, _type, "Variable", None, self.current_class, self.current_function, None, None, "Global", space, None])
                self.class_methods[self.current_class] = [id]
            
            self.symbolTable.add_info_to_cell(self.current_class, "Contains", self.class_methods[self.current_class])

        self.visitChildren(ctx)
        return _type

    def visitNew(self, ctx: YAPLParser.NewContext):
        #print("visitNew")
        _type = ctx.TYPE().getText()
        if(_type == "SELF_TYPE"):
            return "Self"
        return _type
    
    def visitNegative(self, ctx: YAPLParser.NegativeContext):
        #print("visitNegative")
        expr_value = self.visit(ctx.expr())

        if(expr_value.lower() == "int"):
            return "Int"
        else:
            return "Error"

    def visitIsvoid(self, ctx: YAPLParser.IsvoidContext):
        expr_type = self.visit(ctx.expr())
        
        if expr_type == "Error":
            return "Error"

        # if expr_type == "Void":
        #     return "Bool", True
        # else:
        #     return "Bool", False
        
        return "Bool"
    
    def visitTimes(self, ctx: YAPLParser.TimesContext):
        #print("visitTimes")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"
        
        if left_type is not None and right_type is not None:
            if left_type.lower() == "int" and right_type.lower() == "int":
                return "Int"
            elif left_type.lower() == "bool" and right_type.lower() == "int":
                return "Bool"
            elif left_type.lower() == "int" and right_type.lower() == "bool":
                return "Bool"
            elif left_type.lower() == "bool" and right_type.lower() == "bool":
                return "Bool"
            else:
                self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en multiplicación")
                return "Error"
        
        return "Error"
    
    def visitDiv(self, ctx: YAPLParser.DivContext):
        #print("visitDiv")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"
        
        if left_type is not None and right_type is not None:
            if left_type.lower() == "int" and right_type.lower() == "int":
                return "Int"
            elif left_type.lower() == "bool" and right_type.lower() == "int":
                return "Bool"
            elif left_type.lower() == "int" and right_type.lower() == "bool":
                return "Bool"
            elif left_type.lower() == "bool" and right_type.lower() == "bool":
                return "Bool"
            else:
                self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en división")
                return "Error"
        else:
            return "Error"
    
    def visitPlus(self, ctx: YAPLParser.PlusContext):
        #print("visitPlus")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"
            
        if left_type is not None and right_type is not None:
            if left_type.lower() == "int" and right_type.lower() == "int":
                return "Int"
            elif left_type.lower() == "bool" and right_type.lower() == "int":
                return "Bool"
            elif left_type.lower() == "int" and right_type.lower() == "bool":
                return "Bool"
            elif left_type.lower() == "bool" and right_type.lower() == "bool":
                return "Bool"
            elif left_type.lower() == "string" and right_type.lower() == "string":
                return "string"
            else:
                self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en suma")
                return "Error"
        
        return "Error"
    
    def visitMinus(self, ctx: YAPLParser.MinusContext):
        #print("visitMinus")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if left_type is not None and right_type is not None:
            if left_type.lower() == "int" and right_type.lower() == "int":
                return "Int"
            elif left_type.lower() == "bool" and right_type.lower() == "int":
                return "Bool"
            elif left_type.lower() == "int" and right_type.lower() == "bool":
                return "Bool"
            elif left_type.lower() == "bool" and right_type.lower() == "bool":
                return "Bool"
            else:
                self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en resta")
                return "Error"
        else:
            return "Error"
    
    def visitLessThanOrEqual(self, ctx: YAPLParser.LessThanOrEqualContext):
        #print("visitLessThanOrEqual")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if (left_type.lower() == "int" and right_type.lower() == "int"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en operación <=")
            return "Error"
    
    def visitLessThan(self, ctx: YAPLParser.LessThanContext):
        #print("visitLessThan")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if (left_type.lower() == "int" and right_type.lower() == "int"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en operación <")
            return "Error"
    
    def visitGreaterThan(self, ctx: YAPLParser.GreaterThanContext):
        #print("visitGreaterThan")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if (left_type.lower() == "int" and right_type.lower() == "int"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en operación >")
            return "Error"
    
    def visitGreaterThanOrEqual(self, ctx: YAPLParser.GreaterThanOrEqualContext):
        #print("visitGreaterThanOrEqual")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if (left_type.lower() == "int" and right_type.lower() == "int"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en operación >=")
            return "Error"
    
    def visitEqual(self, ctx: YAPLParser.EqualContext):
        #print("visitEqual")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
 
        if(left_type == "Error" or right_type == "Error"):
            return "Error"
                    
        if (left_type.lower() == "int" and right_type.lower() == "int"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "string" and right_type.lower() == "string"):
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en operación =")
            return "Error"
    
    def visitAnd(self, ctx:YAPLParser.AndContext):
        #print("visitAnd")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if (left_type.lower() == "int" and right_type.lower() == "int"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en & lógico")
            return "Error"
    
    def visitOr(self, ctx:YAPLParser.OrContext):
        #print("visitOr")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
    
        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if (left_type.lower() == "int" and right_type.lower() == "int"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en | lógico")
            return "Error"
    
    def visitNeg(self, ctx:YAPLParser.NegContext):
        #print("visitNeg")
        expr_type = self.visit(ctx.expr())
        
        if (expr_type.lower() == "bool"):
            return "Bool"
        else:
            return "Error"
    
    def visitParens(self, ctx:YAPLParser.ParensContext):
        #print("visitParens")
        return self.visit(ctx.expr())
    
    def visitId(self, ctx:YAPLParser.IdContext):
        #print("visitId")
        id = ctx.ID().getText()
        row = self.symbolTable.get_cell(id)
        if id not in self.symbolTable.get_cell(self.current_class)[6]:

            clase = self.current_class
            if(id != 'self'):
                self.customErrors.append(f"El atributo '{id}' no ha sido declarado en la clase '{clase}'")
                return "Error"
        if row:
            return row[1]
        return "Error"
    
    def visitInt(self, ctx: YAPLParser.IntContext):
        #print("visitInt")
        # res = int(ctx.INT().getText())
        return "Int"
    
    def visitString(self, ctx: YAPLParser.StringContext):
        #print("visitString")
        # res = ctx.STRING().getText()
        return "String"
    
    def visitBoolean(self, ctx: YAPLParser.BooleanContext):
        #print("visitBoolean")
        # res = None
        # if(ctx.getText().capitalize() == "False"):
        #     res = False
        # elif(ctx.getText().capitalize() == "True"):
        #     res = True
        return "Bool"
    
    def visitSelf(self, ctx: YAPLParser.SelfContext):
        
        cl = self.symbolTable.get_cell(self.current_class)
        fun = self.symbolTable.get_cell(self.current_function)
        
        if(cl):
            if(cl[1]):
                return cl[1]
            elif(fun):
                if(fun[1]):
                    return fun[1]
        elif(fun):
            if(fun[1]):
                return fun[1]
        else:
            return "Self"

def main():
    file_name = "./tests/arith.cl"
    # file_name = "./tests/arith.cl"
    input_stream = FileStream(file_name)
    lexer = YAPLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = YAPLParser(token_stream)
    tree = parser.prog()
    YV = YAPLVisitorImpl()
    
    try:
        res = YV.visit(tree)
        if(str(res) == "Error" or len(YV.customErrors) > 0):
            print("----------------------------------")
            print("  Errores semánticos encontrados")
            print("----------------------------------\n")
            clean_errors(YV.customErrors)
            print()
        else:
            print("\nResultado Lectura: Todo está semánticamente correcto\n")
            
    except TypeError as e:
        print(e);
    treeF = YV.symbolTable.build_Table()
    #print(treeF)
    with open("SymbolTable.txt", "w", encoding="utf-8") as f:
        f.write(treeF.get_string())
    
if __name__ == "__main__":
    main()