class CodigoIntermedio:

    def __init__(self, fileName:str) -> None:

        self.filename = fileName
        self.text = ""

        # counters
        self.tag_counter = 0
        self.temp_counter = 0



    def add_If(self):
        
        self.text += f"\t\tif condition goto L{self.tag_counter + 1}\n"
        


    def build(self):

        self.text += "EOF"

        try:
            with open(self.filename, 'w') as file:
                file.write(self.text)

        except:
            print(f"Error abriendo archivo {self.filename}")

