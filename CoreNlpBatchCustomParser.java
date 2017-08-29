import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

public class CoreNlpBatchCustomParser {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		parseTheInitialFileAndCreateASetOfDocs("/home/noushin/summerTask");
	}
	
	public static void parseTheInitialFileAndCreateASetOfDocs(String path) throws IOException{
		File dir = new File(path + "/dev");
		File[] files = dir.listFiles();
		System.out.println("beginning \n");
		File newDir = new File(path + "/Sub Files");
		if(!newDir.exists())
			newDir.mkdirs();
		
		for(File f:files){
		System.out.println("in for \n");
			if(!f.getName().contains("dev-muc"))
				continue;
			List<String> lines = Files.readAllLines(Paths.get(f.getAbsolutePath()));
			String content = "";
			for(String l:lines)
				content += " " + l;
			content = content.replaceAll("[ ]+", " ").substring(1);
			String[] texts = content.split("DEV-MUC");
			for(int i=1;i<texts.length;i++){
				String t = "DEV-MUC" + texts[i];
//				String header = t.split("\\)")[0] + ")";
//				t = t.replace(header + " ", "");
				String title = t.split("\\(")[0];
				t = "[" + t.split("-- \\[")[1];
				BufferedWriter bw = new BufferedWriter(new FileWriter(newDir.getAbsolutePath() + "/" + title));
				bw.write(t);
				bw.close();
		System.out.println("end \n");
			}
		}
	}
	
	
}
