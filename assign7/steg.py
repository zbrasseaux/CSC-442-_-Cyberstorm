#!/usr/bin/env python

import sys
from PIL import Image
import binascii

####### Error Codes #######
# 0 : Exited with no issues
# 1 : Invalid flag
# 2 : No MODE set
# 3 : No METHOD set

# global var declarations

# INTERVAL defaults to 1
INTERVAL = 1

FLAG = ''
MODE = ''
METHOD = ''
OFFSET = ''
WRAPPER_FILE = ''
HIDDEN_FILE = ''

# 2 : No mode set

# interval defaults to 1
interval = 1


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
				# print(wrapper_bin)
				byte = file.read(1)
			except ValueError:
				break

	return out_bin

def test():
	'''some code to test that the different flags work'''

	print('Mode : ' + str(mode))

	try:
		print('Method : ' + str(method))
	except NameError:
		print("Method : Not set")

	print('Interval : ' + str(interval))

	try:
		print('Offset : ' + str(offset))
	except NameError:
		print("Offset : Not set")

	try:
		print('Hidden File : ' + hiddenFile)
	except NameError:
		print("Hidden File : Not set")

	try:
		print('Wrapper : ' + wrapper)
	except NameError:
		print("Wrapper : Not set")

def store():
	return 0

def retrieve():
	wrapper_bin = file_to_bin(wrapper)[offset:]

	sys.stdout.write("Converting to arrays of binary.\n")

	for byte in wrapper_bin:
		print(byte)

	# print(wrapper_bin)

	if (method == 1): # Byte method
		return 0
	elif (method == 0): # Bit method
		return 0
	else:
		sys.stderr.write\
		("Method (bit/byte) not set, please try again or see '--help' for more options.")

	# sys.stdout.write(binArr)


##### Main Program #####

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

test()

# runs retrieve or store based on the mode
# includes error handling for errors that I encountered
try:
	if (mode == 1):
		retrieve()
	elif (mode == 0):
		store()
except IndexError:
	sys.stderr.write("Invalid mode... Exiting with error code 2...\n")
	exit(2)
except NameError:
	sys.stderr.write\
	("Mode (store/retrieve) not set, please try again or see '--help' for more options.\n")
	exit(2)

# test()

# Program exits successfully
exit(0)