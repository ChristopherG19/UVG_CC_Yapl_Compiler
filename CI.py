from antlr4 import *
from YAPLLexer import YAPLLexer
from YAPLParser import YAPLParser
from YAPLVisitor import YAPLVisitor
from utils.node import *
from utils.symbolTable import *

class CodigoIntermedio(YAPLVisitor):

    def __init__(self, fileName:str, symbolTable) -> None:

        self.filename = fileName
        self.text = ""
        self.symbolTable = symbolTable

        # counters
        self.tag_counter = 0
        self.temp_counter = 0
        self.goto_true = 0
        self.goto_false = 0
        self.goto_end = 0
        
        #stacks
        self.temp_stack = []

        #
        self.currentClass = ""

        self.functions = {}
        self.registers = {}

        self.inFunction = False


    def visitStart(self, ctx:YAPLParser.StartContext):
        print("#start")
        stages = ctx.class_def()
        for stage in stages:
            self.visit(stage)
        
        # escribir al archivo
        self.text += "EOF"
        try:
            with open(self.filename, 'w') as file:
                file.write(self.text)
        except:
            print(f"El archivo {self.filename} no se pudo abrir")

        print("\n___________")
        print(self.functions, "\n")
        print(self.registers)

        return

    def visitDefClass(self, ctx:YAPLParser.DefClassContext):
        print("#defclass")

        self.temp_counter = 0

        self.currentClass = ctx.TYPE(0).getText()
        self.text += f"CLASS {self.currentClass}\n"

        #inicializar diccionario de diccionario
        self.functions[self.currentClass] = {}
        self.registers[self.currentClass] = {}

        for feature in ctx.feature():
            self.visit(feature)

        self.text += "EOC\n"

        return 

    def visitDefFunc(self, ctx:YAPLParser.DefFuncContext):
        print("#deffun")

        self.inFunction = True

        id = ctx.ID().getText()
        self.text += f"\t{self.currentClass}.{id}\n"

        self.funcText = ""

        for formal in ctx.formal():
            self.visit(formal)

        self.visit(ctx.expr())

        self.text += self.funcText
        self.functions[self.currentClass][id] = self.funcText

        self.text += f"\tEND FUNC {id}\n"

        self.inFunction = False

        return
    
    def visitDefAssign(self, ctx:YAPLParser.DefAssignContext):
        print("#visitdefassign")

        # se agrega solamente si se define la variable
        if ctx.expr():
            x = ""
            if ctx.getChildCount() > 1 :
                temp_ = "t" + str(self.temp_counter)
                self.addToTemp()
                self.temp_stack.append(temp_)
                self.visit(ctx.expr())
                x = temp_
            else: 
                text_ = ctx.expr().getText()
                if text_ in self.registers[self.currentClass].keys:
                    x = self.registers[self.currentClass][text_]
                else:
                    x = ctx.expr().getText
                self.visit(ctx.expr())
            
            # agregar al registro 
            id_ = ctx.ID().getText()
            type_ = ctx.TYPE().getText()
            print("row ", self.symbolTable.get_cell(id = id_, addType = type_, addParent = self.currentClass))
            disp = self.symbolTable.get_displacement(id = id_, addType = type_, addParent = self.currentClass)

            var = f"SP[{disp}]"
            self.registers[self.currentClass][id_] = var

            if self.inFunction:
                self.funcText += f"\t\tLW {var}, {x}\n"
            else:
                self.text += f"\t\tLW {var}, {x}\n"
        
        return
    
    def visitFormalAssign(self, ctx:YAPLParser.FormalAssignContext):
        print("#formalassign")
        
        return 
    
    def visitDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        print("#dispatchexplicit")
        return 

    def visitDispatchImplicit(self, ctx:YAPLParser.DispatchImplicitContext):
        print("#dispatchimplicit")

        id = ctx.ID().getText()

        paramslist = []

        for expr in ctx.expr():
            if expr.getChildCount() > 1:
                temp = "t" + str(self.temp_counter)
                self.addToTemp()
                self.temp_stack.append(temp)
                paramslist.append(temp)
                
            else: 
                paramslist.append(expr.getText())
            self.visit(expr)

        for p in paramslist:
            print("p ", p)
            self.funcText += f"\t\tPARAM {p}\n"


        self.funcText += f"\t\tCALL {id}, {len(paramslist)}\n"
        
        return 

    def visitDispatchAttribute(self, ctx:YAPLParser.DispatchAttributeContext):
        print("#dispatchattribute")
        
        return 
    
    def visitIf(self, ctx:YAPLParser.IfContext):
        print("#if")

        # evaluar expresión de la condición 
        temp_ = "t" + str(self.temp_counter) # creamos una temporal
        self.addToTemp
        self.temp_stack.append(temp_)
        self.visit(ctx.expr(0))
        print("if exp1 ", ctx.expr(0).getText())

        self.funcText += f"\t\tIF {temp_} > 0 GOTO L_TRUE_{self.goto_true}\n"
        self.funcText += f"\t\tGOTO L_FALSE_{self.goto_false}\n"

        true_ = self.goto_true 
        self.goto_true += 1

        false_ = self.goto_false 
        self.goto_false += 1

        end_ = self.goto_end
        self.goto_end += 1

        # caso real
        self.funcText += f"L_TRUE_{true_}:\n"        
        self.visit(ctx.expr(1))
        self.funcText += f"\t\tGOTO L_END_{end_}\n"

        # caso falso 
        self.funcText += f"L_FALSE_{false_}:\n"   
        self.visit(ctx.expr(2))
        self.funcText += f"\t\tGOTO L_END_{end_}\n"

        # continuar con el resto del codigo
        self.funcText += f"L_END_{end_}:\n"

        return 
    
    def visitWhile(self, ctx:YAPLParser.WhileContext):
        print("#while")
        
        return 
    
    def visitBlock(self, ctx:YAPLParser.BlockContext):
        print("#block")
        for expr in ctx.expr():
            print("exp block: ", expr.getText())
            self.visit(expr)
        return
    
    def visitLetId(self, ctx:YAPLParser.LetIdContext):
        print("#letId")
        
        return
    
    def visitNew(self, ctx:YAPLParser.NewContext):
        print("#new")
        
        return
    
    def visitNegative(self, ctx:YAPLParser.NegativeContext):
        print("#negative")

        self.visit(ctx.expr())
        
        return
    
    def visitIsVoid(self, ctx:YAPLParser.IsvoidContext):
        print("#isvoid")

        self.visit(ctx.expr())
        
        return
    
    def visitTimes(self, ctx:YAPLParser.TimesContext):

        line = "\t\tMULT "

        print("stack ", self.temp_stack)

        if len(self.temp_stack) > 0:
            line += self.temp_stack.pop() + ", "
        else: 
            line += "t" + str(self.temp_counter) + ", "
            self.addToTemp()

        # parte izquierda
        if ctx.expr(0).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(0))
            line += leftTemp + ", "
        else:
            self.visit(ctx.expr(0))
            # print("mult ", ctx.expr(0).getText())
            if ctx.expr(0).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}, "
            else:
                line += f"{ctx.expr(0).getText()}, "
                # print("Gt ", ctx.expr(0).getText())


        # parte derecha
        if ctx.expr(1).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(1))
            line += leftTemp
        else:
            self.visit(ctx.expr(1))
            # print("mult ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                # print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"
        
        return
    
    def visitDiv(self, ctx:YAPLParser.DivContext):
        print("#div")

        line = "\t\tDIV "

        print("stack ", self.temp_stack)

        if len(self.temp_stack) > 0:
            line += self.temp_stack.pop() + ", "
        else: 
            line += "t" + str(self.temp_counter) + ", "
            self.addToTemp()

        # parte izquierda
        if ctx.expr(0).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(0))
            line += leftTemp + ", "
        else:
            self.visit(ctx.expr(0))
            print("div ", ctx.expr(0).getText())
            if ctx.expr(0).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}, "
            else:
                line += f"{ctx.expr(0).getText()}, "
                print("Gt ", ctx.expr(0).getText())


        # parte derecha
        if ctx.expr(1).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(1))
            line += leftTemp
        else:
            self.visit(ctx.expr(1))
            print("div ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"
        
        return
    
    def visitPlus(self, ctx:YAPLParser.PlusContext):
        print("#plus")

        line = "\t\tADD "

        print("stack ", self.temp_stack)

        if len(self.temp_stack) > 0:
            line += self.temp_stack.pop() + ", "
        else: 
            line += "t" + str(self.temp_counter) + ", "
            self.addToTemp()

        # parte izquierda
        if ctx.expr(0).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(0))
            line += leftTemp + ", "
        else:
            self.visit(ctx.expr(0))
            # print("suma ", ctx.expr(0).getText())
            if ctx.expr(0).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}, "
            else:
                line += f"{ctx.expr(0).getText()}, "
                # print("Gt ", ctx.expr(0).getText())


        # parte derecha
        if ctx.expr(1).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(1))
            line += leftTemp
        else:
            self.visit(ctx.expr(1))
            # print("suma ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                # print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"
        
        return
    
    def visitMinus(self, ctx:YAPLParser.MinusContext):
        print("#minus")

        line = "\t\tSUB "

        print("stack ", self.temp_stack)

        if len(self.temp_stack) > 0:
            line += self.temp_stack.pop() + ", "
        else: 
            line += "t" + str(self.temp_counter) + ", "
            self.addToTemp()

        # parte izquierda
        if ctx.expr(0).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(0))
            line += leftTemp + ", "
        else:
            self.visit(ctx.expr(0))
            # print("rest ", ctx.expr(0).getText())
            if ctx.expr(0).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}, "
            else:
                line += f"{ctx.expr(0).getText()}, "
                # print("Gt ", ctx.expr(0).getText())


        # parte derecha
        if ctx.expr(1).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(1))
            line += leftTemp
        else:
            self.visit(ctx.expr(1))
            print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"
        
        return
    
    def visitLessThanOrEqual(self, ctx:YAPLParser.LessThanOrEqualContext):
        print("#lessThanorEqual")

        line = "\t\tSLE "

        print("stack ", self.temp_stack)

        if len(self.temp_stack) > 0:
            line += self.temp_stack.pop() + ", "
        else: 
            line += "t" + str(self.temp_counter) + ", "
            self.addToTemp()

        # parte izquierda
        if ctx.expr(0).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(0))
            line += leftTemp + ", "
        else:
            self.visit(ctx.expr(0))
            # print("rest ", ctx.expr(0).getText())
            if ctx.expr(0).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}, "
            else:
                line += f"{ctx.expr(0).getText()}, "
                # print("Gt ", ctx.expr(0).getText())


        # parte derecha
        if ctx.expr(1).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(1))
            line += leftTemp
        else:
            self.visit(ctx.expr(1))
            print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"
        
        return
    
    def visitLessThan(self, ctx:YAPLParser.LessThanContext):
        print("#lessThan")

        line = "\t\tSLG "

        print("stack ", self.temp_stack)

        if len(self.temp_stack) > 0:
            line += self.temp_stack.pop() + ", "
        else: 
            line += "t" + str(self.temp_counter) + ", "
            self.addToTemp()

        # parte izquierda
        if ctx.expr(0).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(0))
            line += leftTemp + ", "
        else:
            self.visit(ctx.expr(0))
            # print("rest ", ctx.expr(0).getText())
            if ctx.expr(0).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}, "
            else:
                line += f"{ctx.expr(0).getText()}, "
                # print("Gt ", ctx.expr(0).getText())


        # parte derecha
        if ctx.expr(1).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(1))
            line += leftTemp
        else:
            self.visit(ctx.expr(1))
            print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"
        
        return
    
    def visitGreaterThan(self, ctx:YAPLParser.GreaterThanContext):
        print("#greaterThan")

        line = "\t\tSGT "

        print("stack ", self.temp_stack)

        if len(self.temp_stack) > 0:
            line += self.temp_stack.pop() + ", "
        else: 
            line += "t" + str(self.temp_counter) + ", "
            self.addToTemp()

        # parte izquierda
        if ctx.expr(0).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(0))
            line += leftTemp + ", "
        else:
            self.visit(ctx.expr(0))
            # print("rest ", ctx.expr(0).getText())
            if ctx.expr(0).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}, "
            else:
                line += f"{ctx.expr(0).getText()}, "
                # print("Gt ", ctx.expr(0).getText())


        # parte derecha
        if ctx.expr(1).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(1))
            line += leftTemp
        else:
            self.visit(ctx.expr(1))
            print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"
        
        return
    
    def visitGreaterThanOrEqual(self, ctx:YAPLParser.GreaterThanOrEqualContext):
        print("#greaterThanOrEqual")

        line = "\t\tSGE "

        print("stack ", self.temp_stack)

        if len(self.temp_stack) > 0:
            line += self.temp_stack.pop() + ", "
        else: 
            line += "t" + str(self.temp_counter) + ", "
            self.addToTemp()

        # parte izquierda
        if ctx.expr(0).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(0))
            line += leftTemp + ", "
        else:
            self.visit(ctx.expr(0))
            # print("rest ", ctx.expr(0).getText())
            if ctx.expr(0).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}, "
            else:
                line += f"{ctx.expr(0).getText()}, "
                # print("Gt ", ctx.expr(0).getText())


        # parte derecha
        if ctx.expr(1).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(1))
            line += leftTemp
        else:
            self.visit(ctx.expr(1))
            print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"
        
        return
    
    def visitEqual(self, ctx:YAPLParser.EqualContext):
        print("#equal")

        line = "\t\tSEQ "

        print("stack ", self.temp_stack)

        if len(self.temp_stack) > 0:
            line += self.temp_stack.pop() + ", "
        else: 
            line += "t" + str(self.temp_counter) + ", "
            self.addToTemp()

        # parte izquierda
        if ctx.expr(0).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(0))
            line += leftTemp + ", "
        else:
            self.visit(ctx.expr(0))
            # print("rest ", ctx.expr(0).getText())
            if ctx.expr(0).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}, "
            else:
                line += f"{ctx.expr(0).getText()}, "
                # print("Gt ", ctx.expr(0).getText())


        # parte derecha
        if ctx.expr(1).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(1))
            line += leftTemp
        else:
            self.visit(ctx.expr(1))
            print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"
        
        return
    
    def visitAnd(self, ctx:YAPLParser.AndContext):
        print("#and")

        line = "\t\tAND "

        print("stack ", self.temp_stack)

        if len(self.temp_stack) > 0:
            line += self.temp_stack.pop() + ", "
        else: 
            line += "t" + str(self.temp_counter) + ", "
            self.addToTemp()

        # parte izquierda
        if ctx.expr(0).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(0))
            line += leftTemp + ", "
        else:
            self.visit(ctx.expr(0))
            # print("rest ", ctx.expr(0).getText())
            if ctx.expr(0).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}, "
            else:
                line += f"{ctx.expr(0).getText()}, "
                # print("Gt ", ctx.expr(0).getText())


        # parte derecha
        if ctx.expr(1).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(1))
            line += leftTemp
        else:
            self.visit(ctx.expr(1))
            print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"
        
        return
    
    def visitOr(self, ctx:YAPLParser.OrContext):

        line = "\t\tOR "

        print("stack ", self.temp_stack)

        if len(self.temp_stack) > 0:
            line += self.temp_stack.pop() + ", "
        else: 
            line += "t" + str(self.temp_counter) + ", "
            self.addToTemp()

        # parte izquierda
        if ctx.expr(0).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(0))
            line += leftTemp + ", "
        else:
            self.visit(ctx.expr(0))
            # print("rest ", ctx.expr(0).getText())
            if ctx.expr(0).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}, "
            else:
                line += f"{ctx.expr(0).getText()}, "
                # print("Gt ", ctx.expr(0).getText())


        # parte derecha
        if ctx.expr(1).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(1))
            line += leftTemp
        else:
            self.visit(ctx.expr(1))
            print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers.keys():
                line += f"{self.registers[self.currentClass][ctx.exp(0)]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"
        
        return
    
    def visitNeg(self, ctx:YAPLParser.NegContext):
        print("#")

        self.visit(ctx.expr())
        
        return
    
    def visitParens(self, ctx:YAPLParser.ParensContext):
        print("#parens")

        self.visit(ctx.expr())
        
        return
    
    def visitAssignment(self, ctx:YAPLParser.AssignmentContext):
        print("#assignment")

        # se agrega solamente si se define la variable
        if ctx.expr():
            x = ""
            firstchar = ctx.expr().getText()[:1]
            if ctx.getChildCount() > 1:
                if firstchar == '"':
                    # es un string
                    x = ctx.expr().getText()
                else: 
                    temp_ = "t" + str(self.temp_counter)
                    self.addToTemp()
                    self.temp_stack.append(temp_)
                    self.visit(ctx.expr())
                    print("assi ", ctx.expr().getText())
                    x = temp_
            else: 
                text_ = ctx.expr().getText()
                if text_ in self.registers[self.currentClass].keys:
                    x = self.registers[self.currentClass][text_]
                else:
                    x = ctx.expr().getText
                self.visit(ctx.expr())
            
            # agregar al registro 
            id_ = ctx.ID().getText()
            print("row ", self.symbolTable.get_cell(id = id_, addParent = self.currentClass))
            disp = self.symbolTable.get_displacement(id = id_, addParent = self.currentClass)

            var = f"SP[{disp}]"
            self.registers[self.currentClass][id_] = var

            if self.inFunction:
                self.funcText += f"\t\tLW {var}, {x}\n"
            else:
                self.text += f"\t\tLW {var}, {x}\n"
        
        return
    
    def visitID(self, ctx:YAPLParser.IdContext):
        print("#id")
        
        return
    
    def visitInt(self, ctx:YAPLParser.IntContext):
        print("#int")
        
        return
    
    def visitString(self, ctx:YAPLParser.StringContext):
        print("#string")
        
        return
    
    def visitBoolean(self, ctx:YAPLParser.BooleanContext):
        print("#boolean")
        
        return
    
    def visitSelf(self, ctx:YAPLParser.SelfContext):
        print("#self")
        
        return

    def add_If(self):
        
        self.text += f"\t\tif condition goto L{self.tag_counter + 1}\n"
        
    def addToTemp(self):
        self.temp_counter += 1
        if self.temp_counter > 6:
            self.resetTemp()

    def resetTemp(self):
        self.temp_counter = 0

    def build(self):

        self.text += "EOF"

        try:
            with open(self.filename, 'w') as file:
                file.write(self.text)

        except:
            print(f"Error abriendo archivo {self.filename}")

