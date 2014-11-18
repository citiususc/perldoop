#!/usr/bin/perl

#<PERL><COMENTARIO>ProLNat NER 
#<PERL><COMENTARIO>autor: Grupo ProLNat@GE, CITIUS
#<PERL><COMENTARIO>Universidade de Santiago de Compostela

use strict; 
binmode STDIN, ':utf8';
binmode STDOUT, ':utf8';
use utf8;

#<PERL><COMENTARIO> Absolute path 
use Cwd 'abs_path';
use File::Basename;
my $abs_path = dirname(abs_path($0));



##<PERL><COMENTARIO>#lexico formato freeling
open (LEX, $abs_path."/lexicon/dicc.src") or die "O ficheiro do lexico não pode ser aberto: $!\n";
binmode LEX,  ':utf8';

##<PERL><COMENTARIO>#lexico de formas ambiguas
open (AMB, $abs_path."/lexicon/ambig.txt") or die "O ficheiro de palavras ambiguas não pode ser aberto: $!\n";
binmode AMB,  ':utf8';


#<PERL><COMENTARIO>print STDERR "$abs_path\n";
#<PERL><COMENTARIO>#variaveis globais
#<PERL><COMENTARIO>#para sentences e tokens:
my $UpperCase = "[A-ZÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÑÇÜ]" ;
my $LowerCase = "[a-záéíóúàèìòùâêîôûñçü]" ;
my $Punct =  qr/[\,\;\«\»\“\”\'\"\&\$\#\=\(\)\<\>\!\¡\?\¿\\\[\]\{\}\|\^\*\-\€\·\¬\…]/;
my $Punct_urls = qr/[\:\/\~]/ ;
my $w = "[A-ZÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÑÇÜa-záéíóúàèìòùâêîôûñçü]";

#<PERL><COMENTARIO>#########CARGANDO RECURSOS COMUNS
#<PERL><COMENTARIO>#cargando o lexico freeling e mais variaveis globais
my %Entry;
my %Lex;
my %StopWords;
my %Ambig;
while (my $line = <LEX>) {
    
    chomp $line;
    (my @entry) = split (" ", $line);
    my $token = $entry[0];
    
    (my $entry) = ($line =~ /^[^ ]+ ([\w\W]+)$/);
    $Entry{$token} = $entry;
    my $i=1;
    while ($i<=$#entry) {
        my $lemma =  $entry[$i];
        $i++  ;
        my $tag =  $entry[$i];
	#<PERL><COMENTARIO>$Lex{$token}{$lemma} = $tag;
        $Lex{$token}++;
        $StopWords{$token} = $tag if ($tag =~ /^(P|SP|R|D|I)/);
        $i++;
    }
   
}
#<PERL><COMENTARIO>#cargando palavras ambiguas
while (my $t = <AMB>) {
    $t = Trim ($t);
    $Ambig{$t}++;
}

sub ner_es {
  my (@text) = @_ ;

  my $N=10;
  my $saidaString;
  my @saida;

  #<PERL><COMENTARIO>#####################info dependente da língua!!!####################################################################################
  my $Prep = "(de|del)" ;  #<PERL><COMENTARIO>#preposiçoes que fazem parte dum NP composto
  my $Art = "(el|la|los|las)" ; #<PERL><COMENTARIO>#artigos que fazem parte dum NP composto
  my $currency = "(euro|euros|dólar|dolares|peseta|pesetas|yen|yenes|escudo|escudos|franco|francos|real|reales|\$|€)";
  my $measure = "(kg|kilogramo|quilogramo|gramo|g|centímetro|cm|hora|segundo|minuto|tonelada|tn|metro|m|km|kilómetro|quilómetro|%)";
  my $quant = "(ciento|cientos|miles|millón|millones|billón|billones|trillón|trillones)";  
  my $cifra = "(dos|tres|catro|cinco|seis|siete|ocho|nueve|diez|cien|mil)";  #<PERL><COMENTARIO>#hai que criar as cifras básicas: once, doce... veintidós, treinta y uno...
  my $meses =  "(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)";
  #<PERL><COMENTARIO>#####################info dependente da língua!!!####################################################################################

  my $SEP = "_";
 #<PERL><COMENTARIO> my @tokens;
  my %Tag;
  my $Candidate;
  my $Nocandidate;
  #<PERL><COMENTARIO>my $ContarCandidatos=0;
  my $linhaFinal;
  my $token;
  my $adiantar;  

 
  my $text = join("\n",@text)  ;  
  (my @tokens) = split ('\n', $text);
  
  for (my $i=0; $i<=$#tokens; $i++) {

       chomp $tokens[$i];
          #<PERL><COMENTARIO>#marcar fim de frase
      $Tag{$tokens[$i]} = "";
      my $lowercase = lowercase ($tokens[$i] ); 
#<PERL><COMENTARIO><PERL><START>
      if   ($tokens[$i] =~ /^[ ]*$/) {
          $tokens[$i] = "#SENT#";
      }
     #<PERL><COMENTARIO> print STDERR "---- $tokens[$i]\n";
          my $k = $i - 1 ;
          my $j = $i + 1;
       
		if($k<0){
			$k = 0;
		}
		if($j>$#tokens){
			$j = $#tokens;
		}
		
		

         #<PERL><COMENTARIO>###CADEA COM TODAS PALAVRAS EM MAIUSCULA
         if   ($tokens[$i] =~ /^$UpperCase+$/ && $tokens[$j] =~ /^$UpperCase+$/ && $Lex{$lowercase} && $Lex{lowercase($tokens[$j])} ) {

             $Tag{$tokens[$i]} = "UNK"; #<PERL><COMENTARIO>#identificamos cadeas de tokens so em maiusculas e estao no dicionario
         }
         elsif   ($tokens[$i] =~ /^$UpperCase+$/ && $tokens[$k] =~ /^$UpperCase+$/ && $Lex{$lowercase} && $Lex{lowercase($tokens[$k])} && ($tokens[$j] =~ /^(\#SENT\#|\<blank\>|\"|\»|\”|\.|\-|\s|\?|\!)$/ || $i == $#tokens ) ) { #<PERL><COMENTARIO>#ultimo token de uma cadea com so maiusculas
             $Tag{$tokens[$i]} = "UNK";             
         }
         
         #<PERL><COMENTARIO>###CADEAS ENTRE ASPAS com palavras que começam por maiuscula 
       elsif   ( $i<($#tokens-1) && $tokens[$k]  =~ /^(\"|\“|\«|\')/ && $tokens[$i] =~ /^$UpperCase/ && $tokens[$i+1] =~ /^$UpperCase/ && $tokens[$i+2] =~ /[\"\»\”\']/) {
             
             #<PERL><COMENTARIO> print STDERR  "#$tokens[$i]# --- #$tokens[$k]#\n";
	      $Candidate =  $tokens[$i] . $SEP . $tokens[$i+1] ;  
              $i = $i + 1; 
              $tokens[$i] = $Candidate;
                                
       }
       elsif   ($i<($#tokens-2) &&$tokens[$k]  =~ /^(\"|\“|\«|\')/ && $tokens[$i] =~ /^$UpperCase/ && $tokens[$i+1] =~ /^$UpperCase/ && $tokens[$i+2] =~ /^$UpperCase/ && $tokens[$i+3] =~ /[\"\»\”\']/) {
             
              #<PERL><COMENTARIO>print STDERR  "#$tokens[$i]# --- #$tokens[$k]#\n";
	      $Candidate =  $tokens[$i] . $SEP . $tokens[$i+1] . $SEP . $tokens[$i+2] ;   
              $i = $i + 2;
              $tokens[$i] = $Candidate;
                            
       }
       elsif   ($i<($#tokens-3) &&$tokens[$k]  =~ /^(\"|\“|\«|\')/ && $tokens[$i] =~ /^$UpperCase/ && $tokens[$i+1] =~ /^$UpperCase/ && $tokens[$i+2] =~ /^$UpperCase/ && $tokens[$i+3] =~ /^$UpperCase/ && $tokens[$i+4] =~ /[\"\»\”\']/) {
                $Candidate =  $tokens[$i] . $SEP . $tokens[$i+1] . $SEP .  $tokens[$i+2] . $SEP . $tokens[$i+3];   
                $i = $i + 3;   
                $tokens[$i] = $Candidate;           
       }
       elsif   ($i<($#tokens-4) &&$tokens[$k]  =~ /^(\"|\“|\«|\')/ && $tokens[$i] =~ /^$UpperCase/ && $tokens[$i+1] =~ /^$UpperCase/ && $tokens[$i+2] =~ /^$UpperCase/ && $tokens[$i+3] =~ /^$UpperCase/ && $tokens[$i+4] =~ /^$UpperCase/ && $tokens[$i+5] =~ /[\"\»\”\']/) {
                $Candidate =  $tokens[$i] . $SEP . $tokens[$i+1] . $SEP .  $tokens[$i+2] . $SEP . $tokens[$i+3] . $SEP . $tokens[$i+4];   
                $i = $i + 4;   
                $tokens[$i] = $Candidate;           
       }
       elsif   ($i<($#tokens-5) &&$tokens[$k]  =~ /^(\"|\“|\«|\')/ && $tokens[$i] =~ /^$UpperCase/ && $tokens[$i+1] =~ /^$UpperCase/ && $tokens[$i+2] =~ /^$UpperCase/ && $tokens[$i+3] =~ /^$UpperCase/ && $tokens[$i+4] =~ /^$UpperCase/  && $tokens[$i+5] =~ /^$UpperCase/ && $tokens[$i+6] =~ /[\"\»\”\']/) {
                $Candidate =  $tokens[$i] . $SEP . $tokens[$i+1] . $SEP .  $tokens[$i+2] . $SEP . $tokens[$i+3] . $SEP . $tokens[$i+4] . $SEP . $tokens[$i+5];   
                $i = $i + 5;   
                $tokens[$i] = $Candidate;           
       }

        #<PERL><COMENTARIO>##Palavras que começam por maiúscula
         #<PERL><COMENTARIO> print STDERR "---- #$tokens[$i]# --- #$tokens[$k]#\n";
	elsif   ( ($tokens[$i] =~ /^$UpperCase/) && $tokens[$k] !~ /^(\#SENT\#|\<blank\>|\"|\“|\«|\.|\-|\s|\¿|\¡)$/ && $i>0 ) { #<PERL><COMENTARIO>#começa por maiúscula e nao vai a principio de frase
                 $Tag{$tokens[$i]} = "NP00000"; 
                 
                #<PERL><COMENTARIO>print "TOKEN::: ##$tokens[$i]##\n" ;
                 #<PERL><COMENTARIO>print  STDERR "1TOKEN::: ##$i## --  ##$tokens[$i]## - - #$Tag{$tokens[$i]}# --  prev:#$tokens[$k]# --  post:#$tokens[$j]#\n" if ($tokens[$i] eq "De");
                
         }
         elsif   ( ($tokens[$i] =~ /^$UpperCase/ && $tokens[$k]  =~ /^(\#SENT\#|\<blank\>|\"|\“|\«|\.|\-|\s|\¿|\¡)$/) || ($i==0) ) { #<PERL><COMENTARIO>#começa por maiúscula e vai a principio de frase 
	       #<PERL><COMENTARIO> $token = lowercase ($tokens[$i]);
                #<PERL><COMENTARIO> print STDERR "2TOKEN::: lowercase: #$lowercase# -- token: #$tokens[$i]# --  token_prev: #$tokens[$k]# --  post:#$tokens[$j]#--- #$Tag{$tokens[$i]}#\n" if ($tokens[$i] eq "De");       
                if (!$Lex{$lowercase} || $Ambig{$lowercase}) {
		   #<PERL><COMENTARIO> print STDERR "--AMBIG::: #$lowercase#\n";
                  $Tag{$tokens[$i]} = "NP00000"; 
                   #<PERL><COMENTARIO> print STDERR "OKKKK::: lowercase: #$lowercase# -- token: #$tokens[$i]# --  token_prev: #$tokens[$k]#  --  post:#$tokens[$j]#\n" ;       
		}
                #<PERL><COMENTARIO> print STDERR "##$tokens[$i]## -  #$tokens[$k]#\n" if ($tokens[$i] eq "De");
           }
                         
      
     #<PERL><COMENTARIO># if   ( $tokens[$i] =~ /^$UpperCase$LowerCase+/ && ($StopWords{$lowercase} && ($tokens[$k]  =~ /^(\#SENT\#|\<blank\>|\"|\“|\«|\.|\-|\s|\¿|\¡)$/) || ($i==0)) ) {   }##se em principio de frase a palavra maiuscula e uma stopword, nao fazemos nada
 
        if   ( ($tokens[$i] =~ /^$UpperCase$LowerCase+/ && $Lex{$lowercase} &&  !$Ambig{$lowercase}) && ($tokens[$k]  =~ /^(\#SENT\#|\<blank\>|\"|\“|\«|\.|\-|\s|\¿|\¡)$/ || $i==0) ) {  
        
          #<PERL><COMENTARIO>print  STDERR "1TOKEN::: ##$lowercase## // #!$Ambig{$lowercase}# - - #$Tag{$tokens[$i]}# --  #$tokens[$k]#\n" ;      
    
        }#<PERL><COMENTARIO>#se em principio de frase a palavra maiuscula e está no lexico sem ser ambigua, nao fazemos nada

      #<PERL><COMENTARIO>#caso que seja maiuscula
      #<PERL><COMENTARIO>##construimos candidatos para os NOMES PROPRIOS COMPOSTOS#############################################################
      elsif  ($tokens[$i] =~ /^$UpperCase$LowerCase+/) {
            #<PERL><COMENTARIO> print "##$tokens[$i]## - #$Tag{$tokens[$i]}# --  #$tokens[$k]# ---- #$StopWords{$lowercase}#\n"; 
	     $Candidate = $tokens[$i]  ;
	     #<PERL><COMENTARIO>$Candidate = $tokens[$i];
            #<PERL><COMENTARIO> $Nocandidate = $tokens[$i] ;
              #<PERL><COMENTARIO> print  STDERR "4TOKEN::: ##$tokens[$i]## - - #$Tag{$tokens[$i]}# --  #$tokens[$k]#\n" ;         
             my $count = 1;
             my $found = 0; #<PERL><COMENTARIO><PERL><VARIABLE><BOOLEAN>
            #<PERL><COMENTARIO> print  STDERR "Begin: ##$i## - ##$count##- $tokens[$i]\n";
            #<PERL><COMENTARIO> while ( (!$found) && ($count < $N) )    {
              while  (!$found)      {
                my $j = $i + $count;
                #<PERL><COMENTARIO>chomp $tokens[$j];
               #<PERL><COMENTARIO>print  STDERR "****Begin: ##$i## - ##$j##- #$tokens[$i]# --- #$tokens[$j]#\n";
               if($j > $#tokens){
               	$j = $#tokens;
               }
               
                if ($tokens[$j] eq "" || ($tokens[$j] =~ /^($Art)$/i && $tokens[$j-1] !~ /^($Prep)$/i) ) { #<PERL><COMENTARIO>se chegamos ao final de uma frase sem ponto ou se temos um artigo sem uma preposiçao precedente, paramos (Pablo el muchacho)
                  $found=1; #<PERL><COMENTARIO><PERL><VARIABLE><BOOLEAN>
                }
                elsif ( ($tokens[$j] !~ /^$UpperCase$LowerCase+/ ||  $Candidate =~ /($Punct)|($Punct_urls)/ ) && ($tokens[$j] !~ /^($Prep)$/i && $tokens[$j] !~ /^($Art)$/i )  )  { 
                    #<PERL><COMENTARIO>   print  STDERR "4TOKEN::: ##$i## - ##$j## - ##$count##----> ##$tokens[$i]## - - #$tokens[$j]# --  #$tokens[$k]#\n" ;
                      $found = 1 ; #<PERL><COMENTARIO><PERL><VARIABLE><BOOLEAN>
                 }
                                
                 else {
                   $Candidate .= $SEP . $tokens[$j] ;
                  #<PERL><COMENTARIO> $Nocandidate .=  " " . $tokens[$j] ; 
                   $count++;
                   #<PERL><COMENTARIO>print STDERR "okk: #$Candidate#\n";         
                   if ($j >= $#tokens){
							$found = 1;#<PERL><COMENTARIO><PERL><VARIABLE><BOOLEAN>
						}        
	         }
             }
             
             #<PERL><COMENTARIO>print STDERR "---------#$count# -- #$Candidate# - #$SEP#  - #$N#\n";

            if ( ($count > 1) && ($count <= $N) && ($Candidate !~ /$Punct$SEP/ || $Candidate !~ /$Punct_urls$SEP/) &&  $Candidate !~ /$SEP($Prep)$/ && $Candidate !~ /$SEP($Prep)$SEP($Art)$/  ) {
		#<PERL><COMENTARIO>print STDERR "----------#$Candidate#\n";
                 
                 $i = $i + $count - 1;
                 if(!($i<=$#tokens)){
                 	$i = $#tokens;
                 }
                 
		 $tokens[$i] =  $Candidate ; 
            }

            elsif ( ($count > 1) && ($count <= $N) && ($Candidate !~ /$Punct$SEP/ || $Candidate !~ /$Punct_urls$SEP/) &&  $Candidate =~ /$SEP($Prep)$/i ) {
              $i = $i + $count - 2;
              if(!($i<=$#tokens)){
                 	$i = $#tokens;
                 }
              $Candidate =~ s/$SEP($Prep)$//;  
	      $tokens[$i] =  $Candidate ;
              #<PERL><COMENTARIO>print STDERR "OK----------#$Candidate#\n";
	    }
            elsif ( ($count > 1) && ($count <= $N) && ($Candidate !~ /$Punct$SEP/ || $Candidate !~ /$Punct_urls$SEP/) &&  $Candidate =~ /$SEP($Prep)$SEP($Art)$/i ) {
              $i = $i + $count - 2;
              if(!($i<=$#tokens)){
                 	$i = $#tokens;
                 }
              $Candidate =~ s/$SEP($Prep)$SEP($Art)$//i;  
	      $tokens[$i] =  $Candidate ;
             #<PERL><COMENTARIO>print STDERR "----------#$Candidate#\n"; 
	    }
            elsif ( ($count > 1) && ($count <= $N) && ($Candidate !~ /$Punct$SEP/ || $Candidate !~ /$Punct_urls$SEP/) &&  $Candidate =~ /SEP($Art)$/i ) {
              $i = $i + $count - 2;
              if(!($i<=$#tokens)){
                 	$i = $#tokens;
                 }
              $Candidate =~ s/$SEP($Art)$//i;  
	      $tokens[$i] =  $Candidate ;
             #<PERL><COMENTARIO>print STDERR "----------#$Candidate#\n"; 
	    }
            
          }
          #<PERL><COMENTARIO>##FIM CONSTRUÇAO DOS NP COMPOSTOS##############################


          #<PERL><COMENTARIO>#NP se é composto
	  if ($tokens[$i] =~ /[^\s]+_[^\s]+/ ) { 
              $Tag{$tokens[$i]} = "NP00000" ;
              #<PERL><COMENTARIO> print  STDERR "TOKEN::: $i --  $tokens[$i] --- $Candidate\n";
	  }
          #<PERL><COMENTARIO>#se não lhe foi assigado o tag NP, entao UNK (provisional)
          elsif   (! ($Tag{$tokens[$i]}) || ($Tag{$tokens[$i]} eq "")) {
              $Tag{$tokens[$i]} = "UNK" ; 
	  }

          #<PERL><COMENTARIO>#se é UNK (é dizer nao é NP), entao vamos buscar no lexico
          if ($Tag{$tokens[$i]} eq "UNK") {
	     $token = lowercase ($tokens[$i]);
             if ($Lex{$token}) {
		 $Tag{$tokens[$i]} = $Entry{$token};
                
	     }
	     
          }
          elsif ($Tag{$tokens[$i]} eq "NP00000") {
             $token = lowercase ($tokens[$i]); 
          }

         $adiantar=0;
         #<PERL><COMENTARIO>#os numeros, medidas e datas #USAR O FICHEIRO QUANTITIES.DAT##################

         #<PERL><COMENTARIO>#CIFRAS OU NUMEROS
         if ($tokens[$i] =~ /[0-9]+/ || $tokens[$i] =~ /^$cifra$/) {
	        $token = $tokens[$i];
	        #<PERL><COMENTARIO>print  STDERR "Entrou con ".$tokens[$i];
                $Tag{$tokens[$i]} = "Z"; 
	  }         

         #<PERL><COMENTARIO>#MEAUSURES
         if  ($Tag{$tokens[$i]} =~ /^Z/ && $i<$#tokens && $tokens[$i+1] =~ /^$measure(s|\.)?$/i) {
	        $tokens[$i] = $tokens[$i] . "_" . $tokens[$i+1] ;
	        $token = lc ($tokens[$i]); #<PERL><COMENTARIO>#haveria que lematizar/normalizar o token: kg=kilogramo,...
                $Tag{$tokens[$i]} = "Zu"; 
                $adiantar=1 ;
	  }
          elsif ($Tag{$tokens[$i]} =~ /^Z/ && $i<($#tokens-1)  && $tokens[$i+1] =~ /^$quant$/i &&  $tokens[$i+2] =~ /^$measure(s|\.)?$/i) {
	      $tokens[$i] = $tokens[$i] . "_" . $tokens[$i+1] . "_" . $tokens[$i+2]  ;
	        $token = lc ($tokens[$i]); 
                $Tag{$tokens[$i]} = "Zu"; 
                $adiantar=2;	        
	  }

          #<PERL><COMENTARIO>#CURRENCY
          elsif ($Tag{$tokens[$i]} =~ /^Z/ && $i<$#tokens && $tokens[$i+1] =~ /^$currency$/i) {
	      $tokens[$i] = $tokens[$i] . "_" . $tokens[$i+1];
	        $token = lc ($tokens[$i]); #<PERL><COMENTARIO>#haveria que lematizar/normalizar o token: euros=euro...
                $Tag{$tokens[$i]} = "Zm"; 
                $adiantar=1;	        
	  }
          elsif ($Tag{$tokens[$i]} =~ /^Z/ && $i<($#tokens-2)  && $tokens[$i+1] =~ /^$quant$/i && $tokens[$i+2] =~ /^de$/i && $tokens[$i+3] =~ /^$currency$/i) {
	      $tokens[$i] = $tokens[$i] . "_" . $tokens[$i+1] . "_" . $tokens[$i+2] . "_" . $tokens[$i+3] ;
	        $token = lc ($tokens[$i]); #<PERL><COMENTARIO>#haveria que lematizar/normalizar o token: euros=euro...
                $Tag{$tokens[$i]} = "Zm"; 
                $adiantar=3;	        
	  }
          elsif ($Tag{$tokens[$i]} =~ /^Z/ && $i<($#tokens-1)  && $tokens[$i+1] =~ /^$quant$/i && $tokens[$i+2] =~ /^$currency$/i) {
	      $tokens[$i] = $tokens[$i] . "_" . $tokens[$i+1] . "_" . $tokens[$i+2]  ;
	        $token = lc ($tokens[$i]); #<PERL><COMENTARIO>#haveria que lematizar/normalizar o token: euros=euro...
                $Tag{$tokens[$i]} = "Zm"; 
                $adiantar=2;	        
	  }
          elsif ($Tag{$tokens[$i]} =~ /^Z/ && $i<($#tokens-1)  && $tokens[$i+1] =~ /^de$/i && $tokens[$i+2] =~ /^$currency$/i) {
	      $tokens[$i] = $tokens[$i] . "_" . $tokens[$i+1] . "_" . $tokens[$i+2] ;
	        $token = lc ($tokens[$i]); #<PERL><COMENTARIO>#haveria que lematizar/normalizar o token: euros=euro...
                $Tag{$tokens[$i]} = "Zm"; 
                $adiantar=2;	        
	  }
          #<PERL><COMENTARIO>#QUANTITIES
          elsif ($Tag{$tokens[$i]} =~ /^Z/ && $i<($#tokens-1) && $tokens[$i+1] =~ /^$quant$/i) {
	        $tokens[$i] = $tokens[$i] . "_" . $tokens[$i+1] ;
	        $token = lc ($tokens[$i]); #<PERL><COMENTARIO>#haveria que lematizar/normalizar o token: kg=kilogramo,...
                $Tag{$tokens[$i]} = "Z"; 
                $adiantar=1 ;
	  }
        

          #<PERL><COMENTARIO>#DATES
          elsif ($Tag{$tokens[$i]} =~ /^Z/ && $i<($#tokens-3)  && $tokens[$i+1] =~ /^de$/i && $tokens[$i+2] =~ /^$meses$/i  && $tokens[$i+3] =~ /^de$/i && $tokens[$i+4] =~ /[0-9]+/) {
	        $tokens[$i] = $tokens[$i] . "_" . $tokens[$i+1] . "_" . $tokens[$i+2] . "_" . $tokens[$i+3] . "_" . $tokens[$i+4]  ;
	        $token = lc ($tokens[$i]); #<PERL><COMENTARIO>#haveria que lematizar/normalizar o token: kg=kilogramo,...
                $Tag{$tokens[$i]} = "W"; 
                $adiantar=4;	        
	  }
          elsif ($Tag{$tokens[$i]} =~ /^Z/ && $i<($#tokens-1)  && $tokens[$i+1] =~ /^de$/i && $tokens[$i+2] =~ /^$meses$/i) {
	        $tokens[$i] = $tokens[$i] . "_" . $tokens[$i+1]  . "_" . $tokens[$i+2] ;
	        $token = lc ($tokens[$i]); #<PERL><COMENTARIO>#haveria que lematizar/normalizar o token: kg=kilogramo,...
                $Tag{$tokens[$i]} = "W"; 
                $adiantar=2;   
	  }
         
          #<PERL><COMENTARIO>################################FIM DATAS E NUMEROS

          #<PERL><COMENTARIO>agora etiquetamos os simbolos de puntuaçao
          if ($tokens[$i] eq "\.") {
	        $token = "\.";
                $Tag{$tokens[$i]} = "Fp"; 
	  }

          elsif ($tokens[$i] eq "#SENT#" && $i>0 && $tokens[$i-1] ne "\." && $tokens[$i-1] ne "<blank>" ){
               #<PERL><COMENTARIO> print STDERR "--- #$tokens[$i]# #$tokens[$i-1]#\n";
	        $tokens[$i] = "<blank>";
	        $token = "<blank>";
                $Tag{$tokens[$i]} = "Fp"; 
	  }
          
     
         elsif ($tokens[$i] =~ /^$Punct$/ || $tokens[$i] =~ /^$Punct_urls$/ || $tokens[$i] =~ /^(\.\.\.|\`\`|\'\'|\<\<|\>\>|\-\-)$/ ) {
            $Tag{$tokens[$i]} = punct ($tokens[$i]);
            $token = $tokens[$i]; 
           #<PERL><COMENTARIO> print STDERR "token: #$token# -- #$tokens[$i]# -- #$Tag{$tokens[$i]}# \n";
	 }
         
         #<PERL><COMENTARIO>#as linhas em branco eliminam-se 
         if ($tokens[$i] eq  "#SENT#") {
           next
	 }


        #<PERL><COMENTARIO>#parte final..
        if ( $Tag{$tokens[$i]} =~ /^(UNK|F|NP|Z|W)/  ){
        	$Tag{$tokens[$i]} = $token . " " . $Tag{$tokens[$i]};
        }
        #<PERL><COMENTARIO>Linha de Paulo: $Tag{$tokens[$i]} = $token . " " . $Tag{$tokens[$i]} if ( $Tag{$tokens[$i]} =~ /^(UNK|F|NP|Z|W)/  );
       #<PERL><COMENTARIO> print "$tokens[$i] $Tag{$tokens[$i]}\n";

         $saidaString  = $tokens[$i]." ".$Tag{$tokens[$i]};
         push (@saida, $saidaString);

         #<PERL><COMENTARIO>#caso especial: final de texto sem puntuaçao

        if ($i == $#tokens && $tokens[$i] ne "\.") {
	   $saidaString = "<blank> <blank> Fp";
           push (@saida, $saidaString);
        }


        $Tag{$tokens[$i]} = "";
        
        if($adiantar>0){
	        $i += $adiantar;
        }
        #<PERL><COMENTARIO>$i += $adiantar if ($adiantar); #<PERL><COMENTARIO>#adiantar o contador se foram encontradas expressoes compostas
        #<PERL><COMENTARIO><PERL><END>
     }

  return @saida;
}


#<PERL><COMENTARIO>##OUTRAS FUNÇOES

sub punct {
   my ($p) = @_ ;
   my $result;
  
   if ($p eq "\.") {
         $result = "Fp"; 
   }
   elsif ($p eq "\,") {
         $result = "Fc"; 
   }
   elsif ($p eq "\:") {
         $result = "Fd"; 
   }
   elsif ($p eq "\;") {
         $result = "Fx"; 
   }
   elsif ($p =~ /^(\-|\-\-)$/) {
         $result = "Fg"; 
   } 
   elsif ($p =~ /^(\'|\"|\`\`|\'\')$/) {
         $result = "Fe"; 
  }
  elsif ($p eq "\.\.\.") {
         $result = "Fs"; 
   }
  elsif ($p =~ /^(\<\<|«|\“)/) {
         $result = "Fra"; 
  }
   elsif ($p =~ /^(\>\>|»|\”)/) {
         $result = "Frc"; 
  }
  elsif ($p eq "\%") {
         $result = "Ft"; 
  }
  elsif ($p =~ /^(\/|\\)$/) {
         $result = "Fh"; 
  }
  elsif ($p eq "\(") {
         $result = "Fpa"; 
  }
  elsif ($p eq "\)") {
         $result = "Fpt"; 
  }
  elsif ($p eq "\¿") {
         $result = "Fia"; 
  } 
  elsif ($p eq "\?") {
         $result = "Fit"; 
  }
   elsif ($p eq "\¡") {
         $result = "Faa"; 
  }
  elsif ($p eq "\!") {
         $result = "Fat"; 
  }
  elsif ($p eq "\[") {
         $result = "Fca"; 
  } 
  elsif ($p eq "\]") {
         $result = "Fct"; 
  }
  elsif ($p eq "\{") {
         $result = "Fla"; 
  } 
  elsif ($p eq "\}") {
         $result = "Flt"; 
  }
  elsif ($p eq "\…") {
         $result = "Fz"; 
  }

  return $result;
}


sub lowercase {
  my ($x) = @_ ;
  $x = lc ($x);
  $x =~  tr/ÁÉÍÓÚÇÑ/áéíóúçñ/;

  return $x;

} 
sub Trim {
  my ($x) = @_ ;

  $x =~ s/^[\s]*//;  
  $x =~ s/[\s]$//;  

  return $x
}
       
