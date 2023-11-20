class Main inherits IO {
   a: Int <- 0;

   main(): SELF_TYPE {{
      while a < 10 loop {
         out_int(a);
         a <- a + 1;
      }
      pool;

      if False
      then 
         out_int(100)
      else 
         out_int(0)
      fi;
   }};
};