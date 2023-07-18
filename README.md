# UVG_Compilador_CC
# Laboratorio#0
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
</p>
<br>
En el cuadro de texto es posible ingresar una expresión a evaluar, luego de haberla ingresado se presiona el botón correspondiente y se muestra el árbol en una GUI independiente y adicional se imprime en consola en forma de texto. Existe la opción de limpiar el inputArea y también salir del programa.

### Ejemplo:
*Gramática*
<a href="https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/blob/main/YAPL.g4">YAPL.g4</a>

Resultado expresión sin errores
<p align="center">
  <img src="https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/assets/60325784/23685454-c7fd-4991-b2c4-2244d01bda95"/>
</p>
<br>
Resultado expresión con errores
<p align="center">
  <img src="https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/assets/60325784/f8a9b4df-463d-49a1-805a-b451858c843f"/>
</p>
En este segundo caso no sé muestra ningún árbol porque existen varios errores

## Resultados

### Ejemplo 1
![image](https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/assets/60325784/fa1014ab-0d26-48b7-84de-9c26cd2de1ad)

### Ejemplo 2
![image](https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/assets/60325784/33f3a7db-37c5-4fdb-a474-7fc7b41dad9e)

### Ejemplo 3
![image](https://github.com/ChristopherG19/UVG_CC_Yapl_Compiler/assets/60325784/b311cd04-2227-41b9-aa80-3ab6243e88aa)



