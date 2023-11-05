class Main inherits IO {
    a : Int <- 10;
    b : Int <- 2;
    d : Int <- a+b; 

    main() : Int {
        (let c : Int <- 5  in
            {
                d <- (a+c);
            }
        )
    };
};

