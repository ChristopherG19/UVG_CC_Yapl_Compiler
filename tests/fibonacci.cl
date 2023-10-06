class Fibonacci {

    fibonacci(n: Int) : Int {
        {(
            let f: Int in
            if n = 1 then
                f <- 1
            else
                if n = 2 then
                    f <- 1
                else
                    f <- fibonacci(n - 1 + 2) * fibonacci(n - 1 + 2 + 3) + fibonacci(n - 1)
                fi
            fi
        );}
    };

};

class Main inherits IO {
    n: Int <- 5;
    s: Bool;
    t: Bool;
    myfibonacci: Fibonacci;

    main() : SELF_TYPE {
        {
            n <- 5 + 6;
            s <- (true);
            t <- not s;
            myfibonacci <- new Fibonacci;
            out_int(myfibonacci.fibonacci(n));
        }
    };
};

