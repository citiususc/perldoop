import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import jregex.*;
import jregex.Pattern;

public class Sentences {

	private String nomeFicheiroAbreviaturas = "./Diccionarios.zip/lexicon/abreviaturas-es.txt";
	//private Hashtable<String,String> abreviaturas = new Hashtable<String, String>();
	private ArrayList<String> keysAbr = new ArrayList<String>();
	private String[] splitAbreviatura;
	
	private String mark_abr = "<ABR-TMP>";
	private String mark_sigla= "<SIGLA-TMP>";
	
	private String UpperCase = "[A-ZÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÑÇÜ]" ;
	private String LowerCase = "[a-záéíóúàèìòùâêîôûñçü]" ;
	
	
	
	public Sentences(){
		try{
	
		BufferedReader reader = new BufferedReader(new FileReader(this.nomeFicheiroAbreviaturas));
		String line = null;
		
		
		while ((line = reader.readLine()) != null) {
		    // ...
			if(line.contains(".")){
				splitAbreviatura = line.split(" ");
				//System.out.println(String.valueOf(splitAbreviatura.length));
				//abreviaturas.put(splitAbreviatura[0].toLowerCase(), splitAbreviatura[1]);
				
				keysAbr.add(splitAbreviatura[0].toLowerCase());
			}
			
		}
		
		reader.close();
		
		
		} catch (IOException e) {
			// TODO Auto-generated catch block
			System.out.println(e.toString());
			e.printStackTrace();
			}
	}
	
	public ArrayList<String> runSentencesModule(String entrada)throws PatternSyntaxException{
		
		String texto = entrada;
		
		String[] datosEntrada = texto.split("\n");
		
		Pattern p;
		Replacer r;

		String abr = "";
		ArrayList<String> sentences = new ArrayList<String>();

		sentences.clear();
		
		//for(int i=0;i<abreviaturas.size();i++){
		for(int i=0;i<keysAbr.size();i++){
			//System.out.println(keysAbr.get(i));
			abr = keysAbr.get(i);
			
			//Expresion regular en Perl:  s/\./\\./g;

			p = new Pattern("\\.");
			r = p.replacer("\\\\.");
			abr = r.replace(abr);



			//Expresion regular en Perl:  s/^($abr)/$1$mark_abr/g;

			p = new Pattern("^("+abr+")");
			r = p.replacer(""+"$1"+mark_abr+"");
			texto = r.replace(texto);



			//Expresion regular en Perl:  s/(\s)($abr)/$1$2$mark_abr/g;

			p = new Pattern("(\\s)("+abr+")");
			r = p.replacer(""+"$1"+"$2"+mark_abr+"");
			texto = r.replace(texto);



			//Expresion regular en Perl:  s/\.($mark_abr)/$1/g;

			p = new Pattern("\\.("+mark_abr+")");
			r = p.replacer(""+"$1");
			texto = r.replace(texto);
		}
		
		
		//Expresion regular en Perl:  s/($LowerCase)\.($LowerCase)/$1$mark_sigla$2/g;

		p = new Pattern("("+LowerCase+")\\.("+LowerCase+")");
		r = p.replacer(""+"$1"+mark_sigla+""+"$2");
		texto = r.replace(texto);



		//Expresion regular en Perl:  s/\.\.\./$mark_sigla$mark_sigla$mark_sigla/g;

		p = new Pattern("\\.\\.\\.");
		r = p.replacer(""+mark_sigla+""+mark_sigla+""+mark_sigla+"");
		texto = r.replace(texto);


		//Expresion regular en Perl:   s/([0-9]+)\.([0-9]+)/$1$mark_sigla$2/g;

		p = new Pattern("([0-9]+)\\.([0-9]+)");
		r = p.replacer(""+"$1"+mark_sigla+""+"$2");
		texto = r.replace(texto);
		

		//Expresion regular en Perl:  s/($UpperCase)\.($UpperCase)/$1$mark_sigla$2/g;

		p = new Pattern("("+UpperCase+")\\.("+UpperCase+")");
		r = p.replacer(""+"$1"+mark_sigla+""+"$2");
		texto = r.replace(texto);



		//Expresion regular en Perl:  s/($mark_sigla$UpperCase)\.($UpperCase)/$1$mark_sigla$2/g;

		p = new Pattern("("+mark_sigla+""+UpperCase+")\\.("+UpperCase+")");
		r = p.replacer(""+"$1"+mark_sigla+""+"$2");
		texto = r.replace(texto);



		//Expresion regular en Perl:  s/($mark_sigla$UpperCase)\.([\s]+)($LowerCase)/$1$mark_sigla$2$3/g; ##o P.P. está ....

		p = new Pattern("("+mark_sigla+""+UpperCase+")\\.([\\s]+)("+LowerCase+")");
		r = p.replacer(""+"$1"+mark_sigla+""+"$2"+"$3");
		texto = r.replace(texto);



		//Expresion regular en Perl:  s/\./\.\n/g; ##resto de pontos: final de frase 

		p = new Pattern("\\.");
		r = p.replacer("\\.\n");
		texto = r.replace(texto);

		//Expresion regular en Perl:  s/$/\n/ ; ##final de texto: final de frase

		texto = texto.replaceFirst("$","\n");


		//Expresion regular en Perl:  s/(\n)[\s]+/$1/g;

		p = new Pattern("(\n)[\\s]+");
		r = p.replacer(""+"$1");
		texto = r.replace(texto);



		//Expresion regular en Perl:  s/$mark_abr/\./g;

		p = new Pattern(mark_abr+"");
		r = p.replacer("\\.");
		texto = r.replace(texto);



		//Expresion regular en Perl:  s/$mark_sigla/\./g;

		p = new Pattern(mark_sigla+"");
		r = p.replacer("\\.");
		texto = r.replace(texto);
		
		sentences.add(texto);
		
		return sentences;
	}
	
}
