class A {
   var: Int <- 5;

   returnVar(): Int {
      var
   };
};

class B inherits A {
   var1: Int <- 5;
};

class Main inherits IO {
	
   x: Int;
   str: String;
   y: Int;
   z: Int;

   a: A <- (new A);

   m: Int;
   n: Int <- (5 + 4);

   meth1(n:Int): Int {
      m <- n
   };

   meth2(): String {
      {
         {
            "hola";
         };
      }
   };

   main() : SELF_TYPE {
      {
         x <- ~ 5;

         if (x = 5) then 
            str <- "igual"
         else
            if ((x >= 0) & (x < 10)) then 
               str <- "mayor"
            else
               str <- "menor"
         fi fi;

         if x = 0 then 
            out_string("igual")
         else
            out_string("desigual")
         fi;

         while NOT (x = 0)
         LOOP 
            x <- x - 1
         POOL;

         let 
            str2: String <- "hehe,", 
            jjj: Int <- (5*8),
            lll: Int <- 5,
            mmm: Int, 
            nnn: Bool 
         in 
         {
            mmm <- jjj;
            if mmm = 5 then
               nnn <- False
            else
               nnn <- True
            fi;
            out_string(str2);
         };

         y <- (x - 5) + x * 5;

         out_string(str);

         meth1(5 + 6);

         z <- a.returnVar();
         z <- a.var;

         str.abort();

      }
   };
};






