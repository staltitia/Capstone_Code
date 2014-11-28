import serial
'''
	status : [ 11110000 ]
	expect:
		19 bytes: (in ascii)
		VERSION 0.1, READY\n
		
	confirm : [ 11110001 ]
	expect: n/a
	
	cancel : [ 11110010 ]
	expect : n/a
	
	presets : [ 11110100 (var_1) (var_val) ... \n ]
	expect: [ checksum ]
	
	request: [ 11111000 ]
	expect: [ image data ]
'''
def status(window):
	if window.serial == None:
		return
	window.serial.close()
	window.serial.open()
	
	#identifier byte
	toSend = chr(0b11110000)
	
	window.serial.write( toSend )
	
	#we wait?
	
	readVal = window.read( size = 19 )
	if readVal == "VERSION 0.1, READY\n":
		return True
	return False
	

def requestImage(window): #DEPRECATED. NO LONGER IN USE. EMBEDDED IN MAIN.PY SCREENSHOT METHOD
	if window.serial == None:
		return
	window.serial.close()
	window.serial.open()
	
	#identifier byte
	toSend = chr(0b11110100)
	
	window.serial.write( toSend )
	
	#we wait for a second?
	
	#we expect 
	inVal = window.serial.read(size = 3)
	if int(inVal[0]) != 0b00001111:
		window.serial.flush() #we flush output, and then
		return
	size = int(inVal[1]) * int(inVal[2]) #first three bytes are identifier, numRows, numCols
	window.serial.read( size = size+1 ) #we expect ???
	
def checksum( toSend ): #still in testing
	sum = 0
	#for i in toSend:
	#	sum += int(i)
	#sum = sum%0b10000
	return sum
	
def sendPresets(window):
	if window.serial == None:
		return
	toSend = []
	#identifier byte
	toSend.append( chr(0b11110100) )
	
	#then, we list our variables
	
	#mode: 00000001, [ photo, slow1, slow2, fast, TV ] = [ 00000001, 00000010, 00000100, 00001000, 00010000 ]
	
	modeVal = window.currentMode.get_label()
	toSend.append( chr(0b00000001) )
	if modeVal == "Photo":
		toSend.append( chr(0b00000001) )
	elif modeVal == "Slow 1":
		toSend.append( chr(0b00000010) )
	elif modeVal == "Slow 2":
		toSend.append( chr(0b00000100) )
	elif modeVal == "Fast":
		toSend.append( chr(0b00001000) )
	elif modeVal == "TV":
		toSend.append( chr(0b00010000) )
	else:
		toSend.append( chr(0b00000000) )
		

	#inType: 00000010, [ secondaryElectrons, X-Ray, auxiliary ] = [ 00000001, 00000010, 00000100 ]
	
	toSend.append( chr(0b00000010) )
	inTypeVal = window.inTypeVar
	if modeVal == "Secondary Electron":
		toSend.append( chr(0b00000001) )
	elif modeVal == "X-Ray":
		toSend.append( chr(0b00000010) )
	elif modeVal == "Auxiliary":
		toSend.append( chr(0b00000100) )
	else:
		toSend.append( chr(0b00000000) )
	
	#[ xShift, yShift, xStig, yStig, condLens, objLens, filaCurr, magni ] = [ 00000011, 00000100, 00000101, 00000110, 00000111, 00001000, 00001001, 00001010 ]
	toSend.append( chr(0b00000011) )
	toSend.append( chr( int(window.shiftXVar + 127) ) )
	
	toSend.append( chr(0b00000100) )
	toSend.append( chr( int(window.shiftYVar + 127) ) )
	
	toSend.append( chr(0b00000101) )
	toSend.append( chr( int(window.stigXVar) ) )
	
	toSend.append( chr(0b00000110) )
	toSend.append( chr( int(window.stigYVar) ) )
	
	toSend.append( chr(0b00000111) )
	toSend.append( chr( int(window.condVar) ) )

	toSend.append( chr(0b00001000) )
	toSend.append( chr( int(window.objVar) ) )

	toSend.append( chr(0b00001001) )
	toSend.append( chr( int(window.filaVar) ) )

	toSend.append( chr(0b00001010) )
	if int(window.magVar) <= 255:
		toSend.append( chr( int(window.magVar) ) )
	else:
		toSend.append( chr( 255 ) )
	
	toSend.append('\n')
	
	window.serial.close()	
	window.serial.open()
	window.serial.write( ''.join(toSend) )
	
	return checksum(toSend)