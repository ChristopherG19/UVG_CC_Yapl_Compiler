from antlr4 import *
from YAPLLexer import YAPLLexer
from YAPLParser import YAPLParser
from YAPLVisitor import YAPLVisitor
from utils.node import *
from utils.symbolTable import *
import re

class CodigoIntermedio(YAPLVisitor):

    def __init__(self, fileName:str, symbolTable:Table()) -> None:

        self.filename = fileName
        self.text = ""
        self.symbolTable = symbolTable  

        # counters
        self.tag_counter = 0
        self.temp_counter = 0
        self.goto_true = 0
        self.goto_false = 0
        self.goto_end = 0
        self.goto_while = 0
        self.lastStatement = ""
        
        #stacks
        self.temp_stack = []

        #
        self.currentClass = ""

        self.functions = {}
        self.registers = {}
        self.classes = {}

        self.inFunction = False

        self.genSP(self.symbolTable)
        # print(self.registers)


    def visitStart(self, ctx:YAPLParser.StartContext):
        # print("#start")
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
        # print(self.functions, "\n")
        print(self.registers, "\n")
        print(self.temp_stack)
        # print(self.classes)


    def visitDefClass(self, ctx:YAPLParser.DefClassContext):
        # print("#defclass")

        self.temp_counter = 0
        self.temp_stack = []

        self.currentClass = ctx.TYPE(0).getText()
        self.text += f"CLASS {self.currentClass}\n"

        #inicializar diccionario de diccionario
        self.functions[self.currentClass] = {}
        self.registers[self.currentClass] = {}

        # copiamos todo si hereda de otra clase
        if ctx.INHERITS():
            inherits_ = ctx.TYPE(1).getText()
            # print("inherits_")

            if inherits_ != "IO":
                # copiar
                self.functions[self.currentClass] = self.functions[inherits_]
                self.registers[self.currentClass] = self.registers[inherits_]
                
                self.text += "\t\t" + self.classes[inherits_] + "\n"

        for feature in ctx.feature():
            self.visit(feature)

        self.text += "EOC\n"

        # copiar al diccionario
        # print("text\n", self.text)
        patron = re.compile(rf'CLASS {self.currentClass}(.*?)EOC', re.DOTALL)
        match_ = re.search(patron, self.text)

        if match_:
            contenido = match_.group(1).strip()
            # print(contenido)
            self.classes[self.currentClass] = contenido

 

    def visitDefFunc(self, ctx:YAPLParser.DefFuncContext):
        # print("#deffun")

        self.inFunction = True

        id = ctx.ID().getText()
        self.text += f"\t{self.currentClass}.{id}\n"

        self.funcText = ""

        self.parNames = {}

        for formal in ctx.formal():
            self.visit(formal)

        self.visit(ctx.expr())

        self.text += self.funcText
        self.functions[self.currentClass][id] = self.funcText

        # print("last statement ", self.lastStatement)
        if (ctx.TYPE().getText() == "SELF_TYPE" or ctx.TYPE().getText() == "VOID"):
            self.text += f"\t\tRETURN\n"
        else:
            self.text += f"\t\tRETURN {self.lastStatement}\n"

        self.text += f"\tEND FUNC {id}\n"

        self.inFunction = False

    
    def visitDefAssign(self, ctx:YAPLParser.DefAssignContext):
        # print("#visitdefassign")

        # se agrega solamente si se define la variable
        if ctx.expr():
            x = ""
            exprText = ctx.expr().getText()
            # print("exprText ", exprText, ctx.expr().getChildCount())
            firstchar = exprText[:1]
            if ctx.expr().getChildCount() > 1:
                # revisar si es un string
                if firstchar == '"':
                    x = ctx.expr().getText()
                else: 
                    # revisar si el parámetro existe
                    # print(ctx.expr().getText())
                    bool_ = False
                    try:
                        bool_ =  ctx.expr().getText() in self.parNames.keys()
                    except:
                        0

                    if bool_:
                        x = self.parNames[ctx.expr().getText()]
                    else:
                        temp_ = "t" + str(self.temp_counter)
                        self.addToTemp()
                        self.temp_stack.append(temp_)
                        self.visit(ctx.expr())
                        # print("assi ", ctx.expr().getText())
                        x = temp_
                    
            else: 
                text_ = ctx.expr().getText()
                if text_ in self.registers[self.currentClass].keys():
                    x = self.registers[self.currentClass][text_]
                else:
                    x = text_
                self.visit(ctx.expr())
            
            # agregar al registro 
            id_ = ctx.ID().getText()
            type_ = ctx.TYPE().getText()
            # print("row ", self.symbolTable.get_cell(id = id_, addType = type_, addParent = self.currentClass))
            disp = self.symbolTable.get_displacement(id = id_, addType = type_, addParent = self.currentClass)

            var = f"SP[{disp}]"
            self.registers[self.currentClass][id_] = var

            if self.inFunction:
                self.funcText += f"\t\tLW {var}, {x}\n"
            else:
                self.text += f"\t\tLW {var}, {x}\n"

            self.lastStatement = var

        else:
            # agregar al registro 
            id_ = ctx.ID().getText()
            type_ = ctx.TYPE().getText()
            # print("row ", self.symbolTable.get_cell(id = id_, addType = type_, addParent = self.currentClass))
            disp = self.symbolTable.get_displacement(id = id_, addType = type_, addParent = self.currentClass)

            var = f"SP[{disp}]"
            self.registers[self.currentClass][id_] = var
        
    
    def visitFormalAssign(self, ctx:YAPLParser.FormalAssignContext):
        # print("#formalassign")

        # print("stack ", self.temp_stack)
        temp_ = ""
        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
        else:
            temp_ = f"t{self.temp_counter}"
            self.addToTemp()

        # guardar
        self.parNames[ctx.ID().getText()] = temp_

        self.funcText += f"\t\tLW {temp_}, P\n"

        self.lastStatement = temp_
         
    
    def visitDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        # print("#dispatchexplicit")

        id = ctx.ID().getText()

        paramslist = []

        for i, expr in enumerate(ctx.expr()):
            if i == 0:
                # saltarse el primer elemento
                continue
            else:
                if expr.getChildCount() > 1:
                    temp = "t" + str(self.temp_counter)
                    self.addToTemp()
                    self.temp_stack.append(temp)
                    paramslist.append(temp)
                    
                else: 
                    # revisar si está en la lista de registors
                    if expr.getText() in self.registers[self.currentClass].keys():
                        paramslist.append(self.registers[self.currentClass][expr.getText()])
                    else:
                        paramslist.append(expr.getText())
                self.visit(expr)

        for p in paramslist:
            # print("p ", p)
            self.funcText += f"\t\tPARAM {p}\n"

        bClass = ""
        row = self.symbolTable.get_cell(id= ctx.ID().getText())
        # if row:
        #     print("row ", row)
        # else:
        #     print("no se encontró la row!")

        self.funcText += f"\t\tCALL {bClass}.{id}, {len(paramslist)}\n"

        temp_ = ""
        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            self.funcText += f"\t\tLW {temp_}, R\n"
        else:
            temp_ = f"t{self.temp_counter}"
            self.funcText += f"\t\tLW t{self.temp_counter}, R\n"
            self.addToTemp()

        self.lastStatement = temp_        
         

    def visitDispatchImplicit(self, ctx:YAPLParser.DispatchImplicitContext):
        # print("#dispatchimplicit")

        id = ctx.ID().getText()

        paramslist = []

        for expr in ctx.expr():
            if expr.getChildCount() > 1:
                temp = "t" + str(self.temp_counter)
                self.addToTemp()
                self.temp_stack.append(temp)
                paramslist.append(temp)
                
            else: 
                # revisar si está en la lista de registors
                if expr.getText() in self.registers[self.currentClass].keys():
                    paramslist.append(self.registers[self.currentClass][expr.getText()])
                else:
                    paramslist.append(expr.getText())
            self.visit(expr)

        for p in paramslist:
            # print("p ", p)
            if self.inFunction:
                self.funcText += f"\t\tPARAM {p}\n"
            else: 
                self.text += f"\t\tPARAM {p}\n"

        if self.inFunction:
            self.funcText += f"\t\tCALL {self.currentClass}.{id}, {len(paramslist)}\n"
        else:
            self.text += f"\t\tCALL {self.currentClass}.{id}, {len(paramslist)}\n"

        temp_ = ""
        if len(self.temp_stack) > 0:
            if self.inFunction:
                temp_ = self.temp_stack.pop()
                self.funcText += f"\t\tLW {temp_}, R\n"
            else: 
                temp_ = self.temp_stack.pop()
                self.text += f"\t\tLW {temp_}, R\n"
        else:
            temp_ = f"t{self.temp_counter}"
            if self.inFunction:
                self.funcText += f"\t\tLW t{self.temp_counter}, R\n"
            else:
                self.text += f"\t\tLW t{self.temp_counter}, R\n"
            self.addToTemp()

        self.lastStatement = temp_
         

    def visitDispatchAttribute(self, ctx:YAPLParser.DispatchAttributeContext):
        # print("#dispatchattribute")
        # print(ctx.getText())
        # print("att ", ctx.expr().getText())
        # print(self.temp_stack)

        # if (self.inFunction):
        #     self.funcText += f"\t\t\n"
        # else:
        #     self.text += f"\t\t\n"

        self.visit(ctx.expr())
         
    
    def visitIf(self, ctx:YAPLParser.IfContext):
        # print("#if")

        # evaluar expresión de la condición 
        temp_ = "t" + str(self.temp_counter) # creamos una temporal
        self.addToTemp()
        self.temp_stack.append(temp_)
        self.visit(ctx.expr(0))
        # print("if exp1 ", ctx.expr(0).getText())

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
        self.funcText += f"\t\tGOTO L_IF_END_{end_}\n"

        # caso falso 
        self.funcText += f"L_FALSE_{false_}:\n"   
        self.visit(ctx.expr(2))
        self.funcText += f"\t\tGOTO L_IF_END_{end_}\n"

        # continuar con el resto del codigo
        self.funcText += f"L_IF_END_{end_}:\n"
 
    
    def visitWhile(self, ctx:YAPLParser.WhileContext):
        # print("#while")

        # etiquetas
        loop_ = f"L_LOOP_{self.goto_while}"
        end_ = f"L_LOOP_END_{self.goto_while}"

        self.goto_while += 1

        self.funcText += f"\t\tGOTO {loop_}\n"
        self.funcText += loop_ + ":\n"

        # evaluar expresión de la condición 
        temp_ = "t" + str(self.temp_counter) # creamos una temporal
        self.addToTemp
        self.temp_stack.append(temp_)
        self.visit(ctx.expr(0))
        # print("if exp1 ", ctx.expr(0).getText())

        self.funcText += f"\t\tIF {temp_} = 0 GOTO {end_}\n"
        # self.funcText += f"\t\tGOTO {end_}"

        

        self.visit(ctx.expr(1))

        self.funcText += f"\t\tGOTO {loop_}\n"
        self.funcText += end_ + ":\n"
   
    
    def visitBlock(self, ctx:YAPLParser.BlockContext):
        # print("#block")
        for expr in ctx.expr():
            # print("exp block: ", expr.getText())
            self.visit(expr)
    
    def visitLetId(self, ctx:YAPLParser.LetIdContext):
        # print("#letId")

        trips = []

        children = ctx.getChildren()
        cant = ctx.getChildCount()
        trip = []
        for i,  ch in enumerate(children):
            if 0 < i < cant - 1:
                # print(ch.getText())
                if ch.getText() == ',' or ch.getText().lower() == 'in':
                    trips.append(trip)
                    trip = []
                else:
                    trip.append(ch)

        # print(trips)

        for t in trips:
            if len(t) == 5:
                # se le ha asignado algo
                expr = t[4]
                x = ""
                exprText = expr.getText()
                # print("exprText ", exprText, expr.getChildCount())
                firstchar = exprText[:1]
                if expr.getChildCount() > 1:
                    # revisar si es un string
                    if firstchar == '"':
                        x = expr.getText()
                    else: 
                        # revisar si el parámetro existe
                        if expr.getText() in self.parNames.keys():
                            x = self.parNames[expr.getText()]
                        else:
                            temp_ = "t" + str(self.temp_counter)
                            self.addToTemp()
                            self.temp_stack.append(temp_)
                            self.visit(expr)
                            # print("assi ", expr.getText())
                            x = temp_
                        
                else: 
                    text_ = expr.getText()
                    if text_ in self.registers[self.currentClass].keys():
                        x = self.registers[self.currentClass][text_]
                    else:
                        x = text_
                    self.visit(expr)
                
                # agregar al registro 
                id_ = t[0].getText()
                # print("row ", self.symbolTable.get_cell(id = id_, addParent = self.currentClass))
                disp = self.symbolTable.get_displacement(id = id_, addParent = self.currentClass)

                var = f"SP[{disp}]"
                self.registers[self.currentClass][id_] = var

                if self.inFunction:
                    self.funcText += f"\t\tLW {var}, {x}\n"
                else:
                    self.text += f"\t\tLW {var}, {x}\n"

                self.lastStatement = var


        # visitar el último expr dentro del in
        self.visit(ctx.expr(len(ctx.expr()) - 1))


    
    def visitNew(self, ctx:YAPLParser.NewContext):
        # print("#new")

        temp_ = ""
        line_ = ""
        # definir línea
        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line_ = f"\t\tLW {temp_}"
        else:
            temp_ = f"t{self.temp_counter}"
            line_ = f"\t\tLW {temp_}"
            self.addToTemp()

        self.lastStatement = temp_

        line_ += f", {ctx.TYPE().getText()}\n"

        # añadir a donde corresponde
        if self.inFunction:
            self.funcText += line_
        else: 
            self.text += line_
     
    
    def visitNegative(self, ctx:YAPLParser.NegativeContext):
        # print("#negative")

        # print(ctx.getText())

        line = "\t\tNEG "

        # print("stack ", self.temp_stack)
        temp_ = ""

        # 
        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line += temp_ + ", "
        else: 
            temp_ = "t" + str(self.temp_counter)
            line += temp_ + ", "
            self.addToTemp()

        # parte 
        if ctx.expr().getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr())
            line += leftTemp
        else:
            self.visit(ctx.expr())
            # print("rest ", ctx.expr().getText())
            if ctx.expr().getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr().getText()]} "
            else:
                line += f"{ctx.expr().getText()} "
                # print("Gt ", ctx.expr().getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"

        self.lastStatement = temp_
        
    
    def visitIsVoid(self, ctx:YAPLParser.IsvoidContext):
        # print("#isvoid")

        self.visit(ctx.expr())
        
    
    def visitTimes(self, ctx:YAPLParser.TimesContext):

        line = "\t\tMULT "

        # print("stack ", self.temp_stack)
        temp_ = ""

        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line += temp_ + ", "
        else: 
            temp_ = "t" + str(self.temp_counter)
            line += temp_ + ", "
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
            if ctx.expr(0).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(0).getText()]}, "
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
            # print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(1).getText()]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                # print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"

        self.lastStatement = temp_
        
    
    def visitDiv(self, ctx:YAPLParser.DivContext):
        # print("#div")

        line = "\t\tDIV "

        # print("stack ", self.temp_stack)
        temp_ = ""

        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line += temp_ + ", "
        else: 
            temp_ = "t" + str(self.temp_counter)
            line += temp_ + ", "
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
            if ctx.expr(0).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(0).getText()]}, "
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
            # print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(1).getText()]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                # print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"

        self.lastStatement = temp_
        
    
    def visitPlus(self, ctx:YAPLParser.PlusContext):
        # print("#plus")

        line = "\t\tADD "

        # print("stack ", self.temp_stack)
        temp_ = ""

        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line += temp_ + ", "
        else: 
            temp_ = "t" + str(self.temp_counter)
            line += temp_ + ", "
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
            if ctx.expr(0).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(0).getText()]}, "
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
            # print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(1).getText()]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                # print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"

        self.lastStatement = temp_
        
    
    def visitMinus(self, ctx:YAPLParser.MinusContext):
        # print("#minus")

        line = "\t\tSUB "

        # print("stack ", self.temp_stack)
        temp_ = ""

        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line += temp_ + ", "
        else: 
            temp_ = "t" + str(self.temp_counter)
            line += temp_ + ", "
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
            if ctx.expr(0).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(0).getText()]}, "
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
            # print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(1).getText()]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                # print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"

        self.lastStatement = temp_
        
    
    def visitLessThanOrEqual(self, ctx:YAPLParser.LessThanOrEqualContext):
        # print("#lessThanorEqual")

        line = "\t\tSLE "

        # print("stack ", self.temp_stack)
        temp_ = ""

        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line += temp_ + ", "
        else: 
            temp_ = "t" + str(self.temp_counter)
            line += temp_ + ", "
            self.addToTemp()

        # parte izquierda
        # print("iz ", ctx.expr(0).getText())
        if ctx.expr(0).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(0))
            line += leftTemp + ", "
        else:
            self.visit(ctx.expr(0))
            # print("rest ", ctx.expr(0).getText())
            if ctx.expr(0).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(0).getText()]}, "
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
            # print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(1).getText()]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                # print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"

        self.lastStatement = temp_
        
    
    def visitLessThan(self, ctx:YAPLParser.LessThanContext):
        # print("#lessThan")

        line = "\t\tSLG "

        # print("stack ", self.temp_stack)
        temp_ = ""

        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line += temp_ + ", "
        else: 
            temp_ = "t" + str(self.temp_counter)
            line += temp_ + ", "
            self.addToTemp()

        # parte izquierda
        print("iz ", ctx.expr(0).getText())
        if ctx.expr(0).getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr(0))
            line += leftTemp + ", "
        else:
            self.visit(ctx.expr(0))
            # print("rest ", ctx.expr(0).getText())
            if ctx.expr(0).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(0).getText()]}, "
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
            # print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(1).getText()]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                # print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"

        self.lastStatement = temp_
        
    
    def visitGreaterThan(self, ctx:YAPLParser.GreaterThanContext):
        # print("#greaterThan")

        line = "\t\tSGT "

        # print("stack ", self.temp_stack)
        temp_ = ""

        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line += temp_ + ", "
        else: 
            temp_ = "t" + str(self.temp_counter)
            line += temp_ + ", "
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
            if ctx.expr(0).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(0).getText()]}, "
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
            # print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(1).getText()]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                # print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"

        self.lastStatement = temp_
        
    
    def visitGreaterThanOrEqual(self, ctx:YAPLParser.GreaterThanOrEqualContext):
        # print("#greaterThanOrEqual")

        line = "\t\tSGE "

        # print("stack ", self.temp_stack)
        temp_ = ""

        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line += temp_ + ", "
        else: 
            temp_ = "t" + str(self.temp_counter)
            line += temp_ + ", "
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
            if ctx.expr(0).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(0).getText()]}, "
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
            # print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(1).getText()]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                # print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"

        self.lastStatement = temp_
        
    
    def visitEqual(self, ctx:YAPLParser.EqualContext):
        # print("#equal")

        line = "\t\tSEQ "

        # print("stack ", self.temp_stack)
        temp_ = ""

        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line += temp_ + ", "
        else: 
            temp_ = "t" + str(self.temp_counter)
            line += temp_ + ", "
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
            if ctx.expr(0).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(0).getText()]}, "
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
            # print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(1).getText()]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                # print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"

        self.lastStatement = temp_
        
    
    def visitAnd(self, ctx:YAPLParser.AndContext):
        # print("#and")

        line = "\t\tAND "

        # print("stack ", self.temp_stack)
        temp_ = ""

        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line += temp_ + ", "
        else: 
            temp_ = "t" + str(self.temp_counter)
            line += temp_ + ", "
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
            if ctx.expr(0).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(0).getText()]}, "
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
            # print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr().getText()]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                # print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"

        self.lastStatement = temp_
        
    
    def visitOr(self, ctx:YAPLParser.OrContext):

        line = "\t\tOR "

        # print("stack ", self.temp_stack)
        temp_ = ""

        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line += temp_ + ", "
        else: 
            temp_ = "t" + str(self.temp_counter)
            line += temp_ + ", "
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
            if ctx.expr(0).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(0).getText()]}, "
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
            # print("rest ", ctx.expr(1).getText())
            if ctx.expr(1).getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr(1).getText()]}"
            else:
                line += f"{ctx.expr(1).getText()}"
                # print("Gt ", ctx.expr(1).getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"

        self.lastStatement = temp_
        
    
    def visitNeg(self, ctx:YAPLParser.NegContext):
        # print("#neg")
        
        # print(ctx.getText())

        line = "\t\tNOT "

        # print("stack ", self.temp_stack)
        temp_ = ""

        # 
        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
            line += temp_ + ", "
        else: 
            temp_ = "t" + str(self.temp_counter)
            line += temp_ + ", "
            self.addToTemp()

        # parte 
        if ctx.expr().getChildCount() > 1:
            leftTemp = "t" + str(self.temp_counter)
            self.addToTemp()
            self.temp_stack.append(leftTemp)
            self.visit(ctx.expr())
            line += leftTemp
        else:
            self.visit(ctx.expr())
            # print("rest ", ctx.expr().getText())
            if ctx.expr().getText() in self.registers[self.currentClass].keys():
                line += f"{self.registers[self.currentClass][ctx.expr().getText()]} "
            else:
                line += f"{ctx.expr().getText()} "
                # print("Gt ", ctx.expr().getText())

        if self.inFunction:
            self.funcText += line + "\n" 
        else:
            self.text += line + "\n"

        self.lastStatement = temp_
        
    
    def visitParens(self, ctx:YAPLParser.ParensContext):
        # print("#parens")
        # no es necesario hacer nada
        self.visit(ctx.expr())
        
    
    def visitAssignment(self, ctx:YAPLParser.AssignmentContext):
        # print("#assignment")

        # se agrega solamente si se define la variable
        if ctx.expr():
            x = ""
            exprText = ctx.expr().getText()
            # print("exprText ", exprText, ctx.expr().getChildCount())
            firstchar = exprText[:1]
            if ctx.expr().getChildCount() > 1:
                # revisar si es un string
                if firstchar == '"':
                    x = ctx.expr().getText()
                else: 
                    # revisar si el parámetro existe
                    if ctx.expr().getText() in self.parNames.keys():
                        x = self.parNames[ctx.expr().getText()]
                    else:
                        temp_ = "t" + str(self.temp_counter)
                        self.addToTemp()
                        self.temp_stack.append(temp_)
                        self.visit(ctx.expr())
                        # print("assi ", ctx.expr().getText())
                        x = temp_
                    
            else: 
                text_ = ctx.expr().getText()
                if text_ in self.registers[self.currentClass].keys():
                    x = self.registers[self.currentClass][text_]
                else:
                    x = text_
                self.visit(ctx.expr())
            
            # agregar al registro 
            id_ = ctx.ID().getText()
            # print("row ", self.symbolTable.get_cell(id = id_, addParent = self.currentClass))
            disp = self.symbolTable.get_displacement(id = id_, addParent = self.currentClass)

            var = f"SP[{disp}]"
            self.registers[self.currentClass][id_] = var

            if self.inFunction:
                self.funcText += f"\t\tLW {var}, {x}\n"
            else:
                self.text += f"\t\tLW {var}, {x}\n"

            self.lastStatement = var
        
    
    def visitID(self, ctx:YAPLParser.IdContext):
        # print("#id")

        self.lastStatement = ctx.getText()
        
    
    def visitInt(self, ctx:YAPLParser.IntContext):
        # print("#int")

        self.lastStatement = ctx.getText()
        
    
    def visitString(self, ctx:YAPLParser.StringContext):
        # print("#string")

        self.lastStatement = ctx.getText()
        
    
    def visitBoolean(self, ctx:YAPLParser.BooleanContext):
        # print("#boolean")

        self.lastStatement = ctx.getText()
        
    
    def visitSelf(self, ctx:YAPLParser.SelfContext):
        # print("#self")

        self.lastStatement = ctx.getText()
        

    def add_If(self):
        
        self.text += f"\t\tif condition goto L{self.tag_counter + 1}\n"
        
    def addToTemp(self):
        self.temp_counter += 1
        if self.temp_counter > 12:
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

    def genSP(self, st:Table):
        # conseguir todas las clases 
        noClases = ["Object", "SELF_TYPE", "IO", "VOID", "String", "Int", "Bool"]
        classes = []
        for x in st.columns:
            if x[4] not in noClases and x[4] not in classes:
                classes.append(x[4])
        
        # crear diccionarios individuales
        for c in classes:
            self.registers[c] = {}

        # agregar
        for x in st.columns:
            if (x[2] == "Instance" or x[2] == "Variable") and x[4] not in noClases:
                # print(x[0], ", ",x[4] , ", ", x[7])
                self.registers[x[4]][x[0]] = f"SP[{x[7]}]"


