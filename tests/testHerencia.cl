class Main inherits IO{

   main(): SELF_TYPE {
      out_string("Hello")
   };
};

class A {
   fun(num: Int): Int {
      (let z : Int in
         {
            z <- ~num;
         }
      )
   };
};

class B inherits A {
   fun2(num: String): String {
      (let z : String in
         {
            z <- "Hola";
         }
      )
   };
};
