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
        self.available_temps_stack = [
            "t8", "t7", "t6",
            "t5", "t4", "t3",
            "t2", "t1", "t0",
            ]

        # other variables
        self.position = [] 
        # 0: current class
        # 1: current function
        # 2: let
        self.let_counter = 1

        # self.functions = {}
        self.registers = {}
        self.functions = {}
        self.classes = {}

        self.genDictionary(self.symbolTable)
        
        print("==================================")
        print(self.registers)
        print("==================================")

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

    
    def visitDefClass(self, ctx:YAPLParser.DefClassContext):
        # print("#defClass")
        retText = ""

        self.temp_counter = 0
        self.temp_stack = []

        # self.position[0] = ctx.TYPE(0).getText()
        self.position.append(ctx.TYPE(0).getText())
        retText += f"CLASS {self.position[0]}\n"

        # iniciar diccionarios de diccioanrios
        self.functions[self.position[0]] = {}

        content = ""

        # si hereda de otra clase
        if ctx.INHERITS():
            inherits_ = ctx.TYPE(1).getText()
            # print("inherits_")

            if inherits_ != "IO":
                # copiar
                self.functions[self.position[0]] = self.functions[inherits_]
                                
                content += self.classes[inherits_] + "\n"

                # reemplazar nombre
                old = f"\t{inherits_}."
                new = f"\t{self.position[0]}."
                content = content.replace(old, new)

        for feature in ctx.feature():
            content += self.visit(feature)

        # lo guardamos para futura referencia y herencia
        self.classes[self.position[0]] = content

        retText += content

        retText += "EOC\n"

        # salirse de la clase 
        self.position.pop()

        return retText
    
    def visitDefFunc(self, ctx:YAPLParser.DefFuncContext):
        print("#defFun")
        retText = ""

        id = ctx.ID().getText()
        # self.currentFun = id
        #print("id ", id)
        retText += f"\t{self.position[0]}.{id}\n"
        self.position.append(id) 
        self.let_counter = 1 # reiniciar el conteo de lets por función

        self.parNames = {}

        for i, formal in enumerate(ctx.formal()):
            self.param_num = i
            retText += self.visit(formal)

        ret_ = self.visit(ctx.expr())
        retText += ret_

        # almacenar
        self.functions[self.position[0]][id] = ret_

        # valor de retorno
        # print("type ", ctx.TYPE().getText(), ctx.TYPE().getText().upper())
        if (ctx.TYPE().getText().upper() == "SELF_TYPE" or ctx.TYPE().getText().upper() == "VOID"):
            retText += f"\t\tRETURN\n"
        else:
            retText += f"\t\tRETURN {self.lastStatement}\n"

        retText += f"\tEND FUNC {id}\n"

        self.position.pop()

        return retText
    
    def visitDefAssign(self, ctx:YAPLParser.DefAssignContext):
        # print("#defAssign")
        retText = ""

        # solamente hacer algo si la variable es definida
        if ctx.expr():
            # obtener id
            id_ = ctx.ID().getText()
            var, _ = self.getRegister(id_)

            # obtener expresión
            value = ""
            exprText = ctx.expr().getText()
            if ctx.expr().getChildCount() > 1:
                print("> 1", ctx.expr().getText())

                retText += self.visit(ctx.expr())
                # print("deffasin retTExt ", retText)
                if len(self.temp_stack) > 0:
                    value = self.temp_stack.pop()
                else:
                    value = "tt"

            else:
                # print("1")
                text_ = ctx.expr().getText()
                # print("text ", text_)
                value, _ = self.getRegister(text_)
                # print("text ret ", text_)
                retText += self.visit(ctx.expr())

            retText += f"\t\tLW {var}, {value}\n"
            self.lastStatement = var

        return retText
    
    def visitFormalAssign(self, ctx:YAPLParser.FormalAssignContext):
        # print("#formalAssign")
        retText = ""

        id_f = ctx.ID().getText()
        pos_, _ = self.getRegister(id_f)
        retText += f"\t\tPARAM {pos_}, P{self.param_num}\n"


        return retText
    
    def visitDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        print("#dispatchExplicit")
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
            p_iz_t = ctx.expr(0).getText()
            p_iz, found = self.getRegister(p_iz_t)

            if not found:
                temp_ = f"t{self.temp_counter}"
                self.addToTemp()
                retText += f"\t\tLW {temp_}, {p_iz}\n"
                p_iz = temp_

        paramlist = []
        for i, expr in enumerate(ctx.expr()):
            if i == 0:
                continue # nos saltamos el primer expr

            par = ""
            if expr.getChildCount() > 1: 
                # visitar hijos
                retText += self.visit(expr)
                if len(self.temp_stack)> 0:
                    par = self.temp_stack.pop()
                else: 
                    par = "tt"
            else: 
                # obtener valor individual
                exprText = expr.getText()
                par, _ = self.getRegister(exprText)
            paramlist.append(par)  

        for p in paramlist:
            retText += f"\t\tPARAM {p}\n"

        id = ctx.ID().getText()
        row1 = self.symbolTable.get_cell(id= ctx.ID().getText())
        # print("id ", id)
        # print("row1 ", row1)

        retText += f"\t\tCALL {p_iz}.{id}, {len(paramlist)}\n"
        print(f"\t\tCALL {p_iz}.{id}, {len(paramlist)}\n")

        # if (not (row[1].upper() == "SELF_TYPE" or row[1].upper() == "VOID")):
        # name = f"t{self.temp_counter}"
        # self.addToTemp()
        # self.temp_stack.append(name)
        name = self.lastStatement
        print("row1 ", row1)

        if (not (
            row1[1].upper() == "SELF_TYPE" or 
            row1[1].upper() == "VOID" or 
            row1[1].upper() == "OBJECT"
            )):
            print("retonro")
            
            retText += f"\t\tLW {name}, RET\n"

            self.lastStatement = name

        else: print("no retorno")

        self.lastStatement = name
        print("name", name)

        return retText
    
    def visitDispatchImplicit(self, ctx:YAPLParser.DispatchImplicitContext):
        print("#dispatchImplicit")
        retText = ""

        id = ctx.ID().getText()

        paramlist = []

        for expr in ctx.expr():
            par = ""
            print("par")
            if expr.getChildCount() > 1: 
                # visitar hijos
                retText += self.visit(expr)
                if len(self.temp_stack)> 0:
                    par = self.temp_stack.pop()
                else: 
                    par = "tt"
            else: 
                # obtener valor individual
                exprText = expr.getText()
                par, _ = self.getRegister(exprText)
            paramlist.append(par)  

        print("paramlist ", paramlist)

        for p in paramlist:
            retText += f"\t\tPARAM {p}\n"

        row1 = self.symbolTable.get_cell(id= ctx.ID().getText())
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
        print("#dispatchAttribute")
        retText = ""

        # parte de la expresión
        p_iz = ""
        if ctx.expr().getChildCount() > 1:
            # visitar hijos
            retText += self.visit(ctx.expr())
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr().getText()
            p_iz, direction = self.getRegister(p_iz_t)

        id = ctx.ID().getText()
        if direction:
            split = direction.split('.')
            id_dir = split[len(split) - 1]
            row = self.symbolTable.get_cell(id=id_dir, addScope = direction)
            # print("row1, ", row)
        
        else:
            # print("id_expr ", ctx.expr().getText())
            row = self.symbolTable.get_cell(id= ctx.expr().getText(), addParent = self.position[0])
        # print("row, ", row)
        # print("id ", id)
        # print("direccion ", direction)
        if row:
            id, _ = self.getRegister(id, [row[1]])
        # print("id ", id)

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
        
        # obtener id
        id_ = ctx.ID().getText()
        var, _ = self.getRegister(id_)

        # obtener expresión
        value = ""
        exprText = ctx.expr().getText()
        if ctx.expr().getChildCount() > 1:
            # visitar hijos
            retText += self.visit(ctx.expr())
            if len(self.temp_stack) > 0:
                value = self.temp_stack.pop()
            else:
                value = "tt"

        else:
            # obtener valor único
            text_ = ctx.expr().getText()
            value, _ = self.getRegister(text_)
            retText += self.visit(ctx.expr())

        retText += f"\t\tLW {var}, {value}\n"
        self.lastStatement = var

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

        retText += f"\t\tIF {temp_} > 0 GOTO L_TRUE_{if_}\n"
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
        condition = ""
        if ctx.expr(0).getChildCount() > 1:
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                condition = self.temp_stack.pop()
            else:
                condition = "tt"
        else: 
            condition_t = ctx.expr(0).getText()
            print("condition ", condition, " ", ctx.getText())
            # revisar si está en el diccionario de registros
            condition, _ = self.getRegister(condition_t)
        

        retText += f"\t\tIF {condition} = 0 GOTO {end_}\n"

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
        print("#letId")
        retText = ""
        
        trips = []

        #position
        posName = f"Let{self.let_counter}"
        self.let_counter += 1 #añadir al contador
        self.position.append(posName)
        # print(self.position)

        # parte de las asignaciones
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
                # obtener id
                id_ = t[0].getText()
                # print(self.position, id_)
                var, _ = self.getRegister(id_)

                # se le ha asignado algo 
                expr = t[4]
                value = ""
                if expr.getChildCount() > 1:
                    retText += self.visit(expr)
                    # print("deffasin retTExt ", retText)
                    if len(self.temp_stack) > 0:
                        value = self.temp_stack.pop()
                    else:
                        value = "tt"

                else:
                    # print("1")
                    text_ = expr.getText()
                    # print("text ", text_)
                    value, _ = self.getRegister(text_)
                    # print("text ret ", text_)
                    retText += self.visit(expr)

                retText += f"\t\tLW {var}, {value}\n"
                # self.lastStatement = var

        # parte del in
        retText += self.visit(ctx.expr(len(ctx.expr()) - 1))

        self.position.pop() # salirse del let

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

        usedTemps = []

        # parte 
        p_iz = ""
        if ctx.expr().getChildCount() > 1:
            # visitar hijos
            retText += self.visit(ctx.expr())
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
                usedTemps.append(p_iz)
            else:
                p_iz = "tt"
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr().getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
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

        usedTemps = []

        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
                usedTemps.append(p_iz)
            else:
                p_iz = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr(0).getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0:
                p_der = self.temp_stack.pop()
                usedTemps.append(p_der)
            else: 
                p_der = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_der_t = ctx.expr(1).getText()
            p_der, _ = self.getRegister(p_der_t)

        # temp_ = f"t{self.temp_counter}"
        # self.addToTemp()
        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append(temp_)

        retText += f"\t\tMULT {temp_}, {p_iz}, {p_der}\n"
        self.lastStatement = temp_

        # regresar temporales
        self.retunTemps(usedTemps)

        return retText
    
    def visitDiv(self, ctx:YAPLParser.DivContext):
        # print("#div")
        retText = ""

        # parte izquierda
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr(0).getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0:
                p_der = self.temp_stack.pop()
            else: 
                p_der = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_der_t = ctx.expr(1).getText()
            p_der, _ = self.getRegister(p_der_t)

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
            # visitar a los hijos
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr(0).getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0:
                p_der = self.temp_stack.pop()
            else: 
                p_der = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_der_t = ctx.expr(1).getText()
            p_der, _ = self.getRegister(p_der_t)

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
            # visitar a los hijos
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr(0).getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0:
                p_der = self.temp_stack.pop()
            else: 
                p_der = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_der_t = ctx.expr(1).getText()
            p_der, _ = self.getRegister(p_der_t)

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
            # visitar a los hijos
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr(0).getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0:
                p_der = self.temp_stack.pop()
            else: 
                p_der = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_der_t = ctx.expr(1).getText()
            p_der, _ = self.getRegister(p_der_t)

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
        p_iz = ""
        if ctx.expr(0).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr(0).getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0:
                p_der = self.temp_stack.pop()
            else: 
                p_der = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_der_t = ctx.expr(1).getText()
            p_der, _ = self.getRegister(p_der_t)

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
            # visitar a los hijos
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr(0).getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0:
                p_der = self.temp_stack.pop()
            else: 
                p_der = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_der_t = ctx.expr(1).getText()
            p_der, _ = self.getRegister(p_der_t)

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
            # visitar a los hijos
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr(0).getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0:
                p_der = self.temp_stack.pop()
            else: 
                p_der = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_der_t = ctx.expr(1).getText()
            p_der, _ = self.getRegister(p_der_t)

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
            # visitar a los hijos
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr(0).getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0:
                p_der = self.temp_stack.pop()
            else: 
                p_der = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_der_t = ctx.expr(1).getText()
            p_der, _ = self.getRegister(p_der_t)

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
            # visitar a los hijos
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr(0).getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0:
                p_der = self.temp_stack.pop()
            else: 
                p_der = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_der_t = ctx.expr(1).getText()
            p_der, _ = self.getRegister(p_der_t)

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
            # visitar a los hijos
            retText += self.visit(ctx.expr(0))
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr(0).getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
        # parte derecha
        p_der = ""
        if ctx.expr(1).getChildCount() > 1:
            # visitar a los hijos
            retText += self.visit(ctx.expr(1))
            if len(self.temp_stack) > 0:
                p_der = self.temp_stack.pop()
            else: 
                p_der = "tt" # hubo un error
        else: 
            # obtener valor individual
            p_der_t = ctx.expr(1).getText()
            p_der, _ = self.getRegister(p_der_t)

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
            # visitar hijos
            retText += self.visit(ctx.expr())
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr().getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
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
        # print("parens expr ", ctx.expr().getText())
        p_iz = ""
        if ctx.expr().getChildCount() > 1:
            # visitar hijos
            retText += self.visit(ctx.expr())
            if len(self.temp_stack) > 0: 
                p_iz = self.temp_stack.pop()
            else:
                p_iz = "tt"
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr().getText()
            p_iz, _ = self.getRegister(p_iz_t)
        
        # volver a meter el valor al stack
        self.temp_stack.append(p_iz)

        return retText
    
    def visitId(self, ctx:YAPLParser.IdContext):
        # print("#id") 
        retText = ""
        pos_, _ = self.getRegister(ctx.getText())
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

    def genDictionary(self, st:Table):
        # conseguir las clases 
        # clases que se ignoran
        noClases = ["object", "self_type", "io", "void", "string", "int", "bool"]

        for x in st.columns:
            if (x[2] == "Instance" or x[2] == "Variable" or x[2] == "Param") and x[4].lower() not in noClases:
                # print(x[0], x[7], x[8])
                if type(x[7]) == int: #revisar que no sea null
                    # determinar el largo
                    pos_ = x[8].split(".") # separamos por puntos
                    if len(pos_) > 2:
                        # es una variable global
                        self.registers[x[8]] = f"SP[{x[7]}]"
                    else:
                        # es una variable local
                        self.registers[x[8]] = f"GP[{x[7]}]"
                    # {class_name.method_name.let_#.variable_name}

    def getRegister(self, name_:str, position = None):
        ret = ""

        pos = []
        if position:
            # copiar la posición dada
            for x in position:
                pos.append(x)
        else:
            # copiar la posición global
            for x in self.position:
                pos.append(x)

        search = ""
        while (len(pos) >= 1):
            # conseguir el nombre
            search = ""
            for p in pos:
                search += p + "."
            search += name_ 
            # print(search)

            # buscar si existe en el diccionario
            if search in self.registers.keys():
                # conseguir el registro correcto
                ret = self.registers[search]
                # print("break ", name_)
                break # salirse del loop

            else:
                pos.pop() # buscar un nivel más arriba

        if ret != "":
            # encontró el registro
            return ret, search
        else:
            # retornar lo que se estaba buscando
            return name_, None
        
    def retunTemps(self, usedTemps:list):

        for temp in usedTemps:
            pos = 0
            for i, t in enumerate(self.available_temps_stack):
                print(int(temp[1:]) , int(t[1:]))
                if int(temp[1:]) < int(t[1:]):
                    pos = i + 1
            
            self.available_temps_stack.insert(pos, temp)
