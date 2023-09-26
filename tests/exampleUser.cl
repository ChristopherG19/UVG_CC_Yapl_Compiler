class Main inherits IO {
  val : Int <- 10;
  main() : String {
    (let val : String in
      {
        val <- "a";
      }
    )
  };
  val2 : Int <- 10;
};