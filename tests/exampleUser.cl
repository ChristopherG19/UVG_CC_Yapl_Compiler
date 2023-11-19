class A inherits IO {
   var: Int <- 5;
};

class Main inherits IO {
   
   a(): Int {
      3
   };

   minia : A <- (new A);

   main () : SELF_TYPE {{
      out_int(a());
      out_int(minia.var);
   }};
};