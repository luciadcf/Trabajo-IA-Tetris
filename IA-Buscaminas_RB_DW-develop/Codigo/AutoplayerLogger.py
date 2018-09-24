import AutoplayMinesweeper
import os.path
import datetime
import win32api
import random

def autoplay_log(num_iterations, gameBoards, pause_finish_iteration = False):
	filePath = input("Enter the full path with file name to create the log file: ")

	if filePath[-4:] == ".txt":
		filePath = filePath[:-4]

	now = datetime.datetime.now()
	filePath = filePath + "_" + now.strftime("%d%m%y_%H%M%S") + ".txt"

	if os.path.isfile(filePath):
		print("This path already exists. Please enter a valid one that doesn't exist.")
	else:
		print("Creating log file \"{0}\"".format(filePath))

		with open(filePath, "w") as logFile:
			logFile.write("--------------- Log file for Minesweeper Game Artificial Intelligence with Bayesian Network\n")
			logFile.write("--------------- \n")
			logFile.write("--------------- Date: {0}\n".format(now.isoformat(timespec='seconds')))
			logFile.write("\n")
			logFile.write("\n")

		for gameBoard in gameBoards:
			loseCounts = []
			total_times = []
			for _ in range(num_iterations):
				loseCount, total_time = AutoplayMinesweeper.play(gameBoard[0], gameBoard[1], gameBoard[2], filePath)
				loseCounts.append(loseCount)
				total_times.append(total_time)
			avg_loseCounts = sum(loseCounts)/len(loseCounts)
			avg_total_times = sum(total_times)/len(total_times)
			with open(filePath, "a") as logFile:
				logFile.write("\n")
				logFile.write("Finished playing {0} times\n".format(num_iterations))
				logFile.write("Board: Num x = {0} ; Num y = {1} ; Mines = {2}\n".format(gameBoard[0], gameBoard[1], gameBoard[2]))
				logFile.write("Total loses counts: {0}\n".format(loseCounts))
				logFile.write("Total times (mins): {0}\n".format(total_times))
				total_times_secs = []
				for var in total_times:
					total_times_secs.append(var*60)
				logFile.write("Total times (secs): {0}\n".format(total_times_secs))
				logFile.write("Average loses: {0}\n".format(avg_loseCounts))
				logFile.write("Average time: {0} ({1} secs)\n".format(avg_total_times, avg_total_times*60))

			if pause_finish_iteration:
				win32api.MessageBox(0, 'Finished iteration for board: x = {0} ; y = {1} ; Mines = {2}\nAverage loses: {3}\nAverage time: {4}'.format(gameBoard[0], gameBoard[1], gameBoard[2], avg_loseCounts, avg_total_times),
					'Minesweeper IA - Finished iteration', 0x00001000)

'''
autoplay_log(10, [[5,5,5]], False)
autoplay_log(10, [[5,5,6]], False)
autoplay_log(10, [[5,5,7]], False)

autoplay_log(10, [[8,8,13]], False)
autoplay_log(10, [[8,8,14]], False)
autoplay_log(10, [[8,8,15]], False)

autoplay_log(10, [[10,10,20]], False)
autoplay_log(10, [[10,10,22]], False)
autoplay_log(10, [[10,10,25]], False)
'''