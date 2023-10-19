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
        self.symbolTable = symbolTable

        # counters
        self.tag_counter = 0
        self.temp_counter = 0 
        self.goto_if = 0
        self.goto_while = 0
        self.lastStatement = ""
        self.param_num = 0

        # stacks
        self.temp_stack = []

        # other variables
        self.currentClass = ""

        self.position = []
        self.let = 0

        # self.functions = {}
        self.registers = {}
        self.functions = {}
        self.classes = {}

        self.genSP(self.symbolTable)

    # ================================================================================
    # visitor
    # ================================================================================

    def visitStart(self, ctx:YAPLParser.StartContext):
        # print("#start")
        self.finalText = ""
        stages = ctx.class_def()
        for stage in stages:
            self.finalText += self.visit(stage)

        # fin del archivo
        self.finalText += "EOF"

        try:
            with open(self.filename, 'w') as file:
                file.write(self.finalText)

        except:
            print(f"El archivo {self.filename} no se pudo abrir")

        print("\n=================")
        # print(self.functions, "\n")
        for r in self.registers:
            print(r)
            print(self.registers[r])
        print(self.temp_stack)
        # print(self.classes)

    
    def visitDefClass(self, ctx:YAPLParser.DefClassContext):
        # print("#defClass")
        retText = ""

        self.temp_counter = 0
        self.temp_stack = []

        self.currentClass = ctx.TYPE(0).getText()
        retText += f"CLASS {self.currentClass}\n"

        # iniciar diccionarios de diccioanrios
        self.functions[self.currentClass] = {}
        # self.registers[self.currentClass] = {}

        content = ""

        # si hereda de otra clase
        if ctx.INHERITS():
            inherits_ = ctx.TYPE(1).getText()
            # print("inherits_")

            if inherits_ != "IO":
                # copiar
                self.functions[self.currentClass] = self.functions[inherits_]
                # self.registers[self.currentClass] = self.registers[inherits_]
                
                content += self.classes[inherits_] + "\n"

                # reemplazar nombre
                old = f"\t{inherits_}."
                new = f"\t{self.currentClass}."
                content = content.replace(old, new)

        for feature in ctx.feature():
            content += self.visit(feature)

        # lo guardamos para futura referencia y herencia
        self.classes[self.currentClass] = content

        retText += content

        retText += "EOC\n"

        return retText
    
    def visitDefFunc(self, ctx:YAPLParser.DefFuncContext):
        # print("#defFun")
        retText = ""

        id = ctx.ID().getText()
        self.currentFun = id
        print("id ", id)
        retText += f"\t{self.currentClass}.{id}\n"

        self.parNames = {}

        for i, formal in enumerate(ctx.formal()):
            self.param_num = i
            retText += self.visit(formal)

        ret_ = self.visit(ctx.expr())
        retText += ret_

        # almacenar
        self.functions[self.currentClass][id] = ret_

        # valor de retorno
        print("type ", ctx.TYPE().getText(), ctx.TYPE().getText().upper())
        if (ctx.TYPE().getText().upper() == "SELF_TYPE" or ctx.TYPE().getText().upper() == "VOID"):
            retText += f"\t\tRETURN\n"
        else:
            retText += f"\t\tRETURN {self.lastStatement}\n"

        retText += f"\tEND FUNC {id}\n"

        return retText
    
    def visitDefAssign(self, ctx:YAPLParser.DefAssignContext):
        # print("#defAssign")
        retText = ""

        # solamente hacer algo si la variable es definida
        if ctx.expr():
            name = ""
            exprText = ctx.expr().getText()
            if ctx.expr().getChildCount() > 1:
                print("> 1")
                # revisar si es un string
                if exprText[:1] == '"':
                    print("string")
                    name = ctx.expr().getText()

                else:
                    # revisar si el parámetro existe
                    bool_ = False
                    try:
                        bool_ =  ctx.expr().getText() in self.parNames.keys()
                    except:
                        0

                    if bool_:
                        name = self.parNames[ctx.expr().getText()]

                    else:
                        retText += self.visit(ctx.expr())
                        # print("deffasin retTExt ", retText)
                        if len(self.temp_stack) > 0:
                            name = self.temp_stack.pop()
                        else:
                            name = "tt"

            else:
                print("1")
                text_ = ctx.expr().getText()
                if text_ in self.registers[self.currentClass].keys():
                    name = self.registers[self.currentClass][text_]
                else:
                    name = text_
                retText += self.visit(ctx.expr())

            # obtener desplazamiento
            id_ = ctx.ID().getText()
            type_ = ctx.TYPE().getText()
            
            disp = self.symbolTable.get_displacement(id = id_, addType = type_, addParent = self.currentClass)
            var = f"GP[{disp}]"

            self.lastStatement = var

            retText += f"\t\tLW {var}, {name}\n"

        return retText
    
    def visitFormalAssign(self, ctx:YAPLParser.FormalAssignContext):
        # print("#formalAssign")
        retText = ""

        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)

        # guardar
        self.parNames[ctx.ID().getText()] = temp_

        id_f = ctx.ID().getText()
        pos_ = self.registers[self.currentClass][id_f]
        retText += f"\t\tPARAM {pos_}, P{self.param_num}\n"

        self.lastStatement = temp_

        return retText
    
    def visitDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        # print("#dispatchExplicit")
        retText = ""

        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr(0).getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        

        id = ctx.ID().getText()

        paramlist = []

        for i, expr in enumerate(ctx.expr()):
            if i == 0:
                continue # nos saltamos el primer expr
            # print("in expr°")
            par = ""
            exprText = expr.getText()
            # print("exprText ", exprText)
            if expr.getChildCount() > 1: 
                # print(">>1")
                retText += self.visit(expr)
                if len(self.temp_stack)> 0:
                    par = self.temp_stack.pop()
                else: 
                    par = "tt"
            else:
                # print("==1")
                # revisar si está en la lista
                if exprText in self.registers[self.currentClass].keys():
                    par = self.registers[self.currentClass][exprText]
                else: 
                    par = exprText
            
            if par != "":
                paramlist.append(par)

        for p in paramlist:
            retText += f"\t\tPARAM {p}\n"

        # print("info ", id, ", ", self.currentClass)
        row1 = self.symbolTable.get_cell(id= ctx.ID().getText())
        # print("row ", row1)
        bClass = ""

        retText += f"\t\tCALL {p_iz}.{id}, {len(paramlist)}\n"

        # if (not (row[1].upper() == "SELF_TYPE" or row[1].upper() == "VOID")):
        name = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(name)

        if (not (
            row1[1].upper() == "SELF_TYPE" or 
            row1[1].upper() == "VOID" or 
            row1[1].upper() == "OBJECT"
            )):
            
            retText += f"\t\tLW {name}, RET\n"

            self.lastStatement = name

        self.lastStatement = name

        return retText
    
    def visitDispatchImplicit(self, ctx:YAPLParser.DispatchImplicitContext):
        # print("#dispatchImplicit")
        retText = ""

        id = ctx.ID().getText()

        paramlist = []

        for expr in ctx.expr():
            # print("in expr°")
            par = ""
            exprText = expr.getText()
            # print("exprText ", exprText)
            if expr.getChildCount() > 1: 
                # # print(">>1")
                retText += self.visit(expr)
                if len(self.temp_stack)> 0:
                    par = self.temp_stack.pop()
                else: 
                    par = "tt"
            else:
                # # print("==1")
                # revisar si está en la lista
                if exprText in self.registers[self.currentClass].keys():
                    par = self.registers[self.currentClass][exprText]
                else: 
                    par = exprText
            
            if par != "":
                paramlist.append(par)


        for p in paramlist:
            retText += f"\t\tPARAM {p}\n"

        row1 = self.symbolTable.get_cell(id= ctx.ID().getText())
        # print("row1 ", row1)
        retText += f"\t\tCALL {row1[4]}.{id}, {len(paramlist)}\n"

        if (not (
            row1[1].upper() == "SELF_TYPE" or 
            row1[1].upper() == "VOID" or 
            row1[1].upper() == "OBJECT"
            )):
            name = f"t{self.temp_counter}"
            self.addToTemp()
            self.temp_stack.append(name)
            retText += f"\t\tLW {name}, RET\n"

            self.lastStatement = name

        return retText
    
    def visitDispatchAttribute(self, ctx:YAPLParser.DispatchAttributeContext):
        # print("#dispatchAttribute")
        retText = ""

        # parte izquierda
        p_iz = ""
        if ctx.expr().getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr())
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr().getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        id = ctx.ID().getText()

        # print("info ", id, ", ", self.currentClass)
        row = self.symbolTable.get_cell(id= ctx.expr().getText(), addParent = self.currentClass)
        print(row)
        if row:
            id = self.registers[row[1]][id]
        
        # print("row ", row1)
        bClass = ""

        retText += f"\t\tCALL {p_iz}.{id}, 0\n"

        # if (not (row[1].upper() == "SELF_TYPE" or row[1].upper() == "VOID")):
        name = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(name)

        if (not (
            row[1].upper() == "SELF_TYPE" or 
            row[1].upper() == "VOID" or 
            row[1].upper() == "OBJECT"
            )):
            
            retText += f"\t\tLW {name}, RET\n"

            self.lastStatement = name

        self.lastStatement = name

        return retText
    
    def visitAssignment(self, ctx:YAPLParser.AssignmentContext):
        # print("#assignment")
        # print("ass ", ctx.getText())
        retText = ""
        
        name = ""
        exprText = ctx.expr().getText()
        if ctx.expr().getChildCount() > 1:
            # revisar si es un string
            if exprText[:1] == '"':
                print("string")
                name = ctx.expr().getText()

            else:
                # revisar si el parámetro existe
                bool_ = False
                try:
                    bool_ =  ctx.expr().getText() in self.parNames.keys()
                except:
                    0

                if bool_:
                    name = self.parNames[ctx.expr().getText()]

                else:
                    retText += self.visit(ctx.expr())
                    # print("deffasin retTExt ", retText)
                    if len(self.temp_stack) > 0:
                        name = self.temp_stack.pop()
                    else:
                        name = "tt"

        else:
            text_ = ctx.expr().getText()
            if text_ in self.registers[self.currentClass].keys():
                name = self.registers[self.currentClass][text_]
                print(f"\n{text_}, {name}\n")
            else:
                name = text_
            retText += self.visit(ctx.expr())

        # obtener desplazamiento
        id_ = ctx.ID().getText()
        disp = self.symbolTable.get_displacement(id = id_, addParent = self.currentClass)
        var = f"SP[{disp}]"
        self.lastStatement = var

        retText += f"\t\tLW {var}, {name}\n"
        

        return retText
    
    def visitIf(self, ctx:YAPLParser.IfContext):
        # print("#if")
        retText = ""

        # visitar la condición
        retText += self.visit(ctx.expr(0))

        temp_ = ""
        if len(self.temp_stack) > 0:
            temp_ = self.temp_stack.pop()
        else:
            temp_ = "tt"

        # obtener contadores
        if_ = self.goto_if
        self.goto_if += 1

        retText += f"\t\tIF {temp_} < 0 GOTO L_TRUE_{if_}\n"
        retText += f"\t\tGOTO L_FALSE_{if_}\n"

        # caso real
        retText += f"L_TRUE_{if_}:\n"
        retText += self.visit(ctx.expr(1))
        retText += f"\t\tGOTO L_IF_END_{if_}\n"

        # caso falso 
        retText += f"L_FALSE_{if_}:\n"   
        retText += self.visit(ctx.expr(2))
        retText += f"\t\tGOTO L_IF_END_{if_}\n"

        # continuar con el resto del codigo
        retText += f"L_IF_END_{if_}:\n"

        return retText
    
    def visitWhile(self, ctx:YAPLParser.WhileContext):
        # print("#while")
        retText = ""

        # guardar las etiquetas a usar
        loop_ = f"L_LOOP_{self.goto_while}"
        end_ = F"L_LOOP_END_{self.goto_while}"

        # agregar a la etiqueta de loop
        self.goto_while += 1

        retText += f"\t\tGOTO {loop_}\n"
        retText += loop_ + ":\n"

        # evaluar la expresión de la condición
        # parte 
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            p_iz = ctx.expr(0).getText()
            print("p_iz ", p_iz, " ", ctx.getText())
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        

        retText += f"\t\tIF {p_iz} < 0 GOTO {end_}\n"

        # hacer lo de adentro 
        # print("res ", type(ctx.expr(1)))
        retText += self.visit(ctx.expr(1))

        retText += f"\t\tGOTO {loop_}\n"
        retText += end_ + ":\n"

        return retText
    
    def visitBlock(self, ctx:YAPLParser.BlockContext):
        # print("#block")
        retText = ""

        for expr in ctx.expr():
            retText += self.visit(expr)

        return retText
    
    def visitLetId(self, ctx:YAPLParser.LetIdContext):
        # print("#letId")
        retText = ""
        
        trips = []

        # parte del let 
        cant = ctx.getChildCount()
        trip = []
        for i,  ch in enumerate(ctx.getChildren()):
            if 0 < i < cant - 1:
                # print(ch.getText())
                if ch.getText() == ',' or ch.getText().lower() == 'in':
                    trips.append(trip)
                    trip = []
                else:
                    trip.append(ch)


        for t in trips: 
            if len(t) == 5:
                # se le ha asignado algo 
                expr = t[4]
                exprText = expr.getText()
                if expr.getChildCount() > 1:
                    # print("> 1")
                    # revisar si es un string
                    if exprText[:1] == '"':
                        print("string")
                        name = expr.getText()

                    else:
                        # revisar si el parámetro existe
                        bool_ = False
                        try:
                            bool_ =  expr.getText() in self.parNames.keys()
                        except:
                            0

                        if bool_:
                            name = self.parNames[expr.getText()]

                        else:
                            retText += self.visit(expr)
                            # print("letid retTExt ", retText)
                            if len(self.temp_stack) > 0:
                                name = self.temp_stack.pop()
                            else:
                                name = "tt"

                else:
                    print("1")
                    text_ = expr.getText()
                    if text_ in self.registers[self.currentClass].keys():
                        name = self.registers[self.currentClass][text_]
                    else:
                        name = text_
                    retText += self.visit(expr)

                # obtener desplazamiento
                id_ = t[0].getText()
                disp = self.symbolTable.get_displacement(id = id_, addParent = self.currentClass)
                var = f"SP[{disp}]"
                self.lastStatement = var

                retText += f"\t\tLW {var}, {name}\n"

        # parte del in
        print("in")
        retText += self.visit(ctx.expr(len(ctx.expr()) - 1))

        return retText
    
    def visitNew(self, ctx:YAPLParser.NewContext):
        # print("#new")
        retText = ""

        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)
        retText += f"\t\tLW {temp_}, {ctx.TYPE().getText()}\n"

        self.lastStatement = temp_

        return retText
    
    def visitNegative(self, ctx:YAPLParser.NegativeContext):
        # print("#negative")
        retText = ""

        # parte 
        p_iz = ""
        if ctx.expr().getChildCount() > 1:
            # # print(">> 1")
            retText += self.visit(ctx.expr())
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr().getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)

        retText += f"\t\tNEG {temp_}, {p_iz}\n"
        self.lastStatement = temp_
        
        return retText
    
    def visitIsvoid(self, ctx:YAPLParser.IsvoidContext):
        # print("#isvoid")
        retText = ""

        return retText
    
    def visitTimes(self, ctx:YAPLParser.TimesContext):
        # print("#times")
        retText = ""

        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # # print(">> 1")
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr(0).getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0: # TODO
                p_der = self.temp_stack.pop()
            else:
                retText += self.visit(ctx.expr(1))
                if len(self.temp_stack) > 0:
                    p_der = self.temp_stack.pop()
                else: 
                    p_der = "tt"
        else: 
            p_der = ctx.expr(1).getText()
            # revisar si está en el diccionario de registros
            if p_der in self.registers[self.currentClass].keys():
                p_der = self.registers[self.currentClass][p_der]

        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)

        retText += f"\t\tMULT {temp_}, {p_iz}, {p_der}\n"
        self.lastStatement = temp_

        return retText
    
    def visitDiv(self, ctx:YAPLParser.DivContext):
        # print("#div")
        retText = ""

        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr(0).getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0: # TODO
                p_der = self.temp_stack.pop()
            else:
                retText += self.visit(ctx.expr(1))
                if len(self.temp_stack) > 0:
                    p_der = self.temp_stack.pop()
                else: 
                    p_der = "tt"
        else: 
            p_der = ctx.expr(1).getText()
            # revisar si está en el diccionario de registros
            if p_der in self.registers[self.currentClass].keys():
                p_der = self.registers[self.currentClass][p_der]

        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)

        retText += f"\t\tDIV {temp_}, {p_iz}, {p_der}\n"
        self.lastStatement = temp_

        return retText
    
    def visitPlus(self, ctx:YAPLParser.PlusContext):
        # print("#plus")
        retText = ""

        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr(0).getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0: # TODO
                p_der = self.temp_stack.pop()
            else:
                retText += self.visit(ctx.expr(1))
                if len(self.temp_stack) > 0:
                    p_der = self.temp_stack.pop()
                else: 
                    p_der = "tt"
        else: 
            p_der = ctx.expr(1).getText()
            # revisar si está en el diccionario de registros
            if p_der in self.registers[self.currentClass].keys():
                p_der = self.registers[self.currentClass][p_der]

        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)

        retText += f"\t\tADD {temp_}, {p_iz}, {p_der}\n"
        self.lastStatement = temp_

        return retText
    
    def visitMinus(self, ctx:YAPLParser.MinusContext):
        # print("#minus")
        retText = ""

        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr(0).getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0: # TODO
                p_der = self.temp_stack.pop()
            else:
                retText += self.visit(ctx.expr(1))
                if len(self.temp_stack) > 0:
                    p_der = self.temp_stack.pop()
                else: 
                    p_der = "tt"
        else: 
            p_der = ctx.expr(1).getText()
            # revisar si está en el diccionario de registros
            if p_der in self.registers[self.currentClass].keys():
                p_der = self.registers[self.currentClass][p_der]

        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)

        retText += f"\t\tSUB {temp_}, {p_iz}, {p_der}\n"
        self.lastStatement = temp_

        return retText
    
    def visitLessThanOrEqual(self, ctx:YAPLParser.LessThanContext):
        # print("#lessThanOrEqual")
        retText = ""

        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr(0).getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0: # TODO
                p_der = self.temp_stack.pop()
            else:
                retText += self.visit(ctx.expr(1))
                if len(self.temp_stack) > 0:
                    p_der = self.temp_stack.pop()
                else: 
                    p_der = "tt"
        else: 
            p_der = ctx.expr(1).getText()
            # revisar si está en el diccionario de registros
            if p_der in self.registers[self.currentClass].keys():
                p_der = self.registers[self.currentClass][p_der]

        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)

        retText += f"\t\tSLE {temp_}, {p_iz}, {p_der}\n"
        self.lastStatement = temp_

        return retText
    
    def visitLessThan(self, ctx:YAPLParser.LessThanOrEqualContext):
        # print("#lessThan")
        retText = ""

        # parte izquierda
        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr(0).getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0: # TODO
                p_der = self.temp_stack.pop()
            else:
                retText += self.visit(ctx.expr(1))
                if len(self.temp_stack) > 0:
                    p_der = self.temp_stack.pop()
                else: 
                    p_der = "tt"
        else: 
            p_der = ctx.expr(1).getText()
            # revisar si está en el diccionario de registros
            if p_der in self.registers[self.currentClass].keys():
                p_der = self.registers[self.currentClass][p_der]

        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)

        retText += f"\t\tSLT {temp_}, {p_iz}, {p_der}\n"
        self.lastStatement = temp_

        return retText
    
    def visitGreaterThan(self, ctx:YAPLParser.GreaterThanContext):
        # print("#greaterThan")
        retText = ""

        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr(0).getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0: # TODO
                p_der = self.temp_stack.pop()
            else:
                retText += self.visit(ctx.expr(1))
                if len(self.temp_stack) > 0:
                    p_der = self.temp_stack.pop()
                else: 
                    p_der = "tt"
        else: 
            p_der = ctx.expr(1).getText()
            # revisar si está en el diccionario de registros
            if p_der in self.registers[self.currentClass].keys():
                p_der = self.registers[self.currentClass][p_der]

        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)

        retText += f"\t\tSGT {temp_}, {p_iz}, {p_der}\n"
        self.lastStatement = temp_

        return retText
    
    def visitGreaterThanOrEqual(self, ctx:YAPLParser.GreaterThanOrEqualContext):
        # print("#greaterThanOrEqual")
        retText = ""

        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr(0).getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0: # TODO
                p_der = self.temp_stack.pop()
            else:
                retText += self.visit(ctx.expr(1))
                if len(self.temp_stack) > 0:
                    p_der = self.temp_stack.pop()
                else: 
                    p_der = "tt"
        else: 
            p_der = ctx.expr(1).getText()
            # revisar si está en el diccionario de registros
            if p_der in self.registers[self.currentClass].keys():
                p_der = self.registers[self.currentClass][p_der]

        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)

        retText += f"\t\tSGE {temp_}, {p_iz}, {p_der}\n"
        self.lastStatement = temp_

        return retText
    
    def visitEqual(self, ctx:YAPLParser.EqualContext):
        # print("#equal")
        retText = ""

        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr(0).getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0: # TODO
                p_der = self.temp_stack.pop()
            else:
                retText += self.visit(ctx.expr(1))
                if len(self.temp_stack) > 0:
                    p_der = self.temp_stack.pop()
                else: 
                    p_der = "tt"
        else: 
            p_der = ctx.expr(1).getText()
            # revisar si está en el diccionario de registros
            if p_der in self.registers[self.currentClass].keys():
                p_der = self.registers[self.currentClass][p_der]

        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)
        self.lastStatement = temp_

        retText += f"\t\tSEQ {temp_}, {p_iz}, {p_der}\n"
        self.lastStatement = temp_
        
        return retText
    
    def visitAnd(self, ctx:YAPLParser.AndContext):
        # print("#and")
        retText = ""

        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr(0).getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0: # TODO
                p_der = self.temp_stack.pop()
            else:
                retText += self.visit(ctx.expr(1))
                if len(self.temp_stack) > 0:
                    p_der = self.temp_stack.pop()
                else: 
                    p_der = "tt"
        else: 
            p_der = ctx.expr(1).getText()
            # revisar si está en el diccionario de registros
            if p_der in self.registers[self.currentClass].keys():
                p_der = self.registers[self.currentClass][p_der]

        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)

        retText += f"\t\tAND {temp_}, {p_iz}, {p_der}\n"
        self.lastStatement = temp_

        return retText
    
    def visitOr(self, ctx:YAPLParser.OrContext):
        # print("#or")
        retText = ""

        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr(0).getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0: # TODO
                p_der = self.temp_stack.pop()
            else:
                retText += self.visit(ctx.expr(1))
                if len(self.temp_stack) > 0:
                    p_der = self.temp_stack.pop()
                else: 
                    p_der = "tt"
        else: 
            p_der = ctx.expr(1).getText()
            # revisar si está en el diccionario de registros
            if p_der in self.registers[self.currentClass].keys():
                p_der = self.registers[self.currentClass][p_der]

        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)

        retText += f"\t\tOR {temp_}, {p_iz}, {p_der}\n"
        self.lastStatement = temp_

        return retText
    
    def visitNeg(self, ctx:YAPLParser.NegContext):
        # print("#neg")
        retText = ""

        # parte 
        p_iz = ""
        if ctx.expr().getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr())
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr().getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        temp_ = f"t{self.temp_counter}"
        self.addToTemp()
        self.temp_stack.append(temp_)

        retText += f"\t\tNOT {temp_}, {p_iz}\n"
        self.lastStatement = temp_

        return retText

    def visitParens(self, ctx:YAPLParser.ParensContext):
        # print("#parens")
        retText = ""
        # print("par ", ctx.getText())

        # parte 
        # print("expr ", ctx.expr().getText())
        p_iz = ""
        if ctx.expr().getChildCount() > 1:
            # print(">> 1")
            retText += self.visit(ctx.expr())
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # print("== 1")
            p_iz = ctx.expr().getText()
            # revisar si está en el diccionario de registros
            if p_iz in self.registers[self.currentClass].keys():
                p_iz = self.registers[self.currentClass][p_iz]
        
        # volver a meter el valor al stack
        self.temp_stack.append(p_iz)
        
        # temp_ = f"t{self.temp_counter}"
        # self.addToTemp()
        # self.temp_stack.append(temp_)

        # retText += f"\t\tLW {temp_}, {p_iz}\n"
        # self.lastStatement = temp_

        return retText
    
    def visitId(self, ctx:YAPLParser.IdContext):
        # print("#id") 
        retText = ""
        pos_ = self.registers[self.currentClass][ctx.getText()]
        self.lastStatement = pos_
        return retText
    
    def visitInt(self, ctx:YAPLParser.IntContext):
        # print("#int")
        retText = ""
        self.lastStatement = ctx.getText()

        return retText

    def visitString(self, ctx:YAPLParser.StringContext):
        # print("#string")
        retText = ""
        self.lastStatement = ctx.getText()

        return retText
    
    def visitBoolean(self, ctx:YAPLParser.BooleanContext):
        # print("#boolean")
        retText = ""
        self.lastStatement = ctx.getText()

        self.temp_stack.append(ctx.getText())
        
        return retText
    
    def visitSelf(self, ctx:YAPLParser.SelfContext):
        # print("#self")
        retText = ""

        return retText
    

    # ================================================================================
    # otras funciones
    # ================================================================================

    def addToTemp(self):
        self.temp_counter += 1
        if self.temp_counter > 8:
            self.resetTemp()

    def resetTemp(self):
        self.temp_counter = 0

    def genSP(self, st:Table):
        # conseguir todas las clases 
        noClases = ["object", "self_type", "io", "void", "string", "int", "bool"]
        classes = []
        for x in st.columns:
            if x[4].lower() not in noClases and x[4] not in classes:
                classes.append(x[4])
        
        # crear diccionarios individuales
        for c in classes:
            self.registers[c] = {}

        # agregar
        for x in st.columns:
            # print(x[0], x[2], x[8], x[7])
            if (x[2] == "Instance" or x[2] == "Variable" or x[2] == "Param") and x[4].lower() not in noClases:
                # print("yes")
                if (x[8] == "Global"):
                    self.registers[x[4]][x[0]] = f"GP[{x[7]}]"
                elif (x[8] == "Local"):
                    self.registers[x[4]][x[0]] = f"SP[{x[7]}]"
                    # print("Agregado!")