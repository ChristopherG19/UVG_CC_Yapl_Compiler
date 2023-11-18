class Main inherits IO {
    a : Int <- 4;
    b : Int <- 2;
    d : Int <- 1; 
    e : Int <- ~1; 
    f : Int <- 3; 

    sum(x: Int, y: Int): Int {
        {
            (x+y);
        }
    }

    main() : Int {
        let c : Int <- 5  in
            {
                out_int(sum(a,b));
                5;
            }
        
    };
};