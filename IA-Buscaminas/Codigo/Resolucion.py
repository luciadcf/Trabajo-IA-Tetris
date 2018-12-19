from Juego import Juego
import time

NumDerrotas = 0
def resolucion(filas, columnas, minas):
	
	global NumDerrotas
	NumDerrotas = 0

	return _resolucion(filas, columnas, minas)

def _resolucion(filas, columnas, minas):
	
	global NumDerrotas

	
	print("Tamano del tablero: Filas = {0} ; Columnas = {1} ; Minas = {2}".format(filas, columnas, minas))
	
	try:
		
		buscaminas_bayesiano = Juego(filas, columnas, minas)

		print()
		print()
		print("Tablero Destapado")
		print(buscaminas_bayesiano.tableroDestapadoString())
		
		
		"""
			En primer lugar se va a optar por destapar una casilla que no sea mina, aunque puede optarse por destapar una cualquiera.
			
		"""
		casilla_destapada = False
		for fila in range (buscaminas_bayesiano.filas):
			if (casilla_destapada):
				break
			for columna in range (buscaminas_bayesiano.columnas):
				if (buscaminas_bayesiano.tableroBuscaminas[fila][columna] != 'M'):
					buscaminas_bayesiano.destapar_posicion (fila, columna)
					casilla_destapada = True
					break

		"""
			Comienzo del tiempo del juego
		"""
		comienzo = int(round(time.time()))

		while (True):
			
			print()
			print("Tablero oculto")
			print(buscaminas_bayesiano.tableroAResolverString())
			
			# Tiempo inicial de la primera instancia del juego
			paso1 = int(round(time.time()))
			
			
			buscaminas_bayesiano.red_bayesiana()
			
			# Tiempo final de la primera instancia del juego
			paso2 = int(round(time.time()))
			
			print()
			print("Tiempo de paso: {0} segundos".format(float(paso2 - paso1)))
			print("Destapando casilla: {0}".format(buscaminas_bayesiano.mejor_oculta))
			
			"""
				Una vez destapada la primera casilla del juego, se van a optener un conjunto de casillas con mejor probabilidad de no contener una mina,
				por tanto, como opción para un segundo paso y sucesiones es destapar estas casillas.
			"""
			for var in buscaminas_bayesiano.mejor_oculta:
				buscaminas_bayesiano.destapar_posicion (int(var[6]), int(var[7]))
				

			print("Nuevo tablero oculto")
			print(buscaminas_bayesiano.tableroAResolverString())
			
			
			"""
				Cuenta las casillas restantes que faltan por destaparse, es decir, el numero de casillas ocultas existentes para ese momento.
			"""
			contador = 0
			for fila in range (buscaminas_bayesiano.filas):
				for columna in range (buscaminas_bayesiano.columnas):
					if (buscaminas_bayesiano.tableroOculto[fila][columna] == 'T'):
						contador+=1

			"""
				PARTIDA GANADA:
				
				Si el numero de casillas que faltan por destaparse es el mismo numero de minas, es que todas ellas son minas, luego el juego se gana
			"""
			if(contador == buscaminas_bayesiano.minas):
				#buscaminas_bayesiano.mostrarTableroAResolver()
				print ("Has ganado")
				print ("Veces perdidas: {0}".format(NumDerrotas))
				
				break
			
		# Tiempo final del juego
		final = int(round(time.time()))
		tiempoTotal = float(final - comienzo)

		print ('Terminado en {0} segundos'.format(tiempoTotal))
		
	# Perdida
	except Exception as ex:
		print (ex)
		
		final = int(round(time.time()))

		print("Ultimo tablero resuelto")
		print(buscaminas_bayesiano.tableroAResolverString())
		print()
		print("Has perdido!")
		print("Terminado en {0} segundos".format(float((final - comienzo))))
		
		
		NumDerrotas += 1
		buscaminas_bayesiano.minesList = []
		NumDerrotas, tiempoTotal = _resolucion(filas, columnas, minas)

	return NumDerrotas, tiempoTotal

	
def autoresolucion(intentos, tableros):
	


	for tablero in tableros:
		numDerrotas = []
		tiempos = []
		for _ in range(intentos):
			derrota, tiempo = resolucion(tablero[0], tablero[1], tablero[2])
			numDerrotas.append(derrota)
			tiempos.append(tiempo)
		
		
		
		print("Partida terminada tras {0} intentos\n".format(intentos))
		print("Tamano del tablero: Filas = {0} ; Columnas = {1} ; Minas = {2}\n".format(tablero[0], tablero[1], tablero[2]))
		print("Numero de derrotas: {0}\n".format(numDerrotas))
		print("Tiempo : {0} segundos\n".format(tiempos*60))

"""
	Pruebas realizadas	
"""


autoresolucion(10, [[5,5,5]])
'''
autoresolucion(10, [[5,5,6]])

autoresolucion(10, [[5,5,7]])

autoresolucion(10, [[8,8,13]])

autoresolucion(1, [[8,8,14]])

autoresolucion(1, [[8,8,15]])

autoresolucion(1, [[10,10,20]])

autoresolucion(1, [[10,10,22]])

autoresolucion(1, [[10,10,25]])
'''