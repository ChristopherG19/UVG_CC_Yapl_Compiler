prog: (class)*
/*Grammar*/

/* Entry point for the parser */
prog:
    (class)* ;
class:
    class TYPE [inherits TYPE] { (feature)*} ;
feature:
    ID([formal(,formal)*]) : TYPE{ expr }
    | ID : TYPE [ <- expr ]
    ;
formal:
    ID : TYPE ;
expr:
    ID <- expr
    | expr[@TYPE].id([expr(,expr)*])
    | ID([expr(,expr)*])
    | if expr then expr else expr fi
    | while expr loop expr pool
    | { (expr)+ }
    | let ID : TYPE [ <- expr ] (, ID : TYPE [ <- expr ])* in expr
    | new TYPE
    | isvoid expr
    | expr + expr   /* Possible error */
    | expr - expr   /* Possible error */
    | expr * expr   /* Possible error */
    | expr / expr   /* Possible error */
    | ~ expr
    | expr < expr   /* Possible error */
    | expr <= expr  /*Possible error */
    | expr = expr   /* Possible error */
    | not expr
    | (expr)
    | ID
    | integer
    | string
    | true
    | false
    ;

