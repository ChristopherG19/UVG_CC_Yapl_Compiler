class Main inherits IO {
   
   a: Int <- 5 + 3 or 1;            -- a: 1
   b: Int <- (10 - 7 = 3) + 1;      -- b: 2
   c: Bool <- (6 * 4 >= 25) and 1;  -- c: 0
   d: Bool <- (20 / 4) or 0;        -- d: 1
   e: Int <- 3 * 3 + 2 > 10;        -- e: 0         
   m: String;
   o: Int <- 0 + 1=false;

   main(): SELF_TYPE {
      out_string("Hello")
   };
};
