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
from utils.utils import get_space_vars

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
        self.symbolTable.add_column(["Bool", "Bool", "Declaration", None, "Bool", None, None, None, "Global", 8, False])
        self.symbolTable.add_column([False, "Bool", "Declaration", None, "Bool", None, None, None, "Global", 8, 0])
        self.symbolTable.add_column([True, "Bool", "Declaration", None, "Bool", None, None, None, "Global", 8, 1])
        self.symbolTable.add_column(["String", "String", "Declaration", None, "String", None, None, None, "Global", 8, ""])
        self.symbolTable.add_column(["abort", "Object", "Declaration", None, "Object", None, None, None, "Global", 8, "Error"])
        self.symbolTable.add_column(["type_name", "String", "Declaration", None, "Object", None, None, None, "Global", 8, None])
        self.symbolTable.add_column(["copy", "SELF_TYPE", "Declaration", None, "Object", None, None, None, "Global", 8, None])
        
    def add_special_class_IO(self):
        self.symbolTable.add_column(["out_string", "SELF_TYPE", "Method", None, "IO", None, None, None, "Global", None, None])
        self.symbolTable.add_column(["out_int", "SELF_TYPE", "Method", None, "IO", None, None, None, "Global", None, None])
        self.symbolTable.add_column(["in_string", "String", "Method", None, "IO", None, None, None, "Global", None, None])
        self.symbolTable.add_column(["int_int", "Int", "Method", None, "IO", None, None, None, "Global", None, None])
        self.symbolTable.add_column(["lenght", "String", "Method", None, "String", None, None, None, "Global", None, None])
        self.symbolTable.add_column(["concat", "String", "Method", None, "String", None, None, None, "Global", None, None])
        self.symbolTable.add_column(["substr", "String", "Method", None, "String", None, None, None, "Global", None, None])
        
    # Visit a parse tree produced by YAPLParser#start.
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
        #print("defClass")
        id = ctx.TYPE(0).getText()
        type_id = ctx.CLASS_N().__str__()
        self.current_class = id
        if ctx.INHERITS():
            inherits = ctx.TYPE(1).getText()
            if(inherits.lower() in ["string", "int", "bool"]):
                self.customErrors.append(f"Clase Main no puede heredar de esta clase ({inherits})")
                return "Error"
            else:
                if(inherits == "IO"):
                    self.add_special_class_IO()
                self.symbolTable.add_column([id, None, "Class", inherits, self.current_class, self.current_function, None, None, "Global", None, None])
        else:
            self.symbolTable.add_column([id, None, "Class", None, self.current_class, self.current_function, None, None, "Global", None, None])
        
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
        
        cant_ch = ctx.getChildCount()
        # last_child = self.visit(ctx.expr()) 
        
        type_ = self.visit(ctx.getChild(cant_ch-2))
        # if type_ is not None:

        if type_ == "Error":
            return "Error"
        
        return type_
    
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
            result = self.visit(ctx.expr())
            
            if isinstance(result, tuple):
                type_id_res, val = result
            else:
                type_id_res = result
                
            if(type_id_res == "Error"):
                return "Error"
                
            if(type_id != type_id_res):
                if not ((type_id == 'Int' and type_id_res == 'Bool') or (type_id == 'Bool' and type_id_res == 'Int')):
                    self.customErrors.append(f"Mismatch entre tipos de datos en asignacion ({id}: {type_id} <- {type_id_res})")
                    return "Error"
            
            if(val == True):
                val = 1
            elif(val == False):
                val = 0
            
        else:
            if (self.symbolTable.get_cell(type_id, "Declaration") != None):
                val = self.symbolTable.get_cell(type_id, "Declaration")[-1]
        
        if parent_class in self.class_methods:
            self.class_methods[parent_class].append(id)
            self.symbolTable.add_column([id, type_id, "Instance", None, parent_class, self.current_function, None, None, "Local", space, val])
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
        
        if (not self.symbolTable.containsKey(id)): 
            self.customErrors.append(f"{id} no está definido")
            return "Error"
        
        id_type =  self.symbolTable.get_cell(id)[1]
        
        
        if (id not in self.symbolTable.get_cell(self.current_class)[6]):
            self.customErrors.append(f"{id} no definido dentro de {self.current_class}")
            return "Error"
        
        if isinstance(result, tuple):
            type_id, val = result
        else:
            type_id = result
            val = None
         
        if(self.symbolTable.containsKey(id)):
            if(val != None):
                self.symbolTable.add_info_to_cell(id, "Value", val)
        return type_id
    
    def visitDispatchExplicit(self, ctx: YAPLParser.DispatchExplicitContext):
        #print("visitDispatchExplicit")
        obj_expr_type = self.visit(ctx.expr(0))
        method_name = ctx.ID().getText()

        return self.visitChildren(ctx)
    
    def visitDispatchImplicit(self, ctx: YAPLParser.DispatchImplicitContext):
        #print("visitDispatchImplicit")
        return self.visitChildren(ctx)

    def visitIf(self, ctx: YAPLParser.IfContext):
        #print("visitIf")
        self.visitChildren(ctx)
        condition_expr = self.visit(ctx.expr(0))
        if condition_expr != 'Bool':
        # Handle the type mismatch error here
            self.customErrors.append("La condición dentro del if debe de retornar bool")
            return "Error"

        # return self.visitChildren(ctx)s
        return None
    
    def visitWhile(self, ctx: YAPLParser.WhileContext):
        #print("visitWhile")
        self.visitChildren(ctx)

        condition_expr = self.visit(ctx.expr(0))

        if (type(condition_expr) == tuple):
            if condition_expr[0] == 'Int':
                self.customErrors.append(f"La condición dentro del while debe de retornar bool pero se encontró {condition_expr[0]}")
                return "Error"

            if condition_expr[0] != 'Bool':
                self.customErrors.append(f"La condición dentro del while debe de retornar bool pero se encontró {condition_expr[0]}")
                return "Error"

        if condition_expr != 'Bool':
        # Handle the type mismatch error here
            self.customErrors.append(f"La condición dentro del while debe de retornar bool pero se encontró {condition_expr}")
            return "Error"

        return None
    
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
                self.symbolTable.add_column([id, _type, "Variable", None, None, self.current_class, self.current_function, None, "Local", space, None])
            else:
                self.symbolTable.add_column([id, _type, "Variable", None, None, self.current_class, self.current_function, None, "Global", space, None])
                self.class_methods[self.current_class] = [id]
            
            self.symbolTable.add_info_to_cell(self.current_class, "Contains", self.class_methods[self.current_class])
        
        return self.visitChildren(ctx)
    
    def visitNew(self, ctx: YAPLParser.NewContext):
        #print("visitNew")
        _type = ctx.TYPE().getText()
        return _type
    
    def visitNegative(self, ctx: YAPLParser.NegativeContext):
        #print("visitNegative")
        expr_value = self.visit(ctx.expr())
        expr_val = None
        
        if isinstance(expr_value, tuple):
            expr_value, expr_val = expr_value

        if(expr_value.lower() == "int" and expr_val != None):
            return "Int", -expr_val
        else:
            return "Error"
    
    def visitIsvoid(self, ctx: YAPLParser.IsvoidContext):
        expr_type = self.visit(ctx.expr())

        if expr_type:
            return "Bool"
        return "Error"
    
    def visitTimes(self, ctx: YAPLParser.TimesContext):
        #print("visitTimes")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"
        
        if left_type is not None and right_type is not None:
            if left_type.lower() == "int" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    res = left_val * right_val
                    return "Int", res
                return "Int"
            elif left_type.lower() == "bool" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    res = self.symbolTable.get_cell(left_val, "Bool")[-1] * right_val
                    return "Bool", not (res == 0)
                return "Int"
            elif left_type.lower() == "int" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    res = left_val * self.symbolTable.get_cell(right_val, "Bool")[-1]
                    return "Bool", not (res == 0)
                return "Int"
            elif left_type.lower() == "bool" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    res = self.symbolTable.get_cell(left_val, "Bool")[-1] * self.symbolTable.get_cell(right_val, "Bool")[-1]
                    return "Bool", not (res == 0)
                return "Int"
            else:
                self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en multiplicación")
                return "Error"
        
        return "Error"
    
    def visitDiv(self, ctx: YAPLParser.DivContext):
        #print("visitDiv")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"
        
        if left_type is not None and right_type is not None:
            if left_type.lower() == "int" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    if(right_val != 0):
                        res = left_val / right_val
                        if(res % 1 != 0):
                            self.customErrors.append(f"Tipo float no permitido; Valor de: {left_val}/{right_val} = {res:.2f}")
                            return "Error"
                        return "Int", int(res)
                    else:
                        return "Int", 0
                return "Int"
            elif left_type.lower() == "bool" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    if(right_val != 0):
                        res = self.symbolTable.get_cell(left_val, "Bool")[-1] / right_val
                        if(res % 1 != 0):
                            self.customErrors.append(f"Tipo float no permitido; Valor de: {left_val}/{right_val} = {res:.2f}")
                            return "Error"
                        return "Bool", not (int(res) == 0)
                    else:
                        return "Int", 0
                return "Int"
            elif left_type.lower() == "int" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    if(right_val != False):
                        res = left_val / self.symbolTable.get_cell(right_val, "Bool")[-1]
                        if(res % 1 != 0):
                            self.customErrors.append(f"Tipo float no permitido; Valor de: {left_val}/{right_val} = {res:.2f}")
                            return "Error"
                        return "Bool", not (int(res) == 0)
                    else:
                        return "Int", 0
                return "Int"
            elif left_type.lower() == "bool" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    if(right_val != False):
                        res = self.symbolTable.get_cell(left_val, "Bool")[-1] / self.symbolTable.get_cell(right_val, "Bool")[-1]
                        if(res % 1 != 0):
                            self.customErrors.append(f"Tipo float no permitido; Valor de: {left_val}/{right_val} = {res:.2f}")
                            return "Error"
                        return "Bool", not (int(res) == 0)
                    else:
                        return "Int", 0
                return "Int"
            else:
                self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en división")
                return "Error"
        else:
            return "Error"
    
    def visitPlus(self, ctx: YAPLParser.PlusContext):
        #print("visitPlus")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None
        
        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"
            
        if left_type is not None and right_type is not None:
            if left_type.lower() == "int" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    res = left_val + right_val
                    return "Int", res
                return "Int"
            elif left_type.lower() == "bool" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    res = self.symbolTable.get_cell(left_val, "Bool")[-1] + right_val
                    return "Bool", not (res == 0)
                return "Int"
            elif left_type.lower() == "int" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    res = left_val + self.symbolTable.get_cell(right_val, "Bool")[-1]
                    return "Bool", not (res == 0)
                return "Int"
            elif left_type.lower() == "bool" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    res = self.symbolTable.get_cell(left_val, "Bool")[-1] + self.symbolTable.get_cell(right_val, "Bool")[-1]
                    return "Bool", not (res == 0)
                return "Int"
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
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if left_type is not None and right_type is not None:
            if left_type.lower() == "int" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    res = left_val - right_val
                    return "Int", res
                return "Int"
            elif left_type.lower() == "bool" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    res = self.symbolTable.get_cell(left_val, "Bool")[-1] - right_val
                    return "Bool", not (res == 0)
                return "Int"
            elif left_type.lower() == "int" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    res = left_val - self.symbolTable.get_cell(right_val, "Bool")[-1]
                    return "Bool", not (res == 0)
                return "Int"
            elif left_type.lower() == "bool" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    res = self.symbolTable.get_cell(left_val, "Bool")[-1] - self.symbolTable.get_cell(right_val, "Bool")[-1]
                    return "Bool", not (res == 0)
                return "Int"
            else:
                self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en resta")
                return "Error"
        else:
            return "Error"
    
    def visitLessThanOrEqual(self, ctx: YAPLParser.LessThanOrEqualContext):
        #print("visitLessThanOrEqual")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if (left_type.lower() == "int" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", left_val <= right_val
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", self.symbolTable.get_cell(left_val, "Bool")[-1] <= self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", left_val <= self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", self.symbolTable.get_cell(left_val, "Bool")[-1] <= right_val
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en operación <=")
            return "Error"
    
    def visitLessThan(self, ctx: YAPLParser.LessThanContext):
        #print("visitLessThan")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if (left_type.lower() == "int" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", left_val < right_val
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", self.symbolTable.get_cell(left_val, "Bool")[-1] < self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", left_val < self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", self.symbolTable.get_cell(left_val, "Bool")[-1] < right_val
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en operación <")
            return "Error"
    
    def visitGreaterThan(self, ctx: YAPLParser.GreaterThanContext):
        #print("visitGreaterThan")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if (left_type.lower() == "int" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", left_val > right_val
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", self.symbolTable.get_cell(left_val, "Bool")[-1] > self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", left_val > self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", self.symbolTable.get_cell(left_val, "Bool")[-1] > right_val
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en operación >")
            return "Error"
    
    def visitGreaterThanOrEqual(self, ctx: YAPLParser.GreaterThanOrEqualContext):
        #print("visitGreaterThanOrEqual")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if (left_type.lower() == "int" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", left_val >= right_val
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", self.symbolTable.get_cell(left_val, "Bool")[-1] >= self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", left_val >= self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", self.symbolTable.get_cell(left_val, "Bool")[-1] >= right_val
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en operación >=")
            return "Error"
    
    def visitEqual(self, ctx: YAPLParser.EqualContext):
        #print("visitEqual")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"
                    
        if (left_type.lower() == "int" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", left_val == right_val
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", left_val == right_val
            return "Bool"
        elif (left_type.lower() == "string" and right_type.lower() == "string"):
            if (left_val != None and right_val != None):
                return "Bool", left_val == right_val
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", left_val == self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", self.symbolTable.get_cell(left_val, "Bool")[-1] == right_val
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en operación =")
            return "Error"
    
    def visitAnd(self, ctx:YAPLParser.AndContext):
        #print("visitAnd")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if (left_type.lower() == "int" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", not (left_val == 0) and not(right_val == 0)
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", left_val and right_val
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", not(left_val == 0) and not(self.symbolTable.get_cell(right_val, "Bool")[-1] == 0)
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", not(self.symbolTable.get_cell(left_val, "Bool")[-1] == 0) and not(right_val == 0)
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en & lógico")
            return "Error"
    
    def visitOr(self, ctx:YAPLParser.OrContext):
        #print("visitOr")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
            
        if(left_type == "Error" or right_type == "Error"):
            return "Error"

        if (left_type.lower() == "int" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", not (left_val == 0) or not(right_val == 0)
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", left_val or right_val
            return "Bool"
        elif (left_type.lower() == "int" and right_type.lower() == "bool"):
            if (left_val != None and right_val != None):
                return "Bool", not(left_val == 0) or not(self.symbolTable.get_cell(right_val, "Bool")[-1] == 0)
            return "Bool"
        elif (left_type.lower() == "bool" and right_type.lower() == "int"):
            if (left_val != None and right_val != None):
                return "Bool", not(self.symbolTable.get_cell(left_val, "Bool")[-1] == 0) or not(right_val == 0)
            return "Bool"
        else:
            self.customErrors.append(f"Incongruencia de tipos {left_type} y {right_type} en | lógico")
            return "Error"
    
    def visitNeg(self, ctx:YAPLParser.NegContext):
        #print("visitNeg")
        expr_type = self.visit(ctx.expr())
        expr_val = None
        
        if isinstance(expr_type, tuple):
            expr_type, expr_val = expr_type
            
        if (expr_type.lower() == "bool" and expr_val != None):
            return "Bool", not expr_val
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
        return "Int", int(ctx.INT().getText())
    
    def visitString(self, ctx: YAPLParser.StringContext):
        #print("visitString")
        return "String", ctx.STRING().getText()
    
    def visitBoolean(self, ctx: YAPLParser.BooleanContext):
        #print("visitBoolean")
        res = None
        if(ctx.getText().capitalize() == "False"):
            res = False
        elif(ctx.getText().capitalize() == "True"):
            res = True
        return "Bool", res

def main():
    file_name = "./tests/hello_world.cl"
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
            for err in YV.customErrors:
                print("->",err)
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