class A {
   a: Int <- 5;
   var: Int <- 5;
   
   returnA (): Int {
      a
   };

   returnVar(num: Int): Int {
      var <- (var + 5)
   };
   
};

class Main inherits IO {
   a: Int <- 0;
   b: Int <- 8; 
   c: Int <- ((a - (b * 6) + a) * (b * 7));
   d: Int <- ((a * 9) * (b * 7));
   e: Bool <- ((a < b) & (c = d) | (a >= d));
   f: Bool;
   -- k: String;
   classA: A <- (new A);

   retV(): Bool {
      True
   };

   main() : SELF_TYPE{{
      f <-  <- ((a > b) & (a <= d));
      if f = True then {
         a <- (b + 4);
         b <- (7 * d);
      }else 
         b <- (a - 4) 
      fi;

      WHILE a = b LOOP
         WHILE a < c LOOP 
            a <- (b + (8 * 5));
         POOL
      POOL;
      
      let a: Int <- (8 + 5), b: Bool <- ((a < b) | (c > d)), n: Int <- (4*5) in {
         f <- b;
         let a: String <- "hello" in e <- b;
         out_int(a);
         out_int(classA.var);
      };

      classA.returnVar(classA.returnA());

      self;

   }};
};

