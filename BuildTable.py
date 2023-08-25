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
        print("Start")
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
        print("defClass")
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
        print("visitDefFunc")
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
        return type_id_b
    
    def visitDefAssign(self, ctx: YAPLParser.DefAssignContext):
        print("visitDefAssign")
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        space = get_space_vars(type_id.lower())
        parent_class = ctx.parentCtx.TYPE(0).getText() if ctx.parentCtx.TYPE(0) else None
        self.current_class = parent_class
        
        val = None
        if(ctx.expr()):
            result = self.visit(ctx.expr())
            if isinstance(result, tuple):
                type_id, val = result
            else:
                type_id = result
            
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
        print("visitFormalAssign")
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText() 
        return type_id
        
    def visitAssignment(self, ctx: YAPLParser.AssignmentContext):
        print("visitAssignment")
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
        return type_id
    
    def visitDispatchExplicit(self, ctx: YAPLParser.DispatchExplicitContext):
        print("visitDispatchExplicit")
        obj_expr_type = self.visit(ctx.expr(0))
        method_name = ctx.ID().getText()
        print(obj_expr_type, method_name)
        print("Ex-------------\n")

        return self.visitChildren(ctx)
    
    def visitDispatchImplicit(self, ctx: YAPLParser.DispatchImplicitContext):
        print("visitDispatchImplicit")
        method_name = ctx.ID().getText()
        
        if self.current_class:
            row = self.symbolTable.get_cell(self.current_class)
            if row:
                contains = row[self.symbolTable.headers.index("Contains")]
                add_to_parent = self.symbolTable.get_cell(method_name)
                if add_to_parent:
                    self.symbolTable.add_info_to_cell(self.current_function, "Contains", [method_name])
                    self.symbolTable.add_info_to_cell(method_name, "Parent_Fun", self.current_function)
                
                if method_name in contains:
                    method_row = self.symbolTable.get_cell(method_name, addType="Method", addParent=self.current_class)
                    if method_row:
                        print("aaaaaaa", method_row[1])
                    
        return self.visitChildren(ctx)

    def visitIf(self, ctx: YAPLParser.IfContext):
        print("visitIf")
        return self.visitChildren(ctx)
    
    def visitWhile(self, ctx: YAPLParser.WhileContext):
        print("visitWhile")
        return self.visitChildren(ctx)
    
    def visitBlock(self, ctx: YAPLParser.BlockContext):
        print("visitBlock")
        result_type = None
        for expr_ctx in ctx.expr():
            result_type = self.visit(expr_ctx)
        return result_type
    
    def visitLetId(self, ctx: YAPLParser.LetIdContext):
        print("visitLetId")
        for i in range(len(ctx.ID())):
            id = ctx.ID(i).getText()
            _type = ctx.TYPE(i).getText()
            space = get_space_vars(_type.lower())
            if self.current_class in self.class_methods:
                self.class_methods[self.current_class].append(id)
                self.symbolTable.add_column([id, _type, None, "Variable", None, self.current_class, self.current_function, None, "Local", space, None])
            else:
                self.symbolTable.add_column([id, _type, None, "Variable", None, self.current_class, self.current_function, None, "Global", space, None])
                self.class_methods[self.current_class] = [id]
            
            self.symbolTable.add_info_to_cell(self.current_class, "Contains", self.class_methods[self.current_class])
        
        return self.visitChildren(ctx)
    
    def visitNew(self, ctx: YAPLParser.NewContext):
        print("visitNew")
        _type = ctx.TYPE().getText()
        return _type
    
    def visitNegative(self, ctx: YAPLParser.NegativeContext):
        print("visitNegative")
        return self.visitChildren(ctx)
    
    def visitIsvoid(self, ctx: YAPLParser.IsvoidContext):
        print("visitIsvoid")
        expr_type = self.visit(ctx.expr())

        if expr_type:
            return "Bool"
        return "Error"
    
    def visitTimes(self, ctx: YAPLParser.TimesContext):
        print("visitTimes")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
            
        if left_type is not None and right_type is not None:
            if left_type.lower() == "int" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    res = left_val * right_val
                    return "bool", not (res == 0)
                return "int"
            elif left_type.lower() == "bool" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    res = self.symbolTable.get_cell(left_val, "Bool")[-1] * right_val
                    return "int", not (res == 0)
                return "int"
            elif left_type.lower() == "int" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    res = left_val * self.symbolTable.get_cell(right_val, "Bool")[-1]
                    return "int", not (res == 0)
                return "int"
            elif left_type.lower() == "bool" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    res = self.symbolTable.get_cell(left_val, "Bool")[-1] * self.symbolTable.get_cell(right_val, "Bool")[-1]
                    return "int", not (res == 0)
                return "int"
        
        return "Error"
    
    def visitDiv(self, ctx: YAPLParser.DivContext):
        print("visitDiv")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
        
        if left_type is not None and right_type is not None:
            if left_type.lower() == "int" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    if(right_val != 0):
                        res = left_val / right_val
                        if(res % 1 != 0):
                            # Agregar error por decimales
                            return "Error"
                        return "bool", not (res == 0)
                    else:
                        # Agregar error de división por 0
                        return "Error"
                return "int"
            elif left_type.lower() == "bool" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    if(right_val != 0):
                        res = self.symbolTable.get_cell(left_val, "Bool")[-1] / right_val
                        if(res % 1 != 0):
                            # Agregar error por decimales
                            return "Error"
                        return "int", not (int(res) == 0)
                    else:
                        return "Error"
                return "int"
            elif left_type.lower() == "int" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    if(right_val != False):
                        res = left_val / self.symbolTable.get_cell(right_val, "Bool")[-1]
                        if(res % 1 != 0):
                            # Agregar error por decimales
                            return "Error"
                        return "int", not (int(res) == 0)
                    else:
                        return "Error"
                return "int"
            elif left_type.lower() == "bool" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    if(right_val != False):
                        res = self.symbolTable.get_cell(left_val, "Bool")[-1] / self.symbolTable.get_cell(right_val, "Bool")[-1]
                        if(res % 1 != 0):
                            # Agregar error por decimales
                            return "Error"
                        return "int", not (int(res) == 0)
                    else:
                        return "Error"
                return "int"
        else:
            return "Error"
    
    def visitPlus(self, ctx: YAPLParser.PlusContext):
        print("visitPlus")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
        
        if left_type is not None and right_type is not None:
            if left_type.lower() == "int" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    res = left_val + right_val
                    return "bool", not (res == 0)
                return "int"
            elif left_type.lower() == "bool" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    res = self.symbolTable.get_cell(left_val, "Bool")[-1] + right_val
                    return "int", not (res == 0)
                return "int"
            elif left_type.lower() == "int" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    res = left_val + self.symbolTable.get_cell(right_val, "Bool")[-1]
                    return "int", not (res == 0)
                return "int"
            elif left_type.lower() == "bool" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    res = self.symbolTable.get_cell(left_val, "Bool")[-1] + self.symbolTable.get_cell(right_val, "Bool")[-1]
                    return "int", not (res == 0)
                return "int"
            elif left_type.lower() == "string" and right_type.lower() == "string":
                return "string"
        
        return "Error"
    
    def visitMinus(self, ctx: YAPLParser.MinusContext):
        print("visitMinus")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type

        if left_type is not None and right_type is not None:
            if left_type.lower() == "int" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    res = left_val - right_val
                    return "bool", not (res == 0)
                return "int"
            elif left_type.lower() == "bool" and right_type.lower() == "int":
                if(left_val != None and right_val != None):
                    res = self.symbolTable.get_cell(left_val, "Bool")[-1] - right_val
                    return "int", not (res == 0)
                return "int"
            elif left_type.lower() == "int" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    res = left_val - self.symbolTable.get_cell(right_val, "Bool")[-1]
                    return "int", not (res == 0)
                return "int"
            elif left_type.lower() == "bool" and right_type.lower() == "bool":
                if(left_val != None and right_val != None):
                    res = self.symbolTable.get_cell(left_val, "Bool")[-1] - self.symbolTable.get_cell(right_val, "Bool")[-1]
                    return "int", not (res == 0)
                return "int"
        else:
            return "Error"
    
    def visitLessThanOrEqual(self, ctx: YAPLParser.LessThanOrEqualContext):
        print("visitLessThanOrEqual")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type

        if (left_type.lower() == 'int' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", left_val <= right_val
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", self.symbolTable.get_cell(left_val, "Bool")[-1] <= self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "bool"
        elif (left_type.lower() == 'int' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", left_val <= self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", self.symbolTable.get_cell(left_val, "Bool")[-1] <= right_val
            return "bool"
        else:
            return "Error"
    
    def visitLessThan(self, ctx: YAPLParser.LessThanContext):
        print("visitLessThan")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type

        if (left_type.lower() == 'int' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", left_val < right_val
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", self.symbolTable.get_cell(left_val, "Bool")[-1] < self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "bool"
        elif (left_type.lower() == 'int' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", left_val < self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", self.symbolTable.get_cell(left_val, "Bool")[-1] < right_val
            return "bool"
        else:
            return "Error"
    
    def visitGreaterThan(self, ctx: YAPLParser.GreaterThanContext):
        print("visitGreaterThan")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type

        if (left_type.lower() == 'int' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", left_val > right_val
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", self.symbolTable.get_cell(left_val, "Bool")[-1] > self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "bool"
        elif (left_type.lower() == 'int' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", left_val > self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", self.symbolTable.get_cell(left_val, "Bool")[-1] > right_val
            return "bool"
        else:
            return "Error"
    
    def visitGreaterThanOrEqual(self, ctx: YAPLParser.GreaterThanOrEqualContext):
        print("visitGreaterThanOrEqual")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type

        if (left_type.lower() == 'int' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", left_val >= right_val
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", self.symbolTable.get_cell(left_val, "Bool")[-1] >= self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "bool"
        elif (left_type.lower() == 'int' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", left_val >= self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", self.symbolTable.get_cell(left_val, "Bool")[-1] >= right_val
            return "bool"
        else:
            return "Error"
    
    def visitEqual(self, ctx: YAPLParser.EqualContext):
        print("visitEqual")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type
                    
        if (left_type.lower() == 'int' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", left_val == right_val
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", left_val == right_val
            return "bool"
        elif (left_type.lower() == 'string' and right_type.lower() == 'string'):
            if (left_val != None and right_val != None):
                return "bool", left_val == right_val
            return "bool"
        elif (left_type.lower() == 'int' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", left_val == self.symbolTable.get_cell(right_val, "Bool")[-1]
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", self.symbolTable.get_cell(left_val, "Bool")[-1] == right_val
            return "bool"
        else:
            return "Error"
    
    def visitAnd(self, ctx:YAPLParser.AndContext):
        print("visitAnd")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type

        if (left_type.lower() == 'int' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", not (left_val == 0) and not(right_val == 0)
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", left_val and right_val
            return "bool"
        elif (left_type.lower() == 'int' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", not(left_val == 0) and not(self.symbolTable.get_cell(right_val, "Bool")[-1] == 0)
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", not(self.symbolTable.get_cell(left_val, "Bool")[-1] == 0) and not(right_val == 0)
            return "bool"
        else:
            return "Error"
    
    def visitOr(self, ctx:YAPLParser.OrContext):
        print("visitOr")
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        left_val = None
        right_val = None

        if isinstance(left_type, tuple):
            left_type, left_val = left_type

        if isinstance(right_type, tuple):
            right_type, right_val = right_type

        if (left_type.lower() == 'int' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", not (left_val == 0) or not(right_val == 0)
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", left_val or right_val
            return "bool"
        elif (left_type.lower() == 'int' and right_type.lower() == 'bool'):
            if (left_val != None and right_val != None):
                return "bool", not(left_val == 0) or not(self.symbolTable.get_cell(right_val, "Bool")[-1] == 0)
            return "bool"
        elif (left_type.lower() == 'bool' and right_type.lower() == 'int'):
            if (left_val != None and right_val != None):
                return "bool", not(self.symbolTable.get_cell(left_val, "Bool")[-1] == 0) or not(right_val == 0)
            return "bool"
        else:
            return "Error"
    
    def visitNeg(self, ctx:YAPLParser.NegContext):
        print("visitNeg")
        return self.visitChildren(ctx)
    
    def visitParens(self, ctx:YAPLParser.ParensContext):
        print("visitParens")
        return self.visit(ctx.expr())
    
    def visitId(self, ctx:YAPLParser.IdContext):
        print("visitId")
        id = ctx.ID().getText()
        row = self.symbolTable.get_cell(id)
        if not self.symbolTable.is_attribute_declared(id, self.current_class):
            clase = self.current_class
            self.customErrors.append(f"El atributo '{id}' no ha sido declarado en la clase '{clase}'")
            return "Error"
        if row:
            return row[1]
        return "Error"
    
    def visitInt(self, ctx: YAPLParser.IntContext):
        print("visitInt")
        return "Int", int(ctx.INT().getText())
    
    def visitString(self, ctx: YAPLParser.StringContext):
        print("visitString")
        return "String", ctx.STRING().getText()
    
    def visitBoolean(self, ctx: YAPLParser.BooleanContext):
        print("visitBoolean")
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