class Main inherits IO {
  val : Int <- 10;
  main() : String {
    (let val : String in
      {
        val <- "hola mundo";
      }
    )
  };
  val2 : Int <- 10;
};