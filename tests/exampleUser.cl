class Main inherits IO {
   a : Int <- 10;
   b : Int <- 2;
   d : Int <- a+b; 
   f : Int <- 5; 
   g : Int <- 5; 

   h : Bool <- True;
   i : Bool;

   main() : SELF_TYPE {{

      (*
      f <- 4;
      while f > 0 loop
      f <- (f - 1);
      pool;
      *)
      
      if f = 4 then 
         out_int(1)
      else
         out_int(0)
      fi;


      h <- True;
      i <- False;
      
      j <- (h & i);

      if i = True then 
         out_int(1)
      else
         out_int(0)
      fi;
        
    }};
};