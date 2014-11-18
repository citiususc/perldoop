#!/usr/bin/perl

#<PERL><COMENTARIO>#ProLNat NEC (provided with Sentence Identifier, Tokenizer, Splitter, NER, Tagger)
#<PERL><COMENTARIO>#autor: Grupo ProLNat@GE, CITIUS
#<PERL><COMENTARIO>#Universidade de Santiago de Compostela


#<PERL><COMENTARIO># Script que integra 6 funçoes perl: sentences, tokens, splitter, ner_es, tagger e nec_es

use strict; 
binmode STDIN, ':utf8';
binmode STDOUT, ':utf8';
use utf8;

#<PERL><COMENTARIO># Absolute path 
use Cwd 'abs_path';
use File::Basename;
my $abs_path = dirname(abs_path($0));


#<PERL><COMENTARIO>##gazeetters
open (GAZLOC, $abs_path."/gaz/gazLOC.dat" ) or die "O ficheiro nao pode ser aberto: $!\n";
binmode GAZLOC,  ':utf8';
open (GAZPER, $abs_path."/gaz/gazPER.dat" ) or die "O ficheiro nao pode ser aberto: $!\n";
binmode GAZPER,  ':utf8';
open (GAZORG, $abs_path."/gaz/gazORG.dat" ) or die "O ficheiro nao pode ser aberto: $!\n";
binmode GAZORG,  ':utf8';
open (GAZMISC, $abs_path."/gaz/gazMISC.dat" ) or die "O ficheiro nao pode ser aberto: $!\n";
binmode GAZMISC,  ':utf8';

#<PERL><COMENTARIO>##triggerwords
open (TWLOC,  $abs_path."/tw/twLOC.dat") or die "O ficheiro nao pode ser aberto: $!\n";
binmode TWLOC,  ':utf8' ;
open (TWPER, $abs_path."/tw/twPER.dat" ) or die "O ficheiro nao pode ser aberto: $!\n";
binmode TWPER,  ':utf8';
open (TWORG, $abs_path."/tw/twORG.dat" ) or die "O ficheiro nao pode ser aberto: $!\n";
binmode TWORG,  ':utf8';
open (TWMISC, $abs_path."/tw/twMISC.dat" ) or die "O ficheiro nao pode ser aberto: $!\n";
binmode TWMISC,  ':utf8';




#<PERL><COMENTARIO>##variaveis globais 
my $Border = "(Fp|<blank>)";

#<PERL><COMENTARIO>####INFO DEPENDENTE DA LINGUA#############
my $stopwords = "_em_|_en_|_de_|_da_|_das_|_dos_|_da_|_do_|_del_|_o_|_a_|_e_|_por_|_para_|_and_|_the_|_in_|_on_|^el_|^la_|^las_|^los_"; ##CUIDADO COM ESTA VARIAVEL!!!!!!!!!!! hai que especializa-la por lingua
my $prep = "de|por|para"; 
my $titulo = "señor|señora|señorita|señorito|don|doña";
##########################################


#<PERL><COMENTARIO>##Cargando gazeetters e triggerwords e mais variaveis globais
my %TwLoc;
my %TwOrg;
my %TwMisc;
my %TwPer;
my %GazLoc;
my %GazOrg;
my %GazMisc;
my %GazPer;
my %GazPer_part;


while (my $NP = <GAZLOC>) {
 chomp $NP;
 $GazLoc{$NP}++;
}


while (my $NP = <GAZPER>) {
 my %found;
 my @temp;

 chomp $NP;
 $GazPer{$NP}++;

 if ($NP =~ /_/ && $NP !~ /$stopwords/) {
  my @temp = split ("_", $NP);
  for (my $i=0;$i<=$#temp;$i++) {
      my $part = $temp[$i];
      if (!$found{$part} ) {
	 #print  "$part\n";
        $GazPer_part{$part} = $NP;
        $found{$part}++;
      }
   }
 }

}

while (my $NP = <GAZORG>) {
 chomp $NP;
 $GazOrg{$NP}++;
}

while (my $NP = <GAZMISC>) {
 chomp $NP;
 $GazMisc{$NP}++;
}

while (my $NP = <TWLOC>) {
chomp $NP;
$TwLoc{$NP}++;
}

while (my $NP = <TWPER>) {
 chomp $NP;
 $TwPer{$NP}++;
}

while (my $NP = <TWORG>) {
 chomp $NP;
 $TwOrg{$NP}++;
}

while (my $NP = <TWMISC>) {
 chomp $NP;
 $TwMisc{$NP}++;
}

 
sub nec_es {
  my (@text) = @_ ;
  my $saida;
  my @saida;

  my $Window=3; #<PERL><COMENTARIO>##para as triggerwords
  my $last_tag="",
  my $new_tag="";
  my $i=0;;
  my $token;
  my $lema;
  my $tag;
 #<PERL><COMENTARIO># my $prob;
  my @Token;
  my @Lema;
  my @Tag;
  my @Others; #<PERL><COMENTARIO># a remover
  my @composto;
  my $left;
  my $Left_1;
  my $Left_2;
  my $right;
  my $others; #<PERL><COMENTARIO>#a remover
  

 #<PERL><COMENTARIO># (my @line) = split ('\n', $texto);
  foreach my $line (@text) {
   chomp $line;
   if ($line ne "") {
 
    (my @array) = split (" ", $line);
    $token = $array[0];
    $lema = $array[1];
    $tag = $array[2];
    for (my $k=3;$k<=$#array;$k++) { #<PERL><COMENTARIO>##esta parte tera que ser removida se hai desambiguaçao previa
       $others .= $array[$k] .  " ";  
    }
    
    if ($tag !~ /^$Border$/) {
       $Token[$i] = $token;
       $Lema[$i] = $lema;
       $Tag[$i] = $tag;
       $Others[$i] = $others;
       $i++;
       $others="";
    }
  
    else {
       
     for ($i=0;$i<=$#Lema;$i++) {
         my $found=0;        
         #<PERL><COMENTARIO># print STDERR "okk:: #$i# ----------- #$Tag[$i]#\n";

         #<PERL><COMENTARIO>###Caso 'don+NP': todos person
          if ($Lema[$i] =~ /^($titulo)$/ && $Tag[$i+1] =~ /^NP/) {
               $new_tag =  "NP00SP0";
               $Token[$i] =  $Token[$i] . "_" .  $Token[$i+1];
               $Lema[$i] =  $Lema[$i] . "_" .  $Lema[$i+1];
               print "$Token[$i] $Lema[$i] $new_tag\n";
               $found=1;
               $i+=1;
               next;
	  }
 

	 if ($Tag[$i] =~ /^NP/ && !$found) {
         #<PERL><COMENTARIO>#  print STDERR "okk:: #$i# #$Lema[$i]#\n";
           
           #<PERL><COMENTARIO>#if (defined $meses{$Lema[$i]}) {
	    #<PERL><COMENTARIO>#  $new_tag =  "NP00V00";
            #<PERL><COMENTARIO>#  print "$Token[$i] $Lema[$i] $new_tag\n";
            #<PERL><COMENTARIO>#  $found=1;
           #<PERL><COMENTARIO>#}

           #<PERL><COMENTARIO>## buscar NPs nao ambiguos nos gazetteers 
           if (!Ambiguous ($Lema[$i]) &&  Gaz ($Lema[$i]) ) {
               $new_tag = Gaz ($Lema[$i]);
               print "$Token[$i] $Lema[$i] $new_tag\n";
               $found=1;
	   }

           #<PERL><COMENTARIO>##buscar NPs que coincidem com os triggers:
           elsif (Tw ($Lema[$i]) ) {
               $new_tag = Tw ($Lema[$i]);
               print "$Token[$i] $Lema[$i] $new_tag\n";
               $found=1;
	       #<PERL><COMENTARIO>#print STDERR "okkk\n";
	   }
         
           #<PERL><COMENTARIO>##buscar NPs missing ou ambiguos
           elsif (Missing ($Lema[$i]) || Ambiguous ($Lema[$i]) )  {
               # print STDERR "okk:: #$i# #$Lema[$i]#\n";
	       @composto = split ("_", $Lema[$i]);             

               #<PERL><COMENTARIO>##se o NP é PER, é composto e esta Missing ou é ambiguo, e a primeira parte é uma parte dum trigger PER ("Presidente Zapatero" ... - presidente)
	       if ( ( (Ambiguous ($Lema[$i]) && defined $GazPer{$Lema[$i]}) || Missing ($Lema[$i]) ) && defined $TwPer{$composto[0]} ) {
                   $new_tag =  "NP00SP0";
                   $found=1;
	           print "$Token[$i] $Lema[$i] $new_tag\n";
                }   
               elsif ( ( (Ambiguous ($Lema[$i]) && defined $GazOrg{$Lema[$i]})  || Missing ($Lema[$i]) ) && defined $TwOrg{$composto[0]} ) {
                   $new_tag =  "NP00O00";
                   $found=1;
	           print "$Token[$i] $Lema[$i] $new_tag\n";
                }   
               elsif ( ( (Ambiguous ($Lema[$i]) && defined $GazLoc{$Lema[$i]})  || Missing ($Lema[$i]) ) && defined $TwLoc{$composto[0]} ) {
                    #<PERL><COMENTARIO>#print "OKKKKKKKK $Lema[$i]  $composto[0]\n";
                   $new_tag =  "NP00G00";
                   $found=1;
	           print "$Token[$i] $Lema[$i] $new_tag\n";
                   
                }  

               elsif ( ( (Ambiguous ($Lema[$i]) && defined $GazMisc{$Lema[$i]})  || Missing ($Lema[$i]) ) && defined $TwMisc{$composto[0]} ) {
                   #<PERL><COMENTARIO>#print "OKKKKKKKK $Lema[$i]  $composto[0]\n";
                   $new_tag =  "NP00V00";
                   $found=1;#<PERL><COMENTARIO>
	           print "$Token[$i] $Lema[$i] $new_tag\n";
                   
                }  

             	     
               #<PERL><COMENTARIO>##se o NP é PER, é composto e esta Missing, e a primeira parte é uma parte dum gazeteeiro composto (Pablo Gamallo - Pablo Picasso)
	       elsif  ( ( (Ambiguous ($Lema[$i]) && defined $GazPer{$Lema[$i]}) || Missing ($Lema[$i]) ) && defined $GazPer_part{$composto[0]}) {
                   $new_tag =  "NP00SP0";
                   print "$Token[$i] $Lema[$i] $new_tag\n";
                   $found=1;
               } 

               #<PERL><COMENTARIO>###buscar NPs entre aspas que passam a ser MISC
	       elsif  ( (Ambiguous ($Lema[$i]) || Missing ($Lema[$i]) )   && $Lema[$i-1]  =~  /^[\"\“\«\']/ &&  $Lema[$i+1]  =~  /[\"\»\”\']/ ) {
                   $new_tag =  "NP00V00";
                   print "$Token[$i] $Lema[$i] $new_tag\n";
                   $found=1;
	       }

             #<PERL><COMENTARIO>##buscar os contextos (triggers) de  NPs (compostos ou nao) que estao missing ou que sao ambiguos 
	       else {
		my $j;
               #<PERL><COMENTARIO>##buscar nos triggerwords (on the left)
                if ($i > 0) {
	         $left = $i - $Window;
                 #<PERL><COMENTARIO>##para impedir presidente de a  Seat##
	         $Left_1 = $i-1;
                 $Left_2 = $i-2;
                 #<PERL><COMENTARIO>##############
                 for ($j=$left;$j<=$i;$j++) {
                   #<PERL><COMENTARIO>#print STDERR "LEFT:: #$j# #$left# -- $Lema[$i]--$Lema[$j]\n";

		   if (Trigger ($j, $Left_1, $Left_2, @Lema) && !$found) {
                     
                     $found=1;
                     $new_tag = Trigger ($j, $Left_1, $Left_2, @Lema) ;
                   
               	     print "$Token[$i] $Lema[$i] $new_tag\n";
                     #<PERL><COMENTARIO>#print STDERR "TRIGGER-LEFT ---- $Token[$i] $Lema[$i] $new_tag \n";
		   }
                 }
	       }

               #<PERL><COMENTARIO>##buscar nos triggerwords (on the right)
              if (!$found) {

                #<PERL><COMENTARIO>##aqui nao interessa o valor de Left_1 e Left_2 porque nao buscamos preps. Na nova versao fazer dous Trigger: trigger-right e trigger-left
		$Left_1=$i; 
       	        $Left_2=$i;

                $right = $i + $Window;
                for ($j=$i;$j<=$right;$j++) {
                    #<PERL><COMENTARIO>#print STDERR "RIGHT:: #$j# #$left#\n";
                   if ($j <= $#Lema) {
		    if (Trigger ($j, $Left_1, $Left_2, @Lema) && !$found ) {
                     
                     $found=1;
                     $new_tag = Trigger ($j, $Left_1, $Left_2, @Lema) ;
        	     print "$Token[$i] $Lema[$i] $new_tag\n";
                     #<PERL><COMENTARIO>#print STDERR "TRIGGER-RIGHT ---- $Token[$i] $Lema[$i] $new_tag \n";
		   }
		  }
	        }
	     }
	    }
	 } #<PERL><COMENTARIO>##missing ou ambiguous

              #<PERL><COMENTARIO>##se o NP é ambiguo (mas nao missing), e nao tem triggers nos contextos nem partes nos triggers nem nos gazetteers, entao desambiguamos
        if (!$found && (Ambiguous ($Lema[$i]) ) ) {      
		 $new_tag = Disambiguation ($Lema[$i]);
                 print "$Token[$i] $Lema[$i] $new_tag\n";
                 $found=1;
	}

        #<PERL><COMENTARIO>##finalmente, se esta totalmente missing:
        elsif (!$found) {
                 #print "$Token[$i] $Lema[$i] NP00V00\n";
                 $new_tag = DisambiguationAdHoc ($Lema[$i]);
                 print "$Token[$i] $Lema[$i] $new_tag\n";
                 #<PERL><COMENTARIO>#print STDERR "DISAMB AD HOC ---- $Token[$i] $Lema[$i] $new_tag \n";
                 $found=1;
                 
	}
             
       $last_tag = $new_tag if ($found);
      } #<PERL><COMENTARIO>#end NPs

          	  
           
            #<PERL><COMENTARIO>##finalmente, se esta totalmente missing (nao vale para nada: ja foi tomado em conta...)
          #<PERL><COMENTARIO>## else {
              #<PERL><COMENTARIO># #print "OKKKKKKKK$Token[$i] $Lema[$i] NP00V00\n";
	  #<PERL><COMENTARIO># }
      
     

      else { 
          if ($Others[$i]) {
	    print "$Token[$i] $Lema[$i] $Tag[$i] $Others[$i]\n" ; ##a remover
	  }
          else {
	      print "$Token[$i] $Lema[$i] $Tag[$i]\n";
	  }
      }

    }
    print "\. \. Fp\n\n";
    for ($i=0;$i<=$#Lema;$i++) {
	 delete $Lema[$i];
         delete $Token[$i];
         delete $Tag[$i];
         delete $Others[$i];
    }
    $new_tag="";
    $i=0;
   }
  }
 }
}


#<PERL><COMENTARIO>##FUNÇOES DEPENDENTES DE nec_es
sub Missing {

    my ($x) = @_ ;

    if (!defined $GazLoc{$x} && !defined $GazPer{$x} && !defined $GazOrg{$x} && !defined $GazMisc{$x}) {
         
        return 1
   }

   else {
       return 0
   }

}


sub Ambiguous {

    my ($x) = @_ ;

    if ( 
       (defined $GazLoc{$x} && defined $GazPer{$x}) || 
       (defined $GazLoc{$x} && defined $GazOrg{$x}) ||
       (defined $GazPer{$x} && defined $GazOrg{$x}) ||
       (defined $GazLoc{$x} && defined $GazMisc{$x}) ||
       (defined $GazPer{$x} && defined $GazMisc{$x}) ||
       (defined $GazOrg{$x} && defined $GazMisc{$x})
       ) {
         
        return 1
   }

   else {
       return 0
   }
}

sub Disambiguation {

    my ($x) = @_ ;
    my $result;

    if (defined $GazLoc{$x} && defined $GazPer{$x}) {
           $result = "NP00SP0";
    }
    elsif  (defined $GazLoc{$x} && defined $GazOrg{$x}) {
          $result = "NP00G00";
    }
    elsif  (defined $GazPer{$x} && defined $GazOrg{$x}) {
	$result = "NP00SP0";
    }
    elsif  (defined $GazPer{$x} && defined $GazMisc{$x}) {
	$result = "NP00SP0";
    }
    elsif  (defined $GazOrg{$x} && defined $GazMisc{$x}) {
	$result = "NP00O00";
    }
    elsif  (defined $GazLoc{$x} && defined $GazMisc{$x}) {
	$result = "NP00G00";
    }
    else {
         $result = "NP00SP0";
     }

    return $result;
}


sub Trigger {
   my ($x,$L1,$L2,@x) = @_ ;
   my $result;
    #<PERL><COMENTARIO>#print STDERR "okk:: #$x# #$x[$x]#  -- #$x[$L1] -- #$x[$L2]##\n";
   if (!$x[$x]) {
       	$result = 0;
   }
    
   else {
    
    if ($TwLoc{$x[$x]}  || $x[$L2] =~ /^(en|em|in)$/) {

       $result = "NP00G00";
    } 

    elsif ($TwPer{$x[$x]} && ##) { 
          $x[$L1] !~ /^($prep)$/ && $x[$L2] !~ /^($prep)$/ ) {
           #<PERL><COMENTARIO>#print STDERR "okk:: #$x# #$x[$x]# #$x[$L1]# \n";
          $result = "NP00SP0";
    }  
    
    elsif ($TwOrg{$x[$x]} ) {
       $result = "NP00O00";
    } 

    elsif ($TwMisc{$x[$x]} ) {
       $result = "NP00V00";
    } 

    else {
	$result = 0;
    }
   }


    return $result;
   
  
}


sub Gaz {
    my ($x) = @_ ;
    my $result;

    #<PERL><COMENTARIO>#print STDERR "okk:: #$j# #$x#\n";
    if ($GazLoc{$x} ) {
       $result = "NP00G00";
    } 

    elsif ($GazPer{$x} ) {
       $result = "NP00SP0";
    }  
    
    elsif ($GazOrg{$x} ) {
       $result = "NP00O00";
    } 

    elsif ($GazMisc{$x} ) {
       $result = "NP00V00";
    } 

    else {
	$result = 0;
    }


    return $result;
   
  
}

sub Tw {

    my ($x) = @_ ;
    my $result;

    #<PERL><COMENTARIO>#print STDERR "okk:: #$j# #$x#\n";
    if (defined $TwLoc{$x} ) {
       $result = "NP00G00";
    } 

    elsif (defined $TwPer{$x} ) {
       $result = "NP00SP0";
    }  
    
    elsif (defined $TwOrg{$x} ) {
       $result = "NP00O00";
    } 

    elsif (defined $TwMisc{$x} ) {
       $result = "NP00V00";
    }

    else {
	$result = 0;
    }

    return $result;
   
}

sub DisambiguationAdHoc {

    my ($x) = @_ ;
    my $result;
    
 #<PERL><COMENTARIO>#   if (AllUpper ($x) || $x !~ /_/)  {
    if (AllUpper ($x) ) {
	$result = "NP00O00";
    }
     
    else {  
	$result = "NP00O00";
        #$result = $last_tag;
   }
    #<PERL><COMENTARIO>#print STDERR "Ultimo recurso: #$x# -- $result\n";
    return $result;
}


sub AllUpper {
    my ($l) = @_;
    my $countletters=0;
    my $result;

    my @string = split ("", $l) ;
    
    foreach my $letter (@string) {
	if ($letter =~ /[A-ZÁÉÍÓÚÑÇ]/) {
          $countletters++;
        }
    }
    if ( $countletters >= $#string ) {
	$result = 1;
    }
    else {
	$result = 0 ;
    }

    #<PERL><COMENTARIO>#print STDERR "OKKKK $l -- #$countletters# #$#string#-- \n";
    return $result;
}


