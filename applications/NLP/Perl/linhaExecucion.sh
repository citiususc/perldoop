#!/bin/bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -file /home/hduser/Perl/ner-es_exe.perl -mapper /home/hduser/Perl/ner-es_exe.perl -input /home/hduser/Perl/la_regenta.txt.txt -output /home/hduser/saidaRegenta

#En Amazon====================================================
hdfs dfs -copyFromLocal /mnt/tmp/eswiki-latest-pages-articles.xml /eswiki-latest-pages-articles.xml

hadoop jar /home/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -file /home/hadoop/PLN/* -file /home/hadoop/PLN/model/* -file /home/hadoop/PLN/lexicon/* -file /home/hadoop/PLN/Modules/* -mapper /home/hadoop/PLN/prolnat-ner-es.perl -reducer NONE -input /WikipediaPlain.txt -output /saidaPlain2

hadoop jar /home/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -inputreader "StreamXmlRecordReader,begin=<doc>,end=</doc>" -file /home/hadoop/PLN/* -file /home/hadoop/PLN/model/* -file /home/hadoop/PLN/lexicon/* -file /home/hadoop/PLN/Modules/* -mapper /home/hadoop/PLN/prolnat-ner-es.perl -reducer NONE -input /WikipediaDoc.xml -output /saidaXML

[hadoop@ip-10-65-53-253 PLN]$ hadoop jar /home/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -D mapreduce.job.maps=64 -D mapreduce.map.memory.mb=3072 -file /home/hadoop/PLN/* -file /home/hadoop/PLN/model/* -file /home/hadoop/PLN/lexicon/* -file /home/hadoop/PLN/Modules/* -mapper /home/hadoop/PLN/prolnat-ner-es.perl -reducer NONE -input /WikipediaPlain.txt -output /saidaPlain

#TreeTagger Amazon
hadoop jar /home/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -file /home/hadoop/PLN/TreeTagger/* -file /home/hadoop/PLN/TreeTagger/bin/* -file /home/hadoop/PLN/TreeTagger/cmd/* -file /home/hadoop/PLN/TreeTagger/doc/* -file /home/hadoop/PLN/TreeTagger/lib/* -file /home/hadoop/PLN/TreeTagger/parsers/* -mapper execucion.sh -reducer NONE -input /WikipediaPlainEN.txt -output /saidaWikipediaPlainEN

#TreeTagger local

hadoop jar /home/chema/Software/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -file /home/chema/Software/PLN/TreeTagger/* -file /home/chema/Software/PLN/TreeTagger/bin/* -file /home/chema/Software/PLN/TreeTagger/cmd/* -file /home/chema/Software/PLN/TreeTagger/doc/* -file /home/chema/Software/PLN/TreeTagger/lib/* -file /home/chema/Software/PLN/TreeTagger/parsers/* -mapper execucion.sh -reducer NONE -input /WikipediaPlainEN300.txt -output /saidaWikipediaPlainEN300

#En Amazon====================================================

#Singlenode local PC==================================================
chema@debian:~/Software/PLN/Exemplos/Perl$ hadoop jar /home/chema/Software/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -file /home/chema/Software/PLN/Exemplos/Perl/* -file /home/chema/Software/PLN/Exemplos/Perl/model/* -file /home/chema/Software/PLN/Exemplos/Perl/lexicon/* -file /home/chema/Software/PLN/Exemplos/Perl/Modules/* -mapper /home/chema/Software/PLN/Exemplos/Perl/prolnat-ner-es.perl -reducer NONE -input /WikipediaPlain.txt -output /saidaWikipediaPlain

hadoop jar /home/chema/Software/PLN/JavaJar/Prolnat.jar -files /home/chema/Software/PLN/Exemplos/Perl/,/home/chema/Software/PLN/Exemplos/Perl/model/,/home/chema/Software/PLN/Exemplos/Perl/lexicon/,/home/chema/Software/PLN/Exemplos/Perl/Modules/ /regenta.txt /saidaRegenta.txt

hadoop jar /home/chema/Software/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -file /home/chema/Software/PLN/TreeTagger/* -file /home/chema/Software/PLN/TreeTagger/bin/* -file /home/chema/Software/PLN/TreeTagger/cmd/* -file /home/chema/Software/PLN/TreeTagger/doc/* -file /home/chema/Software/PLN/TreeTagger/lib/* -file /home/chema/Software/PLN/TreeTagger/parsers/* -mapper /home/chema/Software/PLN/TreeTagger/execucion.sh -reducer NONE -input /WikipediaPlain.txt -output /saidaWikipediaPlainTT
#Singlenode local PC==================================================

#Singlenode local Portatil
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar -file /home/chema/Dropbox/USC/Tesis/Codigo/PNL/Exemplos/Perl/* -file /home/chema/Dropbox/USC/Tesis/Codigo/PNL/Exemplos/Perl/model/* -file /home/chema/Dropbox/USC/Tesis/Codigo/PNL/Exemplos/Perl/lexicon/* -file /home/chema/Dropbox/USC/Tesis/Codigo/PNL/Exemplos/Perl/Modules/* -mapper /home/chema/Dropbox/USC/Tesis/Codigo/PNL/Exemplos/Perl/ner-es_exe.perl -reducer NONE -input /libros.tar -output /saidaLibros
