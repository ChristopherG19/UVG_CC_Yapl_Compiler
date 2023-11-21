class Main inherits IO {
    main() : SELF_TYPE {
    {
        out_string((new Object).type_name().substr(4,3));
        out_string((isvoid self).type_name().substr(0,3));
        out_string("5");
    }
    };
};