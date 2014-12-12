#!/bin/bash

if [ "$(ls -A ./JavaTranslatedCode/)" ]; then
     rm -R ./JavaTranslatedCode/*
fi

if [ "$(ls -A ./JavaGeneratedClasses/)" ]; then
     rm -R ./JavaGeneratedClasses/*
fi

if [ -f "./JavaProgram/Prolnat.jar" ]; then
	rm -R ./JavaProgram/Prolnat.jar
fi

cp -R ./JavaTemplates/* ./JavaTranslatedCode/

echo '[OPTIONS]' > ../../src/config.txt
echo 'secuencial=false' >> ../../src/config.txt
echo 'hadoop=true' >> ../../src/config.txt

( cd ../../src/ ; python Perldoop.py ../applications/NLP/Perl/Modules/ner-es.perl ../applications/NLP/JavaTemplates/NER.java > ../applications/NLP/JavaTranslatedCode/NER.java )
( cd ../../src/ ; python Perldoop.py ../applications/NLP/Perl/Modules/tagger-es.perl ../applications/NLP/JavaTemplates/Tagger.java > ../applications/NLP/JavaTranslatedCode/Tagger.java )
( cd ../../src/ ; python Perldoop.py ../applications/NLP/Perl/Modules/nec-es.perl ../applications/NLP/JavaTemplates/NEC.java > ../applications/NLP/JavaTranslatedCode/NEC.java )

javac -d ./JavaGeneratedClasses/ -Xlint:none ./JavaTranslatedCode/jregex/*.java

if [ ! -d "./JavaGeneratedClasses/jregex/" ]; then
	mkdir ./JavaGeneratedClasses/jregex/
	mkdir ./JavaGeneratedClasses/jregex/util/
	mkdir ./JavaGeneratedClasses/jregex/util/io/
fi


javac -cp ./JavaGeneratedClasses/ -Xlint:none -d ./JavaGeneratedClasses/ ./JavaTranslatedCode/jregex/util/io/*.java
javac -cp ./JavaTranslatedCode/lib/*:. -Xlint:none -d ./JavaGeneratedClasses/ ./JavaTranslatedCode/*.java

#( cd JavaExit ; jar cfe ../Programa/Prolnat.jar ProlnatSecuencial ./* )
( cd JavaGeneratedClasses ; jar cfe ../JavaProgram/Prolnat.jar Prolnat ./* )

