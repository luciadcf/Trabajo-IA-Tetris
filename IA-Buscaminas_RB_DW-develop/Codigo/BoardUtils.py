import random

def printBoard(matrix):
    print()
    tam_x = len(matrix)
    for i in range (tam_x):
        tam_y = len(matrix[i])
        row = ""
        for j in range (tam_y):
            row += str(matrix[i][j]) + " "
        print (row)

def stringBoard(matrix):
    result = ""
    tam_x = len(matrix)
    for i in range (tam_x):
        tam_y = len(matrix[i])
        row = ""
        for j in range (tam_y):
            row += str(matrix[i][j]) + " "
        result += row + "\n"
    return result

def createMinesweeperBoard (tam_x, tam_y, mines_count):

    if (mines_count > tam_x * tam_y): 
        raise Exception('Mines_count max value: {0}'.format(tam_x * tam_y)) 

    gameBoard = [[0 for y in range(tam_y)] for x in range(tam_x)]
    
    for i in range (mines_count):
        rnd_r = -1
        rnd_c = -1
        while (rnd_r == -1 or rnd_c == -1 or gameBoard[rnd_r][rnd_c] == "*"):  
            rnd_r = random.randint (0, tam_x - 1)
            rnd_c = random.randint (0, tam_y - 1)                
       
        gameBoard[rnd_r][rnd_c] = "*"

    acum = 0

    for i in range (tam_x): 
        for j in range (tam_y):
            if (j+1 < len(gameBoard[0]) and gameBoard[i][j+1] == "*"):
                acum = acum + 1
            if (j > 0 and gameBoard[i][j-1] == "*"):
                acum = acum + 1
            if (i+1 < len(gameBoard) and gameBoard[i+1][j] == "*"):
                acum = acum + 1
            if (i > 0 and gameBoard[i-1][j] == "*"):
                acum = acum + 1
            if (i+1 < len(gameBoard) and j+1 < len(gameBoard[0]) and gameBoard[i+1][j+1] == "*"):
                acum = acum + 1
            if (i+1 < len(gameBoard) and j > 0 and gameBoard[i+1][j-1] == "*"):
                acum = acum + 1
            if (i > 0 and j+1 < len(gameBoard[0]) and gameBoard[i-1][j+1]  == "*"):
                acum = acum + 1
            if (i > 0 and j > 0 and gameBoard[i-1][j-1] == "*"):
                acum = acum + 1

            if (acum > 0 and gameBoard[i][j] != '*'):
                gameBoard[i][j] = str(acum)
            
            acum = 0

    return gameBoard

# BoardToResolve
def createBoardToResolve (tam_x, tam_y):

    boardToResolve = [['?' for y in range(tam_y)] for x in range(tam_x)]

    return boardToResolve


# Destapar casilla
def showSquare (resolvedBoard, boardToResolve, square_x, square_y):

    if (boardToResolve[square_x][square_y] == '?'):

        resolvedSquare = resolvedBoard[square_x][square_y]

        # Casilla es mina
        if (resolvedSquare == '*'):
            raise Exception('That was a mine! Unlucky!')

        # Casilla no es mina
        else:
            boardToResolve[square_x][square_y] = resolvedSquare

        # Casilla es 0 por lo que se debe abrir toda la zona
        if (resolvedSquare == 0):
            if (square_y+1 < len(boardToResolve[0])):
                showSquare (resolvedBoard, boardToResolve, square_x, square_y+1)
            if (square_y > 0):
                showSquare (resolvedBoard, boardToResolve, square_x, square_y-1)
            if (square_x+1 < len(boardToResolve)):
                showSquare (resolvedBoard, boardToResolve, square_x+1, square_y)
            if (square_x > 0):
                showSquare (resolvedBoard, boardToResolve, square_x-1, square_y)
            if (square_x+1 < len(boardToResolve) and square_y+1 < len(boardToResolve[0])):
                showSquare (resolvedBoard, boardToResolve, square_x+1, square_y+1)
            if (square_x+1 < len(boardToResolve) and square_y > 0):
                showSquare (resolvedBoard, boardToResolve, square_x+1, square_y-1)
            if (square_x > 0 and square_y+1 < len(boardToResolve[0])):
                showSquare (resolvedBoard, boardToResolve, square_x-1, square_y+1)
            if (square_x > 0 and square_y > 0):
                showSquare (resolvedBoard, boardToResolve, square_x-1, square_y-1)
        
        return boardToResolve

def getSurroundingSquaresIndex(board, i, j):
    squaresIndex = []

    if (j+1 < len(board[0])):
        squaresIndex.append("{0}{1}".format(i, j+1))
    if (j > 0):
        squaresIndex.append("{0}{1}".format(i, j-1))
    if (i+1 < len(board)):
        squaresIndex.append("{0}{1}".format(i+1, j))
    if (i > 0):
        squaresIndex.append("{0}{1}".format(i-1, j))
    if (i+1 < len(board) and j+1 < len(board[0])):
        squaresIndex.append("{0}{1}".format(i+1, j+1))
    if (i+1 < len(board) and j > 0):
        squaresIndex.append("{0}{1}".format(i+1, j-1))
    if (i > 0 and j+1 < len(board[0])):
        squaresIndex.append("{0}{1}".format(i-1, j+1))
    if (i > 0 and j > 0):
        squaresIndex.append("{0}{1}".format(i-1, j-1))

    return squaresIndex

