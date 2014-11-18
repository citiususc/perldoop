#!/usr/bin/perl -w

#<perl><start>
my $count = 0; #<perl><var><integer>
my $value; 	#<perl><var><integer>
my $newKey; 	#<perl><var><string>
my $newValue; 	#<perl><var><string>
my $oldkey; #<perl><var><string><null>
my $line;	#<perl><var><string>
my @keyValue; #<perl><array><string>

my $returnKey; #<perl><var><string>
my $returnValue; #<perl><var><string>

while ($line = <STDIN>) { #<perl><reduce>
	chomp ($line);
	($newKey, $newValue) = split ("\t",$line); #<perl><var><keyvalue>
	
	$value = $newValue; #<perl><cast><int>
		
	#<perl>Comentario para reiniciar o tipo de variable
		
	if (!(defined($oldkey))) {
	    $oldkey = $newKey;
	    $count  = $value;
	}
	else {
	    if ($oldkey eq $newKey) {
			$count = $count + $value;
	    } 
	    else {
	    
	    	$returnKey = $oldkey."\t"; #<perl><var><key>
	    	
	    	$returnValue = $count; #<perl><cast><string>
			$returnValue = $returnValue."\n"; #<perl><var><value>
	    	
			print $returnKey.$returnValue;
			
			$oldkey = $newKey;
			$count  = $value;
	    }
	}
}

$returnKey = $oldkey."\t"; #<perl><var><key>

$returnValue = $count; #<perl><cast><string>
$returnValue = $returnValue."\n"; #<perl><var><value>

print $returnKey.$returnValue;
#<perl><end>
