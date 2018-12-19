import pgmpy.models as pgmm
import pgmpy.factors.discrete as pgmf
import pgmpy.inference as pgmi
import Metodos as me


class Buscaminas:

	def __init__(self, filas, columnas, minas):
		
		self.filas = filas
		self.columnas = columnas
		self.minas = minas
		self.tableroOculto = me.crearTableroOculto(filas, columnas)
		self.tableroBuscaminas = me.crearTablero (filas, columnas, minas)
		
	"""
		Función que invoca al método encargado de ocultar el tablero
		
	"""
	def mostrarTableroAResolver(self): 
		
		me.mostrarTablero (self.tableroOculto)
		
	
	"""
		Función que invoca al método encargado de mostrar el tablero destapado
		
	"""
	
	
	def mostrarTableroDestapado(self):
		
		me.mostrarTablero (self.tableroBuscaminas)
		
	"""
		Método que convierte el tablero oculto a string para un mejor mapeo.

	"""

	def tableroAResolverString(self):
		
		return me.tableroAString (self.tableroOculto)
	
	"""
		Método que convierte el tablero destapado a string para un mejor mapeo.

	"""

	def tableroDestapadoString(self):
		
		return me.tableroAString (self.tableroBuscaminas)
	
	"""
		Método que destapa la posición de una determinada casilla del tablero.

	"""

	def destapar_posicion(self, fila, columna):
		
		return me.destapar_casillas_tablero (fila, columna,self.tableroBuscaminas, self.tableroOculto)

class Juego (Buscaminas):
	
	def __init__(self, filas, columnas, minas):
		
		super().__init__(filas, columnas, minas)
		self.Minas_encontradas = []

	def red_bayesiana(self):
		
		"""
        Creamos la red bayesiana con la librería pgmpy
    	"""
		Buscaminas_bayesiano = pgmm.BayesianModel()

		"""
        Variables importantes:
         x_totales: casillas ocultas totales del tablero
         x_ocultas: casillas ocultas con vecinos destapados
         y_destapadas: casillas destapadas
    	"""
		x_ocultas = []
		x_totales = []
		y_destapadas = []
		casilla_oculta_sin_colindantes_destapados = False
		
		
		"""
        Añadimos los nodos a la red.
        Serán las casillas ocultas con vecinos destapados y las casillas destapadas.
    	"""
		for fila in range(self.filas):
			for columna in range(self.columnas):
				# Si la casilla no está pulsada
				if (self.tableroOculto[fila][columna] == 'T'):
					x = 'Tapada{0}{1}'.format(fila,columna) # Lo pone en formato Tapada01,Tapada02...

					x_totales.append(x) # Añadimos las casillas sin pulsar a la variable x_totales

					casilla_tiene_vecinos_destapados = False
					# Obtenemos la posicion de las casillas vecinas
					casillas_vecinas = me.posicion_casillas_vecinas(self.tableroOculto, fila, columna)
					
					# Recorro todas las casillas vecinas de la casilla en la que estamos actualmente
					for vecino in casillas_vecinas:
						# Comprobamos que los vecinos de la casilla estan destapados
						if (self.tableroOculto[int(vecino[0])][int(vecino[1])] != 'T'):
							casilla_tiene_vecinos_destapados = True
							break
					
					# Comprobamos que la casilla actual tiene vecino destapado
					if (casilla_tiene_vecinos_destapados or not casilla_oculta_sin_colindantes_destapados):
						# Si lo tiene, añadimos la casilla a la lista de casillas tapadas con vecinos destapados
						x_ocultas.append(x)
						Buscaminas_bayesiano.add_nodes_from([x]) # Se añade la casilla como nodo de nuestra red

					if (not casilla_tiene_vecinos_destapados):
						casilla_oculta_sin_colindantes_destapados = True
				
				# Si la casilla está pulsada
				else:
					y = 'Destapada{0}{1}'.format(fila,columna) # lo pone en formato Destapada 01,Destapada 02...
					
					#Listado_de_minas = listado_de_minas(tableroBuscaminas) # Variable que contiene la posición de las minas del tablero
					casilla_tiene_vecinos_ocultos = False
					casillas_vecinas = me.posicion_casillas_vecinas(self.tableroOculto, fila, columna)
					
					
					for vecino in casillas_vecinas:
						casilla_vecina_oculta = 'Tapada{0}{1}'.format(vecino[0], vecino[1])
						if (self.tableroOculto[int(vecino[0])][int(vecino[1])] == 'T' and
							not self.Minas_encontradas.__contains__(casilla_vecina_oculta)):
							casilla_tiene_vecinos_ocultos = True
							break

					if (casilla_tiene_vecinos_ocultos):
						y_destapadas.append(y)
						Buscaminas_bayesiano.add_nodes_from([y])

		print("Lista de casillas vecinas ocultas:\n")
		print(x_ocultas)
		print("Lista de casillas destapadas:\n")
		print(y_destapadas)

		print("Lista de minas encontradas:\n")
		print(self.Minas_encontradas)

		"""
        Añadimos las aristas entre los nodos.
        Las casillas destapadas tendrán aristas con sus vecinas ocultas
    	"""    	
		Aristas = dict()
		for fila in range(self.filas):
			for columna in range(self.columnas):
				y = 'Destapada{0}{1}'.format(fila,columna)
				
				
				# Si la casilla ha sido destapada y se ha añadido a la lista de casillas destapadas
				if (self.tableroOculto[fila][columna] != 'T' and y_destapadas.__contains__(y)):
					ListaColindantesOcultos = []
					
					# Obtenemos la posicion de las casillas vecinas
					casillas_vecinas = me.posicion_casillas_vecinas(self.tableroOculto, fila, columna)
					
					# Recorremos sus vecinos
					for vecino in casillas_vecinas:
						x = 'Tapada{0}{1}'.format(vecino[0], vecino[1])
						
						# Si el vecino es oculto añadimos la arista de la destapada a la tapada
						if (x_ocultas.__contains__(x)):
							Buscaminas_bayesiano.add_edges_from([(x, y)])
							ListaColindantesOcultos.append(x)
					
					# Asociamos la casilla destapada con todos sus vecinos ocultos  
					Aristas.update({y: ListaColindantesOcultos})

		
		"""
	        Generación de tablas de probabilidad (CPDs)
	         Las tablas de probabilidad de las casillas tapadas no dependen de nada.
	         Las tablas de probabilidad de las casillas destapadas dependen de sus casillas vecinas tapadas.	
		    Para cada variable creamos una instancia de la clase `TabularCPD`, proporcionando:
		    Nombre de la variable (atributo `variable`),
		    Cantidad de valores (cardinalidad) que puede tomar (atributo `variable_card`),
		    Lista de listas, conteniendo cada una de estas las probabilidades para un valor concreto, 
		    según los valores de los padres (atributo `values`, el valor se transforma a un array),
		    Lista con los nombres de los padres (atributo `evidence`, valor `None` si no se proporciona),
		    Lista con la cantidad de valores (cardinalidad) que puede tomar cada uno de los padres (atributo `evidence_card`, 
		    valor `None` si no se proporciona).
    	"""
		"""
        	Tabla de probabilidad de las casillas tapadas
   		"""
		
		ListadoDestapadas = dict()
		for fila in range(self.filas):
			for columna in range(self.columnas):
				
				x = 'Tapada{0}{1}'.format(fila,columna)
				y = 'Destapada{0}{1}'.format(fila,columna)
				if (self.tableroOculto[fila][columna] == 'T' and x_ocultas.__contains__(x)):
					
					# Si la casilla por detapar es una mina
					if (self.Minas_encontradas.__contains__(x)):
						probabilidad_mina = 1
					
					# Si el numero de casillas por destapar es mayor que el numero de minas que tiene el tablero
					elif (len(x_ocultas) > 0):
						probabilidad_mina = (self.minas-len(self.Minas_encontradas))/len(x_totales)
					
					else:
						probabilidad_mina = 0

					# Añadimos la cpd al modelo
					cpd = pgmf.TabularCPD(x, 2, [[1-probabilidad_mina, probabilidad_mina]])
					Buscaminas_bayesiano.add_cpds(cpd)

				# CPD de Destapadas
				elif (self.tableroOculto[fila][columna] != 'T' and y_destapadas.__contains__(y)):
					
					ListadoDestapadas.update({y: int(self.tableroOculto[fila][columna])})
					
					#A continuación divido entre los valores que puede tener 'Destapada' en función de las minas que tenga alrededor
					nColumnasCPD = pow(2, len(Aristas[y]))
					
					numero_maximo_minas = 9

					
					if (fila == 0 or fila == self.filas-1):
						numero_maximo_minas = 6
					if (columna == 0 or columna == self.columnas-1):
						
						if (numero_maximo_minas == 6):
							numero_maximo_minas = 4
						
						else:
							numero_maximo_minas = 6

					if (len(Aristas[y])+1 < numero_maximo_minas):
						numero_maximo_minas = len(Aristas[y])+1

					
					listaProb = []
					for var in range(numero_maximo_minas):
						listaFila = []
						contador = 0
						for x in range(nColumnasCPD):
							if (var == bin (contador).count('1')):
								listaFila.append(1)
							else:
								listaFila.append(0)
							contador += 1

						listaProb.append(listaFila)

					ListaCardinalidad = []
					for _ in range(len(Aristas[y])):
						ListaCardinalidad.append(2)

					
					cpd = pgmf.TabularCPD(y, numero_maximo_minas, listaProb, Aristas[y], ListaCardinalidad)
					Buscaminas_bayesiano.add_cpds(cpd)

		
		Buscaminas_bayesiano_ev = pgmi.VariableElimination(Buscaminas_bayesiano)

		
		consultas = []
		for var in x_ocultas:
			if (not var in self.Minas_encontradas):
				consulta = Buscaminas_bayesiano_ev.query([var], ListadoDestapadas)
				consultas.append(consulta)


		
		ocultasProbabilidadDeNoSerMina = dict()
		for var in consultas:
			x = ''
			probabilidadDeNoSerMina = 0
			for var1 in var.keys():
				x = str(var1)
			for var2 in var.values():
				probabilidadDeNoSerMina = float(var2.values[0])

			if (probabilidadDeNoSerMina == 0.0):
				self.Minas_encontradas.append(x)

			ocultasProbabilidadDeNoSerMina.update({x: probabilidadDeNoSerMina})

		
		maximaProbabilidadDeNoSerMina = 0.
		ocultaMaximaProbabilidadDeNoSerMina = ''
		mejor_oculta = []
		print("Oculta con mayor probabilidad de no ser mina")
		for x, probabilidadDeNoSerMina in ocultasProbabilidadDeNoSerMina.items():
			print("x: {0} -> Probabilidad de no ser mina: {1}".format(x, probabilidadDeNoSerMina))
			if (maximaProbabilidadDeNoSerMina < probabilidadDeNoSerMina):
				ocultaMaximaProbabilidadDeNoSerMina = str(x)
				maximaProbabilidadDeNoSerMina = probabilidadDeNoSerMina
				mejor_oculta = []
				mejor_oculta.append(ocultaMaximaProbabilidadDeNoSerMina)
				
			if (probabilidadDeNoSerMina == 1.0 and not x in mejor_oculta):
				mejor_oculta.append(x)

		
		self.mejor_oculta = mejor_oculta
		print("Lista de mejores ocultas con alta probabilidad de no ser minas: {0}".format(self.mejor_oculta))
		#print(self.mejor_oculta)
				

