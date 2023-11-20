class Main inherits IO {

   out : Int <-		-- out is our 'output'.  It's values are the primes.
   {
      out_string("2 is trivially prime.\n");
      2;
   };

   err : String <- "halt mmmm";
  
   testee : Int <- out;	-- testee is a number to be tested for primeness.   
   divisor : Int;	-- divisor is a number which may factor testee. 
   stop : Int <- 500;	-- stop is an arbitrary value limiting testee. 	

   main() : Object {{	-- main() is an atrophied method so we can parse. {
      while true loop {
         err.abort();
      } pool;
   }};
};