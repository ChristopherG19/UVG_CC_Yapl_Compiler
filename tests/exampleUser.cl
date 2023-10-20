class A {
   var : Int <- 3;

   getVar() : Int {
      var
   };
};

class B {
   var1 : Int <- 0;
   var : Int <- 3;

   getVar() : Int {
      var
   };
};

class Main inherits IO {
   a: Int <- 0;
   c: Int <- ((a + 1) * (a - 3));
   d: Int <- a - (~ c);
   e: String;
   f: String <- "hehe";
   g: Bool <- True;

   setA(numB: Int, d: Int): Int {{
      g <- (a < d);
      a <- (numB * d);
   }};

   method1(num : Int, numB: Int) : SELF_TYPE {{  -- same
      a <- d;
      if g = True then 
         a <- 9
      else
         a <- numB
      fi;
   }};

   classA : A <- (new A);

   main() : SELF_TYPE {{
      a <- (classA.var);
      let classA : B <- (new B) in {
         a <- (classA.getVar());
      };
   }};
};

