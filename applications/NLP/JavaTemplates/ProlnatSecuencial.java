import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import jregex.Pattern;

public class ProlnatSecuencial {

	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub

		
		if(args.length<1){
			System.out.println("Debe pasar o nome do ficheiro a parsear como argumento");
			System.exit(0);
		}
		
		Sentences modSentences = new Sentences();
		Tokens modTokens = new Tokens();
		Splitter modSplitter = new Splitter();
		NER modNer = new NER();
		Tagger modTagger = new Tagger();
		NEC modNec = new NEC();
		
		//System.out.println("Ficheiro: "+args[0]);
		
		BufferedReader reader = new BufferedReader(new FileReader(args[0]));
		String line = null;
		
		ArrayList<String> sentences = new ArrayList<String>();
		ArrayList<String> tokens = new ArrayList<String>();
		ArrayList<String> splits = new ArrayList<String>();
		ArrayList<String> ner = new ArrayList<String>();
		ArrayList<String> tagger = new ArrayList<String>();
		ArrayList<String> nec = new ArrayList<String>();
		
		int i = 0;
		
		
		while ((line = reader.readLine()) != null) {
			//System.out.println("LINHA: "+line);
			sentences.clear();
			tokens.clear();
			splits.clear();
			ner.clear();
			tagger.clear();
			nec.clear();
			
			
		    sentences = modSentences.runSentencesModule(line);
		    /*System.out.println("====SENTENCES====");
		    for(i = 0; i<sentences.size();i++){
		    	System.out.println("Sentence procesada: "+sentences.get(i));
		    }
		    System.out.println("====END-SENTENCES====");
		    */
		    tokens = modTokens.runTokens(sentences);
		    
		    /*System.out.println("=======TOKENS=======");
		    for(i = 0; i<tokens.size();i++){
		    	System.out.println(tokens.get(i));
		    }
		    System.out.println("=======END-TOKENS=======");*/
		    
		    
		    splits = modSplitter.runSplitter(tokens);
		    /*System.out.println("====SPLITS====");
		    for(i = 0; i<splits.size();i++){
		    	System.out.println(String.valueOf(i)+" :: "+splits.get(i));
		    }
		    System.out.println("====END-SPLITS====");
		    */
		    ner = modNer.runNer(splits);
		    
		    /*for(i = 0; i<ner.size();i++){
		    	System.out.println(ner.get(i));
		    }*/
		    
		    tagger = modTagger.runTagger(ner);
		    
		    /*for(i = 0; i<tagger.size();i++){
		    	System.out.println(tagger.get(i));
		    }*/
		    
		    nec = modNec.nec_es(tagger);
		    for(i = 0; i<nec.size();i++){
		    	if(nec.get(i)!="\n" && nec.get(i)!=""){
		    		System.out.println(nec.get(i));
		    	}
		    }
		    //System.out.println(resultado);
		    //resultado = "";
		}
		
		reader.close();
		
	}

}
