import java.util.ArrayList;

import jregex.*;

public class Tokens {

	private String UpperCase = "[A-ZÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÑÇÜ]" ;
	private String LowerCase = "[a-záéíóúàèìòùâêîôûñçü]" ;
	private String Punct =  "[\\,\\;\\«\\»\\“\\”\\'\\\"\\&\\$\\#\\=\\(\\)\\<\\>\\!\\¡\\?\\¿\\\\\\[\\]\\{\\}\\|\\^\\*\\-\\€\\·\\¬\\…]";
	private String Punct_urls = "[\\:\\/\\~]";

	
	private String pron = "(me|te|se|le|les|la|lo|las|los|nos|os)"; 
	
	private String w = "[A-ZÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÑÇÜa-záéíóúàèìòùâêîôûñçü]";
	
	private String susp = "SUSP012";
	private String duplo1 = "DOBR111";
	private String duplo2 = "DOBR222";
	private String duplo3 = "DOBR333";
	private String duplo4 = "DOBR444";

	private String dot_quant = "DOTQUANT77";
	private String comma_quant = "COMMQUANT77";
	private String quote_quant = "QUOTQUANT77";
	
	
	public Tokens(){
		
	}
	
	public ArrayList<String> runTokens(ArrayList<String> sentences){
		
 
		Pattern p;
		Replacer r;
		String texto = "";


		ArrayList<String> saida = new ArrayList<String>();
		saida.clear();

		String[] tokens;

		for(String sentence: sentences){
			
			//System.out.println("Sentence procesada: "+sentence);
			
			//Expresion regular en Perl:  s/\.\.\./ $susp /g ;

			p = new Pattern("\\.\\.\\.");
			r = p.replacer( " "+susp+" ");
			sentence = r.replace(sentence);



			//Expresion regular en Perl:  s/\<\</ $duplo1 /g ;

			p = new Pattern("<<");
			r = p.replacer(" "+duplo1+" ");
			sentence = r.replace(sentence);



			//Expresion regular en Perl:  s/\>\>/ $duplo2 /g ;

			p = new Pattern(">>");
			r = p.replacer(" "+duplo2+" ");
			sentence = r.replace(sentence);



			//Expresion regular en Perl:  s/\'\'/ $duplo3 /g ;

			p = new Pattern("\\'\\'");
			r = p.replacer(" "+duplo3+" ");
			sentence = r.replace(sentence);



			//Expresion regular en Perl:  s/\`\`/ $duplo4 /g ;

			p = new Pattern("\\`\\`");
			r = p.replacer(" "+duplo4+" ");
			sentence = r.replace(sentence);



			//Expresion regular en Perl:  s/([0-9]+)\.([0-9]+)/$1$dot_quant$2 /g ;

			p = new Pattern("([0-9]+)\\.([0-9]+)");
			r = p.replacer(""+"$1"+dot_quant+""+"$2 ");
			sentence = r.replace(sentence);

			//System.out.println(sentence);

			//Expresion regular en Perl:  s/([0-9]+)\,([0-9]+)/$1$comma_quant$2 /g ;

			p = new Pattern("([0-9]+)\\,([0-9]+)");
			r = p.replacer(""+"$1"+comma_quant+""+"$2 ");
			sentence = r.replace(sentence);



			//Expresion regular en Perl:  s/([0-9]+)\'([0-9]+)/$1$quote_quant$2 /g ;

			p = new Pattern("([0-9]+)\\'([0-9]+)");
			r = p.replacer(""+"$1"+quote_quant+""+"$2 ");
			sentence = r.replace(sentence);



			//Expresion regular en Perl:  s/($Punct)/ $1 /g ;

			p = new Pattern("("+Punct+")");
			r = p.replacer(" "+"$1 ");
			sentence = r.replace(sentence);
			


			//Expresion regular en Perl:  s/($Punct_urls)(?:[\s\n]|$)/ $1 /g  ; 

			p = new Pattern("("+Punct_urls+")(?:[\\s\n]|"+"$)");
			r = p.replacer(" "+"$1 ");
			sentence = r.replace(sentence);



			//Expresion regular en Perl:  s/\.$/ \. /g  ; ##ponto final

			p = new Pattern("\\.$");
			r = p.replacer(" \\. ");
			sentence = r.replace(sentence);				
			
			//System.out.print(sentence);
			tokens = sentence.split(" ");
			
			for(String token: tokens){
				
				p = new Pattern("\n$");

				//Este if houbo que metelo a forza
				if((!p.matches(token))&&(token!= " ")){
					//if((token!="\n")&&(token!=" ")){
					//System.out.println("Token procesado: "+token);

					token = token.replace("\n","");
					
					//Expresion regular en Perl:  s/^[\s]*//;

					token = token.replace("^[\\s]*","");



					//Expresion regular en Perl:  s/[\s]*$//;

					token = token.replace("[\\s]*"+"$","");



					//Expresion regular en Perl:  s/$susp/\.\.\./;

					token = token.replaceFirst(susp+"","\\.\\.\\.");



					//Expresion regular en Perl:  s/$duplo1/\<\</;

					token = token.replaceFirst(duplo1+"","<<");



					//Expresion regular en Perl:  s/$duplo2/\>\>/;

					token = token.replaceFirst(duplo2+"",">>");



					//Expresion regular en Perl:  s/$duplo3/\'\'/;

					token = token.replaceFirst(duplo3+"","\\'\\'");



					//Expresion regular en Perl:  s/$duplo4/\`\`/;

					token = token.replaceFirst(duplo4+"","\\`\\`");



					//Expresion regular en Perl:  s/$dot_quant/\./;

					token = token.replaceFirst(dot_quant+"","\\.");



					//Expresion regular en Perl:  s/$comma_quant/\,/;

					token = token.replaceFirst(comma_quant+"","\\,");



					//Expresion regular en Perl:  s/$quote_quant/\'/;

					token = token.replaceFirst(quote_quant+"","\\'");

					/*if((token!="\n")&&(token!=" ")){
					saida.add(token.replace("\n", ""));
				}*/
					//System.out.print(token);
					saida.add(token);
				}
			}
			
			saida.add("\n");
		}

		
		return saida;

	}
	
}
