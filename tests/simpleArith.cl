class Main inherits IO {

  a : Int <- 10;
  b : Int <- 2;
  c : Int <- 5;

  res: Int;

  main() : SELF_TYPE  {{
    out_int(a);
    out_int(b);
    out_int(c);

    res <- a + (b - c)
    out_int(res);

    res <- (a * b) / c;
    out_int(res);

    out_int(a - 8);

    out_int(100/5)

  }};

};