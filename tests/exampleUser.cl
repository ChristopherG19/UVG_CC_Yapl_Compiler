class A {
   og: Int <- 452 + 9;
   var: Int <- ((5) * og) * (4 * (og));
   booool: Bool <- NOT (False);
   xdd: Int <- (5);

   returnVar(): Int {
      var + 7
   };
};

class B inherits A {
   var1: Int <- 5;

   setVar1(h: Int): Int {
      var1 <- h
   };
};

class C inherits B {

   method6(num : Int) : A { -- negate
      (let x : Int in
         {
            x <- ~num;
	    (new A).set_var(x);
         }
      )
   };

   method5(num : Int) : A {  -- cube
      (let x : Int in
	 {
            x <- num * num * num;
	    (new A).set_var(x);
	 }
      )
   };

};

class D inherits B {  
		
   method7(num : Int) : Bool {  -- divisible by 3
      (let x : Int <- num in
            if x < 0 then method7(~x) else
            if 0 = x then true else
            if 1 = x then false else
	    if 2 = x then false else
	       method7(x - 3)
	    fi fi fi fi
      )
   };

};

class E inherits D {

   method6(num : Int) : A {  -- division
      (let x : Int in
         {
            x <- num / 8;
	    (new A).set_var(x);
         }
      )
   };

};


class Main inherits IO {
   
   char : String;
   avar : A; 
   a_var : A;
   flag : Bool <- true;



   is_even(num : Int) : Bool {
      (let x : Int <- num in
            if x < 0 then is_even(~x) else
            if 0 = x then true else
	    if 1 = x then false else
	          is_even(x - 2)
	    fi fi fi
      )
   };

   main() : SELF_TYPE {
      {
         avar <- (new A);
	      avar.set_var(2);
         out_int(avar.value());
         
         if is_even(avar.value()) then
	          out_string(" es par!\n")
	      else
	          out_string(" es impar!\n")
	      fi;
	     
         a_var <- (new A).set_var(3);
	      avar <- (new B).method2(avar.value(), a_var.value());
         out_int(avar.value());
         out_string("\n");
         
         
         avar <- (new C).method6(avar.value());
         out_int(avar.value());
         out_string("\n");
        
         a_var <- (new A).set_var(5);
         avar <- (new D).method4(avar.value(), a_var.value());
         out_int(avar.value());
         out_string("\n");
        
         avar.set_var(5);
         avar <- (new C)@A.method5(avar.value());
         out_int(avar.value());
         out_string("\n");
      	 
         avar.set_var(6);
         avar <- (new C)@A.method5(avar.value());
         out_int(avar.value());
         out_string("\n");



      }
   };
};

