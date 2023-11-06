class Main inherits IO {
    a : Int <- 10;
    b : Int <- 2;
    d : Int <- a+b; 
    f : Int <- 4; 
    g : Int <- 5; 

    main() : SELF_TYPE {
        {
         (let c : Int <- 5  in
            {
               out_int(f);
               d <- ((c + 2) * (5));
               
               out_int(g);
            }
        );

        out_int(d);
        out_int(b);
        }
    };
};