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
        
    # Visit a parse tree produced by YAPLParser#start.
    def visitStart(self, ctx:YAPLParser.StartContext):
        final_type = None
        stages = ctx.class_def()
        for stage in stages:
            #print(stage)
            stage_type = self.visit(stage)
            if stage_type != "Error":
                final_type = stage_type
            else:
                final_type = "Error"
            
        return final_type

    # Visit a parse tree produced by YAPLParser#defClass.
    def visitDefClass(self, ctx:YAPLParser.DefClassContext):
        class_id = ctx.TYPE(0).getText()
        steps = ctx.feature()
        type_class_id = self.visit(ctx.feature())
        if ctx.INHERITS():
            inherits = ctx.TYPE(1).getText()
            self.symbolTable.add_column([class_id, type_class_id, inherits, None, None, None, "Global", None])
        else:
            self.symbolTable.add_column([class_id, type_class_id, None, None, None, None, "Global", None])
        
        self.class_methods[class_id] = []
        print(type_class_id)
        return type_class_id

    # Visit a parse tree produced by YAPLParser#defFunc.
    def visitDefFunc(self, ctx:YAPLParser.DefFuncContext):
        id = ctx.ID().getText()
        type_id = self.visit(ctx.expr())
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

    # Visit a parse tree produced by YAPLParser#defAssign.
    def visitDefAssign(self, ctx:YAPLParser.DefAssignContext):
        id = ctx.ID().getText()
        type_id = self.visit(ctx.expr())
        space = get_space_vars(type_id.lower())
        parent_class = ctx.parentCtx.TYPE(0).getText() if ctx.parentCtx.TYPE(0) else None
        if parent_class in self.class_methods:
            self.class_methods[parent_class].append(id)
            self.symbolTable.add_column([id, type_id, None, parent_class, None, None, "Local", space])
        else:
            self.class_methods[parent_class] = [id]
            
        self.symbolTable.add_info_to_cell(parent_class, "Contains", self.class_methods[parent_class])
        return type_id

    # Visit a parse tree produced by YAPLParser#assign.
    def visitAssign(self, ctx:YAPLParser.AssignContext):
        print("aaaaaaaaaaaaaaaaaaaaaaaaass")
        return super().visitAssign(ctx)

    # Visit a parse tree produced by YAPLParser#minus.
    def visitMinus(self, ctx:YAPLParser.MinusContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'int'
        else:
            return "Error"
            # raise TypeError("Incongruencia de tipos en resta")

    # Visit a parse tree produced by YAPLParser#parens.
    def visitParens(self, ctx:YAPLParser.ParensContext):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaPP")
        return super().visitParens(ctx)

    # Visit a parse tree produced by YAPLParser#string.
    def visitString(self, ctx:YAPLParser.StringContext):
        return 'string'

    # Visit a parse tree produced by YAPLParser#isvoid.
    def visitIsvoid(self, ctx:YAPLParser.IsvoidContext):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaV")
        return super().visitIsvoid(ctx)

    # Visit a parse tree produced by YAPLParser#while.
    def visitWhile(self, ctx:YAPLParser.WhileContext):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaW")
        return super().visitWhile(ctx)

    # Visit a parse tree produced by YAPLParser#div.
    def visitDiv(self, ctx:YAPLParser.DivContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'int'
        else:
            return 'Error'
            # raise TypeError("Incongruencia de tipos en división")

    # Visit a parse tree produced by YAPLParser#neg.
    def visitNeg(self, ctx:YAPLParser.NegContext):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaC")
        return super().visitNeg(ctx)

    # Visit a parse tree produced by YAPLParser#negative.
    def visitNegative(self, ctx:YAPLParser.NegativeContext):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaC2")
        return super().visitNegative(ctx)

    # Visit a parse tree produced by YAPLParser#times.
    def visitTimes(self, ctx:YAPLParser.TimesContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'int'
        else:
            return 'Error'
            # raise TypeError("Incongruencia de tipos en multiplicación")

    # Visit a parse tree produced by YAPLParser#and.
    def visitAnd(self, ctx:YAPLParser.AndContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'bool' and right_type.lower() == 'bool':
            return 'bool'
        else:
            return 'Error'
            # raise TypeError("Incongruencia de tipos en AND")

    # Visit a parse tree produced by YAPLParser#lessThan.
    def visitLessThan(self, ctx:YAPLParser.LessThanContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'bool'
        else:
            return 'Error'
            # raise TypeError("Incongruencia de tipos en menor que")

    # Visit a parse tree produced by YAPLParser#block.
    def visitBlock(self, ctx:YAPLParser.BlockContext):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaBBl")
        return super().visitBlock(ctx)

    # Visit a parse tree produced by YAPLParser#id.
    def visitId(self, ctx:YAPLParser.IdContext):
        id = ctx.ID().getText()
        row = self.symbolTable.get_cell(id)
        return row[1]

    # Visit a parse tree produced by YAPLParser#if.
    def visitIf(self, ctx:YAPLParser.IfContext):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaIf")
        return super().visitIf(ctx)

    # Visit a parse tree produced by YAPLParser#greaterThan.
    def visitGreaterThan(self, ctx:YAPLParser.GreaterThanContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'bool'
        else:
            return 'Error'
            # raise TypeError("Incongruencia de tipos en mayor que")

    # Visit a parse tree produced by YAPLParser#new.
    def visitNew(self, ctx:YAPLParser.NewContext):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaN")
        return super().visitNew(ctx)

    # Visit a parse tree produced by YAPLParser#or.
    def visitOr(self, ctx:YAPLParser.OrContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == 'bool' and right_type.lower() == 'bool':
            return 'bool'
        else:
            return 'Error'
            # raise TypeError("Incongruencia de tipos en OR")

    # Visit a parse tree produced by YAPLParser#assignment.
    def visitAssignment(self, ctx:YAPLParser.AssignmentContext):
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

    # Visit a parse tree produced by YAPLParser#dispatchImplicit.
    def visitDispatchImplicit(self, ctx:YAPLParser.DispatchImplicitContext):
        print("aaaaaaaaaaaaaaaaaaaaaaaaab")
        return super().visitDispatchImplicit(ctx)

    # Visit a parse tree produced by YAPLParser#int.
    def visitInt(self, ctx:YAPLParser.IntContext):
        return 'int'

    # Visit a parse tree produced by YAPLParser#plus.
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
            return 'Error'
            # raise TypeError("Incongruencia de tipos en suma")

    # Visit a parse tree produced by YAPLParser#greaterThanOrEqual.
    def visitGreaterThanOrEqual(self, ctx:YAPLParser.GreaterThanOrEqualContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'bool'
        else:
            return 'Error'
            # raise TypeError("Incongruencia de tipos en mayor o igual que")

    # Visit a parse tree produced by YAPLParser#equal.
    def visitEqual(self, ctx:YAPLParser.EqualContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type.lower() == right_type.lower():
            return 'bool'
        else:
            return 'Error'
            # raise TypeError("Type mismatch in equal operation")

    # Visit a parse tree produced by YAPLParser#boolean.
    def visitBoolean(self, ctx:YAPLParser.BooleanContext):
        return 'bool'

    # Visit a parse tree produced by YAPLParser#letId.
    def visitLetId(self, ctx:YAPLParser.LetIdContext):
        print("aaaaa")
        return super().visitLetId(ctx)

    # Visit a parse tree produced by YAPLParser#lessThanOrEqual.
    def visitLessThanOrEqual(self, ctx:YAPLParser.LessThanOrEqualContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if left_type.lower() == 'int' and right_type.lower() == 'int':
            return 'bool'
        else:
            return 'Error'
            # raise TypeError("Incongruencia de tipos en menor o igual que")

    # Visit a parse tree produced by YAPLParser#dispatchExplicit.
    def visitDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        print("aaaaaaaaaaaaaaaaaaaaaaaaa")
        return super().visitDispatchExplicit(ctx)

def main():
    file_name = './tests/recur.cl'
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