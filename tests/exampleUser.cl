class Obj inherits IO{
    a : Int <- 2;

    print(): SELF_TYPE{
        out_int(a);
    };
};

class Main inherits IO {
    a : Int <- 4;
    b : Obj;

    main() : SELF_TYPE {
        {
            b <- new Obj;
            b.print();
            out_int(a);
        }
    };
};