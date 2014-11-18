#!/bin/bash

rm -R ./JavaTranslatedCode/*
rm -R ./JavaGeneratedClasses/*

cp -R ./JavaTemplates/* ./JavaTranslatedCode/

( cd ../../src/ ; python Perldoop.py ../examples/WordCount/Perl/WordCountMap.pl ../examples/WordCount/JavaTemplates/WordCountMap.java > ../examples/WordCount/JavaTranslatedCode/WordCountMap.java )
( cd ../../src/ ; python Perldoop.py ../examples/WordCount/Perl/WordCountReducer.pl ../examples/WordCount/JavaTemplates/WordCountReducer.java > ../examples/WordCount/JavaTranslatedCode/WordCountReducer.java )

javac -cp ./JavaTranslatedCode/lib/*:. -d ./JavaGeneratedClasses/ ./JavaTranslatedCode/*.java

( cd JavaGeneratedClasses ; jar cfe ../JavaProgram/WordCount.jar WordCount ./* )
