import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Hashtable;

import jregex.Pattern;
import jregex.Replacer;


public class NER {

	private String ficheiroDic = "./Diccionarios.zip/lexicon/dicc.src";
	private String ficheiroAmbig = "./Diccionarios.zip/lexicon/ambig.txt";
	
	private String UpperCase = "[A-ZÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÑÇÜ]" ;
	private String LowerCase = "[a-záéíóúàèìòùâêîôûñçü]" ;
	private String Punct =  "[\\,\\;\\«\\»\\“\\”\\'\\\"\\&\\$\\#\\=\\(\\)\\<\\>\\!\\¡\\?\\¿\\\\\\[\\]\\{\\}\\|\\^\\*\\-\\€\\·\\¬\\…]";
	private String Punct_urls = "[\\:\\/\\~]";

	
	private String pron = "(me|te|se|le|les|la|lo|las|los|nos|os)"; 
	
	private String w = "[A-ZÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÑÇÜa-záéíóúàèìòùâêîôûñçü]";
	
	
	private Hashtable<String,String> Entry = new Hashtable<String, String>();
	
	private Hashtable<String,Integer> Lex = new Hashtable<String, Integer>();
	
	private Hashtable<String,String> StopWords = new Hashtable<String, String>();
	
	private Hashtable<String,Integer> Ambig = new Hashtable<String, Integer>();
	
	private String Prep = "(de|del)" ;
	private String Art = "(el|la|los|las)" ; 
	private String currency = "(euro|euros|dólar|dolares|peseta|pesetas|yen|yenes|escudo|escudos|franco|francos|real|reales|\\$|€)";
	private String measure = "(kg|kilogramo|quilogramo|gramo|g|centímetro|cm|hora|segundo|minuto|tonelada|tn|metro|m|km|kilómetro|quilómetro|%)";
	private String quant = "(ciento|cientos|miles|millón|millones|billón|billones|trillón|trillones)";  
	private String cifra = "(dos|tres|catro|cinco|seis|siete|ocho|nueve|diez|cien|mil)";
	private String meses =  "(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)";
	
	
	
	public NER(){
		
		String line = null;
		String novaPalabra = "";
		String[] entry;
		String token = "";
		String entryCadea = "";
		
		
		Pattern p;
		Replacer r;
		
		Pattern p2;
		
		try {
			BufferedReader reader = new BufferedReader(new FileReader(this.ficheiroDic));
			
			while ((line = reader.readLine()) != null) {
				
				novaPalabra = line;
				
				novaPalabra = novaPalabra.replace("\n", "");
				
				entry = novaPalabra.split(" ");
				
				token = entry[0];
				
				p = new Pattern("^[^ ]+ ([\\w\\W]+)$");//Colle a partir do primeiro espacio, e dicir, dende a segunda palabra
				
				r = p.replacer("$1");
				
				entryCadea = r.replace(line);
				
				
				Entry.put(token, entryCadea);
				
				int i = 1;
				
				String lemma = "";
				String tag = "";
				
				while(i<entry.length){
					lemma = entry[i];
					i++;
					tag = entry[i];
					
					if(Lex.containsKey(token)){
						Lex.put(token, Lex.get(token)+1);
					}
					else{
						Lex.put(token, 1);
					}
					
					p2 = new Pattern("^(P|SP|R|D|I)[\\w\\W]*");
					
					if(p2.matches(tag)){
						StopWords.put(token, tag);
					}
					i++;
				}
				
			}
			
			reader.close();
			
			BufferedReader reader2 = new BufferedReader(new FileReader(this.ficheiroAmbig));
			
			String entrada = "";
			
			while ((line = reader2.readLine()) != null) {
				
				entrada = line;
				
				entrada.replace("^[\\s]*", "");
				entrada.replace("[\\s]$", "");
				
				if(Ambig.containsKey(entrada)){
					Ambig.put(entrada, Ambig.get(entrada)+1);
				}
				else{
					Ambig.put(entrada, 1);
				}
			}

			reader2.close();
	
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			System.out.println(e.toString());
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println(e.toString());
		}
		
		
		
	}
	
	
	public ArrayList<String> runNer(ArrayList<String> text){
		
		String textCadea = "";
		int i,adiantar;
		String[] tokens;
		String lowercase;
		String Candidate = "";
		String SEP = "_";
		int N = 10;
		String token = "";
		String saidaString = "";
		
		//int count = 0;
		//boolean found = false;
		
		Hashtable<String,String> Tag = new Hashtable<String, String>();
		ArrayList<String> saida = new ArrayList<String>();
		saida.clear();
		
		Pattern p;
		Pattern patternUppercase = new Pattern("^"+UpperCase+"+$");
		//Pattern patternLastToken = new Pattern("^(#SENT#|<blank>|\"|»|”|.|-|\\s|?|!)$");
		Pattern patternLastToken = new Pattern("^(#SENT#|<blank>|\"|»|”|.|-|\\s|\\?|!)$");
		Pattern patternEntreAspas = new Pattern("^(\"|“|«|')");
		Pattern patternEntreAspas2 = new Pattern("[\"»”']");
		
		for(i = 0;i<text.size();i++){
			textCadea += text.get(i)+"\n";
		}
		
		tokens = textCadea.split("\n");
		
		for(i = 0;i<tokens.length;i++){
			
			
			
			tokens[i] = tokens[i].replace("\n", "");
			//System.out.println(tokens[i]);
			Tag.put(tokens[i], "");
			
			lowercase = tokens[i].toLowerCase();
			
			//<java><start>
			
			//<java><end>
		}
		
		return saida;
		
	}
	
	
	public String punct(String p){
		
		if(p.equals(".")){
			return "Fp";
		}
		else if(p.equals(",")){
			return "Fc";
		}
		else if(p.equals(":")){
			return "Fd";
		}else if(p.equals(";")){
			return "Fx";
		}else if(new Pattern("^(\\-|\\-\\-)$").matches(p)){
			return "Fg";
		}else if(new Pattern("^(\\'|\\\"|\\`\\`|\\'\\')$").matches(p)){
			return "Fe";
		}else if(p.equals("...")){
			return "Fs";
		}else if(new Pattern("^(\\<\\<|«|\\“)").matches(p)){
			return "Fra";
		}else if(new Pattern("^(\\>\\>|»|\\”)").matches(p)){
			return "Frc";
		}else if(p.equals("%")){
			return "Ft";
		}else if(new Pattern("^(\\/|\\\\)$").matches(p)){
			return "Fh";
		}else if(p.equals("(")){
			return "Fpa";
		}else if(p.equals(")")){
			return "Fpt";
		}else if(p.equals("¿")){
			return "Fia";
		}else if(p.equals("?")){
			return "Fit";
		}else if(p.equals("¡")){
			return "Faa";
		}else if(p.equals("!")){
			return "Fat";
		}else if(p.equals("[")){
			return "Fca";
		}else if(p.equals("]")){
			return "Fct";
		}else if(p.equals("{")){
			return "Fla";
		}else if(p.equals("}")){
			return "Flt";
		}else if(p.equals("…")){
			return "Fz";
		}
		else return "";
	}
	
}
