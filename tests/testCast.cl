class Main inherits IO{
   
    a: Int <- True - 3;            
    b: Int <- (10 - 7 = 3) + 1;      
    c: Bool <- (6 * 4 >= 25) + 1; 
    d: Bool <- (20 / 4) & false;        
    e: Int <- (3 * 3 + 2) + not true;     
    f: Int;
    g: String;
    h: Bool;
    i: Int <- 2 + 2;
    j: Bool <- False;

    main(): SELF_TYPE {
        out_string("Hello World\n")
    };
};