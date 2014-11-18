 cat gaz/gazPER.dat |grep -v justicia |grep -v fuerza |grep -v "_ley$" |grep -v "paso$" |grep -v "_ferro$" |grep -v "_carril$" |grep -v "^m$" 
cat gaz/gazLOC.dat |grep -P -v "^ong$" |grep -v "^ley$" | grep -v "^lei$" |grep -v "^boca$"
cat gazORG.dat |grep -v  internet | grep -v facultad |grep  -v "^ley_"
cat gazMISC.dat |grep -v  "^elvis$"
