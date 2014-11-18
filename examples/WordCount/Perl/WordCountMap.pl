#!/usr/bin/perl -w

#<perl><start>
my $line;			#<perl><var><string>
my @words;			#<perl><array><string>
my $key;			#<perl><var><string>
my $valueNum = "1";	#<perl><var><string>
my $val;			#<perl><var><string>


while ($line = <STDIN>) { #<perl><map>
	chomp ($line);
	@words = split (" ",$line);
	foreach my $w (@words) { 	#<perl><var><string>
		$key = $w."\t"; 		#<perl><var><key>
		$val = $valueNum."\n"; 	#<perl><var><value>
		
		print $key.$val;
	}
} #<perl><ignoreline>

#<perl><end>
