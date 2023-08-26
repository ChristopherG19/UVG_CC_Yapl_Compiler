class Main inherits IO {
    main() : SELF_TYPE {
	{
	    out_string((new String).type_name().substr(4,1)).
	    out_string(("string example").type_name().substr(1,3));
	    out_string("\n");
	}
    };
};
