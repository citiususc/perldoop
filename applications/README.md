# What's in this directory? #

Here you can find some applications we have tested with **Perldoop**. Nowadays the available applications are:

* **NLP**. Natural Language Processing tools. The current version includes three natural language processing modules written in Perl. In particular, the modules process plain text to perform the following tasks: **Named Entity Recognition** (NER), **Part-of-Speech Tagging** and **Named Entity Classification** (NEC). All the modules process text in Spanish language. In the NLP directory, the NLP-Compile.sh bash script translates the Perl modules using Perldoop and compiles the Java applications to execute them on a Hadoop cluster. The script contains the commands to use the jregex library in the compilation of the Java codes. The resulting jar file executes all the modules in order, that is, NER, Tagger and NEC.

All the applications are compiled and have been tested by using Hadoop 2.2.0.
