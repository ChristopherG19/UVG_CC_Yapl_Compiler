class Main inherits IO {

   a : Int <- 0;

   main(): SELF_TYPE {
      while a < 100 loop {
         out_int(a);
         a <- a + 1;

         if a = 15 then 
            "stop".abort() -- parar el programa si a llega a 15
         else 
            0 -- no hacer nada
         fi;
      } pool
   };

};