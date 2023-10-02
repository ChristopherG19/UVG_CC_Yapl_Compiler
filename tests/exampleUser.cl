class Main inherits IO {
	
   x: Int;
   str: String;

   main(): SELF_TYPE {
      {
         x <- 5;
         if ((x > 0) & (x < 10)) then 
            str <- "mayor"
         else
            str <- "menor"
         fi;
         out_string(str);
      }
   };
};


