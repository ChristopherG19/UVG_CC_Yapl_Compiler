class Main inherits IO {
  a : Int <- 10;
  b : Int <- 2;
  
  retA() : Int {
    a
  };

  retB() : Int {
    b
  };


  main() : SELF_TYPE {
    out_int(retA()  + retB());
  };
};