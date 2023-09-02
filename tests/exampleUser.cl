class Str {
  a: String <- "aa";
  b: String <- "bb";
  c: String;
  d: Int <- ~3;
  e: Bool <- True;
  nnn: String <- "lol";

  getA(): String {
    a
  };

  getD(): Int {
    d
  };

  meth(n: String): String {
    {
      c <- n;
    }
  };
};

class Rand {
  
  sss: Str <- (new Str);

};


class Main inherits IO {

  a: Int;
  b: Int;
  xd: String;

  fun(x: Int, y: Int): Int {
    {
      let f: Int <- 0 in 0;
    }
  };

  funss(): String {
    {"a";}
  };

  str_ins: Str <- (new Str);

  rand: Rand <- (new Rand);

  intint: Int;
  intintint: Int;

  fun2(): String {
    {
      intint <- fun(1, 1);
      intintint <- rand.sss.d;
      intintint <- rand.sss.getD();
      str_ins.b;
      funss();
    }
  };

  prueba: String <- rand.sss.a;


  main () : SELF_TYPE { self };
};