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

class YAPLVisitorImpl(YAPLVisitor):
    def __init__(self):
        self.symbolTable = Table()
         
    def visitAssignment(self, ctx: YAPLParser.AssignmentContext):
        id = ctx.ID()
        type_id = self.visit(ctx.expr())
        self.symbolTable.add_column([id, 'temp', type_id])
        return super().visitAssignment(ctx)
    
    def visitDefClass(self, ctx: YAPLParser.DefClassContext):
        return super().visitDefClass(ctx)
    
    def visitId(self, ctx: YAPLParser.IdContext):
        id = ctx.ID().getText()
        val = self.symbolTable.get_cell(id)
        return super().visitId(ctx)
    
    def visitDefClass(self, ctx: YAPLParser.DefClassContext):
        return super().visitDefClass(ctx)
    
    def visitDefFunc(self, ctx: YAPLParser.DefFuncContext):
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        self.symbolTable.add_column([id, 'temp', type_id])
        return super().visitDefFunc(ctx)
    
    def visitDefAsign(self, ctx: YAPLParser.DefAsignContext):
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        self.symbolTable.add_column([id, 'temp', type_id])
        return super().visitDefAsign(ctx)
    
    def visitFeature(self, ctx: YAPLParser.FeatureContext):
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        self.symbolTable.add_column([id, 'temp', type_id])
        return super().visitFeature(ctx)

    def visitInt(self, ctx:YAPLParser.IntContext):
        return super().visitInt(ctx)
    
    def visitTimes(self, ctx:YAPLParser.TimesContext):
        left = ctx.expr(0).getText()
        left_T = self.symbolTable.get_cell(left) if self.symbolTable.containsKey(left) else left
        right = ctx.expr(1).getText()
        right_T = self.symbolTable.get_cell(right) if self.symbolTable.containsKey(right) else right
        
        if left_T[2] == right_T[2]:
            print("Coincide")
        else:
            print("No coincide")
        return super().visitTimes(ctx)

    def visitDiv(self, ctx:YAPLParser.DivContext):
        left = ctx.expr(0).getText()
        left_T = self.symbolTable.get_cell(left) if self.symbolTable.containsKey(left) else left
        right = ctx.expr(1).getText()
        right_T = self.symbolTable.get_cell(right) if self.symbolTable.containsKey(right) else right
        
        if left_T[2] == right_T[2]:
            print("Coincide")
        else:
            print("No coincide")
        return super().visitDiv(ctx)
    
    def visitMinus(self, ctx: YAPLParser.MinusContext):
        left = ctx.expr(0).getText()
        left_T = self.symbolTable.get_cell(left) if self.symbolTable.containsKey(left) else left
        right = ctx.expr(1).getText()
        right_T = self.symbolTable.get_cell(right) if self.symbolTable.containsKey(right) else right
        
        if left_T[2] == right_T[2]:
            print("Coincide")
        else:
            print("No coincide")
        return super().visitMinus(ctx)

    def visitPlus(self, ctx:YAPLParser.PlusContext):
        left = ctx.expr(0).getText()
        left_T = self.symbolTable.get_cell(left) if self.symbolTable.containsKey(left) else left
        right = ctx.expr(1).getText()
        right_T = self.symbolTable.get_cell(right) if self.symbolTable.containsKey(right) else right
        
        if left_T[2] == right_T[2]:
            print("Coincide")
        else:
            print("No coincide")
        return super().visitPlus(ctx)
    
    def visitParens(self, ctx: YAPLParser.ParensContext):
        return self.visit(ctx.expr())
    
    def visitIf(self, ctx: YAPLParser.IfContext):
        condition = self.visit(ctx.expr(0))
        if condition:
            return self.visit(ctx.expr(1))
        else:
            return self.visit(ctx.expr(2))
    
    def visitWhile(self, ctx: YAPLParser.WhileContext):
        result = 0
        while self.visit(ctx.expr(0)):
            result = self.visit(ctx.expr(1))
        return result
    
    def visitBlock(self, ctx: YAPLParser.BlockContext):
        result = 0
        for expr_ctx in ctx.expr():
            result = self.visit(expr_ctx)
        return result
    
    def visitLetid(self, ctx: YAPLParser.LetidContext):
        # Recorre las declaraciones let y agrega las variables a la tabla de símbolos
        for i in range(len(ctx.ID())):
            id = ctx.ID(i).getText()
            _type = ctx.TYPE(i).getText()
            value = self.visit(ctx.expr(i)) if ctx.expr(i) else None
            self.symbolTable.add_column([id, _type, value])
        return self.visit(ctx.expr(-1))
    
    def visitNew(self, ctx: YAPLParser.NewContext):
        _type = ctx.TYPE().getText()
        return None
    
    def visitNegative(self, ctx: YAPLParser.NegativeContext):
        expr_value = self.visit(ctx.expr())
        return -expr_value
    
    def visitIsvoid(self, ctx: YAPLParser.IsvoidContext):
        expr_value = self.visit(ctx.expr())
        return expr_value is None
    
    def visitString(self, ctx: YAPLParser.StringContext):
        return str(ctx.STRING().getText())[1:-1]

    def visitBoolean(self, ctx: YAPLParser.BooleanContext):
        return ctx.bool_ == YAPLParser.TRUE
    
def main():
    file_name = 'test1.expr'
    input_stream = FileStream(file_name)
    lexer = YAPLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = YAPLParser(token_stream)
    tree = parser.prog()
    YV = YAPLVisitorImpl()
    YV.visit(tree)
    treeF = YV.symbolTable.build_Table()
    print(treeF)
    
if __name__ == '__main__':
    main()