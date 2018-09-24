from MinesweeperGame import BayesianNetworkMinesweeperGame
import time
import random

def playStepByStep (boardToResolve, resolvedBoard, minesList, xtam, ytam):

	bayesianMinesweeperGame = BayesianNetworkMinesweeperGame(xtam, ytam, 5)

	bayesianMinesweeperGame.boardToResolve = boardToResolve
	bayesianMinesweeperGame.resolvedBoard = resolvedBoard
	bayesianMinesweeperGame.minesList = minesList

	bayesianMinesweeperGame.createBayesianNetwork ()

	print(bayesianMinesweeperGame.best_x)
	print(bayesianMinesweeperGame.minesList)
	print(bayesianMinesweeperGame.resolvedBoard)
	print(bayesianMinesweeperGame.printBoardToResolve)

playStepByStep ([['?', 1, '?', '?', '?'], ['?', '?', '?', '?', '?'], ['?', '?', '?', '?', '?'], ['?', '?', '?', '?', '?'], ['?', '?', '?', '?', '?']], [['*', 1, 0, 0, 0], [1, 2, 1, 1, 0], [0, 2, '*', 2, 0], [0, 2, '*', 3, 1], [0, 1, 1, 2, '*']], [], 5, 5)
