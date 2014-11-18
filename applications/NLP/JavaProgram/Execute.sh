#!/bin/bash

hadoop jar Prolnat.jar -archives /home/josemanuel.abuin/PLN/PerldoopV0.6.2.0/Programa/Diccionarios.zip -D mapreduce.job.maps=32 -D mapreduce.map.memory.mb=1280 -D mapreduce.input.fileinputformat.split.maxsize=71303168 Wikipedias/WikipediaPlain.txt saidaWikipediaPlain
