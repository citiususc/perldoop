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

from Automata import *



def main():

	getConfig()
	
	#Debug mode
	if(len(sys.argv)<3):

		setProcessingStatus(True)
		setDebugMode(True)
		line = raw_input('$$$$ Perldoop> ')
		
		while(line!='exit;'):

			valor = procesaLinha(line)
			if(valor !=''):
				print valor.replace("\n","")
			
			line = raw_input('$$$$ Perldoop> ')
			
		setProcessingStatus(False)


	else: #Main. The input file is readed line by line
		nomeFicheiro = str(sys.argv[1])
		nomeFicheiroJava = str(sys.argv[2])

		saida = ''

		ficheiro = file(nomeFicheiro,'r')
		i = 1
		for line in ficheiro:

			valor = procesaLinha(line)
			if(valor !=''):

				saida += '//Linha: '+str(i)+' - Contido: '+line
				saida += valor+'\n'

			i += 1
			
		ficheiroJava = file(nomeFicheiroJava)
		
		for line in ficheiroJava:
		
			print line.replace("\n","")
			
			if '<java><start>' in line:
				print saida
			

if __name__ == '__main__':
	main()
