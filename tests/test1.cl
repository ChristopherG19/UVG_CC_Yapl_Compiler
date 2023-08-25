class Main inherits IO {
    a: Int <- 0;
    c: Int <- 0;
    d: Int <- a+c;
    main() : SELF_TYPE {{
      out_string(f);
    }
  };
};