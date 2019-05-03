#!/usr/bin/env python

import sys
import binascii
from PIL import Image

####### Error Codes #######
# 0 : Exited with no issues
# 1 : Invalid flag
# 2 : No MODE set
# 3 : No METHOD set

DEBUG = False

# global var declarations
FLAG = ''
MODE = ''
METHOD = ''
OFFSET = ''
INTERVAL = 1
WRAPPER_FILE = ''
HIDDEN_FILE = ''

interval = INTERVAL

sentinel = [00000000, 11111111, 00000000, 00000000, 11111111, 00000000]

def help():
	'''help fxn that gives the usage and options'''
	sys.stdout.write\
	("Usage: 'python steg.py -(bB) -(sr) -o<val> [-i<val>] -w<val> [-h<val>]'\n\n")
	sys.stdout.write("\t-b\t  Use the bit method\n")
	sys.stdout.write("\t-B\t  Use the byte method\n")
	sys.stdout.write("\t-s\t  Store (and hide) data\n")
	sys.stdout.write("\t-r\t  Retrieve hidden data\n")
	sys.stdout.write("\t-o<val>\t  Set offset to <val>\n")
	sys.stdout.write("\t-i<val>\t  Set interval to <val>\n")
	sys.stdout.write("\t-w<val>\t  Set wrapper file to <val>\n")
	sys.stdout.write("\t-h<val>\t  Set hidden file to <val>\n")
	sys.stdout.write("\n\t--help\t  Display this message\n")
	exit(0)

def file_to_bin(inFile):
	'''Function for converting an input file into raw binary'''
	sys.stdout.write("Converting " + inFile + " to binary.\n")
	out_bin = []
	with open(inFile, "rb") as file:
		byte = file.read(1)
		while (byte != ''):
			try:
				out_bin.append(bin(int(binascii.hexlify(byte), 16))[2:].zfill(8))
				byte = file.read(1)
			except ValueError:
				sys.stderr.write\
				("An error has occurred while converting the image to binary... exitting with error code 1...\n")
				exit(1)
		###########################
	if(DEBUG):
		print(len(out_bin))
	return out_bin

#store (-s) a hidden image within an image
def store():
	hidden_bin = file_to_bin(hiddenFile)
	wrapper_bin = file_to_bin(wrapper)
	if (method == 1): # Byte method
		i = 0
		while(i < len(hidden_bin)):
			wrapper_bin[offset] = hidden_bin[i]
			offset += interval
			i+=1
		###########################
		i = 0
		while(i < len(sentinel)):
			wrapper_bin[offset] = sentinel[i]
			offset += interval
			i+=1
		###########################
	elif (method == 0): # Bit method
		i = offset
		j = 0
		hidden_bin += sentinel
		while(j < len(hidden_bin)):
			for k in range(7):
				wrapper_bin[i] &= 11111110
				wrapper_bin[i] |= ((hidden_bin[j] & 10000000) >> 7)
				hidden_bin[j] <<= 1
			###########################
			j+=1
		###########################
	else:
		sys.stderr.write\
		("Method (bit/byte) not set, please try again or see '--help' for more options.\n")
		exit(3)

#retrieve (-r) a hidden image from an image
def retrieve():
	wrapper_bin = file_to_bin(wrapper)[offset:]
	wrapLength = len(wrapper_bin)
	wrapIndex = 0
	wrapByte = wrapper_bin[wrapIndex]
	if(DEBUG):
		print(len(wrapper_bin))

	hiddenFile = []
	possibleSentinel = []
	psenIndex = 0
	senLegth = len(sentinel)

	sys.stdout.write("Converting to arrays of binary.\n")

	if (method == 1): # Byte method
		while (possibleSentinel != sentinel): #while we haven't found the sentinel
			while(psenIndex < senLegth):
				if(wrapIndex + interval >= wrapLength):
					del hiddenFile[:]
					print("Sentinel was not found... assuming there was no hidden data and exitting...")
					exit(0)
				else:
					wrapIndex += interval
					if(wrapByte == sentinel[psenIndex]):
						possibleSentinel.append(wrapByte)
						psenIndex += 1
					else:
						psenIndex = 0
					hiddenFile.append(wrapByte)
			###########################
		hiddenFile = hiddenFile[:len(hiddenFile)-senLegth]


	elif (method == 0): # Bit method
		return 0
	else:
		sys.stderr.write\
		("Method (bit/byte) not set, please try again or see '--help' for more options.\n")
		exit(3)

#################################################################################################################### Main Program #####

flag = ''

# parser to set/change different values
for i in sys.argv[1:]:
	temp = list(i)

	flag = ''.join(temp[0:2])

	# help menu
	if (i == '--help'):
		help()
	# store mode
	elif (flag == '-s'):
		mode = 0
	# retrieve mode
	elif (flag == '-r'):
		mode = 1
	# bit method
	elif (flag == '-b'):
		method =0
	# byte method
	elif (flag == '-B'):
		method = 1
	# offset value
	elif (flag == '-o'):
		offset = int(''.join(temp[2:]))
	# change default inverval value
	elif (flag == '-i'):
		interval = int(''.join(temp[2:]))
	# declare hidden file
	elif (flag == '-h'):
		hiddenFile = ''.join(temp[2:])
	# declare wrapper file
	elif (flag == '-w'):
		wrapper = ''.join(temp[2:])

	# catch-all error statement for invalid options
	else:
		sys.stderr.write("Invalid option : " + i + \
			", please try again, or use --help for more options.\n")
		exit(1)

# runs retrieve or store based on the mode
# includes error handling for errors that I encountered
try:
	if (mode == 1):
		retrieve()
	elif (mode == 0):
		store()
except IndexError:
	sys.stderr.write("Invalid mode... exitting with error code 2...\n")
	exit(2)
except NameError:
	sys.stderr.write\
	("Mode (store/retrieve) not set, please try again or see '--help' for more options.\n")
	exit(2)

# Program exits successfully
exit(0)