package minesweeper;

import java.util.concurrent.ThreadLocalRandom;
import java.util.stream.IntStream;

public class Minesweeper {

	private int xTam;
	private int yTam;
	private int totalMines;
	private char[][] boardToResolve;
	private char[][] resolvedBoard;

	public Minesweeper(int xTam, int yTam, int totalMines) {
		this.xTam = xTam;
		this.yTam = yTam;
		this.totalMines = totalMines;
		this.resolvedBoard = generateMinesweeperBoard(xTam, yTam, totalMines);
		this.boardToResolve = createEmptyBoard(xTam, yTam);
	}

	public int getxTam() {
		return xTam;
	}

	public void setxTam(int xTam) {
		this.xTam = xTam;
	}

	public int getyTam() {
		return yTam;
	}

	public void setyTam(int yTam) {
		this.yTam = yTam;
	}

	public int getTotalMines() {
		return totalMines;
	}

	public void setTotalMines(int totalMines) {
		this.totalMines = totalMines;
	}

	public char[][] getBoardToResolve() {
		return boardToResolve;
	}

	public void setBoardToResolve(char[][] boardToResolve) {
		this.boardToResolve = boardToResolve;
	}

	public char[][] getResolvedBoard() {
		return resolvedBoard;
	}

	public void setResolvedBoard(char[][] resolvedBoard) {
		this.resolvedBoard = resolvedBoard;
	}

	public char[][] generateMinesweeperBoard(int xTam, int yTam, int totalMines) {
		char[][] res = new char[xTam][yTam];
 	
		IntStream.range(0, xTam).forEach(i -> IntStream.range(0, yTam).forEach(j -> res[i][j] = '0'));

		int minesCount = 0;

		while (minesCount < totalMines) {
			int x = ThreadLocalRandom.current().nextInt(0, xTam);
			int y = ThreadLocalRandom.current().nextInt(0, yTam);

			if (res[x][y] != '*') {
				res[x][y] = '*';
				minesCount++;
			}
		}

		Integer acum = 0;

		for (int i = 0; i < xTam; i++) {
			for (int j = 0; j < yTam; j++) {
				if (j + 1 < yTam && res[i][j + 1] == '*')
					acum++;
				if (j > 0 && res[i][j - 1] == '*')
					acum++;
				if (i + 1 < xTam && res[i + 1][j] == '*')
					acum++;
				if (i > 0 && res[i - 1][j] == '*')
					acum++;
				if (i + 1 < xTam && j + 1 < yTam && res[i + 1][j + 1] == '*')
					acum++;
				if (i + 1 < xTam && j > 0 && res[i + 1][j - 1] == '*')
					acum++;
				if (j + 1 < yTam && i > 0 && res[i - 1][j + 1] == '*')
					acum++;
				if (i > 0 && j > 0 && res[i - 1][j - 1] == '*')
					acum++;
				if (acum > 0 && res[i][j] != '*')
					res[i][j] = acum.toString().charAt(0);
				acum = 0;
			}
		}
		return res;
	}

	public char[][] createEmptyBoard(int xTam, int yTam) {
		char[][] res = new char[xTam][yTam];

		IntStream.range(0, xTam).forEach(i -> IntStream.range(0, yTam).forEach(j -> res[i][j] = '?'));

		return res;
	}

	public void revealPosition(int x, int y) {

		char resolvedPos = this.resolvedBoard[x][y];

		if (this.boardToResolve[x][y] == '?') {
			this.boardToResolve[x][y] = resolvedPos;
			
			if (resolvedPos == '0') {
				if (y + 1 < yTam)
					revealPosition(x, y + 1);
				if (y > 0)
					revealPosition(x, y - 1);
				if (x + 1 < xTam)
					revealPosition(x + 1, y);
				if (x > 0)
					revealPosition(x - 1, y);
				if (x + 1 < xTam && y + 1 < yTam)
					revealPosition(x + 1, y + 1);
				if (x + 1 < xTam && y > 0)
					revealPosition(x + 1, y - 1);
				if (y + 1 < yTam && x > 0)
					revealPosition(x - 1, y + 1);
				if (x > 0 && y > 0)
					revealPosition(x - 1, y - 1);
			}
		}
	}

	public void printBoard(boolean resolved) {
		String res = "";

		char[][] board = boardToResolve;

		if (resolved)
			board = this.resolvedBoard;

		for (int i = 0; i < this.xTam; i++) {
			res += "\n";
			for (int j = 0; j < this.yTam; j++) {
				res += "  " + board[i][j];
			}
		}
		
		System.out.println(res);
	}

}
