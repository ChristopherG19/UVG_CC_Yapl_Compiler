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
    
    def visitId(self, ctx: YAPLParser.IdContext):
        id = ctx.ID().getText()
        val = self.symbolTable.containsKey(id)
        if val != None:
            return val
        return 0

    def visitInt(ctx:YAPLParser.IntContext):
        return int(str(ctx.INT().getText()))
    
    def visitMulDiv(self, ctx: YAPLParser.MulDivContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if (ctx.TIMES == YAPLParser.TIMES):
            return left * right
        return left / right
    
    def visitAddSub(self, ctx: YAPLParser.AddSubContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        if (ctx.PLUS == YAPLParser.PLUS):
            return left + right
        return left - right
    
    def visitInPar(self, ctx: YAPLParser.InParContext):
        return self.visit(ctx.expr())