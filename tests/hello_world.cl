class Main {
   
   a: Int <- True + 3;            -- a: 1
   b: Int <- (10 - 7 = 3) + 1;      -- b: 2
   c: Bool <- (6 * 4 >= 25) & 1;  -- c: 0
   d: Bool <- (20 / 0) | 0;        -- d: 1
   e: Int <- 3 * 3 + 2 > not true;        -- e: 0         
   m: String;
   o: Int <- 4;

   main(): SELF_TYPE {
      out_string("Hello")
   };
};

class A {

  a: Int;
  b: Int;

  fun(x: Int, y: Int): Int {
    {
      b <- y;
      while b > 0 loop 
        b <- b - 1
      pool;
      if b > 10 then 
        b <- b + 1
      else b <- 2
      fi;
      b;
    }
  };
};
