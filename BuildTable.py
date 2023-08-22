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
        self.current_class = None
        
    # Visit a parse tree produced by YAPLParser#start.
    def visitStart(self, ctx:YAPLParser.StartContext):
        final_type = None
        stages = ctx.class_def()
        for stage in stages:
            stage_type = self.visit(stage)
            if stage_type != "Error":
                final_type = stage_type
            else:
                return "Error"
        return final_type
    
    def visitDefClass(self, ctx: YAPLParser.DefClassContext):
        id = ctx.TYPE(0).getText()
        type_id = ctx.CLASS_N().__str__()
        self.current_class = id
        if ctx.INHERITS():
            inherits = ctx.TYPE(1).getText()
            self.symbolTable.add_column([id, type_id, inherits, None, None, None, "Global", None])
        else:
            self.symbolTable.add_column([id, type_id, None, None, None, None, "Global", None])
        
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
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        parent_class = ctx.parentCtx.TYPE(0).getText() if ctx.parentCtx.TYPE(0) else None
        self.current_class = parent_class
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
        
        type_id_b = self.visit(ctx.expr())
        return type_id_b
    
    def visitDefAssign(self, ctx: YAPLParser.DefAssignContext):
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        space = get_space_vars(type_id.lower())
        parent_class = ctx.parentCtx.TYPE(0).getText() if ctx.parentCtx.TYPE(0) else None
        self.current_class = parent_class
        if parent_class in self.class_methods:
            self.class_methods[parent_class].append(id)
            self.symbolTable.add_column([id, type_id, None, parent_class, None, None, "Local", space])
        else:
            self.class_methods[parent_class] = [id]
            
        self.symbolTable.add_info_to_cell(parent_class, "Contains", self.class_methods[parent_class])
        
        if(ctx.expr()):
            type_id = self.visit(ctx.expr())
        return type_id
    
    def visitFormalAssign(self, ctx:YAPLParser.FormalAssignContext):
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText() 
        return type_id
        
    def visitAssignment(self, ctx: YAPLParser.AssignmentContext):
        id = ctx.ID().getText()
        type_id = self.visit(ctx.expr()) 
        return type_id
    
    def visitDispatchExplicit(self, ctx: YAPLParser.DispatchExplicitContext):
        return self.visitChildren(ctx)
    
    def visitDispatchImplicit(self, ctx: YAPLParser.DispatchImplicitContext):
        return self.visitChildren(ctx)
    
    def visitIf(self, ctx: YAPLParser.IfContext):
        return self.visitChildren(ctx)
    
    def visitWhile(self, ctx: YAPLParser.WhileContext):
        return self.visitChildren(ctx)
    
    def visitBlock(self, ctx: YAPLParser.BlockContext):
        return self.visitChildren(ctx)
    
    def visitLetId(self, ctx: YAPLParser.LetIdContext):
        for i in range(len(ctx.ID())):
            id = ctx.ID(i).getText()
            _type = ctx.TYPE(i).getText()
            space = get_space_vars(_type.lower())
            self.symbolTable.add_column([id, _type, None, self.current_class, None, None, "Local", space])
            if self.current_class in self.class_methods:
                self.class_methods[self.current_class].append(id)
                self.symbolTable.add_column([id, _type, None, self.current_class, None, None, "Local", space])
            else:
                self.class_methods[self.current_class] = [id]
            
            self.symbolTable.add_info_to_cell(self.current_class, "Contains", self.class_methods[self.current_class])
        
        return self.visitChildren(ctx)
    
    def visitNew(self, ctx: YAPLParser.NewContext):
        _type = ctx.TYPE().getText()
        return _type
    
    def visitNegative(self, ctx: YAPLParser.NegativeContext):
        return self.visitChildren(ctx)
    
    def visitIsvoid(self, ctx: YAPLParser.IsvoidContext):
        return self.visitChildren(ctx)
    
    def visitTimes(self, ctx: YAPLParser.TimesContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type is not None and right_type is not None:
            if left_type.lower() == 'int' and right_type.lower() == 'int':
                return 'int'
        
        return 'Error'
    
    def visitDiv(self, ctx: YAPLParser.DivContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'int'
        else:
            return "Error"
    
    def visitPlus(self, ctx: YAPLParser.PlusContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if left_type is not None and right_type is not None:
            if left_type.lower() == 'int' and right_type.lower() == 'int':
                return 'int'
            elif left_type.lower() == 'string' and right_type.lower() == 'string':
                return 'string'
        
        return 'Error'
    
    def visitMinus(self, ctx: YAPLParser.MinusContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'int'
        else:
            return "Error"
    
    def visitLessThanOrEqual(self, ctx: YAPLParser.LessThanOrEqualContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'bool'
        else:
            return 'Error'
    
    def visitLessThan(self, ctx: YAPLParser.LessThanContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'bool'
        else:
            return 'Error'
    
    def visitGreaterThan(self, ctx: YAPLParser.GreaterThanContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'bool'
        else:
            return 'Error'
    
    def visitGreaterThanOrEqual(self, ctx: YAPLParser.GreaterThanOrEqualContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'bool'
        else:
            return 'Error'
    
    def visitEqual(self, ctx: YAPLParser.EqualContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == right_type.lower():
            return 'bool'
        else:
            return 'Error'
    
    def visitAnd(self, ctx:YAPLParser.AndContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'bool' and right_type.lower() == 'bool':
            return 'bool'
        else:
            return 'Error'
    
    def visitOr(self, ctx:YAPLParser.OrContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'bool' and right_type.lower() == 'bool':
            return 'bool'
        else:
            return 'Error'
    
    def visitNeg(self, ctx:YAPLParser.NegContext):
        return self.visitChildren(ctx)
    
    def visitParens(self, ctx:YAPLParser.ParensContext):
        return self.visit(ctx.expr())
    
    def visitId(self, ctx:YAPLParser.IdContext):
        id = ctx.ID().getText()
        row = self.symbolTable.get_cell(id)
        if row:
            return row[1]
        return None
    
    def visitInt(self, ctx: YAPLParser.IntContext):
        return "Int"
    
    def visitString(self, ctx: YAPLParser.StringContext):
        return "String"
    
    def visitBoolean(self, ctx: YAPLParser.BooleanContext):
        return "Bool"

def main():
    file_name = './tests/recur.cl'
    input_stream = FileStream(file_name)
    lexer = YAPLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = YAPLParser(token_stream)
    tree = parser.prog()
    YV = YAPLVisitorImpl()
    
    try:
        res = YV.visit(tree)
        print("Final", res)
    except TypeError as e:
        print(e);
    treeF = YV.symbolTable.build_Table()
    #print(treeF)
    with open("SymbolTable.txt", 'w', encoding="utf-8") as f:
        f.write(treeF.get_string())
    
if __name__ == '__main__':
    main()