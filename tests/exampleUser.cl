class Main inherits IO {

   a : Int <- 10;
   b : Int <- 2;

   x : Bool <- True;
   y : Bool <- False; 

   main(): SELF_TYPE {
      if x & y
      then 
         out_int(100)
      else 
         out_int(0)
      fi;
   };

};