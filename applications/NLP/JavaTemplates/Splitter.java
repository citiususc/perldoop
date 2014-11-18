import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Hashtable;
import jregex.*;


public class Splitter {

	private String nomeFicheiroVerbos = "./Diccionarios.zip/lexicon/verbos-es.txt";
	//private Hashtable<String,String> abreviaturas = new Hashtable<String, String>();
	private ArrayList<String> verb = new ArrayList<String>();
	private Hashtable<String,Integer> Verb = new Hashtable<String, Integer>();
	
	
	private String pron = "(me|te|se|le|les|la|lo|las|los|nos|os)"; 
	private String w = "[A-ZÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÑÇÜa-záéíóúàèìòùâêîôûñçü]";
	
	public Splitter() {
		try{
	
		BufferedReader reader = new BufferedReader(new FileReader(this.nomeFicheiroVerbos));
		String line = null;
		String novoVerbo = "";
		
				
		while ((line = reader.readLine()) != null) {
			novoVerbo = line;
			
			novoVerbo = novoVerbo.replace("\n", "");
			
			if(Verb.containsKey(novoVerbo)){
				//Aumentase o valor
				Verb.put(novoVerbo, Verb.get(novoVerbo)+1);
			}
			else{
				//Metese un novo valor
				Verb.put(novoVerbo, 1);
			}
			
			
			//Expresion regular en Perl:  s/ar$/ár/;
			novoVerbo = novoVerbo.replaceFirst("ar"+"$","ár");

			//Expresion regular en Perl:  s/er$/ér/;
			novoVerbo = novoVerbo.replaceFirst("er"+"$","ér");

			//Expresion regular en Perl:  s/ir$/ír/;
			novoVerbo = novoVerbo.replaceFirst("ir"+"$","ír");
			
			verb.add(novoVerbo);
			
			if(Verb.containsKey(novoVerbo)){
				//Aumentase o valor
				Verb.put(novoVerbo, Verb.get(novoVerbo)+1);
			}
			else{
				//Metese un novo valor
				Verb.put(novoVerbo, 1);
			}
			
		}
		
		reader.close();
		
		} catch (IOException e) {
			// TODO Auto-generated catch block
			System.out.println(e.toString());
			e.printStackTrace();
			}
	}
	
	
	public ArrayList<String> runSplitter(ArrayList<String> text){
		
		ArrayList<String> saida = new ArrayList<String>();
		String token = "";
		boolean found = false;
		String verb = "";
		String tmp1 = "";
		String tmp2 = "";
		
		Pattern p;
		Pattern p2;
		Pattern p3;
		Pattern p4;
		Pattern p5;
		Replacer r;
		
		saida.clear();
		
		for(int i = 0;i<text.size();i++){
			
			found = false;
			
			token = text.get(i).replace("\n","");
			
			p = new Pattern("^("+w+"+r)(nos|os|se)(lo|los|las|los)$","i");
			
			if(p.matches(token)){
				
				r = p.replacer("$1");
				
				Replacer r2 = p.replacer("$2");
				Replacer r3 = p.replacer("$3");
				
				verb = r.replace(token);
				tmp1 = r2.replace(token);
				tmp2 = r3.replace(token);
				
				p2 = new Pattern("[\\w\\W]*(ár|ér|ír)(nos|os|se)(lo|los|las|los)$");
				if((Verb.containsKey(verb.toLowerCase()))&&(p2.matches(token))){
					//Expresion regular en Perl:  s/ár/ar/;
					verb = verb.replaceFirst("ár","ar");

					//Expresion regular en Perl:  s/ér/er/;
					verb = verb.replaceFirst("ér","er");

					//Expresion regular en Perl:  s/ír/ir/; 
					verb = verb.replaceFirst("ír","ir");
					
					saida.add(verb);
					saida.add(tmp1);
					saida.add(tmp2);
					found = true;
					
				}
				
			}
			
			p = new Pattern("^("+w+"+r)("+pron+")$","i");
			if((!found)&&(p.matches(token))){				
				
				r = p.replacer("$1");
				
				Replacer r2 = p.replacer("$2");
				
				
				verb = r.replace(token);
				tmp1 = r2.replace(token);
				
				if(Verb.containsKey(verb.toLowerCase())){
					saida.add(verb);
					saida.add(tmp1);
					found = true;
				}
				
				
			}
			
			p = new Pattern("^[dD]el$");
			
			p5 = new Pattern("^[aA]l$");
			
			if((!found)&&(p.matches(token))){
				p2 = new Pattern("^([dD]e)(l)$");
				
				r = p2.replacer("$1");
				
				Replacer r2;
				
				p3 = new Pattern("^del$");
				p4 = new Pattern("^Del$");
				
				tmp1 = r.replace(token);
				tmp2 = "";
				
				saida.add(tmp1);
				
				if(p3.matches(token)){
					r2 = p2.replacer("e$2");
					saida.add(r2.replace(token));
				}
				
				if(p4.matches(token)){
					r2 = p2.replacer("Es$2");
					saida.add(r2.replace(token));
				}
				
				found = true;
				
				
			}
			else if(p5.matches(token)){
				p2 = new Pattern("^([aA])(l)$");
				
				r = p2.replacer("$1");
				
				Replacer r2;
				
				p3 = new Pattern("^al$");
				p4 = new Pattern("^Al$");
				
				tmp1 = r.replace(token); //p2.matcher(token).group(0);
				tmp2 = "";
				
				saida.add(tmp1);
				//System.out.println("tmp1: "+tmp1);
				
				if(p3.matches(token)){
					r2 = p2.replacer("e$2");
					saida.add(r2.replace(token));
					//System.out.println("tmp2 min: "+r2.replace(token));
				}
				
				if(p4.matches(token)){
					r2 = p2.replacer("E$2");
					saida.add(r2.replace(token));
					//System.out.println("tmp2 mai: "+r2.replace(token));
				}
				
				found = true;
			}
			
			if(!found){
				//System.out.println(token);
				saida.add(token);
			}
			
			if((i==text.size()-1)&&(token=="")){
				saida.add("");
			}
			
		}
		
		
		
		return saida;
		
	}
	
	
}
