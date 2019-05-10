#!/usr/bin/env python2

#WHAT TEAM!? CELTS!
#Paige Meeks redo of the binary decoder:
#take binary message as input, decide if it's
#7-bit or 8-bit ASCII, then translate from
#binary to ASCII characters
#NOTE: this is Python 2 (denoted by the ...Py2.py)

from sys import stdin, stdout

#turn on/off debug mode
DEBUG = False

#binMsg is the binary message that the user inputs
binMsg = raw_input()
#mLen is the length of the binary message (it's just convenient to have
#it stored in a variable)
mLen = len(binMsg)
#MODE is the ASCII bit length (7 or 8...hopefully)
MODE = 0

def getMode():
	#add message stating that the ASCII version cannot be determined via
	#the length of the binary message
	if(mLen % 7 == 0 and mLen % 8 == 0):
		print("CAUTION! The binary message that was passed in could be either "
			"ASCII 7-bit or ASCII 8-bit! If you see this message, edit the code "
			"to try 8-bit as well since this code will default to 7-bit.")
	#proceed to determine the ASCII bit length
	if(mLen % 7 == 0):
		MODE = 7
	elif(mLen % 8 == 0):
		MODE = 8
	else:
		print("The length of the string did not match neither ASCII 7-bit nor ASCII 8-bit! Exitting...")
		exit(1)

	if(DEBUG):
		print("The MODE is: %s" % MODE)
	#return an array of the binary bits split up into chunks the size of the MODE
	return [binMsg[i:i+MODE] for i in range(0, mLen, MODE)]

def convertBinary(splitMsg):
	decodedMsg = []
	#convert each chunk into its decimal value and then its corresponding ASCII character
	#and then add it to the decodedMsg array
	for char in splitMsg:
		decodedMsg += chr(int(char, 2))

	if(DEBUG):
		print(decodedMsg)
	#convert the list of ASCII characters into a string and return the string
	return ''.join(decodedMsg)

splitMsg = getMode()
print(convertBinary(splitMsg))
exit(0)