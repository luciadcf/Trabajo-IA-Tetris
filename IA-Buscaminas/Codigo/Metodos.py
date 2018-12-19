import random


"""
    Función para crear un tablero destapado.
    Dependerá del número de filas, columnas y número de minas.
""" 

def crearTablero (nFilas, nColumnas, nMinas):
    # Comprobamos que el número de minas existente en el tablero es menor o igual al número de casillas del mismo
    if (nMinas > nFilas * nColumnas): 
        raise Exception('No puede haber más minas que casillas en el tablero') 

    # Construcción del tablero
    tablero = [[0 for columna in range(nColumnas)] for fila in range(nFilas)]
    
    """
        Creamos minas aleatorias en el tablero. 
        Recorremos el número de minas que queremos pintar y en el tablero mostramos "☠" que indica que en esa casilla existe una mina.
    """
    
    for i in range (nMinas):
        rnd_r = -1
        rnd_c = -1
        while (rnd_r == -1 or rnd_c == -1 or tablero[rnd_r][rnd_c] == "M"):  
            rnd_r = random.randint (0, nFilas - 1)
            rnd_c = random.randint (0, nColumnas - 1)                
        
        #Se van colocando las minas    
        tablero[rnd_r][rnd_c] = "M"
        
    # Ahora pasamos a poner los índices de las casillas colindantes con minas. 
    # El número que aparece en la casilla va en un rango de 1 a 8 (arriba, abajo, izquierda, derecha y las 4 diagonales).
    minas_colindantes = 0

    for fila in range (nFilas): 
        for columna in range (nColumnas):
            if (columna+1 < len(tablero[0]) and tablero[fila][columna+1] == "M"): # La mina se encuentra a la derecha
                minas_colindantes = minas_colindantes + 1
            if (columna > 0 and tablero[fila][columna-1] == "M"): # La mina se encuentra a la izquierda
                minas_colindantes = minas_colindantes + 1
            if (fila+1 < len(tablero) and tablero[fila+1][columna] == "M"): # La mina se encuentra abajo
                minas_colindantes = minas_colindantes + 1
            if (fila > 0 and tablero[fila-1][columna] == "M"): # La mina se encuentra arriba
                minas_colindantes = minas_colindantes + 1
            if (fila+1 < len(tablero) and columna+1 < len(tablero[0]) and tablero[fila+1][columna+1] == "M"): # La mina se encuentra en la diagonal inferior derecha
                minas_colindantes = minas_colindantes + 1
            if (fila+1 < len(tablero) and columna > 0 and tablero[fila+1][columna-1] == "M"): # La mina se encuentra en la diagonal inferior izquierda
                minas_colindantes = minas_colindantes + 1
            if (fila > 0 and columna+1 < len(tablero[0]) and tablero[fila-1][columna+1]  == "M"): # La mina se encuentra en la diagonal superior derecha
                minas_colindantes = minas_colindantes + 1
            if (fila > 0 and columna > 0 and tablero[fila-1][columna-1] == "M"): # La mina se encuentra en la diagonal superior izquierda
                minas_colindantes = minas_colindantes + 1
            
            # Pasamos a guardar el índice de minas colindantes en la casilla del tablero donde no hay ninguna mina.
            if (minas_colindantes > 0 and tablero[fila][columna] != 'M'):
                tablero[fila][columna] = str(minas_colindantes)
            
            minas_colindantes = 0

    return tablero


"""
    Función para generar un tablero tapado.
    Las casillas tapadas se mostrarán con el símbolo T
"""
def crearTableroOculto (nFilas, nColumnas):

    tableroOculto = [['T' for columna in range(nColumnas)] for filas in range(nFilas)]

    return tableroOculto


"""
    Función para destapar una casilla del tablero.
    Al pulsar sobre una casilla que no contiene una mina, se van a destapar un
    conjunto colindante de casillas que no tienen minas ni están proximas con otras, es decir, con índice = 0. 
    Como máximo, el límite del destapado va a ser si la casilla que se destapa tiene al menos un vecino con mina.
"""
def destapar_casillas_tablero (fila, columna,tableroBuscaminas, tableroOculto):

    if (tableroOculto[fila][columna] == 'T'):
        
        # Guardo el valor de la casilla en la que pulsamos
        casillaDestapada = tableroBuscaminas[fila][columna]

        # Si la casilla pulsada es una mina:
        if (casillaDestapada == 'M'):
            raise Exception("Has encontrado una mina. Has perdido")

        # Si no lo es, cambiamos su valor en el tablero oculto por el valor de la casilla destapada
        else:
            tableroOculto[fila][columna] = casillaDestapada

        """
            Comprobamos si la casilla que destapamos tiene 0 minas colindantes.
            Si se da el caso, destapamos todas las casillas colindantes a la seleccionada 
            ya que sabemos que ninguna es una mina se comprueba que las colindantes 
            estén dentro del tablero
        """
        if (casillaDestapada == 0):
            if (columna+1 < len(tableroOculto[0])):
                destapar_casillas_tablero (fila, columna+1,tableroBuscaminas, tableroOculto)
            if (columna > 0):
                destapar_casillas_tablero (fila, columna-1,tableroBuscaminas, tableroOculto)
            if (fila+1 < len(tableroOculto)):
                destapar_casillas_tablero (fila+1, columna,tableroBuscaminas, tableroOculto)
            if (fila > 0):
                destapar_casillas_tablero (fila-1, columna,tableroBuscaminas, tableroOculto)
            if (fila+1 < len(tableroOculto) and columna+1 < len(tableroOculto[0])):
                destapar_casillas_tablero (fila+1, columna+1,tableroBuscaminas, tableroOculto)
            if (fila+1 < len(tableroOculto) and columna > 0):
                destapar_casillas_tablero (fila+1, columna-1,tableroBuscaminas, tableroOculto)
            if (fila > 0 and columna+1 < len(tableroOculto[0])):
                destapar_casillas_tablero (fila-1, columna+1,tableroBuscaminas, tableroOculto )
            if (fila > 0 and columna > 0):
                destapar_casillas_tablero (fila-1, columna-1,tableroBuscaminas, tableroOculto)
        
        return tableroOculto

"""
    Función que devuelve un array con los índices de las casillas vecinas a la que se le pasa por parámetros.
"""
def posicion_casillas_vecinas(tablero, fila, columna):
    indicesCasillas = []

    if (columna+1 < len(tablero[0])):
        indicesCasillas.append("{0}{1}".format(fila, columna+1))
    if (columna > 0):
        indicesCasillas.append("{0}{1}".format(fila, columna-1))
    if (fila+1 < len(tablero)):
        indicesCasillas.append("{0}{1}".format(fila+1, columna))
    if (fila > 0):
        indicesCasillas.append("{0}{1}".format(fila-1, columna))
    if (fila+1 < len(tablero) and columna+1 < len(tablero[0])):
        indicesCasillas.append("{0}{1}".format(fila+1, columna+1))
    if (fila+1 < len(tablero) and columna > 0):
        indicesCasillas.append("{0}{1}".format(fila+1, columna-1))
    if (fila > 0 and columna+1 < len(tablero[0])):
        indicesCasillas.append("{0}{1}".format(fila-1, columna+1))
    if (fila > 0 and columna > 0):
        indicesCasillas.append("{0}{1}".format(fila-1, columna-1))

    return indicesCasillas


def mostrarTablero(matrix):
    print()
    tam_x = len(matrix)
    for i in range (tam_x):
        tam_y = len(matrix[i])
        row = ""
        for j in range (tam_y):
            row += str(matrix[i][j]) + " "
        print (row)

def tableroAString(matrix):
    result = ""
    tam_x = len(matrix)
    for i in range (tam_x):
        tam_y = len(matrix[i])
        row = ""
        for j in range (tam_y):
            row += str(matrix[i][j]) + " "
        result += row + "\n"
    return result

