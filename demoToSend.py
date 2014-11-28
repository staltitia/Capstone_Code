def demoToSend( inVal ):
	'''
	a 
	turns on

	b
	1001VVVVVVVVVVXX
	where V is value

	first byte is 10010000 + int (value / 32) => 100100VV
	second byte is (value % 32) * 4 => VVVVVV00

	c
	same protocol, different slave
	'''
		
	inVal = inVal % 256
	topByte = 0b10010000 + int ( inVal / 32 )
	botByte = int(inVal % 32) * 4
	return [ chr(topByte), chr(botByte) ]