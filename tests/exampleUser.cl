class Main inherits IO {
	
   x: Int;
   str: String;
   y: Int;

   meth1(): Int {
      3
   }

   main(): SELF_TYPE {
      {
         x <- 5;

         if ((x > 0) & (x < 10)) then 
            str <- "mayor"
         else
            str <- "menor"
         fi;

         y <- (x - 5) + 9;

         out_string(str);
      }
   };
};