
class Str {
  a: String <- "aa";
  b: String <- "bb";
  c: String;
  d: Int <- 3;
  nnn: String <- "lol";

  getA(): String {
    a
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

  fun(x: Int, y: Int): Int {
    {
      let f: Int <- 0 in 0;
    }
  };

  str_ins: Str <- (new Str);

  fun2(): String {
    {
      str_ins.b;
    }
  };

  rand: Rand <- (new Rand);

  prueba: String <- rand.sss.a;


  main () : SELF_TYPE { self };
};



