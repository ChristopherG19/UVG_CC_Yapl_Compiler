# Generated from YAPL.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .YAPLParser import YAPLParser
else:
    from YAPLParser import YAPLParser

# This class defines a complete listener for a parse tree produced by YAPLParser.
class YAPLListener(ParseTreeListener):

    # Enter a parse tree produced by YAPLParser#start.
    def enterStart(self, ctx:YAPLParser.StartContext):
        pass

    # Exit a parse tree produced by YAPLParser#start.
    def exitStart(self, ctx:YAPLParser.StartContext):
        pass


    # Enter a parse tree produced by YAPLParser#defClass.
    def enterDefClass(self, ctx:YAPLParser.DefClassContext):
        pass

    # Exit a parse tree produced by YAPLParser#defClass.
    def exitDefClass(self, ctx:YAPLParser.DefClassContext):
        pass


    # Enter a parse tree produced by YAPLParser#defFunc.
    def enterDefFunc(self, ctx:YAPLParser.DefFuncContext):
        pass

    # Exit a parse tree produced by YAPLParser#defFunc.
    def exitDefFunc(self, ctx:YAPLParser.DefFuncContext):
        pass


    # Enter a parse tree produced by YAPLParser#defAssign.
    def enterDefAssign(self, ctx:YAPLParser.DefAssignContext):
        pass

    # Exit a parse tree produced by YAPLParser#defAssign.
    def exitDefAssign(self, ctx:YAPLParser.DefAssignContext):
        pass


    # Enter a parse tree produced by YAPLParser#formalAssign.
    def enterFormalAssign(self, ctx:YAPLParser.FormalAssignContext):
        pass

    # Exit a parse tree produced by YAPLParser#formalAssign.
    def exitFormalAssign(self, ctx:YAPLParser.FormalAssignContext):
        pass


    # Enter a parse tree produced by YAPLParser#minus.
    def enterMinus(self, ctx:YAPLParser.MinusContext):
        pass

    # Exit a parse tree produced by YAPLParser#minus.
    def exitMinus(self, ctx:YAPLParser.MinusContext):
        pass


    # Enter a parse tree produced by YAPLParser#parens.
    def enterParens(self, ctx:YAPLParser.ParensContext):
        pass

    # Exit a parse tree produced by YAPLParser#parens.
    def exitParens(self, ctx:YAPLParser.ParensContext):
        pass


    # Enter a parse tree produced by YAPLParser#string.
    def enterString(self, ctx:YAPLParser.StringContext):
        pass

    # Exit a parse tree produced by YAPLParser#string.
    def exitString(self, ctx:YAPLParser.StringContext):
        pass


    # Enter a parse tree produced by YAPLParser#isvoid.
    def enterIsvoid(self, ctx:YAPLParser.IsvoidContext):
        pass

    # Exit a parse tree produced by YAPLParser#isvoid.
    def exitIsvoid(self, ctx:YAPLParser.IsvoidContext):
        pass


    # Enter a parse tree produced by YAPLParser#while.
    def enterWhile(self, ctx:YAPLParser.WhileContext):
        pass

    # Exit a parse tree produced by YAPLParser#while.
    def exitWhile(self, ctx:YAPLParser.WhileContext):
        pass


    # Enter a parse tree produced by YAPLParser#div.
    def enterDiv(self, ctx:YAPLParser.DivContext):
        pass

    # Exit a parse tree produced by YAPLParser#div.
    def exitDiv(self, ctx:YAPLParser.DivContext):
        pass


    # Enter a parse tree produced by YAPLParser#neg.
    def enterNeg(self, ctx:YAPLParser.NegContext):
        pass

    # Exit a parse tree produced by YAPLParser#neg.
    def exitNeg(self, ctx:YAPLParser.NegContext):
        pass


    # Enter a parse tree produced by YAPLParser#negative.
    def enterNegative(self, ctx:YAPLParser.NegativeContext):
        pass

    # Exit a parse tree produced by YAPLParser#negative.
    def exitNegative(self, ctx:YAPLParser.NegativeContext):
        pass


    # Enter a parse tree produced by YAPLParser#times.
    def enterTimes(self, ctx:YAPLParser.TimesContext):
        pass

    # Exit a parse tree produced by YAPLParser#times.
    def exitTimes(self, ctx:YAPLParser.TimesContext):
        pass


    # Enter a parse tree produced by YAPLParser#and.
    def enterAnd(self, ctx:YAPLParser.AndContext):
        pass

    # Exit a parse tree produced by YAPLParser#and.
    def exitAnd(self, ctx:YAPLParser.AndContext):
        pass


    # Enter a parse tree produced by YAPLParser#lessThan.
    def enterLessThan(self, ctx:YAPLParser.LessThanContext):
        pass

    # Exit a parse tree produced by YAPLParser#lessThan.
    def exitLessThan(self, ctx:YAPLParser.LessThanContext):
        pass


    # Enter a parse tree produced by YAPLParser#block.
    def enterBlock(self, ctx:YAPLParser.BlockContext):
        pass

    # Exit a parse tree produced by YAPLParser#block.
    def exitBlock(self, ctx:YAPLParser.BlockContext):
        pass


    # Enter a parse tree produced by YAPLParser#id.
    def enterId(self, ctx:YAPLParser.IdContext):
        pass

    # Exit a parse tree produced by YAPLParser#id.
    def exitId(self, ctx:YAPLParser.IdContext):
        pass


    # Enter a parse tree produced by YAPLParser#if.
    def enterIf(self, ctx:YAPLParser.IfContext):
        pass

    # Exit a parse tree produced by YAPLParser#if.
    def exitIf(self, ctx:YAPLParser.IfContext):
        pass


    # Enter a parse tree produced by YAPLParser#greaterThan.
    def enterGreaterThan(self, ctx:YAPLParser.GreaterThanContext):
        pass

    # Exit a parse tree produced by YAPLParser#greaterThan.
    def exitGreaterThan(self, ctx:YAPLParser.GreaterThanContext):
        pass


    # Enter a parse tree produced by YAPLParser#new.
    def enterNew(self, ctx:YAPLParser.NewContext):
        pass

    # Exit a parse tree produced by YAPLParser#new.
    def exitNew(self, ctx:YAPLParser.NewContext):
        pass


    # Enter a parse tree produced by YAPLParser#or.
    def enterOr(self, ctx:YAPLParser.OrContext):
        pass

    # Exit a parse tree produced by YAPLParser#or.
    def exitOr(self, ctx:YAPLParser.OrContext):
        pass


    # Enter a parse tree produced by YAPLParser#assignment.
    def enterAssignment(self, ctx:YAPLParser.AssignmentContext):
        pass

    # Exit a parse tree produced by YAPLParser#assignment.
    def exitAssignment(self, ctx:YAPLParser.AssignmentContext):
        pass


    # Enter a parse tree produced by YAPLParser#dispatchImplicit.
    def enterDispatchImplicit(self, ctx:YAPLParser.DispatchImplicitContext):
        pass

    # Exit a parse tree produced by YAPLParser#dispatchImplicit.
    def exitDispatchImplicit(self, ctx:YAPLParser.DispatchImplicitContext):
        pass


    # Enter a parse tree produced by YAPLParser#int.
    def enterInt(self, ctx:YAPLParser.IntContext):
        pass

    # Exit a parse tree produced by YAPLParser#int.
    def exitInt(self, ctx:YAPLParser.IntContext):
        pass


    # Enter a parse tree produced by YAPLParser#plus.
    def enterPlus(self, ctx:YAPLParser.PlusContext):
        pass

    # Exit a parse tree produced by YAPLParser#plus.
    def exitPlus(self, ctx:YAPLParser.PlusContext):
        pass


    # Enter a parse tree produced by YAPLParser#greaterThanOrEqual.
    def enterGreaterThanOrEqual(self, ctx:YAPLParser.GreaterThanOrEqualContext):
        pass

    # Exit a parse tree produced by YAPLParser#greaterThanOrEqual.
    def exitGreaterThanOrEqual(self, ctx:YAPLParser.GreaterThanOrEqualContext):
        pass


    # Enter a parse tree produced by YAPLParser#equal.
    def enterEqual(self, ctx:YAPLParser.EqualContext):
        pass

    # Exit a parse tree produced by YAPLParser#equal.
    def exitEqual(self, ctx:YAPLParser.EqualContext):
        pass


    # Enter a parse tree produced by YAPLParser#boolean.
    def enterBoolean(self, ctx:YAPLParser.BooleanContext):
        pass

    # Exit a parse tree produced by YAPLParser#boolean.
    def exitBoolean(self, ctx:YAPLParser.BooleanContext):
        pass


    # Enter a parse tree produced by YAPLParser#letId.
    def enterLetId(self, ctx:YAPLParser.LetIdContext):
        pass

    # Exit a parse tree produced by YAPLParser#letId.
    def exitLetId(self, ctx:YAPLParser.LetIdContext):
        pass


    # Enter a parse tree produced by YAPLParser#lessThanOrEqual.
    def enterLessThanOrEqual(self, ctx:YAPLParser.LessThanOrEqualContext):
        pass

    # Exit a parse tree produced by YAPLParser#lessThanOrEqual.
    def exitLessThanOrEqual(self, ctx:YAPLParser.LessThanOrEqualContext):
        pass


    # Enter a parse tree produced by YAPLParser#dispatchExplicit.
    def enterDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        pass

    # Exit a parse tree produced by YAPLParser#dispatchExplicit.
    def exitDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        pass



del YAPLParser