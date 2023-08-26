class Main inherits IO {
  x: Int <- 5;
  
  process():Int {
    {
      let x : Int in 0;
      x <- x + 5;
    }
  };
  
  main(): SELF_TYPE {
	  out_string("Hello, World.\n")
  };
};