#reading and writing to a file
	
def writeInitFile(filename):
	#file format is 
	#%SEM CONTROL PANEL INITIALISATION FILE
	#%varName value min max step pagestep
	
	writeFile = open(filename, 'w')
	writeFile.write("%SEM CONTROL PANEL INITIALISATION FILE")
	writeFile.write("\n%xShift 0 -255 255 1 10")
	writeFile.write("\n%yShift 0 -255 255 1 10")
	writeFile.write("\n%xStig 0 0 255 1 10")
	writeFile.write("\n%yStig 0 0 255 1 10")
	writeFile.write("\n%condLens 0 0 255 1 10")
	writeFile.write("\n%objLens 0 0 255 1 10")
	writeFile.write("\n%filaCurrent 0 0 255 1 10")
	writeFile.write("\n%mag 1 1 500 1 10")
	writeFile.close()
	
def readInitFile(filename):
	#file format is 
	#%SEM CONTROL PANEL INITIALISATION FILE
	#%varName value min max step pagestep
	
	toRet = []
	readFile = open(filename, 'r')
	firstLine = readFile.readline()
	if firstLine != "%SEM CONTROL PANEL INITIALISATION FILE\n":
		print "Invalid file " + filename
		print "First line is " + firstLine
		return None
	line=readFile.readline()
	while line != "":
		values = line.split()
		if values[0][0] == '%': 		#then we assume that the format is kind of correct,	and this is a variable
			try:
				varName = (values[0])[1:]
				val = int(values[1])
				minVal = int(values[2])
				maxVal = int(values[3])
				stepVal = int(values[4])
				pageVal = int(values[5])
				toAdd = [varName, val, minVal, maxVal, stepVal, pageVal]
				toRet.append(toAdd)
			except:
				print "Error in reading initialisation file. Please check "+filename
		line=readFile.readline()
	readFile.close()
	return toRet

def writeSavedFile(filename, toWrite):
	#%SEM CONTROL PANEL SAVED PRESETS FILE
	#%varname value
	
	writeFile = open(filename, 'w')
	writeFile.write("%SEM CONTROL PANEL SAVED PRESETS FILE")
	for pair in toWrite:
		toWrite = (pair[1]).replace(' ','_')
		writeFile.write( "\n%"+pair[0]+" "+toWrite )
	writeFile.close()
	
def readSavedFile(filename):
	#%SEM CONTROL PANEL SAVED PRESETS FILE
	#%varname value
	
	toRet = []
	readFile = open(filename, 'r')
	if readFile.readline() != "%SEM CONTROL PANEL SAVED PRESETS FILE\n":
		print "Invalid file " + filename
		return None
	line=readFile.readline()
	while line:
		values = line.split()
		if values[0][0] == '%': 		#then we assume that the format is kind of correct,	and this is a variable
			try:
				varName = (values[0])[1:]
				val = values[1]
				val = val.replace('_',' ')
				toRet.append([varName, val])
			except ReadError:
				print "Error in reading initialisation file. Please check "+filename
		line=readFile.readline()
	readFile.close()
	return toRet