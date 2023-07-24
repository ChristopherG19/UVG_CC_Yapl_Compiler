'''
    Universidad del Valle de Guatemala
    Construcción de Compiladores
    Christopher García 20541
    Ma. Isabel Solano 20504
    Laboratorio#1
'''

import sys
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
        id = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.symbolTable.add_column([id, 'temp', value])
        return value
    
    def visitId(self, ctx: YAPLParser.IdContext):
        id = ctx.ID().getText()
        val = self.symbolTable.containsKey(id)
        if val is not None:
            return val
        return 0

    def visitInt(ctx:YAPLParser.IntContext):
        return int(str(ctx.INT().getText()))
    
    def visitMulDiv(self, ctx: YAPLParser.MulDivContext):
        left = int(self.visit(ctx.expr(0)))
        right = int(self.visit(ctx.expr(1)))
        if (ctx.TIMES == YAPLParser.TIMES):
            return left * right
        if right != 0:
            return left / right
        return 0
    
    def visitAddSub(self, ctx: YAPLParser.AddSubContext):
        left = int(self.visit(ctx.expr(0)))
        right = int(self.visit(ctx.expr(1)))
        if (ctx.PLUS == YAPLParser.PLUS):
            return left + right
        return left - right
    
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
        return ctx.bool.type == YAPLParser.TRUE
    
def main():
    file_name = 'test1.expr'
    input_stream = FileStream(file_name)
    lexer = YAPLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = YAPLParser(token_stream)
    tree = parser.prog()
    print(tree)
    YV = YAPLVisitorImpl()
    YV.visit(tree)
    print(YV.symbolTable.build_Table())
    
if __name__ == '__main__':
    main()