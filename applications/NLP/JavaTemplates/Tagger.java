import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.TreeMap;
import java.util.Arrays;
import java.util.Hashtable;


import jregex.Pattern;

import jregex.Replacer;


public class Tagger {


	private String Border = "[\\w\\W]*(Fp|<blank>)[\\w\\W]*";
	private String nomeFicheiroModel = "./Diccionarios.zip/model/train-es";

	private String[] cat_open = new String[] {"NP", "NC", "VM", "RG", "AQ"};
	private int w = 1;
	private int N;
	private double smooth;


	private Hashtable<String, Hashtable<String,Double>> PriorProb = new Hashtable<String, Hashtable<String,Double>>();
	private Hashtable<String, String> featFreq = new Hashtable<String, String>();
	private Hashtable<String, Double> ProbCat = new Hashtable<String, Double>();
	private Hashtable<String, Double> PostProb = new Hashtable<String, Double>();





	public Tagger(){

		String line = "";

		int count = 0;

		Pattern p;
		Replacer r;
		String texto = "";

		String[] aux;

		String cat = "";
		String prob = "";
		String feat = "";
		String freq = "";


		try {

			BufferedReader reader = new BufferedReader(new FileReader(this.nomeFicheiroModel));

			while ((line = reader.readLine()) != null) {

				count++;

				//chomp

				line = line.replace("\n", "");

				if(count == 1){

					p = new Pattern("[\\w\\W]*<number_of_docs>([0-9]*)<[\\w\\W]*");
					r = p.replacer( "$1");
					texto = r.replace(line);

					N = Integer.parseInt(texto);
					smooth = (double) (1.0/(double)(N));
				}

				else if (new Pattern("[\\w\\W]*<cat>[\\w\\W]*","").matches(line)){

					p = new Pattern("<cat>([^<]*)</cat>");
					r = p.replacer( "$1");
					texto = r.replace(line);

					aux = texto.split(" ");

					cat = aux[0];
					prob = aux[1];

					ProbCat.put(cat, Double.parseDouble(prob));

				}

				else if (!new Pattern("[\\w\\W]*<cat>[\\w\\W]*","").matches(line)){

					aux = line.split(" ");

					feat = aux[0];

					cat = aux[1];

					prob = aux[2];

					freq = aux[3];

				}

				if(!cat.equals("")){

					//PriorProb.put(cat+"_"+feat, Double.parseDouble(prob));
					if(!PriorProb.containsKey(cat)){
						PriorProb.put(cat, new Hashtable<String,Double>());
					}
					PriorProb.get(cat).put(feat, Double.parseDouble(prob));

				}

				featFreq.put(feat, freq);

			}

			reader.close();

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

	public ArrayList<String> runTagger(ArrayList<String> text){



		ArrayList<String> saida = new ArrayList<String>();
		ArrayList<String> Cat = new ArrayList<String>();
		ArrayList<String> Feat = new ArrayList<String>();



		Hashtable<Integer, Hashtable<String,String>> TagHash = new Hashtable<Integer, Hashtable<String,String>>();
		Hashtable<Integer, Hashtable<String,String>> LemaHash = new Hashtable<Integer, Hashtable<String,String>>();





		String line 		= "";
		String tag			= "";
		//String last_entry	= "";
		String result		= "";
		String amb			= "";
		//String cat			= "";
		//String feat			= "";
		//String featL		= "";

		Pattern p;
		Replacer r;
		String texto = "";



		String[] entry;
		String[] Token;
		String[] Lema;
		String[] Tag;



		boolean[] noamb;
		boolean[] unk;



		//int k;
		//int j;
		//int end;



		int s			= 0;
		int textLine	= 0;
		//int i 			= 0;

		int pos 		= 0;
		
		Token = new String[text.size()];
		Lema = new String[text.size()];
		Tag = new String[text.size()];

		noamb = new boolean[text.size()];
		unk = new boolean[text.size()];
		
		for(textLine=0;textLine<text.size();textLine++){


			line = text.get(textLine);


			if ((!new Pattern("[\\w\\W]*[\\w]+[\\w\\W]*","").matches(line))||(new Pattern("^[ ]*$","").matches(line))){

				continue;

			}

			entry = line.split(" ");

			//<java><start>
			
			//<java><end>

		}
		return saida;

	}


	public String classif(ArrayList<String> F,ArrayList<String> C){



		String result 		= "";
		String cat_restr 	= "";
		String feat_restr 	= "";
		String cat 			= "";
		String feat 		= "";

		int n;
		int m;
		boolean First;

		ArrayList<Double> valores;
		Double[] valoresDouble;

		Hashtable<String,Boolean> found = new Hashtable<String,Boolean>();
		ArrayList<String> CAT_RESTR = new ArrayList<String>();

		Pattern p;
		Replacer r;
		String texto = "";

		PostProb.clear();

		int i = 0;
		int j = 0;

		for(i = 0;i<C.size();i++){

			cat = C.get(i);

			for(j = 0;j<F.size();j++){

				feat = F.get(j);

				p = new Pattern("^[a-z]+_([0-9]+)[\\w\\W\\d]*$");
				r = p.replacer("$1");

				texto = r.replace(F.get(j));


				n = Integer.parseInt(texto);

				cat_restr = cat+"_"+String.valueOf(n);

				CAT_RESTR.add(cat_restr);
			}
		}


		for(i = 0;i<CAT_RESTR.size();i++){
			cat_restr = CAT_RESTR.get(i);
			p = new Pattern("([A-Z]+)_[0-9]+$");
			r = p.replacer("$1");

			cat = r.replace(cat_restr);

			if(ProbCat.containsKey(cat)){
				PostProb.put(cat_restr, ProbCat.get(cat));
			}

			found.put(cat_restr, false);

			for(j = 0; j<F.size();j++){

				feat_restr = F.get(j);

				p = new Pattern("^[a-z]+_[0-9]+_[0-9]_([RL]_[^ ]+)[\\w\\W\\d]*$");
				r = p.replacer("$1");
				feat = r.replace(feat_restr);


				if((!featFreq.containsKey(feat))||(featFreq.get(feat)=="")){

					continue;
				}

				if(PriorProb.containsKey(cat) && ((PriorProb.get(cat).containsKey(feat) && (PriorProb.get(cat).get(feat))==0)||(!PriorProb.get(cat).containsKey(feat)))){
					PriorProb.get(cat).put(feat, smooth);
				}

				found.put(cat_restr, true);



				if((PostProb.containsKey(cat_restr)) && (PriorProb.containsKey(cat)) && (PriorProb.get(cat).containsKey(feat))){
					PostProb.put(cat_restr, PostProb.get(cat_restr)*PriorProb.get(cat).get(feat));

				}

			}

			if((PostProb.containsKey(cat_restr)) && (ProbCat.containsKey(cat))){

				PostProb.put(cat_restr, PostProb.get(cat_restr)*ProbCat.get(cat));

			}

			if((found.containsKey(cat_restr))&&!found.get(cat_restr).booleanValue()){

				PostProb.put(cat_restr,(double) 0);
			}

		}

		First = false;

		double score = 0;

		Map<String, Double> sortedMap = sortByComparator(PostProb,false);


		for(String c: sortedMap.keySet()){
			if(!First){

				/*if(PostProb.containsKey(c))
					score = PostProb.get(c);*/

				if(sortedMap.containsKey(c))
					score = sortedMap.get(c);

				p = new Pattern("^([\\w\\W]*)(_[0-9]+)[\\w\\W]*");
				r = p.replacer("$1");
				texto = r.replace(c);


				result = texto;

				First = true;

			}
		}

		return result;
	}

	private static Map<String, Double> sortByComparator(Map<String, Double> unsortMap, final boolean order)
	{

		List<Entry<String, Double>> list = new LinkedList<Entry<String, Double>>(unsortMap.entrySet());

		// Sorting the list based on values
		Collections.sort(list, new Comparator<Entry<String, Double>>()
				{
			public int compare(Entry<String, Double> o1,
					Entry<String, Double> o2)
			{
				if (order)
				{
					return o1.getValue().compareTo(o2.getValue());
				}
				else
				{
					return o2.getValue().compareTo(o1.getValue());

				}
			}
				});

		// Maintaining insertion order with the help of LinkedList
		Map<String, Double> sortedMap = new LinkedHashMap<String, Double>();
		for (Entry<String, Double> entry : list)
		{
			sortedMap.put(entry.getKey(), entry.getValue());
		}

		return sortedMap;
	}

	public static void printMap(Map<String, Integer> map)
	{
		for (Entry<String, Integer> entry : map.entrySet())
		{
			System.out.println("Key : " + entry.getKey() + " Value : "+ entry.getValue());
		}
	}


}
