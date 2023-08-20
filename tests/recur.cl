class Factorial {
  	var: Int <- 0;
  	
  	factorial(n: Int) : Int {
      {( let f : Int in
      	 if n=0 then f<-0 else
         if n=1 then f<-1 else
        	 f<-n*factorial(n-1)
         fi fi
       );}
    };
  
  };

class Fibonacci {
  	
  	fibonacci(n: Int) : Int {
        {( let f : Int in
      	 if n=1 then f<-1 else
         if n=2 then f<-1 else
        	 f<-fibonacci(n-1)+fibonacci(n-2)
         fi fi
       );}
     };
  
  };

class Main inherits IO {
    n: Int <- 10;
  	facto: Factorial;
  	fibo: Fibonacci;
  
  	main() : SELF_TYPE {
	{
	    facto <- new Factorial;
      	fibo <- new Fibonacci;
      	--out_int(facto.factorial(n));
      	out_int(fibo.fibonacci(n));
      	self;
	}
    };
};
