#!/usr/bin/perl

#Separador de frases
#autor: Grupo ProlNat@GE, CITIUS
#Universidade de Santiago de Compostela


# SEPARA FRASES IDENTIFICANDO O PONTO FINAL

#use strict; 
binmode STDIN, ':utf8';
binmode STDOUT, ':utf8';
use utf8;

# Absolute path 
use Cwd 'abs_path';
use File::Basename;
my $abs_path = dirname(abs_path($0));


do $abs_path.'/Modules/sentences-es.perl';
do $abs_path.'/Modules/tokens-es.perl';
do $abs_path.'/Modules/splitter-es.perl';
do $abs_path.'/Modules/ner-es.perl';
do $abs_path.'/Modules/tagger-es.perl';

##lançando funçoes:
my @texto = <STDIN>;
my $texto = join("",@texto);
my @sentences = sentences($texto);
my @tokens = tokens(@sentences);
my @splits = splitter(@tokens);
my @ner = ner_es(@splits);
my @tagger = tagger(@ner);
my $saida = join("\n",@tagger);
print "$saida";
###########

