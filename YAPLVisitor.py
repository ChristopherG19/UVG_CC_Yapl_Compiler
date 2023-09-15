# Generated from YAPL.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .YAPLParser import YAPLParser
else:
    from YAPLParser import YAPLParser

# This class defines a complete generic visitor for a parse tree produced by YAPLParser.

class YAPLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by YAPLParser#start.
    def visitStart(self, ctx:YAPLParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#defClass.
    def visitDefClass(self, ctx:YAPLParser.DefClassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#defFunc.
    def visitDefFunc(self, ctx:YAPLParser.DefFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#defAssign.
    def visitDefAssign(self, ctx:YAPLParser.DefAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#formalAssign.
    def visitFormalAssign(self, ctx:YAPLParser.FormalAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#minus.
    def visitMinus(self, ctx:YAPLParser.MinusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#parens.
    def visitParens(self, ctx:YAPLParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#string.
    def visitString(self, ctx:YAPLParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#isvoid.
    def visitIsvoid(self, ctx:YAPLParser.IsvoidContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#while.
    def visitWhile(self, ctx:YAPLParser.WhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#div.
    def visitDiv(self, ctx:YAPLParser.DivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#neg.
    def visitNeg(self, ctx:YAPLParser.NegContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#negative.
    def visitNegative(self, ctx:YAPLParser.NegativeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#times.
    def visitTimes(self, ctx:YAPLParser.TimesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#and.
    def visitAnd(self, ctx:YAPLParser.AndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#lessThan.
    def visitLessThan(self, ctx:YAPLParser.LessThanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#block.
    def visitBlock(self, ctx:YAPLParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#id.
    def visitId(self, ctx:YAPLParser.IdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#if.
    def visitIf(self, ctx:YAPLParser.IfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#greaterThan.
    def visitGreaterThan(self, ctx:YAPLParser.GreaterThanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#new.
    def visitNew(self, ctx:YAPLParser.NewContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#or.
    def visitOr(self, ctx:YAPLParser.OrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#assignment.
    def visitAssignment(self, ctx:YAPLParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#dispatchImplicit.
    def visitDispatchImplicit(self, ctx:YAPLParser.DispatchImplicitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#int.
    def visitInt(self, ctx:YAPLParser.IntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#plus.
    def visitPlus(self, ctx:YAPLParser.PlusContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#dispatchAttribute.
    def visitDispatchAttribute(self, ctx:YAPLParser.DispatchAttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#greaterThanOrEqual.
    def visitGreaterThanOrEqual(self, ctx:YAPLParser.GreaterThanOrEqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#equal.
    def visitEqual(self, ctx:YAPLParser.EqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#boolean.
    def visitBoolean(self, ctx:YAPLParser.BooleanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#letId.
    def visitLetId(self, ctx:YAPLParser.LetIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#lessThanOrEqual.
    def visitLessThanOrEqual(self, ctx:YAPLParser.LessThanOrEqualContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#self.
    def visitSelf(self, ctx:YAPLParser.SelfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by YAPLParser#dispatchExplicit.
    def visitDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        return self.visitChildren(ctx)



del YAPLParser