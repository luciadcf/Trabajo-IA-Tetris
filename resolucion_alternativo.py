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
		
		print("Tablero oculto")
		print(buscaminas_bayesiano.tableroAResolverString())
		
		
		"""
			En primer lugar se va a optar por destapar una casilla que no sea mina, aunque puede optarse por destapar una cualquiera.
			
		"""
		paso1 = int(round(time.time()))
		buscaminas_bayesiano.destapar_posicion (1, 2)
		
		buscaminas_bayesiano.red_bayesiana()
		
		paso2 = int(round(time.time()))

		"""
			Comienzo del tiempo del juego
		"""
		comienzo = int(round(time.time()))
		
		final = int(round(time.time()))
		tiempoTotal = float(final - comienzo)

		
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


autoresolucion(1, [[5,5,5]])
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