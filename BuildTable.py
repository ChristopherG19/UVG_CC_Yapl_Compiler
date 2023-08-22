'''
    Universidad del Valle de Guatemala
    Construcción de Compiladores
    Christopher García 20541
    Ma. Isabel Solano 20504
    Laboratorio#1
'''

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
         
    def visitAssignment(self, ctx: YAPLParser.AssignmentContext):
        id = ctx.ID()
        type_id = self.visit(ctx.expr())
        parent_class = ctx.parentCtx.TYPE(0).getText() if ctx.parentCtx.TYPE(0) else None
        space = get_space_vars(type_id.lower())
        if parent_class in self.class_methods:
            self.class_methods[parent_class].append(id)
            self.symbolTable.add_column([id, type_id, None, parent_class, None, None, "Local", None])
        else:
            self.class_methods[parent_class] = [id]
            
        self.symbolTable.add_info_to_cell(parent_class, "Contains", self.class_methods[parent_class])
        return type_id
    
    def visitDefClass(self, ctx: YAPLParser.DefClassContext):
        class_id = ctx.TYPE(0).getText()
        type_class_id = ctx.CLASS_N().__str__()
        if ctx.INHERITS():
            inherits = ctx.TYPE(1).getText()
            self.symbolTable.add_column([class_id, type_class_id, inherits, None, None, None, "Global", None])
        else:
            self.symbolTable.add_column([class_id, type_class_id, None, None, None, None, "Global", None])
        
        self.class_methods[class_id] = []
        
        return super().visitDefClass(ctx)
    
    def visitId(self, ctx: YAPLParser.IdContext):
        id = ctx.ID().getText()
        row = self.symbolTable.get_cell(id)
        if row:
            return row[1]
        return None
    
    def visitDefFunc(self, ctx: YAPLParser.DefFuncContext):
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        parent_class = ctx.parentCtx.TYPE(0).getText() if ctx.parentCtx.TYPE(0) else None
        formal_parameters = ctx.formal()
        if formal_parameters:
            for formal_param in formal_parameters:
                param_name = formal_param.ID().getText()
                param_type = formal_param.TYPE().getText()
                space = get_space_vars(param_type.lower())
                self.symbolTable.add_column([param_name, param_type, None, parent_class, None, None, "Parameter", space])
                if parent_class in self.class_methods:
                    self.class_methods[parent_class].append(param_name)
                else:
                    self.class_methods[parent_class] = [param_name]
                
        if parent_class in self.class_methods:
            self.class_methods[parent_class].append(id)
            self.symbolTable.add_column([id, type_id, None, parent_class, None, None, "Local", None])
        else:
            self.class_methods[parent_class] = [id]
            
        self.symbolTable.add_info_to_cell(parent_class, "Contains", self.class_methods[parent_class])
        
        return type_id
    
    def visitLetId(self, ctx: YAPLParser.LetIdContext):
        print("aaaaa")
        return super().visitLetId(ctx)
    
    def visitDefAssign(self, ctx: YAPLParser.DefAssignContext):
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        space = get_space_vars(type_id.lower())
        parent_class = ctx.parentCtx.TYPE(0).getText() if ctx.parentCtx.TYPE(0) else None
        if parent_class in self.class_methods:
            self.class_methods[parent_class].append(id)
            self.symbolTable.add_column([id, type_id, None, parent_class, None, None, "Local", space])
        else:
            self.class_methods[parent_class] = [id]
            
        self.symbolTable.add_info_to_cell(parent_class, "Contains", self.class_methods[parent_class])
        return type_id
    
    def visitFeature(self, ctx: YAPLParser.FeatureContext):
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        self.symbolTable.add_column([id, type_id, None, None, None, None, None, None])
        return type_id

    def visitTimes(self, ctx:YAPLParser.TimesContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'int'
        else:
            raise TypeError("Incongruencia de tipos en multiplicación")

    def visitDiv(self, ctx:YAPLParser.DivContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'int'
        else:
            raise TypeError("Incongruencia de tipos en división")
    
    def visitMinus(self, ctx: YAPLParser.MinusContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'int'
        else:
            raise TypeError("Incongruencia de tipos en resta")

    def visitPlus(self, ctx:YAPLParser.PlusContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'int'
        elif left_type.lower() == 'char' and right_type.lower() == 'char':
            return 'char'
        elif left_type.lower() == 'string' and right_type.lower() == 'string':
            return 'string'
        else:
            raise TypeError("Incongruencia de tipos en suma")
    
    def visitAnd(self, ctx: YAPLParser.AndContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'bool' and right_type.lower() == 'bool':
            return 'bool'
        else:
            raise TypeError("Incongruencia de tipos en AND")

    def visitOr(self, ctx: YAPLParser.OrContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'bool' and right_type.lower() == 'bool':
            return 'bool'
        else:
            raise TypeError("Incongruencia de tipos en OR")
    
    def visitEqual(self, ctx:YAPLParser.EqualContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == right_type.lower():
            return 'bool'
        else:
            raise TypeError("Type mismatch in equal operation")
    
    def visitGreaterThanOrEqual(self, ctx:YAPLParser.GreaterThanOrEqualContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'bool'
        else:
            raise TypeError("Incongruencia de tipos en mayor o igual que")
    
    def visitLessThanOrEqual(self, ctx:YAPLParser.LessThanOrEqualContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'bool'
        else:
            raise TypeError("Incongruencia de tipos en menor o igual que")
    
    def visitLessThan(self, ctx:YAPLParser.LessThanContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'bool'
        else:
            raise TypeError("Incongruencia de tipos en menor que")
    
    def visitGreaterThan(self, ctx:YAPLParser.GreaterThanContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'bool'
        else:
            raise TypeError("Incongruencia de tipos en mayor que")
    
    def visitParens(self, ctx: YAPLParser.ParensContext):
        return self.visit(ctx.expr())
    
    def visitInt(self, ctx: YAPLParser.IntContext):
        return 'int'
    
    def visitString(self, ctx: YAPLParser.StringContext):
        return 'string'
    
    def visitBoolean(self, ctx:YAPLParser.BooleanContext):
        return 'bool'

def main():
    file_name = './tests/exampleUser.expr'
    input_stream = FileStream(file_name)
    lexer = YAPLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = YAPLParser(token_stream)
    tree = parser.prog()
    YV = YAPLVisitorImpl()
    
    try:
        YV.visit(tree)
    except TypeError as e:
        print(e);
    treeF = YV.symbolTable.build_Table()
    #print(treeF)
    with open("SymbolTable.txt", 'w', encoding="utf-8") as f:
        f.write(treeF.get_string())
    
if __name__ == '__main__':
    main()