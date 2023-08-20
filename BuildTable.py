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
        self.symbolTable.add_column([id, type_id, None, None, None, None, None])
        return super().visitAssignment(ctx)
    
    def visitDefClass(self, ctx: YAPLParser.DefClassContext):
        return super().visitDefClass(ctx)
    
    def visitId(self, ctx: YAPLParser.IdContext):
        id = ctx.ID().getText()
        row = self.symbolTable.get_cell(id)
        if row:
            return row[1]
        return None
    
    def visitDefClass(self, ctx: YAPLParser.DefClassContext):
        return super().visitDefClass(ctx)
    
    def visitDefFunc(self, ctx: YAPLParser.DefFuncContext):
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        self.symbolTable.add_column([id, type_id, None, None, None, None, None])
        return type_id
    
    def visitDefAssign(self, ctx: YAPLParser.DefAssignContext):
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        self.symbolTable.add_column([id, type_id, None, None, None, None, None])
        return super().visitDefAssign(ctx)
    
    def visitFeature(self, ctx: YAPLParser.FeatureContext):
        id = ctx.ID().getText()
        type_id = ctx.TYPE().getText()
        self.symbolTable.add_column([id, type_id, None, None, None, None, None])
        return type_id

    def visitInt(self, ctx:YAPLParser.IntContext):
        return super().visitInt(ctx)
    
    def visitTimes(self, ctx:YAPLParser.TimesContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type == 'Int' and right_type == 'Int':
            return left_type
        else:
            raise TypeError("Incongruencia de tipos en multiplicación")

    def visitDiv(self, ctx:YAPLParser.DivContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type == 'Int' and right_type == 'Int':
            return left_type
        else:
            raise TypeError("Incongruencia de tipos en división")
    
    def visitMinus(self, ctx: YAPLParser.MinusContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type == 'Int' and right_type == 'Int':
            return left_type
        else:
            raise TypeError("Incongruencia de tipos en resta")

    def visitPlus(self, ctx:YAPLParser.PlusContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type == 'Int' and right_type == 'Int':
            return left_type
        elif left_type == 'Char' and right_type == 'Char':
            return left_type
        else:
            raise TypeError("Incongruencia de tipos en suma")
    
    def visitAnd(self, ctx: YAPLParser.AndContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type == 'Bool' and right_type == 'Bool':
            return 'Bool'
        else:
            raise TypeError("Incongruencia de tipos en AND")

    def visitOr(self, ctx: YAPLParser.OrContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type == 'Bool' and right_type == 'Bool':
            return 'Bool'
        else:
            raise TypeError("Incongruencia de tipos en OR")
    
    def visitEqual(self, ctx:YAPLParser.EqualContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type == right_type:
            return 'Bool'
        else:
            raise TypeError("Type mismatch in equal operation")
    
    def visitGreaterThanOrEqual(self, ctx:YAPLParser.GreaterThanOrEqualContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if left_type == 'Int' and right_type == 'Int':
            return 'Bool'
        else:
            raise TypeError("Incongruencia de tipos en mayor o igual que")
    
    def visitLessThanOrEqual(self, ctx:YAPLParser.LessThanOrEqualContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if left_type == 'Int' and right_type == 'Int':
            return 'Bool'
        else:
            raise TypeError("Incongruencia de tipos en menor o igual que")
    
    def visitLessThan(self, ctx:YAPLParser.LessThanContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))
        
        if left_type == 'Int' and right_type == 'Int':
            return 'Bool'
        else:
            raise TypeError("Incongruencia de tipos en menor que")
    
    def visitGreaterThan(self, ctx:YAPLParser.GreaterThanContext):
        left_type = self.visit(ctx.expr(0))
        right_type = self.visit(ctx.expr(1))

        if left_type == 'Int' and right_type == 'Int':
            return 'Bool'
        else:
            raise TypeError("Incongruencia de tipos en mayor que")
    
    def visitParens(self, ctx: YAPLParser.ParensContext):
        return self.visit(ctx.expr())
    
    def visitIf(self, ctx: YAPLParser.IfContext):
        condition_type = self.visit(ctx.expr(0))
        then_type = self.visit(ctx.expr(1))
        else_type = self.visit(ctx.expr(2))

        if condition_type == 'Bool':
            return then_type if then_type == else_type else None
        return None
    
    def visitWhile(self, ctx: YAPLParser.WhileContext):
        result = None
        while self.visit(ctx.expr(0)):
            result = self.visit(ctx.expr(1))
        return result
    
    def visitBlock(self, ctx: YAPLParser.BlockContext):
        result_type = None
        for expr_ctx in ctx.expr():
            result_type = self.visit(expr_ctx)
        return result_type
    
    def visitLetid(self, ctx: YAPLParser.LetidContext):
        result_type = None
        for i in range(len(ctx.ID())):
            id = ctx.ID(i).getText()
            _type = ctx.TYPE(i).getText()
            value_type = self.visit(ctx.expr(i)) if ctx.expr(i) else None
            self.symbolTable.add_column([id, _type, value_type])
            result_type = value_type
        return result_type
    
    def visitNew(self, ctx: YAPLParser.NewContext):
        _type = ctx.TYPE().getText()
        return _type
    
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
    print(treeF)
    
if __name__ == '__main__':
    main()