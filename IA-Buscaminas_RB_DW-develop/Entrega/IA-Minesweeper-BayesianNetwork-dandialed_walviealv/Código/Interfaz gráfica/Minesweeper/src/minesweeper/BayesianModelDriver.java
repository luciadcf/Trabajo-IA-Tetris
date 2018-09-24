package minesweeper;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class BayesianModelDriver {

	private Minesweeper ms;
	private List<String> evidences;
	private List<String> bestsX;
	private List<String> xProbabilities;
	
	private String xijNodes;
	private String yijNodes;

	public String FILE = BayesianModelDriver.class.getResource("AutoplayScript.py").getPath();
	public static String PYTHON_PATH = readPythonPath();

	public BayesianModelDriver(Minesweeper ms) {
		this.ms = ms;
		this.evidences = new ArrayList<String>();
		this.bestsX = new ArrayList<String>();
		this.xProbabilities = new ArrayList<String>();
		this.xijNodes = "";
		this.yijNodes = "";
		
		FILE = FILE.substring(1, FILE.length());
	
		//FILE = System.getProperty("user.dir") + "\\AutoplayScript.py";

	}

	public Minesweeper getMinesweeper() {
		return ms;
	}

	public List<String> getEvidences() {
		return evidences;
	}

	public List<String> getBestsX() {
		return bestsX;
	}

	public List<String> getXProbs() {
		return xProbabilities;
	}
	

	public String getXijNodes() {
		return xijNodes;
	}


	public String getYijNodes() {
		return yijNodes;
	}


	public void doStep() {
		modifyFile();

		Runtime rt = Runtime.getRuntime();

		String[] commands = { "powershell", PYTHON_PATH, FILE };
		Process proc = null;

		try {
			proc = rt.exec(commands);
		} catch (IOException e) {
			e.printStackTrace();
		}

		BufferedReader stdInput = new BufferedReader(new InputStreamReader(proc.getInputStream()));
		BufferedReader eeInput = new BufferedReader(new InputStreamReader(proc.getErrorStream()));

		String s = null;

		this.bestsX.clear();
		this.xProbabilities.clear();
		this.evidences.clear();

		try {

			while ((s = stdInput.readLine()) != null) {
				if (s.startsWith("List of best Xij to not be mine")) {
					String line = s;
					line = s.substring(s.indexOf('[') + 1, s.indexOf(']'));

					String[] evs = line.split(",");

					if (evs.length > 0) {
						try {
							this.bestsX.add(evs[0].substring(1, evs[0].length() - 1));
							Arrays.asList(evs).stream().skip(1)
									.forEach(e -> this.bestsX.add(e.substring(2, e.length() - 1)));
						} catch (Exception e) {
						}
					}
				}

				else

				if (s.startsWith("List of Xij nodes that are known to be mine")) {
					String line = s;
					line = s.substring(s.indexOf('[') + 1, s.indexOf(']'));

					String[] evs = line.split(",");

					if (evs.length > 0) {
						try {
							this.evidences.add(evs[0].substring(1, evs[0].length() - 1));
							Arrays.asList(evs).stream().skip(1)
									.forEach(e -> this.evidences.add(e.substring(2, e.length() - 1)));
						} catch (Exception e) {
						}
					}
				}

				else

				if (s.startsWith("x"))
					this.xProbabilities.add(s);
				
				if (s.startsWith("List of Xij nodes:")) 
					this.xijNodes = s;
					
				if (s.startsWith("List of Yij nodes:")) 
					this.yijNodes = s;
			}

			while ((s = eeInput.readLine()) != null) {
				System.out.println(s);
			}

		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	private void modifyFile() {

		try (Stream<String> stream = Files.lines(Paths.get(FILE))) {

			String boardToResolve = Arrays.deepToString(ms.getBoardToResolve());
			String resolvedBoard = Arrays.deepToString(ms.getResolvedBoard());
			String evidences = "[";

			boardToResolve = boardToResolve.replaceAll("\\?", "\'?\'");
			boardToResolve = boardToResolve.replaceAll("\\*", "\'*\'");

			resolvedBoard = resolvedBoard.replaceAll("\\?", "\'?\'");
			resolvedBoard = resolvedBoard.replaceAll("\\*", "\'*\'");
			
			for (String s : this.evidences)
				if (s != null)
					evidences += "\'" + s + "\'";

			evidences += "]";

			String function = "playStepByStep (" + boardToResolve + ", " + resolvedBoard + ", " + evidences + ", "
					+ ms.getxTam() + ", " + ms.getyTam() + ")";

			List<String> fileReaded = stream.collect(Collectors.toList());
			fileReaded.remove(fileReaded.size() - 1);

			fileReaded.add(function);

			Files.write(Paths.get(FILE), fileReaded);
			stream.close();

		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static void changePythonPath(String paht) {
		try {
			
			String username = System.getProperty("user.name");
			Files.write(Paths.get("c:/Users/" + username + "/AppData/Local/phytonPath.txt"), paht.getBytes());
			PYTHON_PATH = paht;
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static String readPythonPath () {
		String username = System.getProperty("user.name");
		String content = "";
		
		try {
			content = new String(Files.readAllBytes(Paths.get("c:/Users/" + username + "/AppData/Local/phytonPath.txt")));
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return content;
	}

}
