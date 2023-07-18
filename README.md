# UVG_Compilador_CC
# Laboratorio#0
## Objetivos:
- Familizarizarse con YAPL: con ayuda de los archivos del curso y herramientas brindadas por el laboratorio se buscaba entender mejor la estructura y funcionamiento de este lenguaje.
- Generación de Scanner y Parser: se recomendó utilizar ANTLR para la generación del parser y lexer que permitieran la creación y recorrido de árboles de análisis sintáctico por lo que se tuvo que realizar una investigación respecto al funcionamiento, sintaxis e implementación de esta herramienta
- Presentación de resultados: para mostrar los resultados obtenidos fue necesario la creación de una GUI funcional y amistosa con el usuario. En la GUI desarrollada se trabaja con un diseño sencillo en el cual el usuario es capaz de ingresar una expresión y generar el árbol. (La gramática se agrega directamente en el código)
 
## Funcionamiento
### *Instalaciones necesarias*
```
pip install antlr4-tools
```
```
pip install antlr4-python3-runtime
```
### *Gramática*<br>
Archivo a modificar: <a href="https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/blob/main/YAPL.g4">YAPL.g4</a>

### *Ejecución del programa*
Archivo a ejecutar: <a href="https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/blob/main/main.py">main.py</a>

Luego de ejecutar el programa, y esperando que se hayan instalado todas las librerías y plugins necesarios, aparece una ventana similar a esta:
<p align="center">
  <img src="https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/assets/60325784/e61ff2a1-5eb0-43d2-9977-bcc888026dff"/>
</p>
<br>
En el cuadro de texto es posible ingresar una expresión a evaluar, luego de haberla ingresado se presiona el botón correspondiente y se muestra el árbol en una GUI independiente y adicional se imprime en consola en forma de texto. Existe la opción de limpiar el inputArea y también salir del programa.

### Ejemplo:
*Gramática*
```
grammar YAPL;

/* Entry point */
prog: (class_def ';')+ EOF
    ;

class_def:
        CLASS_N TYPE (INHERITS TYPE)? '{' (feature ';')* '}'
    ;   

feature:
        ID '(' ( formal (',' formal )* )? ')' ':' TYPE '{' expr '}'
    |   ID ':' TYPE  (ASSIGNMENT expr)?
    ;

formal:
        ID ':' TYPE ';'
    ;

expr:
        ID ASSIGNMENT expr
    |   expr ('@' TYPE)? '.' ID '(' ( expr (',' expr)* )? ')'
    |   ID '(' ( expr (',' expr)* ) ')'
    |   IF expr THEN expr ELSE expr FI
    |   WHILE expr LOOP expr POOL
    |   '{' (expr ';')+ '}'
    |   LET ID ':' TYPE (ASSIGNMENT expr)? (',' ID ':' TYPE (ASSIGNMENT expr)? )* IN expr
    |   NEW TYPE
    |   '~' expr
    |   ISVOID expr
    |   expr op=('*' | '/') expr
    |   expr op=('+' | '-') expr
    |   expr op=('<=' | '<' | '=' ) expr
    |   NOT expr
    |   '(' expr ')'
    |   ID 
    |   INT 
    |   STRING
    |   bool=(TRUE | FALSE)
    ;

/* Comments */
BLOCK_COMMENT   :   '(*' (BLOCK_COMMENT|.)*? '*)'   -> channel(HIDDEN);
LINE_COMMENT    :   '--' .*? '\n'                   -> channel(HIDDEN);

WS:
        [ \t\r\n\f]+ -> skip;

/* Reserved words */
CLASS_N:  
    [cC][lL][aA][sS][sS];
NOT:
    [nN][oO][tT];
ISVOID:
    [iI][sS][vV][oO][iI][dD];
IF:
    [iI][fF];
FI:
    [fF][iI];
THEN:
    [tT][hH][eE][nN];
ELSE:
    [eE][lL][sS][eE];
WHILE:
    [wW][hH][iI][lL][eE];
LET:
    [lL][eE][tT];
IN:
    [iI][nN];
INHERITS:
    [iI][nN][hH][eE][rR][iI][tT][sS];
LOOP:
    [lL][oO][oO][pP];
POOL:
    [pP][oO][oO][lL];
NEW:
    [nN][eE][wW];
TRUE:
    [tT][rR][uU][eE];
FALSE:
    [fF][aA][lL][sS][eE];

/* Data Types */
STRING:
    '"' (ESC | ~ ["\\])* '"';
INT:
    [0-9]+;
TYPE:
    [A-Z][_0-9A-Za-z]*;
ID:
    [a-z][_0-9A-Za-z]*;
ASSIGNMENT:
    '<-';

fragment ESC: '\\' ([/bfnrt] | UNICODE | '"');
fragment UNICODE: 'u' HEX HEX HEX HEX;
fragment HEX: [0-9a-fA-F];
```
*Expresión evaluada (Sin errores)*
```
class Main {
	(This is a comment*)
      bar : B;
    baz: A;

    main(): B {
    {
      bar <- (new B).init();
      baz <- (new A).init(111, "TAC generation");
      bar.createFoo();
    }
  };
};
```

*Expresión evaluada (Con errores)*
```
class Main {
	This is a comment*)
      bar : B;
    baz: 
    
    main(): B {
    {
      bar <- (new B).init();
      baz <- (new A).init(111, "TAC generation");
      bar.createFoo();
    }
  };
};
```

Resultado expresión sin errores
<p align="center">
  <img src="https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/assets/60325784/23685454-c7fd-4991-b2c4-2244d01bda95"/>
</p>
<br>
Resultado expresión con errores
<p align="center">
  <img src="https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/assets/60325784/f8a9b4df-463d-49a1-805a-b451858c843f"/>
</p>
En este segundo caso no sé muestra ningún árbol porque existen varios errores
