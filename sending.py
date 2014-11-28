import serial

ser = serial.Serial(port='COM5', baudrate = 115200, bytesize=8, parity='N', stopbits=1, timeout = 1)

width = 640
height = 480
'''
myRange = range(width)
toWrite = []
for stuff in myRange:
	toWrite.append( chr(stuff%256) )
'''
if (ser.isOpen()):
	for j in range(height):
		toWrite = [chr(j%256)]*width
		ser.write(''.join(toWrite))
else:
	print wat