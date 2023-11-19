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
        self.symbolTable:Table() = symbolTable
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
        self.paramlist_size = 0

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

        # obtener tamaño de la clase
        size = self.symbolTable.class_size(self.position[0])

        # verificación de si es múltiplo de 4
        while size % 4 != 0:
            size += 1

        retText += f"CLASS {self.position[0]}, {str(size)}\n"

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
        # print("#defFun")
        retText = ""

        id = ctx.ID().getText()
        # obtenr tamaño
        # size = self.symbolTable.fun_size(id, self.position[0])
        row = self.symbolTable.get_cell(id, addParent = self.position[0], addScope = "Global")
        size = row[9]
        retText += f"\t{self.position[0]}.{id}, {size}\n"
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

        usedTemps = []

        # solamente hacer algo si la variable es definida
        if ctx.expr():
            # obtener id
            id_ = ctx.ID().getText()
            var, _ = self.getRegister(id_)

            # obtener expresión
            value = ""
            ins = "SW"
            # if ctx.expr().getChildCount() > 1:
            # visitar hijos
            retText += self.visit(ctx.expr())
            # print("deffasin retTExt ", retText)
            if len(self.temp_stack) > 0:
                value, type_ = self.temp_stack.pop()
                usedTemps.append(value)

            else:
                value = "tt"
                type_ = "tt"


            retText += f"\t\t{ins} {var}, {value}({type_})\n"
            self.lastStatement = var

            # regresar variables temporales
            self.returnTemps(usedTemps)

        return retText
    
    def visitFormalAssign(self, ctx:YAPLParser.FormalAssignContext):
        # print("#formalAssign")
        retText = ""

        id_f = ctx.ID().getText()
        pos_, _ = self.getRegister(id_f)
        retText += f"\t\tLW {pos_}, P{self.param_num}\n"

        return retText
    
    def visitDispatchExplicit(self, ctx:YAPLParser.DispatchExplicitContext):
        # print("#dispatchExplicit")
        retText = ""

        usedTemps = []

        # parte izquierda (primera expr)
        p_iz = ""

        # visitar hijos
        retText += self.visit(ctx.expr(0))
        if len(self.temp_stack) > 0: 
            p_iz, type_ = self.temp_stack.pop()
            usedTemps.append(p_iz)

        else:
            # ocurrió un error
            p_iz = "tt"
            type_ = "tt"

        # regresar temporales
        self.returnTemps(usedTemps)
        
        paramlist = []
        usedTemps = []
        for i, expr in enumerate(ctx.expr()):
            if i == 0:
                continue # nos saltamos el primer expr
            
            par = ""
            # visitar hijos
            retText += self.visit(expr)
            if len(self.temp_stack)> 0:
                par, type_par = self.temp_stack.pop()
                usedTemps.append(par)

            else: 
                # a ocurrido un error
                par = "tt"
                type_par = "tt"

            paramlist.append([par, type_par]) 

        # regresar temporales
        self.returnTemps(usedTemps) 

        for p, type_p in paramlist:
            retText += f"\t\tPARAM {p}({type_p})\n"

        id = ctx.ID().getText()
        row1 = self.symbolTable.get_cell(id= ctx.ID().getText())


        # obtener tamaño
        size = self.symbolTable.params_size(id, p_iz)

        retText += f"\t\tCALL {p_iz}({type_}).{id}, {size}\n"

        name = self.lastStatement
        self.temp_stack.append([name, type_])

        if (not (
            row1[1].upper() == "SELF_TYPE" or 
            row1[1].upper() == "VOID" or 
            row1[1].upper() == "OBJECT"
            )):

            temp_ = self.available_temps_stack.pop()
            self.temp_stack.append([temp_, type_])
            retText += f"\t\tLW {temp_}, RET\n"

            self.lastStatement = temp_


        return retText
    
    def visitDispatchImplicit(self, ctx:YAPLParser.DispatchImplicitContext):
        # print("#dispatchImplicit")
        retText = ""

        id = ctx.ID().getText()

        usedTemps = []

        paramlist = []
        self.paramlist_size = 0

        # retText += self.visit(ctx.ID)

        # if len(self.temp_stack) > 0:
        #     temp_, type_ = self.temp_stack.pop()
        #     usedTemps.append(temp_)
        # else:
        #     # ha ocurrido un error
        #     temp_ = "tt"
        #     type_ = "tt"

        for expr in ctx.expr():
            par = ""
            # print("par")
            # visitar hijos
            retText += self.visit(expr)
            if len(self.temp_stack)> 0:
                par, type_par = self.temp_stack.pop()
                usedTemps.append(par)

            else: 
                par = "tt"
                type_par = "tt"

            paramlist.append([par, type_par])  

        # print("paramlist ", paramlist)

        for p, type_p in paramlist:
            retText += f"\t\tPARAM {p}({type_p})\n"

        row1 = self.symbolTable.get_cell(id= ctx.ID().getText())

        # obtener tamaño
        size = self.symbolTable.params_size(id, row1[4])

        retText += f"\t\tCALL {row1[4]}.{id}, {self.paramlist_size}\n"

        if (not (
            row1[1].upper() == "SELF_TYPE" or 
            row1[1].upper() == "VOID" or 
            row1[1].upper() == "OBJECT"
            )):
            name = self.available_temps_stack.pop()
            self.temp_stack.append([name, row1[1]])
            retText += f"\t\tLW {name}, RET\n"

            self.lastStatement = name

        # regresar temporales
        self.returnTemps(usedTemps)

        return retText
    
    def visitDispatchAttribute(self, ctx:YAPLParser.DispatchAttributeContext):
        # print("#dispatchAttribute")
        retText = ""

        usedTemps = []        

        # parte de la expresión
        p_iz = ""
        if ctx.expr().getChildCount() > 1:
            # visitar hijos
            retText += self.visit(ctx.expr())
            if len(self.temp_stack) > 0: 
                p_iz, type_ = self.temp_stack.pop()
                usedTemps.append(p_iz)

            else:
                p_iz = "tt"
                type_ = "tt"
        else: 
            # obtener valor individual
            retText += self.visit(ctx.expr())
            if len(self.temp_stack) > 0: 
                p_iz_t = ctx.expr().getText()
                _, direction = self.getRegister(p_iz_t)
                # obtener del stack
                p_iz, type_ = self.temp_stack.pop()
                usedTemps.append(p_iz)
                
            else:
                p_iz = "tt"
                type_ = "tt"


        id = ctx.ID().getText()
        if direction:
            split = direction.split('.')
            id_dir = split[len(split) - 1]
            row = self.symbolTable.get_cell(id=id_dir, addScope = direction)
            # print("row1, ", row)
        
        else:
            # print("id_expr ", ctx.expr().getText())
            row = self.symbolTable.get_cell(id= ctx.expr().getText(), addParent = self.position[0])

        if row:
            id, _ = self.getRegister(id, [row[1]])

        retText += f"\t\tCALL {p_iz}({type_}).{id}, 0\n"

        name = self.available_temps_stack.pop()
        self.temp_stack.append([name, type_])

        if (not (
            row[1].upper() == "SELF_TYPE" or 
            row[1].upper() == "VOID" or 
            row[1].upper() == "OBJECT"
            )):
            
            retText += f"\t\tLW {name}, RET\n"

            self.lastStatement = name

        self.lastStatement = name

        # regresar temporal
        self.returnTemps(usedTemps)

        return retText
    
    def visitAssignment(self, ctx:YAPLParser.AssignmentContext):
        # print("#assignment")
        # print("ass ", ctx.getText())
        retText = ""

        usedTemps = []
        
        # obtener id
        id_ = ctx.ID().getText()
        var, _ = self.getRegister(id_)

        # obtener expresión
        value = ""
        exprText = ctx.expr().getText()

        # visitar hijos
        retText += self.visit(ctx.expr())
        if len(self.temp_stack) > 0:
            value, type_ = self.temp_stack.pop()
            usedTemps.append(value)

        else:
            # Un error ha ocurrido
            value = "tt"
            type_ = "tt"

        retText += f"\t\tSW {var}, {value}({type_})\n"
        self.lastStatement = var

        # regresar temporales
        self.returnTemps(usedTemps)

        return retText
    
    def visitIf(self, ctx:YAPLParser.IfContext):
        # print("#if")
        retText = ""

        # visitar la condición
        retText += self.visit(ctx.expr(0))

        usedTemps = []

        temp_ = ""
        if len(self.temp_stack) > 0:
            temp_, type_ = self.temp_stack.pop()
            usedTemps.append(temp_)
        else:
            # ha ocurrido un error
            temp_ = "tt"
            type_ = "tt"

        # obtener contadores
        if_ = self.goto_if
        self.goto_if += 1

        retText += f"\t\tIF {temp_} > 0 GOTO L_TRUE_{if_}\n"
        retText += f"\t\tGOTO L_FALSE_{if_}\n"

        # regresar temporal
        self.returnTemps(usedTemps)

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

        usedTemps = []

        # evaluar la expresión de la condición
        # parte 
        condition = ""

        retText += self.visit(ctx.expr(0))
        if len(self.temp_stack) > 0: 
            condition, type_ = self.temp_stack.pop()
            usedTemps.append(condition)

        else:
            condition = "tt"
            type_ = "tt"

        retText += f"\t\tIF {condition}({type_}) = 0 GOTO {end_}\n"

        # regresar temporal
        self.returnTemps(usedTemps)

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
            usedTemps = []

            if len(t) == 5:
                # obtener id
                id_ = t[0].getText()
                # print(self.position, id_)
                var, _ = self.getRegister(id_)

                # se le ha asignado algo 
                expr = t[4]
                value = ""
                retText += self.visit(expr)
                # visitar hijos
                if len(self.temp_stack) > 0:
                    value, type_ = self.temp_stack.pop()
                    usedTemps.append(value)
    
                else:
                    # ha ocurrido un error
                    value = "tt"
                    type_ = "tt"
              
                # retText += f"\t\tLW {var}, {value}\n"
                ins = "SW"
                try:
                    n = int(value)
                    ins = "LI"
                    retText += f"        {ins} {var}, {value}({type_})\n"
                except:
                    retText += f"        {ins} {var}, {value}({type_})\n"
                # self.lastStatement = var

            # regresar temporal
            self.returnTemps(usedTemps)

        # parte del in
        retText += self.visit(ctx.expr(len(ctx.expr()) - 1))

        self.position.pop() # salirse del let

        return retText
    
    def visitNew(self, ctx:YAPLParser.NewContext):
        # print("#new")
        retText = ""

        temp_ = self.available_temps_stack.pop()
        type_ = ctx.TYPE()

        self.temp_stack.append([temp_, type_])
        retText += f"\t\tLW {temp_}({type_}), {ctx.TYPE().getText()}\n"

        self.lastStatement = temp_

        return retText
    
    def visitNegative(self, ctx:YAPLParser.NegativeContext):
        # print("#negative")
        retText = ""

        usedTemps = []

        # parte 
        p_iz = ""
        # visitar hijos
        retText += self.visit(ctx.expr())
        if len(self.temp_stack) > 0: 
            p_iz, type_ = self.temp_stack.pop()
            usedTemps.append(p_iz)

        else:
            p_iz = "tt"
            type_ = "tt"

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append({temp_, type_})

        retText += f"\t\tNEG {temp_}({type_}), {p_iz}({type_})\n"
        self.lastStatement = temp_

        # retornar temporales
        self.returnTemps(usedTemps)
        
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
        # visitar a los hijos
        retText += self.visit(ctx.expr(0))
        if len(self.temp_stack) > 0: 
            p_iz, _ = self.temp_stack.pop()
            usedTemps.append(p_iz)
        else:
            p_iz = "tt" # hubo un error

        # parte derecha
        p_der = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(1))
        if len(self.temp_stack) > 0:
            p_der, type_ = self.temp_stack.pop()
            usedTemps.append(p_der)

        else: 
            p_der = "tt" # hubo un error
            type_ = "tt"

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, type_])

        retText += f"\t\tMULT {temp_}({type_}), {p_iz}({type_}), {p_der}({type_})\n"
        self.lastStatement = temp_

        # regresar temporales
        self.returnTemps(usedTemps)

        return retText
    
    def visitDiv(self, ctx:YAPLParser.DivContext):
        # print("#div")
        retText = ""

        usedTemps = []

        # parte izquierda
        p_iz = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(0))
        if len(self.temp_stack) > 0: 
            p_iz, _ = self.temp_stack.pop()
            usedTemps.append(p_iz)
        else:
            p_iz = "tt" # hubo un error

        # parte derecha
        p_der = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(1))
        if len(self.temp_stack) > 0:
            p_der, type_ = self.temp_stack.pop()
            usedTemps.append(p_der)

        else: 
            p_der = "tt" # hubo un error
            type_ = "tt"

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, type_])

        retText += f"\t\tDIV {temp_}({type_}), {p_iz}({type_}), {p_der}({type_})\n"
        self.lastStatement = temp_

        # regresar temporales
        self.returnTemps(usedTemps)

        return retText
    
    def visitPlus(self, ctx:YAPLParser.PlusContext):
        # print("#plus")
        retText = ""

        usedTemps = []

        # parte izquierda
        p_iz = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(0))
        if len(self.temp_stack) > 0: 
            p_iz, _ = self.temp_stack.pop()
            usedTemps.append(p_iz)
        else:
            p_iz = "tt" # hubo un error

        # parte derecha
        p_der = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(1))
        if len(self.temp_stack) > 0:
            p_der, type_ = self.temp_stack.pop()
            usedTemps.append(p_der)

        else: 
            p_der = "tt" # hubo un error
            type_ = "tt"

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, type_])

        retText += f"\t\tADD {temp_}({type_}), {p_iz}({type_}), {p_der}({type_})\n"
        self.lastStatement = temp_

        # regresar temporales
        self.returnTemps(usedTemps)

        return retText
    
    def visitMinus(self, ctx:YAPLParser.MinusContext):
        # print("#minus")
        retText = ""

        usedTemps = []

        # parte izquierda
        p_iz = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(0))
        if len(self.temp_stack) > 0: 
            p_iz, _ = self.temp_stack.pop()
            usedTemps.append(p_iz)
        else:
            p_iz = "tt" # hubo un error

        # parte derecha
        p_der = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(1))
        if len(self.temp_stack) > 0:
            p_der, type_ = self.temp_stack.pop()
            usedTemps.append(p_der)

        else: 
            p_der = "tt" # hubo un error
            type_ = "tt"

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, type_])

        retText += f"\t\tSUB {temp_}({type_}), {p_iz}({type_}), {p_der}({type_})\n"
        self.lastStatement = temp_

        # regresar temporales
        self.returnTemps(usedTemps)

        return retText
    
    def visitLessThanOrEqual(self, ctx:YAPLParser.LessThanContext):
        # print("#lessThanOrEqual")
        retText = ""

        usedTemps = []

        # parte izquierda
        p_iz = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(0))
        if len(self.temp_stack) > 0: 
            p_iz, _ = self.temp_stack.pop()
            usedTemps.append(p_iz)
        else:
            p_iz = "tt" # hubo un error

        # parte derecha
        p_der = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(1))
        if len(self.temp_stack) > 0:
            p_der, type_ = self.temp_stack.pop()
            usedTemps.append(p_der)

        else: 
            p_der = "tt" # hubo un error
            type_ = "tt"

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, type_])

        retText += f"\t\tSLE {temp_}({type_}), {p_iz}({type_}), {p_der}({type_})\n"
        self.lastStatement = temp_

        # Regresar temporales
        self.returnTemps(usedTemps)

        return retText
    
    def visitLessThan(self, ctx:YAPLParser.LessThanOrEqualContext):
        # print("#lessThan")
        retText = ""

        usedTemps = []

        # parte izquierda
        p_iz = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(0))
        if len(self.temp_stack) > 0: 
            p_iz, _ = self.temp_stack.pop()
            usedTemps.append(p_iz)
        else:
            p_iz = "tt" # hubo un error

        # parte derecha
        p_der = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(1))
        if len(self.temp_stack) > 0:
            p_der, type_ = self.temp_stack.pop()
            usedTemps.append(p_der)

        else: 
            p_der = "tt" # hubo un error
            type_ = "tt"

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, type_])

        retText += f"\t\tSLT {temp_}({type_}), {p_iz}({type_}), {p_der}({type_})\n"
        self.lastStatement = temp_

        # regresar temporales
        self.returnTemps(usedTemps)

        return retText
    
    def visitGreaterThan(self, ctx:YAPLParser.GreaterThanContext):
        # print("#greaterThan")
        retText = ""

        usedTemps = []

        # parte izquierda
        p_iz = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(0))
        if len(self.temp_stack) > 0: 
            p_iz, _ = self.temp_stack.pop()
            usedTemps.append(p_iz)
        else:
            p_iz = "tt" # hubo un error

        # parte derecha
        p_der = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(1))
        if len(self.temp_stack) > 0:
            p_der, type_ = self.temp_stack.pop()
            usedTemps.append(p_der)

        else: 
            p_der = "tt" # hubo un error
            type_ = "tt"

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, type_])

        retText += f"\t\tSGT {temp_}({type_}), {p_iz}({type_}), {p_der}({type_})\n"
        self.lastStatement = temp_

        # regresar temporales
        self.returnTemps(usedTemps)

        return retText
    
    def visitGreaterThanOrEqual(self, ctx:YAPLParser.GreaterThanOrEqualContext):
        # print("#greaterThanOrEqual")
        retText = ""

        usedTemps = []

        # parte izquierda
        p_iz = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(0))
        if len(self.temp_stack) > 0: 
            p_iz, _ = self.temp_stack.pop()
            usedTemps.append(p_iz)
        else:
            p_iz = "tt" # hubo un error

        # parte derecha
        p_der = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(1))
        if len(self.temp_stack) > 0:
            p_der, type_ = self.temp_stack.pop()
            usedTemps.append(p_der)

        else: 
            p_der = "tt" # hubo un error
            t_type = "tt"

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, type_])

        retText += f"\t\tSGE {temp_}({type_}), {p_iz}({type_}), {p_der}({type_})\n"
        self.lastStatement = temp_

        # regresar temporales
        self.returnTemps(usedTemps)

        return retText
    
    def visitEqual(self, ctx:YAPLParser.EqualContext):
        # print("#equal")
        retText = ""

        usedTemps = []

        # parte izquierda
        p_iz = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(0))
        if len(self.temp_stack) > 0: 
            p_iz, _ = self.temp_stack.pop()
            usedTemps.append(p_iz)
        else:
            p_iz = "tt" # hubo un error

        # parte derecha
        p_der = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(1))
        if len(self.temp_stack) > 0:
            p_der, type_ = self.temp_stack.pop()
            usedTemps.append(p_der)

        else: 
            p_der = "tt" # hubo un error
            type_ = "tt"

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, type_])

        retText += f"\t\tSEQ {temp_}({type_}), {p_iz}({type_}), {p_der}({type_})\n"
        self.lastStatement = temp_

        # regresar temporales
        self.returnTemps(usedTemps)
        
        return retText
    
    def visitAnd(self, ctx:YAPLParser.AndContext):
        # print("#and")
        retText = ""

        usedTemps = []

        # parte izquierda
        p_iz = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(0))
        if len(self.temp_stack) > 0: 
            p_iz, _ = self.temp_stack.pop()
            usedTemps.append(p_iz)
        else:
            p_iz = "tt" # hubo un error

        # parte derecha
        p_der = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(1))
        if len(self.temp_stack) > 0:
            p_der, type_ = self.temp_stack.pop()
            usedTemps.append(p_der)

        else: 
            p_der = "tt" # hubo un error
            type_ = "tt"

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, type_])

        retText += f"\t\tAND {temp_}({type_}), {p_iz}({type_}), {p_der}({type_})\n"
        self.lastStatement = temp_

        # regresar temporales
        self.returnTemps(usedTemps)

        return retText
    
    def visitOr(self, ctx:YAPLParser.OrContext):
        # print("#or")
        retText = ""

        usedTemps = []

        # parte izquierda
        p_iz = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(0))
        if len(self.temp_stack) > 0: 
            p_iz, _ = self.temp_stack.pop()
            usedTemps.append(p_iz)
        else:
            p_iz = "tt" # hubo un error

        # parte derecha
        p_der = ""
        # visitar a los hijos
        retText += self.visit(ctx.expr(1))
        if len(self.temp_stack) > 0:
            p_der, type_ = self.temp_stack.pop()
            usedTemps.append(p_der)

        else: 
            p_der = "tt" # hubo un error
            type_ = "tt"

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, type_])

        retText += f"\t\tOR {temp_}({type_}), {p_iz}({type_}), {p_der}({type_})\n"
        self.lastStatement = temp_

        # regresar temporales
        self.returnTemps(usedTemps)

        return retText
    
    def visitNeg(self, ctx:YAPLParser.NegContext):
        # print("#neg")
        retText = ""

        usedTemps = []

        # parte 
        p_iz = ""
        # visitar hijos
        retText += self.visit(ctx.expr())
        if len(self.temp_stack) > 0: 
            p_iz, type_ = self.temp_stack.pop()
            usedTemps.append(p_iz)

        else:
            p_iz = "tt"
            type_ = "tt"

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, type_])

        retText += f"\t\tNOT {temp_}({type_}), {p_iz}({type_})\n"
        self.lastStatement = temp_

        # retornar temporal
        self.returnTemps(usedTemps)

        return retText

    def visitParens(self, ctx:YAPLParser.ParensContext):
        # print("#parens")
        retText = ""

        # parte 
        p_iz = ""
        if ctx.expr().getChildCount() > 1:
            # visitar hijos
            retText += self.visit(ctx.expr())
            if len(self.temp_stack) > 0: 
                p_iz, type_ = self.temp_stack.pop()
            else:
                p_iz = "tt"
                type_ = "tt"
        else: 
            # obtener valor individual
            p_iz_t = ctx.expr().getText()
            p_iz, _ = self.getRegister(p_iz_t)
            type_ = "ttt"
        
        # volver a meter el valor al stack
        self.temp_stack.append([p_iz, type_])

        return retText
    
    def visitId(self, ctx:YAPLParser.IdContext):
        # print("#id") 
        retText = ""
        pos_, scope = self.getRegister(ctx.getText())

        row = self.symbolTable.get_cell(id=ctx.getText(), addScope = scope)
        type_ = row[1]

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, type_])

        retText += f"\t\tLW {temp_}({type_}), {pos_}\n"
        self.lastStatement = temp_

        return retText
    
    def visitInt(self, ctx:YAPLParser.IntContext):
        # print("#int")
        retText = ""
        
        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, "Int"])

        retText += f"\t\tLI {temp_}(Int), {ctx.getText()}\n"
        self.lastStatement = temp_

        return retText

    def visitString(self, ctx:YAPLParser.StringContext):
        # print("#string")
        retText = ""

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, "String"])

        retText += f"\t\tLI {temp_}(String), {ctx.getText()}\n"
        self.lastStatement = temp_

        return retText
    
    def visitBoolean(self, ctx:YAPLParser.BooleanContext):
        # print("#boolean")
        retText = ""
        value = ctx.getText()

        temp_ = self.available_temps_stack.pop()
        self.temp_stack.append([temp_, "Bool"])

        if value.lower() == "true":
            value = 1
        else:
            value = 0

        retText += f"\t\tLI {temp_}(Bool), {value}\n"
        self.temp_stack.append([temp_, "Bool"])
        
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
        
    def returnTemps(self, usedTemps:list):
        validTemps = [
            "t8", "t7", "t6",
            "t5", "t4", "t3",
            "t2", "t1", "t0",
            ]
        
        for temp in usedTemps:
            pos = 0
            if temp in validTemps:
                for i, t in enumerate(self.available_temps_stack):
                    # print(int(temp[1:]) , int(t[1:]))
                    if int(temp[1:]) < int(t[1:]):
                        pos = i + 1

                self.available_temps_stack.insert(pos, temp)


