class Main inherits IO {
	
   x: Int;
   str: String;
   y: Int;

   m: Int;
   n: Int <- (5 + 4);

   meth1(n:Int): Int {
      m <- n
   };

   main(): SELF_TYPE {
      {
         x <- 5;

         if (x = 5) then 
            str <- "igual"
         else
            if ((x >= 0) & (x < 10)) then 
               str <- "mayor"
            else
               str <- "menor"
         fi fi;

         y <- (x - 5) + 9 * 5;

         out_string(str);

         meth1(5 + 6);

      }
   };
};


