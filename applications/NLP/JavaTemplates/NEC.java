import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Hashtable;

import jregex.Pattern;

public class NEC {

	
	
	private String ficheiroGazloc = "./Diccionarios.zip/gaz/gazLOC.dat";
	private String ficheiroGazper = "./Diccionarios.zip/gaz/gazPER.dat";
	private String ficheiroGazorg = "./Diccionarios.zip/gaz/gazORG.dat";
	private String ficheiroGazmisc = "./Diccionarios.zip/gaz/gazMISC.dat";
	private String ficheiroTwloc = "./Diccionarios.zip/tw/twLOC.dat";
	private String ficheiroTwper = "./Diccionarios.zip/tw/twPER.dat";
	private String ficheiroTworg = "./Diccionarios.zip/tw/twORG.dat";
	private String ficheiroTwmisc = "./Diccionarios.zip/tw/twMISC.dat";
	
	
	private Hashtable<String,Integer> TwLoc = new Hashtable<String,Integer>();
	private Hashtable<String,Integer> TwOrg = new Hashtable<String,Integer>();
	private Hashtable<String,Integer> TwMisc = new Hashtable<String,Integer>();
	private Hashtable<String,Integer> TwPer = new Hashtable<String,Integer>();
	private Hashtable<String,Integer> GazLoc = new Hashtable<String,Integer>();
	private Hashtable<String,Integer> GazOrg = new Hashtable<String,Integer>();
	private Hashtable<String,Integer> GazMisc = new Hashtable<String,Integer>();
	private Hashtable<String,Integer> GazPer = new Hashtable<String,Integer>();
	private Hashtable<String,String> GazPer_part = new Hashtable<String,String>();
	
	private String Border = "(Fp|<blank>)";
	private String stopwords = "_em_|_en_|_de_|_da_|_das_|_dos_|_da_|_do_|_del_|_o_|_a_|_e_|_por_|_para_|_and_|_the_|_in_|_on_|^el_|^la_|^las_|^los_";
	private String prep = "de|por|para"; 
	private String titulo = "señor|señora|señorita|señorito|don|doña";
	
	
	public NEC(){
		
		String NP = "";
		String part = "";
		
		Hashtable<String,Boolean> found = new Hashtable<String, Boolean>();
		
		String[] temp;
		
		int i;
		
		try {
			BufferedReader reader = new BufferedReader(new FileReader(this.ficheiroGazloc));
			
			while ((NP = reader.readLine()) != null) {
				if(!GazLoc.containsKey(NP)){
					GazLoc.put(NP, 1);
				}
				else{
					GazLoc.put(NP, GazLoc.get(NP)+1);
				}
			}
			
			
			reader.close();
			
			reader = new BufferedReader(new FileReader(this.ficheiroGazper));
			
			while ((NP = reader.readLine()) != null) {
				
				if(!GazPer.containsKey(NP)){
					GazPer.put(NP, 1);
				}
				else{
					GazPer.put(NP, GazPer.get(NP)+1);
				}
				
				if (new Pattern("[\\w\\W]*_[\\w\\W]*","").matches(NP )  && !(new Pattern("[\\w\\W]*"+stopwords+""+"[\\w\\W]*","").matches(NP ))) {
					
					temp = NP.split("_");
					
					for(i = 0;i<=temp.length-1;i++){
						part = temp[i];
						
						if(!found.containsKey(part)||!found.get(part)){
							GazPer_part.put(part, NP);
							found.put(part, true);
						}
						
					}
					
				}
				
			}
			
			reader.close();
			
			reader = new BufferedReader(new FileReader(this.ficheiroGazorg));
			
			while ((NP = reader.readLine()) != null) {
				if(!GazOrg.containsKey(NP)){
					GazOrg.put(NP, 1);
				}
				else{
					GazOrg.put(NP, GazOrg.get(NP)+1);
				}
			}
			
			reader.close();
			
			
			reader = new BufferedReader(new FileReader(this.ficheiroGazmisc));
			
			while ((NP = reader.readLine()) != null) {
				if(!GazMisc.containsKey(NP)){
					GazMisc.put(NP, 1);
				}
				else{
					GazMisc.put(NP, GazMisc.get(NP)+1);
				}
			}
			
			reader.close();
			
			reader = new BufferedReader(new FileReader(this.ficheiroTwloc));
			
			while ((NP = reader.readLine()) != null) {
				if(!TwLoc.containsKey(NP)){
					TwLoc.put(NP, 1);
				}
				else{
					TwLoc.put(NP, TwLoc.get(NP)+1);
				}
			}
			
			reader.close();
			
			reader = new BufferedReader(new FileReader(this.ficheiroTwper));
			
			while ((NP = reader.readLine()) != null) {
				if(!TwPer.containsKey(NP)){
					TwPer.put(NP, 1);
				}
				else{
					TwPer.put(NP, TwPer.get(NP)+1);
				}
			}
			
			reader.close();
			
			reader = new BufferedReader(new FileReader(this.ficheiroTworg));
			
			while ((NP = reader.readLine()) != null) {
				if(!TwOrg.containsKey(NP)){
					TwOrg.put(NP, 1);
				}
				else{
					TwOrg.put(NP, TwOrg.get(NP)+1);
				}
			}
			
			reader.close();
			
			reader = new BufferedReader(new FileReader(this.ficheiroTwmisc));
			
			while ((NP = reader.readLine()) != null) {
				if(!TwMisc.containsKey(NP)){
					TwMisc.put(NP, 1);
				}
				else{
					TwMisc.put(NP, TwMisc.get(NP)+1);
				}
			}
			
			reader.close();
			
			
			
		}catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			System.out.println(e.toString());
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println(e.toString());
		}
		
		
	}
	
	ArrayList<String> nec_es(ArrayList<String> text){
		
		ArrayList<String> saida = new ArrayList<String>();
		
		String saidaString = "";
		
		int Window = 3;
		String last_tag = "";
		String new_tag = "";
		int i = 0;
		//int k = 0;
		//int j = 0;
		
		String token = "";
		String lema = "";
		String tag = "";
		String others = "";
		
		String line = "";
		
		String[] Token = new String[text.size()];
		String[] Lema = new String[text.size()];
		String[] Tag = new String[text.size()];
		String[] Others = new String[text.size()];
		String[] composto = new String[text.size()];
		
		String array[];
		
		int left;
		int Left_1;
		int Left_2;
		int right;
		
		int numLine = 0;
		//boolean found;
		
		for(i = 0;i<text.size();i++){
			Token[i] = "";
			Lema[i] = "";
			Tag[i] = "";
			Others[i] = "";
			composto[i] = "";
		}
		
		i = 0;
		
		
		for(numLine = 0;numLine<text.size();numLine++){
			line=text.get(numLine);
			
			if(!line.equals("") && line.split(" ").length>=3){
				
				array = line.split(" ");
				
				//<java><start>
				
				
				//<java><end>
				
			}
			
			
		}
		
		return saida;
		
		
	}
	
	
	boolean Missing(String x){
		
		if((!GazLoc.containsKey(x))&&(!GazPer.containsKey(x))&&(!GazOrg.containsKey(x))&&(GazMisc.containsKey(x))){
			return true;
		}
		else{
			return false;
		}
	}
	
	
	
	boolean Ambiguous(String x){
		if((GazLoc.containsKey(x) && GazPer.containsKey(x)) ||
				(GazLoc.containsKey(x) && GazOrg.containsKey(x)) || 
				(GazPer.containsKey(x) && GazOrg.containsKey(x)) || 
				(GazLoc.containsKey(x) && GazMisc.containsKey(x)) || 
				(GazPer.containsKey(x) && GazMisc.containsKey(x)) || 
				(GazOrg.containsKey(x) && GazMisc.containsKey(x))
				){
			return true;
		}
		else{
			return false;
		}
	}
	
	String Disambiguation(String x){
		
		String result = "";
		
		
		if(GazLoc.containsKey(x) && GazPer.containsKey(x)){
			result = "NP00SP0";
		}
		else if(GazLoc.containsKey(x) && GazOrg.containsKey(x)){
			result = "NP00G00";
		}
		else if(GazPer.containsKey(x) && GazOrg.containsKey(x)){
			result = "NP00SP0";
		}
		else if(GazPer.containsKey(x) && GazMisc.containsKey(x)){
			result = "NP00SP0";
		}
		else if(GazOrg.containsKey(x) && GazMisc.containsKey(x)){
			result = "NP00O00";
		}
		else if(GazLoc.containsKey(x) && GazMisc.containsKey(x)){
			result = "NP00G00";
		}
		else{
			result = "NP00SP0";
		}
		
		return result;
		
		
	}
	
	
	String Trigger(int x, int L1, int L2, String[] X){
		
		//String result="";
		
		if( (x>=X.length) || (x<0) || (L1>=X.length) || (L1<0) || (L2>=X.length) || (L2<0) ){
			return "0";
		}
		else if(X[x]==""){
			return "0";
		}
		else{
			
			if (TwLoc.containsKey(X[x]) || new Pattern("^(en|em|in)"+"$","").matches(X[L2] )) {
				return "NP00G00";
			}
			
			else if (TwPer.containsKey(X[x]) && !(new Pattern("^("+prep+")"+"$","").matches(X[L1] ))  && !(new Pattern("^("+prep+")"+"$","").matches(X[L2] )) ) {
				return "NP00SP0";
			}
			
			else if(TwOrg.containsKey(X[x])){
				return "NP00O00";
			}
			
			else if(TwMisc.containsKey(X[x])){
				return "NP00V00";
			}
			
			else{
				return "0";
			}
		}
		
		//return result;
	}
	
	String Gaz(String x){
		String result = "";
		
		if(GazLoc.containsKey(x)){
			result = "NP00G00";
		}
		
		else if(GazPer.containsKey(x)){
			result= "NP00SP0";
		}
		
		else if(GazOrg.containsKey(x)){
			result = "NP00O00";
		}
		else if(GazMisc.containsKey(x)){
			result = "NP00V00";
		}
		else{
			result = "0";
		}
		return result;
	}
	
	String Tw(String x){
		String result = "";
		
		if(TwLoc.containsKey(x)){
			result = "NP00G00";
		}
		
		else if(TwPer.containsKey(x)){
			result = "NP00SP0";
		}
		
		else if(TwOrg.containsKey(x)){
			result = "NP00O00";
		}
		
		else if(TwMisc.containsKey(x)){
			result = "NP00V00";
		}
		
		else{
			result = "0";
		}
		
		return result;
	}
	
	String DisambiguationAdHoc(String x){
		String result = "";
		
		if (AllUpper(x)){
			result = "NP00O00";
		}
		else{
			result = "NP00O00";
		}
		
		
		return result;
	}
	
	
	boolean AllUpper(String l){
		boolean result = false;
		
		int countletters = 0;
		int i = 0;
		
		String[] string = l.split("");
		String letter = "";
		
		for(i = 0;i<string.length;i++){
			letter = string[i];
			
			if (new Pattern("[\\w\\W]*[A-ZÁÉÍÓÚÑÇ][\\w\\W]*","").matches(letter )) {
				countletters++;
			}
			
		}
		
		if(countletters >= string.length-1){
			result = true;
		}
		else{
			result = false;
		}
		
		return result;
	}
	
}

