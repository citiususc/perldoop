#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright 2014 José Manuel Abuín Mosquera <josemanuel.abuin@usc.es>
#
#This file is part of Perldoop.
#
#Perldoop is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Perldoop is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Perldoop.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import re

from Status import *

#Automata function
def procesaLinha(linha):

	if(getComentario().replace("\n","") == ignoreLine):
		return ''

	#Perl code followed by comment
	expresionComentario = re.compile(r'^([\w\W\d ]*)([\#]+)'+comentarioLinha+'[\s]*([\w\W\d ]*)$').match(linha)

	#variable assign to: operation, concatenations...
	
	expresionAsignacionVariableParentese = re.compile(r'^[\s]*[\(]{1}[\s]*(my){0,1}[\s]*[\$@]{0,1}([\w]+[\w\d\W]*)[\s]*[\)]{1}[\s ]*(={1})[\s]*([\w\W\d]+)[\s]*(;)').match(linha)
	
	expresionAsignacionVariable = re.compile(r'^[\s]*[\(]{0,1}[\s]*(my){0,1}[\s]*[\$@]{0,1}([\w]+[\w\d\W]*)[\s]*[\)]{0,1}[\s ]*(={1})[\s ]*([\w\W\d]+)[\s]*(;){1}').match(linha)
	
	expresionAsignacionVariableSenPuntoComa = re.compile(r'^[\s]*[\(]{0,1}[\s]*(my){0,1}[\s]*[\$@]{0,1}([\w]+[\w\d\W]*)[\s]*[\)]{0,1}[\s ]*(={1})[\s ]*([\w\W\d]+)[\s]*').match(linha)
	
	expresionDeclaracionVariable = re.compile(r'^[\s]*[\(]{0,1}[\s]*(my){1}[\s]*[\$@]{1}([\w]+[\w\d\W]*)[\s]*[\)]{0,1}[\s]*(;){1}').match(linha)
	
	expresionDeclaracionHash = re.compile(r'^[\s]*[\(]{0,1}[\s]*(my){1}[\s]*[%]{1}([\w]+[\w\d\W]*)[\s]*[\)]{0,1}[\s]*(;){1}').match(linha)
	
	#Expressions of the type: if (Condition/s) {
	expresionIf = re.compile(r'^[\s]*(if|elsif)[\s]*([\(]{1})[\s]*([\w\d\W ]+)[\s]*([\)]{1})[\s]*(\{){0,1}').match(linha)
	
	#Expressions of the type: while (Condition/s)
	expresionWhile = re.compile(r'^[\s]*(while)[\s]*([\(]{1})[\s]*([\w\d\W ]+)[\s]*([\)]{1})[\s]*(\{){0,1}').match(linha)
	
	#Expresions do tipo for (Condicion/s)
	expresionFor = re.compile(r'[\s]*for[\s]*([\(]{1})[\s]*([\w\d\W ]+)[\s]*([\)]{1})[\s]*(\{){0,1}[\s]*').match(linha)
	
	#Expresions do tipo foreach (Condicion/s)
	#expresionForeach = re.compile(r'[\s]*foreach[\s]*([\(]{1})[\s]*([\w\d\W ]+)[\s]*([\)]{1})[\s]*(\{){0,1}[\s]*').match(linha)
	expresionForeach = re.compile(r'[\s]*foreach[\s]*[\s]*([\w\d\W ]+)[\s]*').match(linha)
	
	#Expresions do tipo for my $variable
	
	#Expresion de concatenacion de variables e strings
	expresionOperacionConcat = re.compile(r'^[\s]*[\$]{0,1}([\w\d\W]+)[\s]*([.]){1}[\s]*[\$]{0,1}([\w\d\W]+)[\s]*([;]{1})[\s]*').match(linha)
	
	#Expresion de operacion aritmetica
	expresionOperacion = re.compile(r'^[\s]*[\$]{0,1}([\w\d\W]+)[\s]*([+\-\*\/]){1}[\s]*[\$]{0,1}([\w\d\W]+)[\s]*([;]{1})[\s]*').match(linha)
	
	#Expresion regular
	expresionRegular = re.compile(r'^[\s]*[\$]*([\w\d_.\[\]\$]+)[\s]*(=[\s]*~)[\s]*([\w\d\W]]+)[\s]*').match(linha)
	
	#Expresion para insercion ou modificacion nunha taboa hash
	expresionHashAsignacion = re.compile(r'[\s]*[\$]{0,1}([\w]+[\w\d\W]*)[\{]([\w\d\W]+)[\}][\s]*[=]{1}[\s]*([\w\W\d]+)[\t\s]*(;)[\s]*').match(linha)
	
	#Idem pero para un hash con dobre key
	expresionHashAsignacionDoble = re.compile(r'[\s]*[\$]{0,1}([\w]+[\w\d\W]*)[\{]([\w\d\W]+)[\}][\{]([\w\d\W]+)[\}][\s]*[=]{1}[\s]*([\w\W\d]+)[\t\s]*(;)[\s]*').match(linha)
	
	#Expresion para procesar unha chamada a unha funcion
	expresionFuncion = re.compile(r'[\s]*([\w][\w\d_]*)[\s]*\([\s]*([\w\d\W]+)\)[\s]*([;]{1})[\s\t]*').match(linha)
	
	#Expresion que chama a unha funcion sen parenteses
	expresionFuncionSenParentese = re.compile(r'[\s]*(delete|undef|print)[\s]*([\w\d\W]+)[\s]*([;]{1})[\s]*').match(linha)
	
	#Expresion simbolo sencillo
	expresionSimbolo = re.compile(r'[\s]*([\W])[\s]*$').match(linha)
	
	#Expresion incremento
	expresionIncremento = re.compile(r'[\s]*[\$]{1}([\w]+[\w\d\W]*)([+]{2})[\s]*([;]{1})').match(linha)
	
	if(expresionComentario):
		

		comentario = expresionComentario.group(3).replace('\n','')

		if(comentario == inicioProcesadoPerl):
			setProcessingStatus(True)

			return ''
	
		if(comentario == finProcesadoPerl):
			setProcessingStatus(False)

			return ''
		
		if(comentario == headerInit):
			setReadingHeaderStatus(True)
			return ''
			
		if(comentario == headerEnd):
			setReadingHeaderStatus(False)
			return ''
	
	
	if(getReadingHeaderStatus()): #The header is been readed
		expresionOpcion = re.compile(r'[\s]*([\#]+)'+comentarioLinha+'([\w\d\W]+)[\s]*(=)[\s]*([\w\d\W]+)[\s]*').match(linha)
		
		if(getDebugMode()):
			print 'Reading header option :: '+linha
			
		nomeOpcion = ""
		valorOpcion = ""
		
		if (expresionOpcion):
			nomeOpcion = expresionOpcion.group(2)
			valorOpcion = expresionOpcion.group(4)
			
			#options[nomeOpcion] = valorOpcion
			setHeaderOption(nomeOpcion, valorOpcion)
			
			return ''
			
		else:
			print 'ERROR: Bad expression at header'
			return ''		
		
	if(getProcessingStatus()):

		if(getDebugMode()):
			print 'procesaLinha function :: '+linha
			
		if(expresionComentario):
			if(getDebugMode()):
				print 'Processing expression with comment :: '+expresionComentario.group(3)
			setComentario(expresionComentario.group(3))
			return procesaLinha(expresionComentario.group(1))

		#Condicional if
		elif(expresionIf):
			
			if(getDebugMode()):
				print 'procesaLinha function :: expresionIf :: '+expresionIf.group(0)
			
			
			if(expresionIf.group(1) == 'if'):
				cadeaDevolver = 'if ('+procesaInteriorIf(expresionIf.group(3))+') {'

			elif(expresionIf.group(1) == 'elsif'):
				cadeaDevolver = 'else if ('+procesaInteriorIf(expresionIf.group(3))+') {'
				
			else:
				cadeaDevolver = 'ERRoR'
			
			return cadeaDevolver
		
		elif(expresionWhile):
			
			cadeaDevolver = ""
			
			if(getDebugMode()):
				print 'procesaLinha function :: expresionWhile :: '+expresionWhile.group(0)
		
			if(not cadeaStdin in expresionWhile.group(3)):
			
				cadeaDevolver = 'while ('+procesaInteriorIf(expresionWhile.group(3))+') {'
			else:
			
				if(getDebugMode()):
					print 'procesaLinha function :: expresionWhile :: con STDIN'
			
				if(getConfigOption('hadoop')):

					if(getComentario()== mapStart):
					
						partesInternas = expresionWhile.group(3).split("=")
						cadeaDevolver = procesaVariable(partesInternas[0])+ " = value.toString();"
						
						return cadeaDevolver
						
					elif(getComentario()==reduceStart):
					
						partesInternas = expresionWhile.group(3).split("=")
						
						cadeaDevolver = "for (Text val : values) {\n"
						cadeaDevolver = cadeaDevolver + procesaVariable(partesInternas[0])+ " = val.toString();"
						return cadeaDevolver
						
				else:
					partesInternas = expresionWhile.group(3).split("=")
					cadeaDevolver = 'BufferedReader br = new BufferedReader(new InputStreamReader(System.in));\n'
					cadeaDevolver = cadeaDevolver + "while(("+procesaVariable(partesInternas[0])+"=br.readLine())!=null){"
					
					return cadeaDevolver
					
					
			return cadeaDevolver
		

		
		elif(expresionForeach):
		
			if(getDebugMode()):
				print 'procesaLinha function :: Procesando expresion de bucle FOREACH'
		
		
			cadeaDevolver = procesaInteriorForeach(linha)
		
			return cadeaDevolver
		
		elif(expresionFor):
		
			cadeaDevolver = ""
		
			if(getDebugMode()):
				print 'procesaLinha function :: Procesando expresion de bucle FOR'
		
			partesCondicionFor = expresionFor.group(2).split(";")
		
			if(len(partesCondicionFor)<3):
				
				if(".." in expresionFor.group(2)):
					
					indices = expresionFor.group(2).split("..")
				
					cadeaDevolver = "for (int varRangosFP = "+indices[0]+"; varRangosFP <="+indices[1]+";varRangosFP++) {"
					
				
				
			else:
		
				cadeaDevolver = 'for ('+procesaLinha(partesCondicionFor[0])+';'+procesaInteriorIf(partesCondicionFor[1])+';'+procesaLinha(partesCondicionFor[2])+') {'
		
			return cadeaDevolver
		
		elif(expresionFuncion):
		
			if(getDebugMode()):
				print 'procesaLinha function :: Procesando chamada a funcion'
			
			
			if(expresionFuncion.group(1) == 'lowercase'):
				return procesaVariable(expresionFuncion.group(2))+'.toLowerCase()'+expresionFuncion.group(3)
				
			elif(expresionFuncion.group(1) == 'chomp'):
				return procesaVariable(expresionFuncion.group(2))+' = '+procesaVariable(expresionFuncion.group(2))+".trim()"+expresionFuncion.group(3)
				
			elif(expresionFuncion.group(1) == 'lc'):#TODO: Change procesaVariable function and put the function that processes functions arguments instead.
				return procesaVariable(expresionFuncion.group(2))+'.toLowerCase()'+expresionFuncion.group(3)
				
			elif(expresionFuncion.group(1) == 'push'):
				partesPush = expresionFuncion.group(2).split(",")
				
				if(len(partesPush)==2):
					
					return partesPush[0].replace("@","")+".add("+procesaOperacion(partesPush[1])+");"
				else:
					return expresionFuncion.group(1)+' ('+procesaArgumentosFuncion(expresionFuncion.group(2))+')'+expresionFuncion.group(3)
			
			elif(expresionFuncion.group(1) == 'printf'):
			
				return "System.out.format("+procesaArgumentosFuncion(expresionFuncion.group(2))+')'+expresionFuncion.group(3)
			
			else:

				return expresionFuncion.group(1)+' ('+procesaArgumentosFuncion(expresionFuncion.group(2))+')'+expresionFuncion.group(3)
		
		
		#Assign to hash table with double key
		elif(expresionHashAsignacionDoble):
			if(getDebugMode()):
				print 'procesaLinha function :: Processing assign to hash table with double key'

			
			cadeaDevolta = ''
			nomeVariable = expresionHashAsignacionDoble.group(1)
			key1 = procesaVariable(expresionHashAsignacionDoble.group(2))
			key2 = procesaVariable(expresionHashAsignacionDoble.group(3))
			valor = procesaOperacion(expresionHashAsignacionDoble.group(4))

			
			if((getComentario() !='') and (getComentario != '\n') and(getComentario().replace('\n','') == key1String)):
			
				cadeaDevolta += 'if (!'+nomeVariable+'.containsKey(String.valueOf('+key1+'))) {\n\t'+nomeVariable+'.put(String.valueOf('+key1+'),new Hashtable<String,String>());\n}\n'
				
				
				cadeaDevolta += nomeVariable+'.get(String.valueOf('+key1+')).put('+key2+','+valor+')'+expresionHashAsignacionDoble.group(5)
			
				return cadeaDevolta
			else:
				
				cadeaDevolta += 'if (!'+nomeVariable+'.containsKey('+key1+')) {\n\t'+nomeVariable+'.put('+key1+',new Hashtable<String,String>());\n}\n'
				
				
				cadeaDevolta += nomeVariable+'.get('+key1+').put('+key2+','+valor+')'+expresionHashAsignacionDoble.group(5)
			
				return cadeaDevolta
		
		
		#Asignacion nunha taboa hash
		elif(expresionHashAsignacion):
			
			if(getDebugMode()):
				print 'procesaLinha function :: Procesando asignacion a taboa Hash'
				
			
			return expresionHashAsignacion.group(1)+'.put('+procesaOperacion(expresionHashAsignacion.group(2))+','+procesaOperacion(expresionHashAsignacion.group(3))+')'+expresionHashAsignacion.group(4)
	
		elif(('=~' in linha)or('!~' in linha)):
			if(getDebugMode()):
				print 'procesaLinha function :: Procesando expresion regular simple'
			
			simboloER = ''
			
			if('=~' in  linha):
				simboloER = '=~'
				
			elif('!~' in  linha):
				simboloER = '!~'
				
				
			partes = linha.split(simboloER)
			
			if(getDebugMode()):
				print '==========================='
				print partes[0]
				print partes[1]
				print '==========================='
			
			
			if("=" in partes[0]):
				partesIgualdade = partes[0].split("=")
			
				if(len(partesIgualdade)==2):
			
			
					if(getDebugMode()):
						print 'procesaLinha function :: Procesando asignacion a variable con expresion regular'
				
					if(partes[1][len(partes[1])-1]==';'):
						partes[1] = partes[1][0:len(partes[1])-1]
				
					elif((partes[1][len(partes[1])-2]==';')and(partes[1][len(partes[1])-1]=='\n')):
						partes[1] = partes[1][0:len(partes[1])-2]
					
					return procesaExpresionRegular(partesIgualdade[1]+" "+simboloER+" "+partes[1],partesIgualdade[0])
					
				else:
					return procesaExpresionRegular(linha)
			
			else:
				return procesaExpresionRegular(linha)
	
		elif('+=' in linha):
			partes = linha.split("+=")
			
			nomeVariable = partes[0]
			valorVariable = partes[1]
			
			return procesaVariable(nomeVariable)+' += '+procesaOperacion(valorVariable)+';'
			
		elif('.=' in linha):
			partes = linha.split(".=")
			
			nomeVariable = partes[0]
			valorVariable = partes[1]
			
			return procesaVariable(nomeVariable)+' += '+procesaOperacion(valorVariable)+';'
	
		
			
		#Asignacion de variable cun valor (string, int ou float)
		elif(expresionAsignacionVariableParentese):
			
			if(getDebugMode()):
				print 'procesaLinha function :: Procesando asignacion a variable con parentese :: '+expresionAsignacionVariableParentese.group(2)
				
			if(getComentario().replace("\n","") == tipoKeyValue):
				variables = expresionAsignacionVariableParentese.group(2).split(",")
				
				variableKey = procesaVariable(variables[0])
				variableValue = procesaVariable(variables[1])
				
				linha1 = variableKey+" = key.toString();\n"
				linha2 = variableValue+" = val.toString();"
				
				return linha1+linha2
			
			else:
				nomeVariable = expresionAsignacionVariableParentese.group(2)
				valorVariable = expresionAsignacionVariableParentese.group(4)
			
				return procesaVariable(nomeVariable)+' = '+procesaOperacion(valorVariable)+';'
	
		#Asignacion de variable cun valor (string, int ou float)
		elif(expresionAsignacionVariable):

			tipoDato = ''
			
			if(getDebugMode()):
				print 'procesaLinha function :: Procesando asignacion a variable :: '+expresionAsignacionVariable.group(2)
			
			if(expresionAsignacionVariable.group(1)=='my' and getComentario()!=""):
				if(getComentario().replace("\n","") == tipoString):
					tipoDato = 'String'
				elif(getComentario().replace("\n","") == tipoInt):
					tipoDato = 'int'
				elif(getComentario().replace("\n","") == tipoBoolean):
					tipoDato = 'boolean'
				elif(getComentario().replace("\n","") == tipoArrayString):
					tipoDato = 'String[]'
				elif(getComentario().replace("\n","") == tipoDouble):
					tipoDato = 'double'
				elif(getComentario().replace("\n","") == tipoLong):
					tipoDato = 'long'
				else:
					tipoDato = 'String'
			
			nomeVariable = expresionAsignacionVariable.group(2)
			valorVariable = expresionAsignacionVariable.group(4)
			
			if(getComentario().replace("\n","") == castInt):
				return procesaVariable(nomeVariable)+' = Integer.parseInt('+procesaOperacion(valorVariable)+')'+expresionAsignacionVariable.group(5)
				
			elif(getComentario().replace("\n","") == castString):
				return procesaVariable(nomeVariable)+' = String.valueOf('+procesaOperacion(valorVariable)+')'+expresionAsignacionVariable.group(5)
			
			
			return tipoDato+' '+procesaVariable(nomeVariable)+' = '+procesaOperacion(valorVariable)+expresionAsignacionVariable.group(5)
		
		elif(expresionAsignacionVariableSenPuntoComa):

			tipoDato = ''
			
			if(getDebugMode()):
				print 'procesaLinha function :: Procesando asignacion a variable sen punto coma :: '+expresionAsignacionVariableSenPuntoComa.group(2)
			
			if(expresionAsignacionVariableSenPuntoComa.group(1)=='my' and getComentario()!=""):
				if(getComentario().replace("\n","") == tipoString):
					tipoDato = 'String'
				elif(getComentario().replace("\n","") == tipoInt):
					tipoDato = 'int'
				elif(getComentario().replace("\n","") == tipoBoolean):
					tipoDato = 'boolean'
				elif(getComentario().replace("\n","") == tipoArrayString):
					tipoDato = 'String[]'
				elif(getComentario().replace("\n","") == tipoDouble):
					tipoDato = 'double'
				elif(getComentario().replace("\n","") == tipoLong):
					tipoDato = 'long'
				else:
					tipoDato = 'String'
			
			nomeVariable = expresionAsignacionVariableSenPuntoComa.group(2)
			valorVariable = expresionAsignacionVariableSenPuntoComa.group(4)
			
			if(getComentario().replace("\n","") == castInt):
				return procesaVariable(nomeVariable)+' = Integer.parseInt('+procesaOperacion(valorVariable)+')'
					
			
			
			return tipoDato+' '+procesaVariable(nomeVariable)+' = '+procesaOperacion(valorVariable)
		
		elif(expresionDeclaracionVariable):
			if(getDebugMode()):
				print 'procesaLinha function :: Procesando declaracion de variable :: '+expresionDeclaracionVariable.group(0)
	
			tipoDato = ''
			valorAsignacion = ''
			if(getComentario().replace("\n","") == tipoString):
				tipoDato = 'String'
			elif(getComentario().replace("\n","") == tipoInt):
				tipoDato = 'int'
			elif(getComentario().replace("\n","") == tipoBoolean):
				tipoDato = 'boolean'
			elif(getComentario().replace("\n","") == tipoArrayString):
				tipoDato = 'String[]'
			elif(getComentario().replace("\n","") == tipoStringNull):
				tipoDato = 'String'
				valorAsignacion = ' = null'
			elif(getComentario().replace("\n","") == tipoLong):
					tipoDato = 'long'
			else:
				if(getDebugMode()):
					print 'procesaLinha function :: Tipo non atopado :: Predefinido -> String'
				tipoDato = 'String'
	
			nomeVariable = expresionDeclaracionVariable.group(2)
			
			return tipoDato+' '+procesaVariable(nomeVariable)+valorAsignacion+';'

		elif(expresionDeclaracionHash):
			if(getDebugMode()):
				print 'procesaLinha function :: Procesando declaracion de taboa hash :: '+expresionDeclaracionHash.group(0)
	
			tipoDato = 'Hashtable '
			valorAsignacion = ''
			if(getComentario().replace("\n","") == tipoHashStringLong):
				tipoDato = tipoDato + '<String, Long>'
				valorAsignacion = ' = new Hashtable<String, Long>()'
				
			elif(getComentario().replace("\n","") == tipoHashStringInteger):
				tipoDato = tipoDato + '<String, Integer>'
				valorAsignacion = ' = new Hashtable<String, Integer>()'
				
			else:
				if(getDebugMode()):
					print 'procesaLinha function :: Tipo non atopado :: Predefinido -> String'
				tipoDato = tipoDato + '<String, String>'
				valorAsignacion = ' = new Hashtable<String, String>()'
	
			nomeVariable = expresionDeclaracionHash.group(2)
			
			return tipoDato+' '+procesaVariable(nomeVariable)+valorAsignacion+';'

		elif(expresionSimbolo):
		
			if(getDebugMode()):
				print 'procesaLinha function :: Procesando simbolo'
		
			return expresionSimbolo.group(1)
		
		#Chamada a unha funcion na que os argumentos van sen parentese
		elif(expresionFuncionSenParentese):
			if(getDebugMode()):
				print 'procesaLinha function :: Procesando chamada a funcion sen parentese'
			
			nomeFuncion = expresionFuncionSenParentese.group(1)
			argumento = expresionFuncionSenParentese.group(2)+expresionFuncionSenParentese.group(3)
		
			cadeaDevolta = ''
			
			if(nomeFuncion == "delete"):
				
				if(getDebugMode()):
					print 'procesaLinha function :: Procesando chamada a funcion sen parentese DELETE :: '+argumento
				
				#Obtenhense as partes do hash
			
				expresionAuxPartesHash = re.compile(r'[\s]*[\$]{1}([\w][\w\d\W]*)[\{]{1}[\$]{1}([\w\d\W]+)[\}]{1}[\s]*([;]{0,1})[\s]*').match(argumento)
			
				if(expresionAuxPartesHash):

					cadeaDevolta = expresionAuxPartesHash.group(1)+'.remove('+expresionAuxPartesHash.group(2)+');'
					
				else:
					cadeaDevolta = procesaVariable(argumento).replace(";","")+'= "";'
			
			elif(nomeFuncion == 'chomp'):
				return procesaVariable(expresionFuncionSenParentese.group(2))+' = '+procesaVariable(expresionFuncionSenParentese.group(2))+".trim()"+expresionFuncionSenParentese.group(3)
			
			elif(nomeFuncion == 'print'):
				if(getConfigOption('hadoop')):
					
					keyValue = argumento.split(".")
				
					cadeaDevolta = 'context.write('+getDefaultKey()+procesaVariable(keyValue[0])+'),'+getDefaultValue()+procesaVariable(keyValue[1].replace(";",""))+'));'
					
				else:
					cadeaDevolta = 'System.out.print('+procesaOperacion(argumento).replace(";","").replace("\\+",". ")+');'
					
			elif(nomeFuncion == 'undef'):
				if(getDebugMode()):
					print 'procesaLinha function :: Procesando chamada a funcion sen parentese UNDEF :: '+argumento
			
				if((getComentario()!='')and(getComentario()!='\n')and(getComentario().replace('\n','') == tipoArrayString)):
					cadeaDevolta = expresionFuncionSenParentese.group(2).replace("@","").replace("\n","").replace(";","").replace(" ","")+" = new String[text.size()];"
				
				elif((getComentario()!='')and(getComentario()!='\n')and(getComentario().replace('\n','') == tipoArrayBoolean)):
					cadeaDevolta = expresionFuncionSenParentese.group(2).replace("@","").replace("\n","").replace(";","").replace(" ","")+" = new boolean[text.size()];"
				else:
					cadeaDevolta = expresionFuncionSenParentese.group(2).replace("@","").replace("\n","").replace(";","").replace(" ","")+'.clear();'
			
			return cadeaDevolta
		
		elif(expresionIncremento):
			
			if(getDebugMode()):
				print 'procesaLinha function :: ExpresionIncremento'
				
			return procesaVariable(expresionIncremento.group(1))+expresionIncremento.group(2)+expresionIncremento.group(3)
			
		else:
			if(getDebugMode()):
				print 'procesaLinha function :: Expresion non atopada!!'
	
			variable = linha.replace("$","").replace(" ","")
			if(not('next' in variable)):
				return variable
			elif('next;' in variable.replace("\n","")):
				return 'continue;'
			else:
				return ''
	
	else:
		return ''



