***ESTRUCTURA DEL CÓDIGO PYTHON***

La estructura del código ha sido debidamente explicada haciendo uso de comentarios en los propios archivos del código. 

***GUÍA PYTHON***

IMPORTANTE:
	Durante la realización de las pruebas, han aparecido errores con la librería de pgmpy.
	Para evitar estos errores, se ha realizado la siguiente modificación en el código de la librería:
	- pgmpy/factors/discrete/DiscreteFactor.py Función "normalize" : En la línea 376 se debe añadir la siguiente condición:
		if (phi.values.sum() != 0):
            		phi.values = phi.values / phi.values.sum()

AutoplayerLogger.py : Contiene el método principal para realizar cualquier test.
			Se debe indicar el número de iteraciones que se desean realizar para cada configuración de tablero introducida.
			Se debe indicar la ruta en la que guardar el logfile (nombre del archivo de texto incluido).

AutoplayMinesweeper.py : Script auxiliar para la lógica del comienzo de un nuevo tablero, además de controlar cuando se pierde o gana un tablero.

MinesweeperGame.py : Script principal para la creación del modelo de red bayesiano y la posterior inferencia estadística.

BoardUtils.py : Script auxiliar para la generación del tablero del juego del buscaminas y algunas otras funciones para la consulta de estos tableros.

***ESTRUCTURA DEL CÓDIGO DE INTERFAZ GRÁFICA***

Minesweeper.java : Modela la estructura del juego del buscaminas.

Main.java : Interfaz gráfica de usuario y lógica para la interacción con una instancia de la clase Minesweeper.

BayesianModelDriver.java: Se encarga de la interacción con el intérprete de Phyton para obtener los resultados de la inferencia probabilística aplicada
			  a un tablero dado. 


***GUÍA INTERFAZ GRÁFICA***

Requisitos: 
-JRE 1.8_171 o superior
-Windows 10
-Los archivos AutoplayScript.py, BoardUtils.py y MinesweeperGame.py deben estar contenidos en la misma carpeta que Autosweeper.jar

Para hacer uso del sistema implementado a través de su interfaz gráfica debe iniciar Autosweeper.jar

En primer lugar tendremos que hacer click en el botón `Phyton´ y seleccionar la ruta de su intérprete de python (debe
extrictamente llamarse python.exe). Si todo es correcto el color del texto del botón debería ser azul.

A partir de ahora ya podremos jugar al juego del buscaminas.

A través de las cajas de textos correspondientes a 'Rows', 'Columns' y 'Mines' configuraremos el número de columnas, filas y 
total de minas que tendrá el tablero generado despues de hacer click en el botón de 'Reset'.

**Modos de juego:

La interfaz está capacitada para soportar 3 tipos de modos de juego:

	
-Modo clásico: Consiste en el modo mas básico de juego, sin ningún tipo de automatización ni ayuda. 
	
-Modo automático: Se accede mediante el botón 'Autoplay' y se activará todo el proceso de creación de redes bayesianas e
	          inferencia para que el tablero se vaya resolviendo de forma autónoma.
	
-Modo automático completo: Consiste en la repetición del proceso realizado por el modo automático tras resolver o perder un juego.

**Mejor movimiento: 

Si se opta por el modo clásico podemos hacer uso del botón 'Next move' para que nos recomiende la mejor casilla que pulsar en el siguiente
movimiento.

**Game Info

En la parte derecha podemos observar una 'consola' donde continuamente se representará información como:
	-Nodos Xij de la red bayesiana generada.
	-Nodos Yij de la red bayesiana generada.
	-Última casilla destapada
	-Mejores casillas para destapar
	-Casillas que se sabe que son minas
	-Probabilidad de cada nodo Xij de no ser mina

**Información adicional

La duración de una partida siempre se representará en el campo 'Time'.

En caso de jugar en modo automático completo el total de partidas ganadas, perdidas, y media de tiempo por partida ganada se 
reprentará en sus correspondientes campos. 


