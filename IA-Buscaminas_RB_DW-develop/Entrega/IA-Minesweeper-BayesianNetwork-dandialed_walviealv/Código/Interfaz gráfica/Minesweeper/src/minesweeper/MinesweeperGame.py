import random
import timer
import networkx
import pgmpy.models as pgmm
import pgmpy.factors.discrete as pgmf
import pgmpy.inference as pgmi
import BoardUtils as bu

class MinesweeperGame:

	def __init__(self, x_len, y_len, totalMines):
		"""
		Constructor for Minesweeper Game

		Parameters
		----------
		variables: 
			x_len: Number of rows
			y_len: Number of columns
			totalMines: Total number of mines
		"""
		self.x_len = x_len
		self.y_len = y_len
		self.totalMines = totalMines
		self.boardToResolve = bu.createBoardToResolve (x_len, y_len)
		self.resolvedBoard = bu.createMinesweeperBoard (x_len, y_len, totalMines)

	def printBoardToResolve(self):
		"""
        Prints the empty board with all the mines and squares that were revealed before
        """
		bu.printBoard (self.boardToResolve)

	def printResolvedBoard(self):
		"""
        Prints the full board with all the mines and revealed squares
        """
		bu.printBoard (self.resolvedBoard)

	def stringBoardToResolve(self):
		"""
        Returns the empty board with all the mines and squares that were revealed before in string format

        Returns
        ----------
		string: Board to resolve
        """
		return bu.stringBoard (self.boardToResolve)

	def stringResolvedBoard(self):
		"""
        Returns the full board with all the miens and revealed squares in string format

        Returns
        ----------
		string: Resolved board
        """
		return bu.stringBoard (self.resolvedBoard)

	def revealPos(self, x, y):
		"""
		Method to reveal a square of the board to resolve

		Parameters
		----------
		variables: 
			x: Row of square to reveal
			y: Column of square to reveal
		"""
		return bu.showSquare (self.resolvedBoard, self.boardToResolve, x, y)

class BayesianNetworkMinesweeperGame (MinesweeperGame):
	
	def __init__(self, x_len, y_len, totalMines):
		"""
		Constructor for Bayesian Network Minesweeper Game

		Parameters
		----------
		variables: 
			x_len: Number of rows
			y_len: Number of columns
			totalMines: Total number of mines
		"""
		super().__init__(x_len, y_len, totalMines)
		self.minesList = []

	def createBayesianNetwork(self):
		"""
        Method to create the bayesian network associated with the Minesweeper Game refreshing the list of best squares with more probability to not be mine and be revealed
        """
		# Creating Bayesian Model with pgmpy library
		Model_minesweeper = pgmm.BayesianModel()

		# Creating the involved variables : Xij, Yij
		# 	Xij for squares with '?' (not revealed)
		# 	Yij for revealed squares that are not mine
		xList = []
		fullXList = []
		yList = []
		xWithoutYSurrounding = False
		for i in range(self.x_len):
			for j in range(self.y_len):
				if (self.boardToResolve[i][j] == '?'):
					x = 'x{0}{1}'.format(i,j)

					fullXList.append(x)

					hasYSurrounding = False
					surroundingSquares = bu.getSurroundingSquaresIndex(self.boardToResolve, i, j)
					for surrounding in surroundingSquares:
						if (self.boardToResolve[int(surrounding[0])][int(surrounding[1])] != '?'):
							hasYSurrounding = True
							break

					if (hasYSurrounding or not xWithoutYSurrounding):
						xList.append(x)
						Model_minesweeper.add_nodes_from([x])

					if (not hasYSurrounding):
						xWithoutYSurrounding = True
				else:
					y = 'y{0}{1}'.format(i,j)
					
					hasXSurrounding = False
					surroundingSquares = bu.getSurroundingSquaresIndex(self.boardToResolve, i, j)
					for surrounding in surroundingSquares:
						surroundingX = 'x{0}{1}'.format(surrounding[0], surrounding[1])
						if (self.boardToResolve[int(surrounding[0])][int(surrounding[1])] == '?' and
							not self.minesList.__contains__(surroundingX)):
							hasXSurrounding = True
							break

					if (hasXSurrounding):
						yList.append(y)
						Model_minesweeper.add_nodes_from([y])

		print("\nList of Xij nodes: {0}".format(xList))
		print("\nList of Yij nodes: {0}".format(yList))



		# Calculting Yij parent lists
		#	In order to get the CPDS of Yij squares, we will need their parent squares
		# Adding edges of Bayesian Model between nodes
		#	Yij nodes will have edges with all of its Xij parents
		inverseEdges = dict()
		for i in range(self.x_len):
			for j in range(self.y_len):
				y = 'y{0}{1}'.format(i,j)
				if (self.boardToResolve[i][j] != '?' and yList.__contains__(y)):
					xParentsList = []

					surroundingSquares = bu.getSurroundingSquaresIndex(self.boardToResolve, i, j)
					for surrounding in surroundingSquares:
						x = 'x{0}{1}'.format(surrounding[0], surrounding[1])
						if (xList.__contains__(x)):
							Model_minesweeper.add_edges_from([(x, y)])
							xParentsList.append(x)
					
					inverseEdges.update({y: xParentsList})

		# Creating the probability tables (CPDS)
		#	Xij CPDS will not depend of any other node
		#	Yij CPDS will depend of their parents Xij nodes
		yListValues = dict()
		for i in range(self.x_len):
			for j in range(self.y_len):
				# X node
				x = 'x{0}{1}'.format(i,j)
				y = 'y{0}{1}'.format(i,j)
				if (self.boardToResolve[i][j] == '?' and xList.__contains__(x)):
					# Known mine
					if (self.minesList.__contains__(x)):
						probToBeMine = 1
					# Probability to be mine
					elif (len(xList) > 0):
						probToBeMine = (self.totalMines-len(self.minesList))/len(fullXList)
					# There are no mines left, it cannot be mine
					else:
						probToBeMine = 0

					# Adding CPD to bayesian model
					cpd = pgmf.TabularCPD(x, 2, [[1-probToBeMine, probToBeMine]])
					Model_minesweeper.add_cpds(cpd)

				# Y node
				elif (self.boardToResolve[i][j] != '?' and yList.__contains__(y)):
					# Creating CPD table
					yListValues.update({y: int(self.boardToResolve[i][j])})
					n_columnas = pow(2, len(inverseEdges[y]))
					
					nMaxMines = 9

					# Square at the top or bottom of the board
					if (i == 0 or i == self.x_len-1):
						nMaxMines = 6
					if (j == 0 or j == self.y_len-1):
						# Corner square
						if (nMaxMines == 6):
							nMaxMines = 4
						# Square at the left or right of the board
						else:
							nMaxMines = 6

					if (len(inverseEdges[y])+1 < nMaxMines):
						nMaxMines = len(inverseEdges[y])+1

					# Generating CPD table
					probList = []
					for nMines in range(nMaxMines):
						filaList = []
						count = 0
						for x in range(n_columnas):
							if (nMines == bin (count).count('1')):
								filaList.append(1)
							else:
								filaList.append(0)
							count += 1

						probList.append(filaList)

					numList = []
					for _ in range(len(inverseEdges[y])):
						numList.append(2)

					# Adding CPD to bayesian model
					cpd = pgmf.TabularCPD(y, nMaxMines, probList, inverseEdges[y], numList)
					Model_minesweeper.add_cpds(cpd)

		# Getting best Xij
		#	Execute variable elimination method to get the queries
		Model_minesweeper_ev = pgmi.VariableElimination(Model_minesweeper)

		# Asking queries for all Xij nodes that are known to not be mine
		queries = []
		for var in xList:
			if (not var in self.minesList):
				query = Model_minesweeper_ev.query([var], yListValues)
				queries.append(query)


		# Creating dictionary with all the Xij queried and their probability to not be mine
		xProbToNotBeMine = dict()
		for var in queries:
			x = ''
			probToNotBeMine = 0
			for var1 in var.keys():
				x = str(var1)
			for var2 in var.values():
				probToNotBeMine = float(var2.values[0])

			if (probToNotBeMine == 0.0):
				self.minesList.append(x)

			xProbToNotBeMine.update({x: probToNotBeMine})

		# Getting the best Xij with more probability to not be mine
		maxProbToNotBeMine = 0.
		xMaxProbToNotBeMine = ''
		best_x = []
		print("\nGetting the best Xij with more probability to not be mine")
		for x, probToNotBeMine in xProbToNotBeMine.items():
			print("x: {0} -> Probability to not be mine: {1}".format(x, probToNotBeMine))
			if (maxProbToNotBeMine < probToNotBeMine):
				xMaxProbToNotBeMine = str(x)
				maxProbToNotBeMine = probToNotBeMine
				best_x = []
				best_x.append(xMaxProbToNotBeMine)
				
			if (probToNotBeMine == 1.0 and not x in best_x):
				best_x.append(x)

		# Refreshing list of best_x to not be mine
		self.best_x = best_x
		print("\nList of best Xij to not be mine: {0}".format(self.best_x))
		print("\nList of Xij nodes that are known to be mine: {0}".format(self.minesList))
				

