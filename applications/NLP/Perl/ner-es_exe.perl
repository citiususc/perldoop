#!/usr/bin/perl

#ProLNat NER 
#autor: Grupo ProLNat@GE, CITIUS
#Universidade de Santiago de Compostela



#use strict; 
binmode STDIN, ':utf8';
binmode STDOUT, ':utf8';
use utf8;



do './Modules/ner-es.perl';


#####EXECUTANDO AS FUNÇOES:
#my @split = <STDIN>;
#my $tmp = join("\n",@split);
	#@split = split (" ", $tmp);
#my @ner = ner_es(@split);
#my $saida = join("\n",@ner);
#print "$saida";


while ($linha = <STDIN>) {
	
	@split = split(" ", $linha);
	@ner = ner_es(@split);
	$saida = join("\n",@ner);
	print "$saida";

	}

###########

