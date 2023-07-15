grammar Expr;
/* Entry point for the parser */
prog: (class)* EOF ;

/* Data types */
LETTER:
    [a-zA-Z];
INTEGER:
    DIGIT+;
STRING:
    '"' (ESC | ~["\\])* '"';
ID:
    [a-zA-Z_][a-zA-Z0-9_]*;
WS:
    [ \t\r\n\f]+ -> skip;
TYPE: 
    LETTER (LETTER | DIGIT | '_')*;

/* Reserved words */
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

/* operators */
DOT:
    '.';
AT:
    '@';
TILDE:
    '~';
ISVOID:
    [iI][sS][vV][oO][iI][dD];
TIMES:
    '*';
DIV:
    '/';
PLUS: 
    '+';
MINUS:
    '-';
EQLESS:
    '<=';
LESS:
    '<';
EQ:
    '=';
NOT:
    [nN][oO][tT];
LARROW:
    '<-';
LPAR:
    '(';
RPAR:
    ')';
LCBRACE:
    '{';
RCBRACE:
    '}';
LBRACKET:
    '[';
RBRACKET:
    ']';
COLON:
    ':';
COMA:
    ',';

/* Producctions */
class:
    'class' TYPE LBRACKET INHERITS TYPE RBRACKET LCBRACE (feature)* RCBRACE;
feature:
    ID LPAR LBRACKET formal ( COMA formal)* RBRACKET RPAR COLON TYPE LCBRACE expr RCBRACE
    | ID COLON TYPE LBRACKET LARROW expr RBRACKET
;
formal:
    ID COLON TYPE;
expr:
    expr PLUS expr   
    | expr MINUS expr   
    | expr TIMES expr   
    | expr DIV expr
    | expr EQLESS expr 
    | unary_exp
;
unary_exp:
    MINUS expr
    | TILDE expr
    | primary_exp
    | NOT expr
;
expr_list:
    expr
    | ID
    | INTEGER
    | STRING
    | TRUE
    | FALSE
    | ID LARROW expr
    | expr LBRACKET AT TYPE RBRACKET DOT ID LPAR LBRACKET expr( COMA expr )* RBRACKET RPAR
    | ID LPAR LBRACKET expr(COMA expr )* RBRACKET RPAR
    | IF expr THEN expr ELSE expr FI
    | WHILE expr LOOP expr POOL
    | LCBRACE (expr)+ RCBRACE
    | LET ID COLON TYPE LBRACKET LARROW expr RBRACKET ( COMA ID COLON TYPE LBRACKET LARROW expr RBRACKET )* IN expr
    | NEW TYPE
    | ISVOID expr   
    | expr EQ expr   
    | LPAR expr RPAR
;

/* fragment rules */
fragment ESC: 
    '\\' (["\\/bfnrt] | 'u' HEX HEX HEX HEX);
fragment HEX: 
    [0-9a-fA-F];
fragment DIGIT: 
    [0-9];