# HelloWorld #

Here you can find a full working **Perldoop** example. In this case we are talking about the HelloWorld example.
To build these example you can just run the `HelloWorldCompile.sh` bash script, and it will do all the work for you. The generated files are organized as follows:

* _JavaTemplates_ This is where Java templates are stored. You don't need to modify these files, they are used by **Perldoop** to create the final Java codes.
* _JavaTranslatedCode_ Here is where the automatically generated Java source code is stored.
* _JavaGeneratedClasses_ In this directory is where the `HelloWorldCompile.sh` stores the .class files.
* _JavaProgram_ And here is where the final .jar file is stored. This file is the one you can run in Java.
* _Perl_ The original Perl source code.

To clean all the generated files, you can use the `Clean.sh` script.

To run this example you need to change the contents of the `/src/config.txt` file and put the options as follows:

* secuencial=true
* hadoop=false

This example is compiled and has been tested by using Hadoop 2.2.0.
