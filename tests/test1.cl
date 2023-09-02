class Main inherits IO {
    a: Int <- 0;
    c: Int <- 2;
    d: Int <- a+c;
    e: String;
    main() : SELF_TYPE {{
      out_string(e);
    }
  };
};