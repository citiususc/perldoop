#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#Copyright 2014 Jose Manuel Abuin Mosquera <josemanuel.abuin@usc.es>
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

simbolosAceptados 			= ['\\\\n'] #,'\\s','\\w','\\W']
simbolosAceptadosValid 		= ['\\n'] #,'\s','\w','\W']

caracteresNoEscape 			= ['\\<','\\>','\\.','\\+']
caracteresNoEscapeSubs 		= ['<','>','\\.','+']

#Variables globais para procesar variable privada
procesandoVariablePrivada 	= False
variablePrivada = ""
tipoVariablePrivada 		= ""

novaVariable 				= ""
novoArray					= ""
novoHash					= ""

valorNovaVariable			= ""

inicioProcesadoJava			= "<java><start>"
finProcesadoJava			= "<java><end>"

comentarioLinha				= "<perl>"

inicioProcesadoPerl			= "<start>"
finProcesadoPerl			= "<end>"

headerInit					= "<header><start>"
headerEnd					= "<header><end>"

#Para identificacion de tipos de variables usadas
booleanVar					= "<var><boolean>"
key1String					= "<key1><integer>"

#Para declaracions de variables
tipoString					= "<var><string>"
tipoBoolean					= "<var><boolean>"
tipoInt						= "<var><integer>"
tipoDouble					= "<var><double>"
tipoLong					= "<var><long>"

tipoArrayString				= "<array><string>"
tipoArrayBoolean			= "<array><boolean>"

tipoStringNull				= "<var><string><null>"

tipoArraylistString			= "<arraylist><string>"
#Tipos para Hash <Key,Value>

tipoHash					= "<hashtable>"
tipoHashStringLong			= "<hashtable><string><long>"
tipoHashStringInteger		= "<hashtable><string><integer>"

#Identificacion de clave-valor para Hadoop
tipoKey						= "<var><key>"
tipoValue					= "<var><value>"
tipoKeyValue				= "<var><keyvalue>"

#Casts en asignacions
castInt						= "<cast><int>"
castString					= "<cast><string>"

#Detectar cando se emprega <STDIN> en Perl
cadeaStdin					= "<STDIN>"

processingStatus 			= False
readingHeader 				= False

mapStart					= "<map>"
reduceStart					= "<reduce>"

#Para ignorar unha linha
ignoreLine					= "<ignoreline>"

debugMode 					= False

comment 					= ''

headerOptions				= {}

configOptions				= {}

defaultKey					= "new Text("
defaultValue				= "new Text("

#Estado procesando
def setProcessingStatus(valor):
	global processingStatus
	processingStatus = valor

def getProcessingStatus():
	global processingStatus
	return processingStatus

#Estado lendo header
def setReadingHeaderStatus(valor):
	global readingHeader
	readingHeader = valor

def getReadingHeaderStatus():
	global readingHeader
	return readingHeader

#Modo debug
def setDebugMode(valor):
	global debugMode
	debugMode = valor

def getDebugMode():
	global debugMode
	return debugMode

#Tags nos comentarios (para variables ou todo o que queiramos por ahi)
def setComentario(novoComentario):
	global comment
	comment = novoComentario.replace("\n","")
	
def getComentario():
	global comment
	return comment

#Opcions
def setHeaderOption(clave, valor):
	global headerOptions
	headerOptions[clave] = valor

def getHeaderOption(clave):
	global headerOptions
	return headerOptions[clave]

def getHeaderOptionKeys():
	global headerOptions
	return headerOptions.keys()

def getDefaultKey():
	global defaultKey
	return defaultKey

def getDefaultValue():
	global defaultValue
	return defaultValue

#Saber si un string e un numero
def isNumber(variable):
	try:
		float(variable)
		return True
	except:
		return False

#Saber si un string conten un numero enteiro
def check_int(s):
    if s[0] in ('-', '+'):
    	return s[1:].isdigit()
    return s.isdigit()

#Funcion para reemplazar os caracteres que non tenhen que ir escapados
def reemplazoCaracteresSenEscapar(cadea):

	for j in range(0,len(caracteresNoEscape)):
		if(caracteresNoEscape[j] in cadea):
			cadea = cadea.replace(caracteresNoEscape[j],caracteresNoEscapeSubs[j])
			
	cadea = cadea.replace('\\','\\\\')
	cadea = cadea.replace('"','\\"')
	for j in range(0,len(simbolosAceptados)):
		if(simbolosAceptados[j] in cadea):
			cadea = cadea.replace(simbolosAceptados[j],simbolosAceptadosValid[j])
			
	return cadea
	
def getConfig():
	
	ficheiroConfig = './config.txt'
	
	ficheiro = open(ficheiroConfig,"r")
	
	for line in ficheiro:
		if("=" in line):
			partes = line.split("=")
			
			if(partes[1].replace("\n","")=="true"):
				configOptions[partes[0]] = True
			else:
				configOptions[partes[0]] = False
			
def getConfigOption(opcion):
	return configOptions[opcion]
	
