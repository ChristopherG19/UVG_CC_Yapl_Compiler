grammar YAPL;

/* Entry point */
prog: (class_def ';')+ #start
    ;

class_def:
        CLASS_N TYPE (INHERITS TYPE)? '{' (feature ';')* '}' #defClass
    ;   

feature:
        ID '(' ( formal (',' formal )* )? ')' ':' TYPE '{' expr '}' #defFunc
    |   ID ':' TYPE  (ASSIGNMENT expr)? #defAssign
    ;

formal:
        ID ':' TYPE #formalAssign
    ;

expr: 
        
        expr ('@' TYPE)? '.' ID '(' ( expr (',' expr)* )? ')' #dispatchExplicit
    |   ID '(' ( expr (',' expr)* ) ? ')' #dispatchImplicit
    |   expr '.' ID #dispatchAttribute
    |   IF expr THEN expr ELSE expr FI #if
    |   WHILE expr LOOP expr POOL #while
    |   '{' (expr ';')+ '}' #block
    |   LET ID ':' TYPE (ASSIGNMENT expr)? (',' ID ':' TYPE (ASSIGNMENT expr)? )* IN expr #letId
    |   NEW TYPE #new
    |   '~' expr #negative
    |   ISVOID expr #isvoid
    |   expr '*' expr #times
    |   expr '/' expr #div
    |   expr '+' expr #plus
    |   expr '-' expr #minus
    |   expr '<=' expr #lessThanOrEqual
    |   expr '<' expr #lessThan
    |   expr '>' expr #greaterThan
    |   expr '>=' expr #greaterThanOrEqual
    |   expr '=' expr #equal
    |   expr '&' expr #and
    |   expr '|' expr #or
    |   NOT expr #neg
    |   '(' expr ')' #parens
    |   ID ASSIGNMENT expr #assignment
    |   ID #id
    |   INT #int
    |   STRING #string
    |   bool=(TRUE | FALSE) #boolean
    |   SELF #self
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
SELF:
    [sS][eE][lL][fF];

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

/* operators */
TIMES:
    '*';
DIV:
    '/';
PLUS: 
    '+';
MINUS:
    '-';
TILDE:
    '~';
LESS:
    '<';
EQLESS:
    '<=';
EQ:
    '=';
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
DOT:
    '.';
AT:
    '@';
COLON:
    ':';
COMA:
    ',';

fragment ESC: '\\' ([/bfnrt] | UNICODE | '"');
fragment UNICODE: 'u' HEX HEX HEX HEX;
fragment HEX: [0-9a-fA-F];