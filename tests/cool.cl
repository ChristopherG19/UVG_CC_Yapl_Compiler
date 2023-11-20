class Main inherits IO {
    main() : Void {
    {
        out_string((new Object).type_name().substr(3,2));
        out_string((isvoid self).type_name().substr(0,3));
        out_string("5");
    }
    };
};