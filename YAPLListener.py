# Generated from YAPL.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .YAPLParser import YAPLParser
else:
    from YAPLParser import YAPLParser

# This class defines a complete listener for a parse tree produced by YAPLParser.
class YAPLListener(ParseTreeListener):

    # Enter a parse tree produced by YAPLParser#prog.
    def enterProg(self, ctx:YAPLParser.ProgContext):
        pass

    # Exit a parse tree produced by YAPLParser#prog.
    def exitProg(self, ctx:YAPLParser.ProgContext):
        pass


    # Enter a parse tree produced by YAPLParser#class_def.
    def enterClass_def(self, ctx:YAPLParser.Class_defContext):
        pass

    # Exit a parse tree produced by YAPLParser#class_def.
    def exitClass_def(self, ctx:YAPLParser.Class_defContext):
        pass


    # Enter a parse tree produced by YAPLParser#feature.
    def enterFeature(self, ctx:YAPLParser.FeatureContext):
        pass

    # Exit a parse tree produced by YAPLParser#feature.
    def exitFeature(self, ctx:YAPLParser.FeatureContext):
        pass


    # Enter a parse tree produced by YAPLParser#formal.
    def enterFormal(self, ctx:YAPLParser.FormalContext):
        pass

    # Exit a parse tree produced by YAPLParser#formal.
    def exitFormal(self, ctx:YAPLParser.FormalContext):
        pass


    # Enter a parse tree produced by YAPLParser#new.
    def enterNew(self, ctx:YAPLParser.NewContext):
        pass

    # Exit a parse tree produced by YAPLParser#new.
    def exitNew(self, ctx:YAPLParser.NewContext):
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


    # Enter a parse tree produced by YAPLParser#assignment.
    def enterAssignment(self, ctx:YAPLParser.AssignmentContext):
        pass

    # Exit a parse tree produced by YAPLParser#assignment.
    def exitAssignment(self, ctx:YAPLParser.AssignmentContext):
        pass


    # Enter a parse tree produced by YAPLParser#isvoid.
    def enterIsvoid(self, ctx:YAPLParser.IsvoidContext):
        pass

    # Exit a parse tree produced by YAPLParser#isvoid.
    def exitIsvoid(self, ctx:YAPLParser.IsvoidContext):
        pass


    # Enter a parse tree produced by YAPLParser#addSub.
    def enterAddSub(self, ctx:YAPLParser.AddSubContext):
        pass

    # Exit a parse tree produced by YAPLParser#addSub.
    def exitAddSub(self, ctx:YAPLParser.AddSubContext):
        pass


    # Enter a parse tree produced by YAPLParser#while.
    def enterWhile(self, ctx:YAPLParser.WhileContext):
        pass

    # Exit a parse tree produced by YAPLParser#while.
    def exitWhile(self, ctx:YAPLParser.WhileContext):
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


    # Enter a parse tree produced by YAPLParser#mulDiv.
    def enterMulDiv(self, ctx:YAPLParser.MulDivContext):
        pass

    # Exit a parse tree produced by YAPLParser#mulDiv.
    def exitMulDiv(self, ctx:YAPLParser.MulDivContext):
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


    # Enter a parse tree produced by YAPLParser#boolean.
    def enterBoolean(self, ctx:YAPLParser.BooleanContext):
        pass

    # Exit a parse tree produced by YAPLParser#boolean.
    def exitBoolean(self, ctx:YAPLParser.BooleanContext):
        pass


    # Enter a parse tree produced by YAPLParser#letid.
    def enterLetid(self, ctx:YAPLParser.LetidContext):
        pass

    # Exit a parse tree produced by YAPLParser#letid.
    def exitLetid(self, ctx:YAPLParser.LetidContext):
        pass


    # Enter a parse tree produced by YAPLParser#block.
    def enterBlock(self, ctx:YAPLParser.BlockContext):
        pass

    # Exit a parse tree produced by YAPLParser#block.
    def exitBlock(self, ctx:YAPLParser.BlockContext):
        pass


    # Enter a parse tree produced by YAPLParser#comparisson.
    def enterComparisson(self, ctx:YAPLParser.ComparissonContext):
        pass

    # Exit a parse tree produced by YAPLParser#comparisson.
    def exitComparisson(self, ctx:YAPLParser.ComparissonContext):
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


    # Enter a parse tree produced by YAPLParser#dispatchExplicit.
    def enterDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        pass

    # Exit a parse tree produced by YAPLParser#dispatchExplicit.
    def exitDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        pass



del YAPLParser