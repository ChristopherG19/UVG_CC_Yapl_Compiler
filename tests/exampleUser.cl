class Main inherits IO {
   a: Int <- 0;
   c: Int <- 2;
   d: Int <- (a*c);
   e: String;
   f: String <- "hehe";

   setA(numB: Int, d: Int): Int {
      a <- d
   };

   method1(num : Int, numB: Int) : SELF_TYPE {{  -- same
      a <- d;
   }};

   main() : SELF_TYPE {{
      let x: Int <- 9 in {
        let x: Int <- 10 in out_int(x);
        out_int(x);
        let y: Int <- 11 in out_int(y);
      };
   }};
};