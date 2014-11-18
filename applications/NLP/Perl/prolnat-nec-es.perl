#!/usr/bin/perl

#Separador de frases
#autor: Grupo ProlNat@GE, CITIUS
#Universidade de Santiago de Compostela


# SEPARA FRASES IDENTIFICANDO O PONTO FINAL

#use strict; 
binmode STDIN, ':utf8';
binmode STDOUT, ':utf8';
use utf8;


#do $abs_path.'/Modules/sentences-es.perl';
do './Modules/sentences-es.perl';
do './Modules/tokens-es.perl';
do './Modules/splitter-es.perl';
do './Modules/ner-es.perl';
do './Modules/tagger-es.perl';
do './Modules/nec-es.perl';

##lançando funçoes:
#my @texto = <STDIN>;
#my $texto = join("",@texto);
#my @sentences = sentences($texto);
#my @tokens = tokens(@sentences);
#my @splits = splitter(@tokens);
#my @ner = ner_es(@splits);

#my $saida = join("\n",@ner);
#print "$saida";

while ($linha = <STDIN>) {
	
	#$texto = join("",$linha);
	@sentences = sentences($linha);
	
	#print "====SENTENCES====";
	#foreach (@sentences) {
	#	#print "Sentence procesada: ";
 	#	print $_;
	#	print "\n";
 	#}
 	#print "====SENTENCES====";
	@tokens = tokens(@sentences);
	#foreach (@tokens) {
 	#	print $_;
 	#	#print "\n";
 	#}
 	#print "====SENTENCES====";
	@splits = splitter(@tokens);
	#foreach (@splits) {
 	#	print $_;
 	#	print "\n";
 	#} 
	@ner = ner_es(@splits);
	
	@tagger = tagger(@ner);
	
	@nec = nec_es(@tagger);
	
	#$saida = join("\n",@tagger);
	$saida = join("\n",@nec);
	#$saida = join("\n",@ner);

	print "$saida";
	print "\n";
}


###########

