# UVG_Compilador_CC
# Laboratorio#1
## Objetivos:
- Familizarizarse con YAPL: con ayuda de los archivos del curso y herramientas brindadas por el laboratorio se buscaba entender mejor la estructura y funcionamiento de este lenguaje.
- Generación de Scanner y Parser: se recomendó utilizar ANTLR para la generación del parser y lexer que permitieran la creación y recorrido de árboles de análisis sintáctico por lo que se tuvo que realizar una investigación respecto al funcionamiento, sintaxis e implementación de esta herramienta
- Presentación de resultados: para mostrar los resultados obtenidos fue necesario la creación de una GUI funcional y amistosa con el usuario. En la GUI desarrollada se trabaja con un diseño sencillo en el cual el usuario es capaz de ingresar una expresión y generar el árbol. (La gramática se agrega directamente en el código)
 
## Funcionamiento
### *Instalaciones necesarias*
```
pip install antlr4-tools
```
```
pip install antlr4-python3-runtime
```
### *Gramática*<br>
Archivo a modificar: <a href="https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/blob/main/YAPL.g4">YAPL.g4</a>

### *Ejecución del programa*
Archivo a ejecutar: <a href="https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/blob/main/main.py">main.py</a>

Luego de ejecutar el programa, y esperando que se hayan instalado todas las librerías y plugins necesarios, aparece una ventana similar a esta:
<p align="center">
  <img src="https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/assets/60325784/e61ff2a1-5eb0-43d2-9977-bcc888026dff"/>
  <br>Ahora en modo oscuro
</p>
<br>
En el cuadro de texto es posible ingresar una expresión a evaluar, luego de haberla ingresado se presiona el botón correspondiente y se muestra el árbol en una GUI independiente y adicional se imprime en consola en forma de texto. Existe la opción de limpiar el inputArea y también salir del programa.<br>

Luego de haber corrido el programa una vez, o podría intentar de una vez con los archivos que ya están subidos, ejecutar el siguiente archivo: Archivo a modificar: <a href="https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/blob/visitor-pattern/BuildTable.py">BuildTable.py</a>


