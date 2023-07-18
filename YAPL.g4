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
        ID ':' TYPE
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