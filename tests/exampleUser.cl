class Main inherits IO {
   a: Int <- 0;
   b: Int <- 8; 
   c: Int <- ((a * 9) * (b * 7))
   d: Int <- ((a * 9) * (b * 7))
   

   main() : SELF_TYPE {{
      self;
   }};
};

