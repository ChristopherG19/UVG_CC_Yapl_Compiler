# Generated from YAPL.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .YAPLParser import YAPLParser
else:
    from YAPLParser import YAPLParser

# This class defines a complete generic visitor for a parse tree produced by YAPLParser.

class YAPLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by YAPLParser#prog.
    def visitProg(self, ctx:YAPLParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#class_def.
    def visitClass_def(self, ctx:YAPLParser.Class_defContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#feature.
    def visitFeature(self, ctx:YAPLParser.FeatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#formal.
    def visitFormal(self, ctx:YAPLParser.FormalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#new.
    def visitNew(self, ctx:YAPLParser.NewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#parens.
    def visitParens(self, ctx:YAPLParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#string.
    def visitString(self, ctx:YAPLParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#assignment.
    def visitAssignment(self, ctx:YAPLParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#isvoid.
    def visitIsvoid(self, ctx:YAPLParser.IsvoidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#addSub.
    def visitAddSub(self, ctx:YAPLParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#while.
    def visitWhile(self, ctx:YAPLParser.WhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#dispatchImplicit.
    def visitDispatchImplicit(self, ctx:YAPLParser.DispatchImplicitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#int.
    def visitInt(self, ctx:YAPLParser.IntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#mulDiv.
    def visitMulDiv(self, ctx:YAPLParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#neg.
    def visitNeg(self, ctx:YAPLParser.NegContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#negative.
    def visitNegative(self, ctx:YAPLParser.NegativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#boolean.
    def visitBoolean(self, ctx:YAPLParser.BooleanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#letid.
    def visitLetid(self, ctx:YAPLParser.LetidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#block.
    def visitBlock(self, ctx:YAPLParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#comparisson.
    def visitComparisson(self, ctx:YAPLParser.ComparissonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#id.
    def visitId(self, ctx:YAPLParser.IdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#if.
    def visitIf(self, ctx:YAPLParser.IfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#dispatchExplicit.
    def visitDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        return self.visitChildren(ctx)



del YAPLParser