package minesweeper;

import java.awt.Color;
import java.awt.EventQueue;
import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.JTextPane;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class Main {

	private JFrame frame;
	private JTextPane textPane = new JTextPane();
	private JScrollPane scrollPane = new JScrollPane();
	private JFileChooser fc =  new JFileChooser();
	private final JLabel stateInfo = new JLabel("Are you ready?");
	private final JLabel xTam = new JLabel("Rows: ");
	private final JLabel yTam = new JLabel("Collumns:");
	private final JLabel lblNewLabel = new JLabel("Mines: ");
	private final JLabel timeLabel = new JLabel("Time: ");
	private final JLabel totalWonGames = new JLabel("Total won games: ");
	private final JLabel totalLostGames = new JLabel("Total lost games: ");
	private final JLabel lastRevealedPos = new JLabel("Last revealed pos: ");
	private final JLabel timeAvg = new JLabel("Time average: ");
	private JTextField yTamInput;
	private JTextField minesInput;
	private JTextField xTamInput;
	private final JButton autoButton = new JButton("Autoplay");
	private final JButton fullAuto = new JButton("Full Autoplay");
	private final JButton resetButton = new JButton("Reset");
	private final JButton nextMove = new JButton("Next move");
	private final JButton pythonPath = new JButton("Python");
	
	private Minesweeper ms;
	private BayesianModelDriver bayesianModel;

	private boolean countEnabled = false;
	private boolean autoplaying;
	private int winCount = 0;
	private int loseCount = 0;
	private int totalGames = 0;
	private int time = 0;
	private int timeavg= 0;
	private List<JButton> buttons = new ArrayList<JButton>();
	private List<Integer> times;
	
	private Thread timerThread;
	private Thread autoplayingThread;
	private Thread fUtoplayingThread;

	public static void main(String[] args) throws ClassNotFoundException, InstantiationException,
			IllegalAccessException, UnsupportedLookAndFeelException {

		UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());

		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Main window = new Main();
					window.frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	public Main() {
		initialize();
	}

	private void initialize() {

		frame = new JFrame();
		frame.setBounds(100, 100, 715, 599);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setResizable(false);

		frame.setTitle("Autosweeper");
		frame.getContentPane().setLayout(null);

		stateInfo.setBounds(10, 545, 228, 14);
		frame.getContentPane().add(stateInfo);

		resetButton.setBounds(10, 511, 61, 23);

		resetButton.addActionListener(a -> {
			resetBoard();
			textPane.setText("AUTOSWEEPER INFO: ");
			buttons.forEach(b -> {
				b.setText("");
				b.setEnabled(true);
			});
		});
		
		frame.getContentPane().add(resetButton);

		scrollPane.setBounds(398, 11, 301, 475);
		scrollPane.setBorder(BorderFactory.createTitledBorder("Game Info"));
		frame.getContentPane().add(scrollPane);

		textPane.setText("AUTOSWEEPER INFO: ");
		textPane.setEditable(false);
		scrollPane.setViewportView(textPane);
		xTam.setBounds(10, 422, 46, 14);

		frame.getContentPane().add(xTam);
		yTam.setBounds(10, 447, 46, 14);

		frame.getContentPane().add(yTam);
		lblNewLabel.setBounds(10, 472, 34, 14);

		frame.getContentPane().add(lblNewLabel);

		xTamInput = new JTextField();
		xTamInput.setText("10");
		xTamInput.setBounds(66, 419, 46, 20);
		xTamInput.setColumns(10);
		frame.getContentPane().add(xTamInput);

		yTamInput = new JTextField();
		yTamInput.setText("10");
		yTamInput.setBounds(66, 444, 46, 20);
		yTamInput.setColumns(10);
		frame.getContentPane().add(yTamInput);

		minesInput = new JTextField();
		minesInput.setText("10");
		minesInput.setBounds(66, 469, 46, 20);
		frame.getContentPane().add(minesInput);
		minesInput.setColumns(10);
		autoButton.setBounds(81, 511, 75, 23);

		autoButton.addActionListener((e) -> autoPlay());

		frame.getContentPane().add(autoButton);
		fullAuto.setBounds(166, 511, 102, 23);
		
		fullAuto.addActionListener((e) -> fullAutoPlay());

		frame.getContentPane().add(fullAuto);
		timeLabel.setBounds(122, 422, 116, 14);

		frame.getContentPane().add(timeLabel);
		totalWonGames.setBounds(122, 447, 116, 14);

		frame.getContentPane().add(totalWonGames);
		totalLostGames.setBounds(122, 472, 116, 14);

		frame.getContentPane().add(totalLostGames);
		lastRevealedPos.setBounds(248, 422, 451, 14);

		frame.getContentPane().add(lastRevealedPos);
		timeAvg.setBounds(248, 447, 451, 14);

		frame.getContentPane().add(timeAvg);

		nextMove.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				Runnable r = () -> {
					printInfo("Calculating next step...");
					bayesianModel.doStep();
					logStepInfo();
				};
				
				Thread t = new Thread(r);
				t.start();
			}
		});
		
		nextMove.setBounds(278, 511, 89, 23);
		frame.getContentPane().add(nextMove);

		pythonPath.setBounds(610, 511, 89, 23);
		frame.getContentPane().add(pythonPath);
		
		pythonPath.addActionListener((e) -> {
			fc.showOpenDialog(frame);
			File f = fc.getSelectedFile();
			BayesianModelDriver.changePythonPath(f.getAbsolutePath());
				if (BayesianModelDriver.PYTHON_PATH.endsWith("python.exe")) {
					pythonPath.setForeground(Color.BLUE);
				} else {
					pythonPath.setForeground(Color.RED);
				}
		});

		if (BayesianModelDriver.PYTHON_PATH.endsWith("python.exe")) {
			pythonPath.setForeground(Color.BLUE);
		} else {
			pythonPath.setForeground(Color.RED);
		}
		
		resetBoard();
	}

	void generateButtons() {

		buttons.stream().forEach(b -> frame.remove(b));
		buttons = new ArrayList<JButton>();

		frame.repaint();

		for (int i = 0; i < ms.getxTam(); i++) {
			for (int j = 0; j < ms.getyTam(); j++) {
				JButton button = new JButton("");
				button.setBounds((12 + 27) * j, (12 + 27) * i, 40, 40);
				button.setFocusable(false);
				button.setName("" + i + j);

				final int fi = i;
				final int fj = j;

				button.addActionListener(e -> {

					stateInfo.setText("Playing...");
					stateInfo.setForeground(Color.blue);

					if (!countEnabled && !autoplaying) {
						countEnabled = true;
						updateTime();
					}

					ms.revealPosition(fi, fj);
					button.setText(ms.getResolvedBoard()[fi][fj] + "");

					String pos = button.getName().charAt(0) + ", " + button.getName().charAt(1);
					printInfo("[CLICK IN POS]: " + "(" + pos + ")");
					
					lastRevealedPos.setText("Last revealed pos: " + pos);

					if (ms.getResolvedBoard()[fi][fj] == '*') {
						stateInfo.setText("Unlucky! You lost...");
						stateInfo.setForeground(Color.red);
						buttons.forEach(b -> b.setEnabled(false));

						countEnabled = false;
						autoplaying = false;
					
						printInfo("[STATE INFO]: You lost =(");

						printInfo("[TIME INFO LOST]: " + time + " seconds");

					} else {
						button.setEnabled(false);

						if (ms.getResolvedBoard()[fi][fj] == '0') {
							for (int i1 = 0; i1 < ms.getxTam(); i1++) {
								for (int j1 = 0; j1 < ms.getyTam(); j1++) {
									final int fi1 = i1;
									final int fj1 = j1;

									if (ms.getBoardToResolve()[i1][j1] != '?') {
										JButton but = buttons.stream().filter(b -> b.getName().equals("" + fi1 + fj1))
												.findFirst().get();
										but.setText(ms.getResolvedBoard()[fi1][fj1] + "");
										but.setEnabled(false);
									}
								}
							}
						}
					}
					checkVictory(true);
				});

				frame.getContentPane().add(button);
				buttons.add(button);
			}
		}
	}

	void resetBoard() {

		if (Integer.valueOf(xTamInput.getText()) > 10)
			xTamInput.setText("10");
		if (Integer.valueOf(yTamInput.getText()) > 10)
			yTamInput.setText("10");
		if (Integer.valueOf(minesInput.getText()) >= Integer.valueOf(yTamInput.getText())
				* Integer.valueOf(xTamInput.getText()))
			minesInput.setText((Integer.valueOf(yTamInput.getText()) * Integer.valueOf(xTamInput.getText()) - 1) + "");

		ms = new Minesweeper(Integer.valueOf(yTamInput.getText()), Integer.valueOf(xTamInput.getText()),
				Integer.valueOf(minesInput.getText()));

		stateInfo.setText("Are you ready?");
		stateInfo.setForeground(Color.black);
		generateButtons();

		bayesianModel = new BayesianModelDriver(ms);
		autoplaying = false;
		countEnabled = false;
	
		autoButton.setEnabled(true);
		fullAuto.setEnabled(true);
		nextMove.setEnabled(true);

		time = 0;
		
		frame.repaint();
	}

	void printInfo(String s) {
		textPane.setText(textPane.getText() + "\n" + s);
		scrollPane.getVerticalScrollBar().setValue(scrollPane.getMaximumSize().height);
	}

	boolean checkVictory(boolean show) {
		int buttonsRem = buttons.stream().filter(b -> b.getText().equals("")).collect(Collectors.toList()).size();
		if (buttonsRem == ms.getTotalMines()) {

			if (show) {
				printInfo("[STATE INFO]: You won the game");
				printInfo("[TIME INFO WIN]: " + time + " seconds");
			}

			stateInfo.setText("YOU WON!");
			stateInfo.setForeground(Color.GREEN);

			countEnabled = false;

			buttons.forEach(b -> b.setEnabled(false));
			autoplaying = false;

			return true;
		}

		return false;
	}

	void updateTime() {
		
		if (timerThread==null) {
			
			Runnable r = () -> {
				timeLabel.setText("Time: ");
				while (countEnabled) {
					try {
						time++;
						timeLabel.setText("Time: " + time + " secs.");
						Thread.sleep(1000);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
				}

			};
			
			timerThread = new Thread(r);
			timerThread.start();
			
		}
		
		time = 0;
	}

	void autoPlay() {
		
		resetBoard();
		
		autoplaying = true;
		
		if (!countEnabled) {
			countEnabled = true;
			updateTime();			
		}

		stateInfo.setText("Playing...");
		stateInfo.setForeground(Color.blue);
		
		
		autoButton.setEnabled(false);
		fullAuto.setEnabled(false);
		nextMove.setEnabled(false);
		
		boolean revealed = false;
		for (int i = 0; i < ms.getxTam(); i++) {
			for (int j = 0; j < ms.getyTam(); j++) {
				if (ms.getResolvedBoard()[i][j] != '*') {
					final int fi = i;
					final int fj = j;
					
					buttons.stream().filter(b -> b.getName().equals(""+fi+fj)).findFirst().get().doClick();
					revealed = true;
					break;
				}
			}
			if (revealed)
				break;
		}
		
		Runnable run = () -> {

			while (autoplaying) {
				
				printInfo("Calculating next step...");

				bayesianModel.doStep();
								
				logStepInfo() ;

				for (String s : bayesianModel.getBestsX()) {
					try {
						buttons.stream().filter(b -> b.getName().equals("" + s.charAt(1) + s.charAt(2))).findFirst()
								.get().doClick();
					} catch (Exception e) {

					}
				}

				if (checkVictory(false))
					break;
			}

		};

		autoplayingThread = new Thread(run);
		autoplayingThread.start();
	}

	void fullAutoPlay() {
		totalGames = 0;
		winCount = 0;
		loseCount = 0;
		timeavg = 0;
		times = new ArrayList<Integer>();
		
		totalLostGames.setText("Total lost games: " + loseCount);
		totalWonGames.setText("Total won games: " + winCount);
		timeAvg.setText("Time average: " + timeavg + " secs.");
		
		Runnable run = () -> {
			autoPlay();

			while (true) {
				if (checkVictory(false)) {
					winCount++;
					totalWonGames.setText("Total won games: " + winCount);
					updateAutoplay(true);
				}
				
				if(stateInfo.getText().equals("Unlucky! You lost...")) {
					loseCount++;
					totalLostGames.setText("Total lost games: " + loseCount);
					updateAutoplay(false);
				}
			}

		};

		fUtoplayingThread = new Thread(run);
		fUtoplayingThread.start();
	}
	
	void updateAutoplay(boolean updateAvg) {
		if (updateAvg) {
			times.add(time);
			totalGames++;
			timeavg = times.stream().mapToInt(i -> i).sum() / totalGames;
			timeAvg.setText("Time average: " + timeavg + " secs.");
		}
		
		resetBoard();
		autoPlay();
	}
	
	void logStepInfo() {
		
		printInfo("[NODES Xij]: " + bayesianModel.getXijNodes());
		printInfo("[NODES Yij]: " + bayesianModel.getYijNodes());
		
		String xProb = "";
		for (String s : bayesianModel.getXProbs())
			xProb += s + "\n";

		printInfo("[PROBABILITY INFO]: \n" + xProb);
		
		printInfo("[MINES EVIDENCES]: " + bayesianModel.getEvidences());
		
		printInfo("[BEST CANDIDATES]: " + bayesianModel.getBestsX());
	}
}
