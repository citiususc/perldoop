#!/bin/bash

rm -R ./JavaTranslatedCode/*
rm -R ./JavaGeneratedClasses/*
rm -R ./JavaProgram/Prolnat.jar

cp -R ./JavaTemplates/* ./JavaTranslatedCode/

echo '[OPTIONS]' > ../../src/config.txt
echo 'secuencial=false' >> ../../src/config.txt
echo 'hadoop=true' >> ../../src/config.txt

( cd ../../src/ ; python Perldoop.py ../applications/NLP/Perl/Modules/ner-es.perl ../applications/NLP/JavaTemplates/NER.java > ../applications/NLP/JavaTranslatedCode/NER.java )
( cd ../../src/ ; python Perldoop.py ../applications/NLP/Perl/Modules/tagger-es.perl ../applications/NLP/JavaTemplates/Tagger.java > ../applications/NLP/JavaTranslatedCode/Tagger.java )
( cd ../../src/ ; python Perldoop.py ../applications/NLP/Perl/Modules/nec-es.perl ../applications/NLP/JavaTemplates/NEC.java > ../applications/NLP/JavaTranslatedCode/NEC.java )

javac -d ./JavaGeneratedClasses/ ./JavaTranslatedCode/jregex/*.java

mkdir ./JavaGeneratedClasses/jregex/
mkdir ./JavaGeneratedClasses/jregex/util/
mkdir ./JavaGeneratedClasses/jregex/util/io/

javac -cp ./JavaGeneratedClasses/ -d ./JavaGeneratedClasses/ ./JavaTranslatedCode/jregex/util/io/*.java
javac -cp ./JavaTranslatedCode/lib/*:. -d ./JavaGeneratedClasses/ ./JavaTranslatedCode/*.java

#( cd JavaExit ; jar cfe ../Programa/Prolnat.jar ProlnatSecuencial ./* )
( cd JavaGeneratedClasses ; jar cfe ../JavaProgram/Prolnat.jar Prolnat ./* )

