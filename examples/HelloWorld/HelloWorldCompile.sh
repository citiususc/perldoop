#!/bin/bash

rm -R ./JavaTranslatedCode/*
rm -R ./JavaGeneratedClasses/*

cp -R ./JavaTemplates/* ./JavaTranslatedCode/

echo '[OPTIONS]' > ../../src/config.txt
echo 'secuencial=true' >> ../../src/config.txt
echo 'hadoop=false' >> ../../src/config.txt

( cd ../../src/ ; python Perldoop.py ../examples/HelloWorld/Perl/HelloWorld.pl ../examples/HelloWorld/JavaTemplates/HelloWorld.java > ../examples/HelloWorld/JavaTranslatedCode/HelloWorld.java )

javac -cp . -d ./JavaGeneratedClasses/ ./JavaTranslatedCode/*.java

( cd JavaGeneratedClasses ; jar cfe ../JavaProgram/HelloWorld.jar HelloWorld ./* )
