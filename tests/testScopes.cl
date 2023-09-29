class Main inherits IO {
  x: Int <- 5;
  y: Int <- 5;

  process(y: Int, z: Int):Int {
    {
      let x : Int in 0;
      x <- y;
    }
  };

  z: Bool;
  
  main(): SELF_TYPE {
	  out_int(1)
  };
};