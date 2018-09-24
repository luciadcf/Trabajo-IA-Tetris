***ESTRUCTURA DEL C�DIGO PYTHON***

La estructura del c�digo ha sido debidamente explicada haciendo uso de comentarios en los propios archivos del c�digo. 

***GU�A PYTHON***

IMPORTANTE:
	Durante la realizaci�n de las pruebas, han aparecido errores con la librer�a de pgmpy.
	Para evitar estos errores, se ha realizado la siguiente modificaci�n en el c�digo de la librer�a:
	- pgmpy/factors/discrete/DiscreteFactor.py Funci�n "normalize" : En la l�nea 376 se debe a�adir la siguiente condici�n:
		if (phi.values.sum() != 0):
            		phi.values = phi.values / phi.values.sum()

AutoplayerLogger.py : Contiene el m�todo principal para realizar cualquier test.
			Se debe indicar el n�mero de iteraciones que se desean realizar para cada configuraci�n de tablero introducida.
			Se debe indicar la ruta en la que guardar el logfile (nombre del archivo de texto incluido).

AutoplayMinesweeper.py : Script auxiliar para la l�gica del comienzo de un nuevo tablero, adem�s de controlar cuando se pierde o gana un tablero.

MinesweeperGame.py : Script principal para la creaci�n del modelo de red bayesiano y la posterior inferencia estad�stica.

BoardUtils.py : Script auxiliar para la generaci�n del tablero del juego del buscaminas y algunas otras funciones para la consulta de estos tableros.

***ESTRUCTURA DEL C�DIGO DE INTERFAZ GR�FICA***

Minesweeper.java : Modela la estructura del juego del buscaminas.

Main.java : Interfaz gr�fica de usuario y l�gica para la interacci�n con una instancia de la clase Minesweeper.

BayesianModelDriver.java: Se encarga de la interacci�n con el int�rprete de Phyton para obtener los resultados de la inferencia probabil�stica aplicada
			  a un tablero dado. 


***GU�A INTERFAZ GR�FICA***

Requisitos: 
-JRE 1.8_171 o superior
-Windows 10
-Los archivos AutoplayScript.py, BoardUtils.py y MinesweeperGame.py deben estar contenidos en la misma carpeta que Autosweeper.jar

Para hacer uso del sistema implementado a trav�s de su interfaz gr�fica debe iniciar Autosweeper.jar

En primer lugar tendremos que hacer click en el bot�n `Phyton� y seleccionar la ruta de su int�rprete de python (debe
extrictamente llamarse python.exe). Si todo es correcto el color del texto del bot�n deber�a ser azul.

A partir de ahora ya podremos jugar al juego del buscaminas.

A trav�s de las cajas de textos correspondientes a 'Rows', 'Columns' y 'Mines' configuraremos el n�mero de columnas, filas y 
total de minas que tendr� el tablero generado despues de hacer click en el bot�n de 'Reset'.

**Modos de juego:

La interfaz est� capacitada para soportar 3 tipos de modos de juego:

	
-Modo cl�sico: Consiste en el modo mas b�sico de juego, sin ning�n tipo de automatizaci�n ni ayuda. 
	
-Modo autom�tico: Se accede mediante el bot�n 'Autoplay' y se activar� todo el proceso de creaci�n de redes bayesianas e
	          inferencia para que el tablero se vaya resolviendo de forma aut�noma.
	
-Modo autom�tico completo: Consiste en la repetici�n del proceso realizado por el modo autom�tico tras resolver o perder un juego.

**Mejor movimiento: 

Si se opta por el modo cl�sico podemos hacer uso del bot�n 'Next move' para que nos recomiende la mejor casilla que pulsar en el siguiente
movimiento.

**Game Info

En la parte derecha podemos observar una 'consola' donde continuamente se representar� informaci�n como:
	-Nodos Xij de la red bayesiana generada.
	-Nodos Yij de la red bayesiana generada.
	-�ltima casilla destapada
	-Mejores casillas para destapar
	-Casillas que se sabe que son minas
	-Probabilidad de cada nodo Xij de no ser mina

**Informaci�n adicional

La duraci�n de una partida siempre se representar� en el campo 'Time'.

En caso de jugar en modo autom�tico completo el total de partidas ganadas, perdidas, y media de tiempo por partida ganada se 
reprentar� en sus correspondientes campos. 


