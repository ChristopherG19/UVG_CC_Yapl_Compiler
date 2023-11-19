class Fibonacci {
  	
  	fibonacci(n: Int) : Int {
        {( let f : Int in
      	 if n=1 then f<-1 else
         if n=2 then f<-1 else
        	 f<-(fibonacci(n-1)+fibonacci(n-2) + fibonacci(n-3))
         fi fi
       );}
     };
  
  };

class Main inherits IO {
    n: Int <- 4;
    myfibonacci: Fibonacci;

    main() : SELF_TYPE {
        {
            myfibonacci <- new Fibonacci;
            out_int(myfibonacci.fibonacci(n));
        }
    };
};

