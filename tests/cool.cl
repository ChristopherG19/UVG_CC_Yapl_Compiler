class Main inherits IO {
    main() : SELF_TYPE {
    {
        out_string((new Object).type_name().substr(3,2));
        out_string((new Int).type_name().substr(0,3));
        out_string("5");
    }
    };
};