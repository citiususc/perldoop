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

from Globals import *


def procesaVariableIf(expresion):

	cadea = ''

	#Obtencion de elemento de taboa hash
	expresionHash = re.compile(r'[\s]*([\(]{0,1})[\s]*[\$]{0,1}([\w]+[\w\d\W]*)[\{]([\w\d\W]+)[\}]([\(]{0,1})').match(expresion)

	#Expresion de lonxitude de array
	expresionLonxitudeArray = re.compile(r'[\s]*([\(\s]*)[\s]*[\$]{0,1}[\#]([\w]+)[\s]*([\)\s]*)[\s]*').match(expresion)

	#Expresion para procesar unha chamada a unha funcion
	expresionFuncion = re.compile(r'[\s]*([\w][\w\d_]*)[\s]*\([\s]*([\$\w\d\W]+)\)[\s]*').match(expresion)

	if(expresionHash):
		if(getDebugMode()):
			print 'Function procesaVariableIf:: '+expresionHash.group(0)
	
		cadea += expresionHash.group(1)+expresionHash.group(2)+'.get('+procesaArgumentosFuncion(expresionHash.group(3))+')'+expresionHash.group(4)

	elif(expresionLonxitudeArray):
		if(getDebugMode()):
			print 'Function procesaVariableIf:: '+expresionLonxitudeArray.group(0)
		
		nomeVariableLA = expresionLonxitudeArray.group(2).replace(" ","")
		
		return expresionLonxitudeArray.group(1)+nomeVariableLA+'.length - 1'+expresionLonxitudeArray.group(3)
		
	elif(expresionFuncion):
			
		if(getDebugMode()):
			print 'Function procesaVariableIF:: expresionFuncion '+expresionFuncion.group(0)
			
			
		if(expresionFuncion.group(1) == 'lowercase'):
			return procesaVariable(expresionFuncion.group(2))+'.toLowerCase()'
		
		elif(expresionFuncion.group(1) == 'lc'):
			return procesaArgumentosFuncion(expresionFuncion.group(2))+'.toLowerCase()'
		
		elif(expresionFuncion.group(1) == 'push'):
			partesPush = expresionFuncion.group(2).split(",")
				
			if(len(partesPush)==2):
				return partesPush[0].replace("@","")+".add("+procesaArgumentosFuncion(partesPush[1])+");"
			else:
				return expresionFuncion.group(1)+' ('+procesaArgumentosFuncion(expresionFuncion.group(2))+')'
				
		elif(expresionFuncion.group(1) == 'substr'):
			partesSubstr = expresionFuncion.group(2).split(",")
			
			cadeaDevolver = procesaVariable(partesSubstr[0])+".substring("
			
			for argIndex in range(1,len(partesSubstr)-1):
				cadeaDevolver = cadeaDevolver + procesaOperacion(partesSubstr[argIndex])+","
			
			cadeaDevolver = cadeaDevolver + procesaOperacion(partesSubstr[len(partesSubstr)-1])+"+"+procesaOperacion(partesSubstr[len(partesSubstr)-2])
			
			return cadeaDevolver+")"
		
		elif(expresionFuncion.group(1) == 'index'):
			partesIndex = expresionFuncion.group(2).split(",")
			
			cadeaDevolver = procesaVariable(partesIndex[0])+".indexOf("
			
			for argIndex in range(1,len(partesIndex)-1):
				cadeaDevolver = cadeaDevolver + procesaOperacion(partesIndex[argIndex].replace("\\t"," "))+","
			
			cadeaDevolver = cadeaDevolver + procesaOperacion(partesIndex[len(partesIndex)-1])
			
			return cadeaDevolver+")"
		
		elif(expresionFuncion.group(1) == 'length'):
			
			
			return procesaVariable(expresionFuncion.group(2))+".length()"
				
		else:
			if(getDebugMode()):
				print 'Function procesaVariableIF:: normal function'
			return expresionFuncion.group(1)+' ('+procesaArgumentosFuncion(expresionFuncion.group(2))+')'
		
	else:
		if(getDebugMode()):
			print 'Function procesaVariableIF:: expression not found '+expresion
		
		cadea += expresion.replace("$","").replace('\\','')
		
		
	return cadea



#Procesa cada unha das partes internas a unha condicion ou bucle while
def procesaParteIf(expresion):
	
	cadea = ''
	
	expresionRegular = re.compile(r'[\s]*([\(]{0,1})([\w\d\W]+)[\s]*([\)]{0,1})').match(expresion)

	expresionEq = re.compile(r'[\s]*([\(]{0,1})[\$]{0,1}([\w][\w\d\W]*)[\s]*eq[\s]*([\w\W\d]+)([\)]{0,1})').match(expresion)
	
	expresionNe = re.compile(r'[\s]*([\(]{0,1})[\$]{0,1}([\w][\w\d\W]*)[\s]+ne[\s]+([\w\W\d]+)([\)]{0,1})').match(expresion)
	
	expresionComparacionVarios = re.compile(r'[\s]*([\(]*)[\$]{0,1}([\w\d\W]+)[\s]*([\\<\\>]{1}[=]{1})[\s]*([\W\w\d]+)([\)]*)').match(expresion)
	
	expresionComparacion = re.compile(r'[\s]*([\(]*)[\$]{0,1}([\w\d\W]+)[\s]*([=]{2}|!=|>|<)[\s]*([\w\W\d]+)([\)]*)').match(expresion)
	
	expresionHash = re.compile(r'[\s]*([\(]{0,1})[\$]{0,1}([\w]+[\w\d\W]*)[\{]([\w\d\W]+)[\}]([\)]{0,1})').match(expresion)

	expresionHashDobre = re.compile(r'[\s]*([\(]{0,1})[\$]{0,1}([\w]+[\w\d\W]*)[\{]([\w\d\W]+)[\}][\{]([\w\d\W]+)[\}]([\)]{0,1})').match(expresion)
	
	expresionVariableFalse = re.compile(r'[\s]*([\(]{0,1})([!]{1})[\s]*([\w\d\W]+)[\s]*([\)]{0,1})').match(expresion)

	#Expresion para procesar unha chamada a unha funcion
	expresionFuncion = re.compile(r'[\s]*([\(]*)[\s]*([\w][\w\d_]*)[\s]*\([\s]*([\$\w\d\W]+)[\s]*([\)]+)[\s]*').match(expresion)

	#Expresion que chama a unha funcion sen parenteses
	expresionFuncionSenParentese = re.compile(r'[\s]*(defined)[\s]+([\w\d\W]+)[\s]*').match(expresion)

	if(('=~' in expresion) or ('!~' in expresion)):
		#Tratase a expresion regular
		if(expresionRegular):
			if(getDebugMode()):
				print 'Expresion regular en If: '+expresionRegular.group(0)
				print 'Resultado: '+expresionRegular.group(1)+procesaExpresionRegular(expresionRegular.group(2))+expresionRegular.group(3)
			cadea += expresionRegular.group(1)+procesaExpresionRegular(expresionRegular.group(2))+expresionRegular.group(3)
		else:
			#cadea += '('+procesaExpresionRegular(expresion)+')'
			cadea += procesaExpresionRegular(expresion)

	elif(expresionEq):
		
		variable = expresionEq.group(2)
		if(variable[len(variable)-1] == ' '):
			novaVariable = variable[:len(variable)-1]
		else:
			novaVariable = variable
			
		cadea += expresionEq.group(1)+procesaVariableIf(novaVariable)+'.equals('+procesaVariableIf(expresionEq.group(3))+') '+expresionEq.group(4)

	elif(expresionNe):
		variable = expresionNe.group(2)
		
		if(variable[len(variable)-1] == ' '):
			novaVariable = variable[:len(variable)-1]
		else:
			novaVariable = variable
			
		cadea += expresionNe.group(1)+'!('+procesaVariableIf(novaVariable)+'.equals('+procesaVariableIf(expresionNe.group(3))+')) '+expresionNe.group(4)

	elif(('<=' in expresion)or('>=' in expresion)):
		
		if(getDebugMode()):
			print 'Procesando comparacion dentro de IF con <= ou >= '
	
		if('<=' in expresion):
			partes = expresion.split('<=')
			
			cadea +=procesaVariableIf(partes[0])+'<='+procesaOperacion(partes[1])

			return cadea
			
		elif('>=' in expresion):
			partes = expresion.split('>=')
			
			cadea +=procesaVariableIf(partes[0])+'>='+procesaOperacion(partes[1])
			
			return cadea

	elif(expresionComparacion):
		
		if(getDebugMode()):
			print 'Procesando comparacion dentro de IF '+ cadea+' '+expresionComparacion.group(3)
	
		cadea += expresionComparacion.group(1)+procesaVariableIf(expresionComparacion.group(2))+' '+expresionComparacion.group(3)+' '+procesaOperacion(expresionComparacion.group(4))+expresionComparacion.group(5)

	elif(expresionFuncion):
				
		if(getDebugMode()):
			print 'Function procesaParteIf:: expresionFuncion:: '+expresionFuncion.group(0)
			
		#TODO: Review this, maybe is not correct
		if(expresionFuncion.group(2) == 'lowercase' or expresionFuncion.group(2) == 'lc'):
			return expresionFuncion.group(1)+procesaVariable(expresionFuncion.group(3))+'.toLowerCase()'+expresionFuncion.group(4)
		
		
		elif(expresionFuncion.group(2) == 'push'):
			partesPush = expresionFuncion.group(2).split(",")
				
			if(len(partesPush)==2):
				return partesPush[0].replace("@","")+".add("+procesaOperacion(partesPush[1])+");"
			else:
				return expresionFuncion.group(1)+expresionFuncion.group(2)+' ('+procesaArgumentosFuncion(expresionFuncion.group(3))+')'+expresionFuncion.group(4)
				
		elif(expresionFuncion.group(2) == 'defined'):
			return expresionFuncion.group(1)+procesaVariable(expresionFuncion.group(3)).replace(")","")+"!= null"+expresionFuncion.group(4)
		
		elif(expresionFuncion.group(2) == 'substr'):
			partesSubstr = expresionFuncion.group(3).split(",")
			
			cadeaDevolver = procesaVariable(partesSubstr[0])+".substring("
			
			for argIndex in range(1,len(partesSubstr)-1):
				cadeaDevolver = cadeaDevolver + procesaOperacion(partesSubstr[argIndex])+","
			
			cadeaDevolver = cadeaDevolver + procesaOperacion(partesSubstr[len(partesSubstr)-1])+"+"+procesaOperacion(partesSubstr[len(partesSubstr)-2])
			
			return cadeaDevolver+")"
		
		else:
		
			if(getDebugMode()):
				print 'Normal function'
				
			return expresionFuncion.group(1)+expresionFuncion.group(2)+' ('+procesaArgumentosFuncion(expresionFuncion.group(3))+expresionFuncion.group(4)
		
	
	elif(expresionFuncionSenParentese):
		return procesaParteIf(expresionFuncionSenParentese.group(2))

	elif(expresionHashDobre):
		if(getDebugMode()):
			print 'Procesando hash multikey en condicion'

		cadea += expresionHashDobre.group(1)+ expresionHashDobre.group(2)+'.containsKey('+procesaVariableIf(expresionHashDobre.group(3))+') && '+ expresionHashDobre.group(2)+'.get('+procesaVariableIf(expresionHashDobre.group(3))+').containsKey('+procesaVariableIf(expresionHashDobre.group(4))+')'+expresionHashDobre.group(5)


	elif(expresionHash):
		
		if(getDebugMode()):
			print 'Procesando hash en condicion'
		
		cadea += expresionHash.group(1)+ expresionHash.group(2)+'.containsKey('+procesaVariableIf(expresionHash.group(3))+')'+expresionHash.group(4)
			
	elif(expresionVariableFalse):
	
		if(getDebugMode()):
			print 'Procesando expresion de negacion '+ cadea
	
		cadea += expresionVariableFalse.group(1)+'!'+procesaParteIf(expresionVariableFalse.group(3))+expresionVariableFalse.group(4)
	
	else:
	
		if(getDebugMode()):
			print 'Procesando comparacion dentro de IF. Sustitucion de dolar en '+ cadea
	
		cadea += '('+expresion.replace("$","").replace("(","").replace(")","")+')'


	return cadea
	

def procesaInteriorIf(expresion):

	cadea = ''

	expresionInteriorIf = re.compile(r'[\s]*([\(]{0,1})([\w\d\W]*)[\s]*([&]{2}|[|]{2})[\s]*([\w\d\W]*)([\)]{0,1})').match(expresion)
	
	if(expresionInteriorIf): #E un if composto de varias condicions
		cadea += expresionInteriorIf.group(1)+procesaInteriorIf(expresionInteriorIf.group(2))+' '+expresionInteriorIf.group(3)+' '+procesaInteriorIf(expresionInteriorIf.group(4))+expresionInteriorIf.group(5)


	else:
		if(getDebugMode()):
			print 'Procesando expresion booleana '+expresion
		cadea += procesaParteIf(expresion)
		
	return cadea
	
def procesaExpresionRegular(line, varFinal = None):

		cadeaDevolta = ""

		if(('=~' in line)or('!~' in line)):
		
			negacion = False
			
			
			if('!~' in line):
				negacion = True
				posibleER = line.split('!~')
			elif('=~' in line):
				posibleER = line.split('=~')
			
			if(len(posibleER)==2):
			
				
			
				if(varFinal != None): #Este caso e o de $var = $variable =~ expresion_regular
				
					if(getDebugMode()):
						print 'Procesando asignacion en expresion regular '+line
				
					if(posibleER[1][0] == " "):
						posibleER[1] = posibleER[1][1:len(posibleER[1])]

			
				#EXPRESION REGULAR DE SUSTITUCION DE TODOLOS ITEMS s/*/*/g
				exptTodosItems = re.compile(r'[\s]*s/([\w\W\d]+)/([\w\W\d]+)/g').match(posibleER[1]) #Procuramos as partes da expresion regular de sustitucion
				
				#EXPRESION REGULAR DE SUSTITUCION DO PRIMEIRO ITEM ATOPADO s/*/*
				exprFirstItem = re.compile(r'[\s]*s/([\w\W\d]+)/([\w\W\d]*)/([i]*)').match(posibleER[1])
				
				#EXPRESION REGULAR CON IGNORE CASE
				exprIgnoreCase = re.compile(r'[\s]*s/([\w\W]+)/i').match(posibleER[1])
				
				#EXPRESION REGULAR QUE BUSCA SIN SUSTITUIR
				exprBusqueda = re.compile(r'[\s]*/([\w\d\W]+)/([i]{0,1})([\)\s]*)').match(posibleER[1])
				
				if(exptTodosItems):
					if(getDebugMode()):
						print 'Expresion regular sustitucion global todolos items'
					
					primeiraParte = exptTodosItems.group(1)
					segundaParte = exptTodosItems.group(2)
					
					#PRIMEIRA PARTE DA EXPRESION REGULAR. O QUE BUSCAMOS


					#Dividimos seguno os nimbolos de dolar na cadea, que veñen sendo as variables en Perl
					splitsDolar = primeiraParte.split('$')
					
					cadeaResPrimeiraParte = '' #Para gardar a cadea resultante
					
					if(len(splitsDolar) == 1): #Non hai o simbolo dolar na cadea
						cadeaResPrimeiraParte += 'p = new Pattern("'+reemplazoCaracteresSenEscapar(primeiraParte)+'");'
						
					else: #Hai a lo menos un simbolo de dolar na cadea (variables en Perl)

						if(splitsDolar[0]==''): #O primeiro que hai xa e unha variable
							cadeaResPrimeiraParte +=  'p = new Pattern('
					
						else:

							splitsDolar[0] = reemplazoCaracteresSenEscapar(splitsDolar[0])
						
							cadeaResPrimeiraParte +=  'p = new Pattern("'+splitsDolar[0]+'"+'
							
						i=1
						while(i<len(splitsDolar)):
							
							splitsDolar[i] = reemplazoCaracteresSenEscapar(splitsDolar[i])

							m1 = re.compile(r'([\w]+)([\W]*)([\W\w]*)').match(splitsDolar[i])
							mSimbolo = re.compile(r'([\W]+)').match(splitsDolar[i])
							
							if(m1):
								if(i<len(splitsDolar)-1):
									cadeaResPrimeiraParte += m1.group(1)+'+"'+m1.group(2)+m1.group(3)+'"+'
								else:
									cadeaResPrimeiraParte += m1.group(1)+'+"'+m1.group(2)+m1.group(3)+'"'
							elif(mSimbolo): #E un simbolo dolar seguido por simbolos
								if(i<len(splitsDolar)-1):
									cadeaResPrimeiraParte += '"$'+mSimbolo.group(1)+'"+'
								else:
									cadeaResPrimeiraParte += '"$'+mSimbolo.group(1)+'"'

							i+=1
					
						if(splitsDolar[len(splitsDolar)-1]==''): #Por si se sinala o dolar o final
							cadeaResPrimeiraParte += '"$"'
					
						cadeaResPrimeiraParte += ");"
					
					cadeaDevolta += cadeaResPrimeiraParte+'\n'
					
					#SEGUNDA PARTE DA EXPRESION REGULAR, POLO QUE SUBSTITUIMOS
					cadeaResSegundaParte = ""
					
					splitsDolar = segundaParte.split('$')
					
					if(len(splitsDolar) == 1): #Non hai o simbolo dolar na cadea
						segundaParte = reemplazoCaracteresSenEscapar(segundaParte)
									
						cadeaResSegundaParte += 'r = p.replacer("'+segundaParte+'");'
					
					else:
					
						if(splitsDolar[0]==''):
						
							cadeaResSegundaParte += 'r = p.replacer(""'
					
						else:
							splitsDolar[0] = reemplazoCaracteresSenEscapar(splitsDolar[0])
						
							cadeaResSegundaParte += 'r = p.replacer("'+splitsDolar[0]+'"'
					
						i = 1
						
						while(i<len(splitsDolar)):

							splitsDolar[i] = reemplazoCaracteresSenEscapar(splitsDolar[i])
					
							mNumero = re.compile(r'([\d]+)').match(splitsDolar[i])
							
							if(mNumero):
								cadeaResSegundaParte += '+"$'+splitsDolar[i]+'"'
							else:
								m1 = re.compile(r'([\w]+)([\W]*)([\W\w]*)').match(splitsDolar[i])
								if(m1):
									if(i<len(splitsDolar)-1):
										cadeaResSegundaParte += '+'+m1.group(1)+'+"'+m1.group(2)+m1.group(3)+'"'
									else:
										cadeaResSegundaParte += '+'+m1.group(1)+'+"'+m1.group(2)+m1.group(3)+'"'
	
							i += 1
						
						cadeaResSegundaParte += ');'

						
					cadeaDevolta += cadeaResSegundaParte+'\n'
					
					if(varFinal == None):
						cadeaDevolta += posibleER[0].replace("$","")+'= r.replace(texto);\n'
	
					else:
						cadeaDevolta += varFinal.replace("$","")+'= r.replace(texto);\n'
					
					return cadeaDevolta;


				elif(exprFirstItem):
					
					if(getDebugMode()):
						print 'Procesando expresion regular de unha sustitucion'
					
					primeiraParte = exprFirstItem.group(1)
					segundaParte = exprFirstItem.group(2)


					cadeaResultante = ''
					
					cadeaResultante += posibleER[0].replace("$","").replace(" ","")+' = '+posibleER[0].replace("$","").replace(" ","")+'.replaceFirst('
					
					#Primeira parte da ER
					splitsDolar = primeiraParte.split('$')
					
					if(len(splitsDolar) == 1): #Non hai o simbolo dolar na cadea
					
						primeiraParte = reemplazoCaracteresSenEscapar(primeiraParte)
						
						if(primeiraParte[0]!='^'):
							primeiraParte = "[\\\\w\\\\W\\\\d]*"+primeiraParte
							
						if(primeiraParte[len(primeiraParte)-1]!="$"):
							primeiraParte = primeiraParte +"[\\\\w\\\\W\\\\d]*"
						
						cadeaResultante += '"'+primeiraParte+'"'
					
					else: #Hai algun simbolo de dolar, como e a primeira parte, teñen que ser variables Perl
						
						if(splitsDolar[0]!=''): #Hai algo antes do primeiro simbolo dolar
						
							splitsDolar[0] = reemplazoCaracteresSenEscapar(splitsDolar[0])
						
							
						i=0
						
						while(i<len(splitsDolar)):
							
							splitsDolar[i] = reemplazoCaracteresSenEscapar(splitsDolar[i])
							
							m1 = re.compile(r'([\w]+)([\W]*)([\W\w]*)').match(splitsDolar[i])
							if(m1):
							
								if(i<len(splitsDolar)-1):
									if(i==0):
										cadeaResultante += '"'+m1.group(1)+'"+'
									else:
										cadeaResultante += m1.group(1)+'+"'+m1.group(2)+m1.group(3)+'"+'
								else:
									cadeaResultante += m1.group(1)+'+"'+m1.group(2)+m1.group(3)+'"'
								
							
							i+=1
					
						if(splitsDolar[len(splitsDolar)-1]==''): #Por si se sinala o dolar o final
							cadeaResultante += '"$"'
			
					cadeaResultante += ','
					
					#Segunda parte da ER
					splitsDolar = segundaParte.split('$')
					
					if(len(splitsDolar) == 1): #Non hai o simbolo dolar na cadea

						cadeaResultante += '"'+reemplazoCaracteresSenEscapar(segundaParte)+'"'
						
					else:
					
						i = 1
						cadeaResultante += '""'
						while(i<len(splitsDolar)):
					
							splitsDolar[i] = reemplazoCaracteresSenEscapar(splitsDolar[i])
					
					
							mNumero = re.compile(r'([\d]+)').match(splitsDolar[i])
					
							mNumeros = re.compile(r'[\{]{1}([\d]+)[\}]([\w\W\d]*)').match(splitsDolar[i])
					
							if(mNumero):
								cadeaResultante += '+"$'+splitsDolar[i]+'"'

							elif(mNumeros):
								cadeaResultante += '+"$'+mNumeros.group(1)+'"+"'+mNumeros.group(2)+'"'

							else:
								m1 = re.compile(r'([\w]+)([\W]*)([\W\w]*)').match(splitsDolar[i])
								if(m1):
									cadeaResultante += '+'+m1.group(1)+'+"'+m1.group(2)+m1.group(3)+'"'
	
							i += 1

					cadeaResultante += ');'

					return cadeaResultante

				elif(exprIgnoreCase):
					
					if(getDebugMode()):
						print 'Expresion regular sustitucion ignore case'
					primeiraParte = exprIgnoreCase.group(1)
					
					#PRIMEIRA PARTE DA EXPRESION REGULAR. O QUE BUSCAMOS


					#Dividimos seguno os nimbolos de dolar na cadea, que veñen sendo as variables en Perl
					splitsDolar = primeiraParte.split('$')
					
					cadeaResPrimeiraParte = '' #Para gardar a cadea resultante
					
					if(len(splitsDolar) == 1): #Non hai o simbolo dolar na cadea
						cadeaResPrimeiraParte += 'p = new Pattern("'+reemplazoCaracteresSenEscapar(primeiraParte)+'");'
						
					else: #Hai a lo menos un simbolo de dolar na cadea (variables en Perl)

						if(splitsDolar[0]==''): #O primeiro que hai xa e unha variable
							cadeaResPrimeiraParte +=  'p = new Pattern('
					
						else:

							splitsDolar[0] = reemplazoCaracteresSenEscapar(splitsDolar[0])
						
							cadeaResPrimeiraParte +=  'p = new Pattern("'+splitsDolar[0]+'"+'
							
						i=1
						while(i<len(splitsDolar)):
							
							splitsDolar[i] = reemplazoCaracteresSenEscapar(splitsDolar[i])

							m1 = re.compile(r'([\w]+)([\W]*)([\W\w]*)').match(splitsDolar[i])
							mSimbolo = re.compile(r'([\W]+)').match(splitsDolar[i])
							
							if(m1):
								if(i<len(splitsDolar)-1):
									cadeaResPrimeiraParte += m1.group(1)+'+"'+m1.group(2)+m1.group(3)+'"+'
								else:
									cadeaResPrimeiraParte += m1.group(1)+'+"'+m1.group(2)+m1.group(3)+'"'
							elif(mSimbolo): #E un simbolo dolar seguido por simbolos
								if(i<len(splitsDolar)-1):
									cadeaResPrimeiraParte += '"$'+mSimbolo.group(1)+'"+'
								else:
									cadeaResPrimeiraParte += '"$'+mSimbolo.group(1)+'"'

							i+=1
					
						if(splitsDolar[len(splitsDolar)-1]==''): #Por si se sinala o dolar o final
							cadeaResPrimeiraParte += '"$"'
					
						cadeaResPrimeiraParte += ");"
					
			
					return cadeaResPrimeiraParte
					
					
					#SEGUNDA PARTE DA EXPRESION REGULAR, POLO QUE SUBSTITUIMOS
					
					print 'texto = r.replace(texto);'

				elif(exprBusqueda):
				
					if(getDebugMode()):
						print 'Expresion regular busqueda'
					
					
					if(varFinal != None):
						nomeVariable = posibleER[0]

						cadeaDevolta = ""
						
						expresionHash = re.compile(r'[\s]*[\$]{0,1}([\w]+[\w\d\W]*)[\{]([\w\d\W]+)[\}][\s\t]*([;]{0,1})').match(nomeVariable)
	
	
						#Dividimos seguno os nimbolos de dolar na cadea, que veñen sendo as variables en Perl
						splitsDolar = exprBusqueda.group(1).split('$')
					
					
						if(len(splitsDolar) == 1): #Non hai o simbolo dolar na cadea
							if(exprBusqueda.group(1)[0]!="^"):
								cadeaDevolta += '"[\\\\w\\\\W]*'+reemplazoCaracteresSenEscapar(exprBusqueda.group(1))+'[\\\\w\\\\W]*"'
						
							else:
								cadeaDevolta += '"'+reemplazoCaracteresSenEscapar(exprBusqueda.group(1))+'[\\\\w\\\\W]*"'
						
						else: #Hai a lo menos un simbolo de dolar na cadea (variables en Perl)

							if(splitsDolar[0]!=''): #O primeiro que hai non e unha variable
								if(splitsDolar[0][0]!="^"):
									cadeaDevolta += '"[\\\\w\\\\W]*'+reemplazoCaracteresSenEscapar(splitsDolar[0])+'"+'
								else:
									cadeaDevolta += '"'+reemplazoCaracteresSenEscapar(splitsDolar[0])+'"+'
							else:
								cadeaDevolta += '"[\\\\w\\\\W]*"+'


							i=1
							while(i<len(splitsDolar)):
							
								splitsDolar[i] = reemplazoCaracteresSenEscapar(splitsDolar[i])

								m1 = re.compile(r'([\w]+)([\W]*)([\W\w]*)').match(splitsDolar[i])
								mSimbolo = re.compile(r'([\W]+)').match(splitsDolar[i])
							
								if(m1):
									if(i<len(splitsDolar)-1):
										cadeaDevolta += m1.group(1)+'+"'+m1.group(2)+m1.group(3)+'"+'
									else:
										cadeaDevolta += m1.group(1)+'+"'+m1.group(2)+m1.group(3)+'"'
								elif(mSimbolo): #E un simbolo dolar seguido por simbolos
									if(i<len(splitsDolar)-1):
										cadeaDevolta += '"$'+mSimbolo.group(1)+'"+'
									else:
										cadeaDevolta += '"$'+mSimbolo.group(1)+'"'

								i+=1
					
							if(splitsDolar[len(splitsDolar)-1]==''): #Por si se sinala o dolar o final
								cadeaDevolta += '"$"'
							else:
								cadeaDevolta += '+"[\\\\w\\\\W]*"'

						
						cadeaDevolver = ''
					
						parte2Split = posibleER[1]
					
						cadeaDevolver += 'p = new Pattern('+cadeaDevolta+');\n'
					
						cadeaDevolver += 'r = p.replacer("$1");\n'
					
						if(expresionHash):

							cadeaDevolver += procesaVariable(varFinal)+' = r.replace('+expresionHash.group(1)+'.get('+procesaVariable(expresionHash.group(2))+');\n'
	
						else:				
					
							cadeaDevolver += procesaVariable(varFinal)+' = r.replace('+procesaVariable(nomeVariable)+');\n'
							
						return cadeaDevolver
						
						
					else:
					
						nomeVariable = posibleER[0]

						cadeaDevolta = ""
					
						expresionHash = re.compile(r'[\s]*[\$]{0,1}([\w]+[\w\d\W]*)[\{]([\w\d\W]+)[\}][\s\t]*([;]{0,1})').match(nomeVariable)
	
	
						#Dividimos seguno os nimbolos de dolar na cadea, que veñen sendo as variables en Perl
						splitsDolar = exprBusqueda.group(1).split('$')
					
						if(len(splitsDolar) == 1): #Non hai o simbolo dolar na cadea
							if(exprBusqueda.group(1)[0]!="^"):
								cadeaDevolta += '"[\\\\w\\\\W]*'+reemplazoCaracteresSenEscapar(exprBusqueda.group(1))+'[\\\\w\\\\W]*"'
						
							else:
								cadeaDevolta += '"'+reemplazoCaracteresSenEscapar(exprBusqueda.group(1))+'[\\\\w\\\\W]*"'
						
						else: #Hai a lo menos un simbolo de dolar na cadea (variables en Perl)

							if(splitsDolar[0]!=''): #O primeiro que hai non e unha variable
								if(splitsDolar[0][0]!="^"):
									cadeaDevolta += '"[\\\\w\\\\W]*'+reemplazoCaracteresSenEscapar(splitsDolar[0])+'"+'
								else:
									cadeaDevolta += '"'+reemplazoCaracteresSenEscapar(splitsDolar[0])+'"+'
							else:
								cadeaDevolta += '"[\\\\w\\\\W]*"+'


							i=1
							while(i<len(splitsDolar)):
							
								splitsDolar[i] = reemplazoCaracteresSenEscapar(splitsDolar[i])

								m1 = re.compile(r'([\w]+)([\W]*)([\W\w]*)').match(splitsDolar[i])
								mSimbolo = re.compile(r'([\W]+)').match(splitsDolar[i])
							
								if(m1):
									if(i<len(splitsDolar)-1):
										cadeaDevolta += m1.group(1)+'+"'+m1.group(2)+m1.group(3)+'"+'
									else:
										cadeaDevolta += m1.group(1)+'+"'+m1.group(2)+m1.group(3)+'"'
								elif(mSimbolo): #E un simbolo dolar seguido por simbolos
									if(i<len(splitsDolar)-1):
										cadeaDevolta += '"$'+mSimbolo.group(1)+'"+'
									else:
										cadeaDevolta += '"$'+mSimbolo.group(1)+'"'

								i+=1
					
							if(splitsDolar[len(splitsDolar)-1]==''): #Por si se sinala o dolar o final
								cadeaDevolta += '"$"'
							else:
								cadeaDevolta += '+"[\\\\w\\\\W]*"'
					
						cadeaDevolver = ''
					
						parte2Split = posibleER[1]
					
						if(nomeVariable[0]=='('):
							cadeaDevolver += '('
							nomeVariable = nomeVariable[1:len(nomeVariable)-1]

						if(expresionHash):
							if(negacion):
								cadeaDevolver += '!(new Pattern('+cadeaDevolta+',"'+exprBusqueda.group(2)+'").matches('+expresionHash.group(1)+'.get('+procesaVariable(expresionHash.group(2))+')'+'))'+exprBusqueda.group(3)
							else:
								cadeaDevolver += 'new Pattern('+cadeaDevolta+',"'+exprBusqueda.group(2)+'").matches('+expresionHash.group(1)+'.get('+procesaVariable(expresionHash.group(2))+')'+')'+exprBusqueda.group(3)
	
	
					
						else:				
					
							if(negacion):
								cadeaDevolver += '!(new Pattern('+cadeaDevolta+',"'+exprBusqueda.group(2)+'").matches('+nomeVariable.replace("$","")+'))'+exprBusqueda.group(3)
							else:
								cadeaDevolver += 'new Pattern('+cadeaDevolta+',"'+exprBusqueda.group(2)+'").matches('+nomeVariable.replace("$","")+')'+exprBusqueda.group(3)
						
						return cadeaDevolver

					
		else:
			return line

#Procesa os argumentos pasados a unha funcion separados por comas
def procesaArgumentosFuncion(linha):
	
	argumentos = linha.split(",")
	
	
	if(len(argumentos)>1):
	
		valores = ''
	
		for novoArgumento in argumentos:
	
			if(getDebugMode()):
				print 'Procesando variable de funcion :: '+procesaOperacion(novoArgumento)
	
			valores = valores + procesaOperacion(novoArgumento)+','
		
		cadeaDevolver = valores[:len(valores)-1]
	
		return cadeaDevolver
	else:
		return procesaOperacion(linha)

#Procesa a parte dereita dunha asignacion (concatenacion de operacions ou chamadas a funcions)
def procesaOperacion(linha):

	#Expresion de concatenacion de variables e strings
	expresionOperacionConcat = re.compile(r'^[\s]*[\$]{0,1}([\w\d\W]*)[\s ]*([.]){1}[\s]*[\$]{0,1}([\w\d\W]+)[\s]*').match(linha)
	
	#Expresion de concatenacion de variables e strings. String a esquerda e variable a dereita
	expresionOperacionConcatEsq = re.compile(r'^[\s]*(["]{1})([\w\d\W]*)(["]{1})[\s]*([.]){1}[\s]*([\w\d\W]+)[\s]*').match(linha)
	
	#Expresion de concatenacion de variables e strings. String a dereita e variable a esquerda
	expresionOperacionConcatDer = re.compile(r'^[\s]*([\w\d\W]*)[\s]*([.]){1}[\s]*(["]{1})([\w\d\W]+)(["]{1})[\s]*').match(linha)
	
	#Expresion de concatenacion de strings
	expresionOperacionConcatString = re.compile(r'^[\s]*(["]{1})([\w\d\W]*)(["]{1})[\s]*([.]){1}[\s]*(["]{1})([\w\d\W]+)(["]{1})[\s]*').match(linha)
	
	#Expresion de concatenacion de variables de tipo texto
	expresionOperacionConcatStringVar = re.compile(r'^[\s]*([\w\d\W]*)[\s]*([.]){1}[\s]*([\w\d\W]+)[\s]*').match(linha)
	
	#Expresion de operacion con array con operacion
	expresionOperacionArrayEsqu = re.compile(r'^[\s]*[\$]{0,1}([\w\d\W]+[\[]{1}[\w\W\d]+[+\-\*\/][\w\W\d]+[\]]{1})[\s]*([+\-\*\/]){1}[\s]*[\$]{0,1}([\w\d\W]+)[\s]*').match(linha)
	
	expresionOperacionArrayDer = re.compile(r'^[\s]*[\$]{0,1}([\w\d\W]+)[\s]*([+\-\*\/]){1}[\s]*[\$]{0,1}([\w\d\W]+[\[]{1}[\w\W\d]+[+\-\*\/][\w\W\d]+[\]]{1})[\s]*').match(linha)
	
	#Expresion de operacion aritmetica
	expresionOperacion = re.compile(r'^[\s]*[\$]{0,1}([\w\d\W]+)[\s ]*([+\-\*\/]){1}[\s]*[\$]{0,1}([\w\d\W]+)[\s]*').match(linha)
	
	#Expresions do tipo = $hash{$key1}{$key2}+$var
	expresionHashEsquDobre = re.compile(r'[\s]*[\$]{0,1}([\w]+[\w\d\W]*[\{][\w\d\W]+[\}][\{][\w\d\W]+[\}])[\s]*([+\-\*\/]){1}[\s]*([\w\d\W]+)[\s]*([;]{0,1})').match(linha)
	
	#Expresions do tipo = $hash{$var}+$var
	expresionHashEsqu = re.compile(r'[\s]*[\$]{0,1}([\w]+[\w\d\W]*[\{][\w\d\W]+[\}])[\s]*([+\-\*\/]){1}[\s]*([\w\d\W]+)[\s]*([;]{0,1})').match(linha)
	
	#Expresions do tipo = $var+$hash{$key1}{$key2}
	expresionHashDerDobre = re.compile(r'[\s]*[\$]{0,1}([\w\d\W]+)[\s]*([+\-\*\/]){1}[\s]*[\$]{0,1}([\w]+[\w\d\W]*[\{][\w\d\W]+[\}])[\s]*([;]{0,1})').match(linha)
	
	#Expresions do tipo = $var+$hash{$var}
	expresionHashDer = re.compile(r'[\s]*[\$]{0,1}([\w\d\W]+)[\s]*([+\-\*\/]){1}[\s]*[\$]{0,1}([\w]+[\w\d\W]*[\{][\w\d\W]+[\}])[\s]*([;]{0,1})').match(linha)
	
	#Expresion un só string
	expresionString = re.compile(r'[\s]*["]{1}([^"]*)["]{1}[\s]*([;]{0,1})').match(linha)
	
	#Expresions array e hash unicas con acceso a posicion operada
	expresionArrayUnico = re.compile(r'^[\s]*[\$]{0,1}([\w\d\W]+[\[]{1}[\w\W\d]+[+\-\*\/][\w\W\d]+[\]]{1})[\s]*([;]{0,1})[\s]*').match(linha)
	
	expresionHashUnico = re.compile(r'[\s]*[\$]{0,1}([\w]+[\w\d\W]*[\{][\w\d\W]+[\}])[\s]*([;]{0,1})').match(linha)
	
	#Expresion para procesar unha chamada a unha funcion	
	expresionFuncion  = re.compile(r'([\w]+[\w\d_]*)[\s]*\([\s]*([\w\d\W]+)[\s]*\)').match(linha)
	
	
	if(expresionOperacionConcatString):
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionOperacionConcatString  '+expresionOperacionConcatString.group(0)
	
		return procesaOperacion(expresionOperacionConcatString.group(1))+procesaOperacion(expresionOperacionConcatString.group(2))+procesaOperacion(expresionOperacionConcatString.group(3))+'+'+procesaOperacion(expresionOperacionConcatString.group(5))+procesaOperacion(expresionOperacionConcatString.group(6))+procesaOperacion(expresionOperacionConcatString.group(7))
	
	elif(expresionOperacionConcatEsq):
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionOperacionConcatEsq  '+expresionOperacionConcatEsq.group(0)
	
		return procesaOperacion(expresionOperacionConcatEsq.group(1))+procesaOperacion(expresionOperacionConcatEsq.group(2))+procesaOperacion(expresionOperacionConcatEsq.group(3))+'+'+procesaOperacion(expresionOperacionConcatEsq.group(5))
	
	elif(expresionOperacionConcatDer):
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionOperacionConcatDer  '+expresionOperacionConcatDer.group(0)
	
		if(getConfigOption('hadoop') and ((getComentario().replace("\n","") == tipoKey) or (getComentario().replace("\n","") == tipoValue) )):
		
			#Para sacar o \t ou \n que adoita a ir no final de cadea
			return procesaOperacion(expresionOperacionConcatDer.group(1))
		
		elif(getComentario().replace("\n","") == tipoString):
			tipoDato = 'String'
			return procesaOperacion(expresionOperacionConcatDer.group(1))+'+'+procesaOperacion(expresionOperacionConcatDer.group(3))+procesaOperacion(expresionOperacionConcatDer.group(4))+procesaOperacion(expresionOperacionConcatDer.group(5))
		
		else:
			return procesaOperacion(expresionOperacionConcatDer.group(1))+'+'+procesaOperacion(expresionOperacionConcatDer.group(3))+procesaOperacion(expresionOperacionConcatDer.group(4))+procesaOperacion(expresionOperacionConcatDer.group(5))
	
	elif(expresionString):
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionString '+expresionString.group(0)
			
		return linha.replace("\\.",".");
		
	#Concatenacion de strings
	elif(expresionOperacionConcatStringVar):
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionOperacionConcatStringVar '+expresionOperacionConcatStringVar.group(0)
		
		return procesaOperacion(expresionOperacionConcatStringVar.group(1))+'+'+procesaOperacion(expresionOperacionConcatStringVar.group(3))
	
	elif(expresionHashEsquDobre):
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionHashEsquDobre '+expresionHashEsquDobre.group(0)
	
		return procesaVariable(expresionHashEsquDobre.group(1))+expresionHashEsquDobre.group(2)+procesaOperacion(expresionHashEsquDobre.group(3))
	
	elif(expresionHashEsqu):
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionHashEsqu '+expresionHashEsqu.group(0)
	
		return procesaVariable(expresionHashEsqu.group(1))+expresionHashEsqu.group(2)+procesaOperacion(expresionHashEsqu.group(3))
	
	elif(expresionHashDerDobre):
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionHashDerDobre '+expresionHashDerDobre.group(0)
			
		return procesaOperacion(expresionHashDerDobre.group(1))+expresionHashDerDobre.group(2)+procesaVariable(expresionHashDerDobre.group(3))
	
	elif(expresionHashDer):
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionHashDer '+expresionHashDer.group(0)
	
		return procesaOperacion(expresionHashDer.group(1))+expresionHashDer.group(2)+procesaVariable(expresionHashDer.group(3))
	
	elif(expresionHashUnico):
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionHashUnico '+expresionHashUnico.group(0)
	
		return procesaVariable(expresionHashUnico.group(1))+expresionHashUnico.group(2)
	
	elif(expresionOperacionArrayEsqu):
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionOperacionArrayEsqu '+expresionOperacionArrayEsqu.group(0)
			
		return procesaVariable(expresionOperacionArrayEsqu.group(1))+expresionOperacionArrayEsqu.group(2)+procesaOperacion(expresionOperacionArrayEsqu.group(3))
	
	elif(expresionOperacionArrayDer):
		if(getDebugMode()):
			print 'Function procesaOperacion :: Procesando Array dereita '+expresionOperacionArrayDer.group(0)
			
		return procesaOperacion(expresionOperacionArrayDer.group(1))+expresionOperacionArrayDer.group(2)+procesaVariable(expresionOperacionArrayDer.group(3))
	
	elif(expresionArrayUnico):
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionArrayUnico '+expresionArrayUnico.group(0)
	
		return procesaVariable(expresionArrayUnico.group(1))+expresionArrayUnico.group(2)

	elif(expresionFuncion):
		
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionFuncion '+expresionFuncion.group(0)
		
		nomeFuncion = expresionFuncion.group(1).replace(" ","").replace("\n","")
		
		if(nomeFuncion == 'lowercase'):#TODO: Cambiar aqui procesaVariable pola funcion que procese os argumentos da funcion
			return procesaVariable(expresionFuncion.group(2))+'.toLowerCase()'
		elif(nomeFuncion == 'lc'):#TODO: Cambiar aqui procesaVariable pola funcion que procese os argumentos da funcion
			return procesaVariable(expresionFuncion.group(2))+'.toLowerCase()'
			
		elif(nomeFuncion == 'split'):#TODO: Cambiar aqui procesaVariable pola funcion que procese os argumentos da funcion
		
			argumentos = expresionFuncion.group(2).split(",")
		
			return procesaVariable(argumentos[1])+'.split('+argumentos[0]+')'
		elif(nomeFuncion == 'push'):
			partesPush = expresionFuncion.group(2).split(",")
				
			if(len(partesPush)==2):
				return partesPush[0].replace("@","")+".add("+procesaOperacion(partesPush[1])
			else:
				return expresionFuncion.group(1)+' ('+procesaArgumentosFuncion(expresionFuncion.group(2))+')'
				
		elif(expresionFuncion.group(1) == 'substr'):
			partesSubstr = expresionFuncion.group(2).split(",")
			
			cadeaDevolver = procesaVariable(partesSubstr[0])+".substring("
			
			for argIndex in range(1,len(partesSubstr)-1):
				cadeaDevolver = cadeaDevolver + procesaOperacion(partesSubstr[argIndex])+","
			
			cadeaDevolver = cadeaDevolver + procesaOperacion(partesSubstr[len(partesSubstr)-1])+"+"+procesaOperacion(partesSubstr[len(partesSubstr)-2])
			
			return cadeaDevolver+")"
		
		elif(expresionFuncion.group(1) == 'index'):
			partesIndex = expresionFuncion.group(2).split(",")
			
			cadeaDevolver = procesaVariable(partesIndex[0])+".indexOf("
			
			for argIndex in range(1,len(partesIndex)-1):
				cadeaDevolver = cadeaDevolver + procesaOperacion(partesIndex[argIndex]).replace("\"","'")+","
			
			cadeaDevolver = cadeaDevolver + procesaOperacion(partesIndex[len(partesIndex)-1])
			
			return cadeaDevolver+")"
		
		elif(expresionFuncion.group(1) == 'length'):
			
			
			return expresionFuncion.group(2)+".length()"		
		
		elif(expresionFuncion.group(1) == 'qw'): #Esta expresion en Perl devolve un array cos strings entre parentese
		
			variablesArray = expresionFuncion.group(2).split(" ")
			valorRetorno = "{"
			
			for i in range(0,len(variablesArray)-1):
				valorRetorno = valorRetorno + '"'+variablesArray[i]+ '",'
			
			valorRetorno = valorRetorno + '"'+variablesArray[len(variablesArray)-1]+ '"}'
			
			return valorRetorno
			
		else:
			return expresionFuncion.group(1)+' ('+procesaArgumentosFuncion(expresionFuncion.group(2))+')'
	
	#Operacion artitmetica
	elif(expresionOperacion):
			
		if(getDebugMode()):
			print 'Function procesaOperacion :: expresionOperacion '+expresionOperacion.group(0)
			
		return procesaOperacion(expresionOperacion.group(1))+expresionOperacion.group(2)+procesaOperacion(expresionOperacion.group(3))

	else:
		if(getDebugMode()):
			print 'Function procesaOperacion :: Expression not found. Calling procesaVariable :: '+linha
		return procesaVariable(linha)
		
		
#Procesa unha variable ou dato
def procesaVariable(linha):

	#Expresions tipos basicos
	expresionNumeroEnteiro = re.compile(r'[\s]*([\(]*)[\s]*([\d]+)[\s]*([\)]*)[\s]*([;]{0,1})').match(linha)
	expresionNumeroFlotante = re.compile(r'[\s]*([\(]*)[\s]*([\d]+.[\d]+)[\s]*([\)]*)[\s]*([;]{0,1})').match(linha)
	expresionString = re.compile(r'[\s]*([\(]*)[\s]*["]([\w\W\d]*)["][\s]*([\)]*)[\s]*([;]{0,1})').match(linha)
	
	#Variable de Perl
	expresionVariable = re.compile(r'[\s]*[\$]{0,1}([a-zA-Z]{1}[\w\d\W]*)[\s]*([;]{0,1})').match(linha)
	
	#Variable declarada con my e sen ;
	expresionVariableDeclarada = re.compile(r'[\s]*(my){1}[\s]*[\$]{0,1}([a-zA-Z]{1}[\w\d\W]*)[\s]*').match(linha)
	
	
	#Acceso a array e Hash
	expresionArray = re.compile(r'[\s]*[\$]{0,1}([\w]+[\W\d\w]*)\[([\w\d\W]+)\][\s]*([\)]*)[\s]*([;]{0,1})').match(linha)
	
	expresionHash = re.compile(r'[\s]*[\$]{0,1}([a-zA-Z]+[\w\d\W]*)[\{]([\w\d\W]+)[\}][\s\t]*([;]{0,1})').match(linha)
	
	expresionHashDobre = re.compile(r'[\s]*[\$]{0,1}([a-zA-Z]+[\w\d\W]*)[\{]([\w\d\W]+)[\}][\{]([\w\d\W]+)[\}][\s\t]*([;]{0,1})').match(linha)
	
	#Expresion array como argumento
	expresionArrayArgumento = re.compile(r'[\s]*\\@([\w]+[\W\d\w]*)[\s\t]*([;]{0,1})').match(linha)
	
	#Expresion de lonxitude de array
	expresionLonxitudeArray = re.compile(r'[\s]*([\(]*)[\s]*[\$]{0,1}[\#]([\w]+[\w\d ]*)[\s]*([\)]*)[\s]*([;]{0,1})').match(linha)
	
	if(getDebugMode()):
			print 'Function procesaVariable. Valor a procesar :: '+linha
	
	if(expresionHashDobre):
		if(getDebugMode()):
			print 'Function procesaVariable. expresionHashDobre'
			
		return expresionHashDobre.group(1)+'.get('+procesaVariable(expresionHashDobre.group(2))+').get('+procesaVariable(expresionHashDobre.group(3))+')'+expresionHashDobre.group(4)
			
	elif(expresionHash):
		if(getDebugMode()):
			print 'Function procesaVariable. expresionHash'
	
		return expresionHash.group(1)+'.get('+procesaOperacion(expresionHash.group(2))+')'+expresionHash.group(3)
	
	elif(expresionArray):
		if(getDebugMode()):
			print 'Function procesaVariable:: expresionArray :: '+expresionArray.group(1)+'['+procesaOperacion(expresionArray.group(2))+']'+expresionArray.group(3)+expresionArray.group(4)
	
		return expresionArray.group(1)+'['+procesaOperacion(expresionArray.group(2))+']'+expresionArray.group(3)+expresionArray.group(4)
	
	elif(expresionVariableDeclarada):
		if(getDebugMode()):
			print 'Function procesaVariable:: expresionVariableDeclarada :: '+expresionVariableDeclarada.group(1)+expresionVariableDeclarada.group(2)
		
		tipoDato = ''
		
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
		
		return tipoDato+" "+expresionVariableDeclarada.group(2)
	
	elif(expresionVariable):
		if(getDebugMode()):
			print 'Function procesaVariable:: expresionVariable :: '+expresionVariable.group(1)+expresionVariable.group(2)
		
		return expresionVariable.group(1)+expresionVariable.group(2)
	
	

	elif(expresionNumeroFlotante):
		if(getDebugMode()):
			print 'Function procesaVariable :: Processing float'
	
		return expresionNumeroFlotante.group(1)+expresionNumeroFlotante.group(2)+expresionNumeroFlotante.group(3)+expresionNumeroFlotante.group(4)
	
	elif(expresionNumeroEnteiro):
		if(getDebugMode()):
			print 'Function procesaVariable :: Processing integer'
	
		numero = expresionNumeroEnteiro.group(2)
	
		if((getComentario() !='') and (getComentario != '\n') and(getComentario().replace('\n','') == booleanVar)):
			if int(numero) == 1:
				numero = 'true'
			else:
				numero = 'false'
				
		setComentario('')
		return expresionNumeroEnteiro.group(1)+numero+expresionNumeroEnteiro.group(3)+expresionNumeroEnteiro.group(4)
	
	elif(expresionString):
		if(getDebugMode()):
			print 'Function procesaVariable :: Processing string'

		cadea = expresionString.group(2)
		for j in range(0,len(caracteresNoEscape)):
			if(caracteresNoEscape[j] in cadea):
				cadea = cadea.replace(caracteresNoEscape[j],caracteresNoEscapeSubs[j])

		return expresionString.group(1)+'"'+cadea+'"'+expresionString.group(3)+expresionString.group(4)
	
	elif(expresionLonxitudeArray):
		if(getDebugMode()):
			print 'Function procesaVariable :: Processing array length'
			
		return expresionLonxitudeArray.group(1)+expresionLonxitudeArray.group(2).replace(" ","")+'.length - 1'+expresionLonxitudeArray.group(3)+expresionLonxitudeArray.group(4)
	
	elif(expresionArrayArgumento):
		if(getDebugMode()):
			print 'Function procesaVariable :: Processing array as function argument'
	
		return expresionArrayArgumento.group(1)
	
	else:
		if(getDebugMode()):
			print 'Function procesaVariable:: Not found:: Replacing $ and @'
			
		return linha.replace("$","").replace("@","")

#Procesa a condicion dentro dun bucle foreach
def procesaInteriorForeach(linha):
	
	if(getDebugMode()):
			print 'Function procesaInteriorForeach'
	
	expresionKeys = re.compile(r'[\s]*foreach[\s]*(my){0,1}[\s]+[\$]{0,1}([\w]+[\w\W\d]*)[\s]*[\(][\s]*keys[\s]+[\%][\{]([\w\W\d]+)[\}]{1}[\s]*[\)]{1}[\s]*[\{]{1}').match(linha)
	
	expresionRecorreArray = re.compile(r'[\s]*foreach[\s]*(my){0,1}[\s]+[\$]{0,1}([\w]+[\w\W\d]*)[\s]*[\(][\s]*[\@]([\w\W\d]+)[\s]*[\)]{1}[\s]*[\{]{1}').match(linha)
	
	cadeaDevolta = ''
	
	if(expresionKeys):
	
		if(getDebugMode()):
			print 'Function procesaInteriorForeach :: accessing keys :: '+linha
	
		nomeVariable = expresionKeys.group(2).replace(" ","")
		
		cadeaDevolta += 'for (String '+nomeVariable+' : '+procesaVariable(expresionKeys.group(3))+'.keySet()) {'
		
		
	elif(expresionRecorreArray):
		if(getDebugMode()):
			print 'Function procesaInteriorForeach ::Accessing array elements :: '+linha
	
		nomeVariable = expresionRecorreArray.group(2).replace(" ","")

		cadeaDevolta += 'for (String '+nomeVariable+' : '+procesaVariable(expresionRecorreArray.group(3))+') {'

	return cadeaDevolta

