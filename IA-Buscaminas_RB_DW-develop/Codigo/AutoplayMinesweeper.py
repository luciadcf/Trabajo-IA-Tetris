from MinesweeperGame import BayesianNetworkMinesweeperGame
import time

loseCount = 0
def play(num_x, num_y, mines, logFilePath = None, inputEnabled = False):
	"""
	Method to start automatically playing Minesweeper

	Parameters
	----------
	variables: 
		num_x: Number of rows
		num_y: Number of columns
		mines: Total number of mines

	optional:
		logFilePath(None): Path of file to write logs
		inputEnabled(False): Whether it should be paused every step of the game

	Returns
	---------
		loseCount: Number of loses
		total_time: Total time spent on won game
	"""
	global loseCount
	loseCount = 0

	return _play(num_x, num_y, mines, logFilePath, inputEnabled)

def _play(num_x, num_y, mines, logFilePath = None, inputEnabled = False):
	"""
	Private method to automatically play Minesweeper

	Parameters
	----------
	variables: 
		num_x: Number of rows
		num_y: Number of columns
		mines: Total number of mines

	optional:
		logFilePath(None): Path of file to write logs
		inputEnabled(False): Whether it should be paused every step of the game

	Returns
	---------
		loseCount: Number of loses
		total_time: Total time spent on won game
	"""
	global loseCount

	print()
	print()
	print("------------------------------")
	print("Playing Minesweeper with Bayesian Networks")
	print("Minesweeper Board: Num x = {0} ; Num y = {1} ; Mines = {2}".format(num_x, num_y, mines))
	if (logFilePath != None):
		with open(logFilePath, "a") as logFile:
			logFile.write("\n")
			logFile.write("\n")
			logFile.write("------------------------------\n")
			logFile.write("Playing Minesweeper with Bayesian Networks\n")
			logFile.write("Minesweeper Board: Num x = {0} ; Num y = {1} ; Mines = {2}\n".format(num_x, num_y, mines))
	
	try:
		# Construct Bayesian Network Minsweeper Game
		bayesianMinesweeperGame = BayesianNetworkMinesweeperGame(num_x, num_y, mines)

		print()
		print()
		print("Resolved Board Created")
		print(bayesianMinesweeperGame.stringResolvedBoard())
		if (logFilePath != None):
			with open(logFilePath, "a") as logFile:
				logFile.write("\n")
				logFile.write("\n")
				logFile.write("Resolved Board Created\n")
				logFile.write(bayesianMinesweeperGame.stringResolvedBoard() + "\n")
		
		# Starting revealed square
		#	By definition in the most known Minsweeper games, it starts revealing the first square that is not mine
		revealed = False
		for i in range (bayesianMinesweeperGame.x_len):
			if (revealed):
				break
			for j in range (bayesianMinesweeperGame.y_len):
				if (bayesianMinesweeperGame.resolvedBoard[i][j] != '*'):
					bayesianMinesweeperGame.revealPos (i, j)
					revealed = True
					break

		# Start time game
		time1 = int(round(time.time()))

		while (True):
			if (inputEnabled):
				input("Paused - Waiting user input to continue...")

			print()
			print("Board to resolve")
			print(bayesianMinesweeperGame.stringBoardToResolve())
			if (logFilePath != None):
				with open(logFilePath, "a") as logFile:
					logFile.write("\n")
					logFile.write("Board to resolve\n")
					logFile.write(bayesianMinesweeperGame.stringBoardToResolve() + "\n")

			# Start time step
			countT1 = int(round(time.time()))
			
			# Bayesian Network
			bayesianMinesweeperGame.createBayesianNetwork()
			
			# End time step
			countT2 = int(round(time.time()))
			
			print()
			print("Decided in {0} minutes".format(float((countT2 - countT1)/60)))
			print("Revealing Positions: {0}".format(bayesianMinesweeperGame.best_x))
			if (logFilePath != None):
				with open(logFilePath, "a") as logFile:
					logFile.write("\n")
					logFile.write("Decided in {0} minutes\n".format(float((countT2 - countT1)/60)))
					logFile.write("Revealing Positions: {0}\n".format(bayesianMinesweeperGame.best_x))

			# Revealing best Xij to not be mine
			for var in bayesianMinesweeperGame.best_x:
				bayesianMinesweeperGame.revealPos (int(var[1]), int(var[2]))
				# At this time, if Xij is mine, an exception will be thrown

			print("New board to resolve")
			print(bayesianMinesweeperGame.stringBoardToResolve())
			if (logFilePath != None):
				with open(logFilePath, "a") as logFile:
					logFile.write("New board to resolve\n")
					logFile.write(bayesianMinesweeperGame.stringBoardToResolve() + "\n")

			# Counting current left squares
			count = 0
			for i in range (bayesianMinesweeperGame.x_len):
				for j in range (bayesianMinesweeperGame.y_len):
					if (bayesianMinesweeperGame.boardToResolve[i][j] == '?'):
						count+=1

			# WON GAME
			if(count == bayesianMinesweeperGame.totalMines):
				#bayesianMinesweeperGame.printBoardToResolve()
				print ("I WON !")
				print ("Times lost: {0}".format(loseCount))
				if (logFilePath != None):
					with open(logFilePath, "a") as logFile:
						logFile.write("\n")
						logFile.write("WON!\n")
						logFile.write("Times lost: {0}\n".format(loseCount))
				break
			
		# End time game
		time2 = int(round(time.time()))
		timeWon = float((time2 - time1)/60)

		print ('Finished in {0} minutes'.format(timeWon))
		if (logFilePath != None):
			with open(logFilePath, "a") as logFile:
				logFile.write("Finished in {0} minutes\n".format(timeWon))

	# Revealed square was mine -> LOST GAME
	except Exception as ex:
		print (ex)
		# End time game
		time2 = int(round(time.time()))

		print("Last board to resolve")
		print(bayesianMinesweeperGame.stringBoardToResolve())
		print()
		print("LOST!")
		print("Finished in {0} minutes".format(float((time2 - time1)/60)))
		if (logFilePath != None):
			with open(logFilePath, "a") as logFile:
				logFile.write("Last board to resolve\n")
				logFile.write(bayesianMinesweeperGame.stringBoardToResolve() + "\n")
				logFile.write("\n")
				logFile.write("LOST!\n")
				logFile.write("Finished in {0} minutes\n".format(float((time2 - time1)/60)))
		
		# Starting new game
		loseCount += 1
		bayesianMinesweeperGame.minesList = []
		loseCount, timeWon = _play(num_x, num_y, mines, logFilePath, inputEnabled)

	return loseCount, timeWon

	
