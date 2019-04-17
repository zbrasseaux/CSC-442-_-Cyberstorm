#!/usr/bin/env python

import sys

####### Error Codes #######
# 0 : Exited with no issues
# 1 : Invalid flag
# 2 : No mode set

# interval defaults to 1
interval = 1

# help fxn that gives the usage and options
def help():
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

# some code to test that the different flags work
def test():
	print('Mode : ' + str(mode))
	print('Method : ' + str(method))
	print('Interval : ' + str(interval))
	print('Offset : ' + str(offset))
	print('Hidden File : ' + hiddenFile)
	print('Wrapper : ' + wrapper)

def store():
	return 0

def retrieve():
	return 1

# parser to set/change different values
for i in sys.argv[1:]:
	temp = list(i)

	# help menu
	if (i == '--help'):
		help()
	# store mode
	elif (temp[1] == 's'):
		mode = 0
	# retrieve mode
	elif (temp[1] == 'r'):
		mode = 1
	# bit method
	elif (temp[1] == 'b'):
		method =0
	# byte method
	elif (temp[1] == 'B'):
		method = 1
	# offset value
	elif (temp[1] == 'o'):
		offset = int(''.join(temp[2:]))
	# change default inverval value
	elif (temp[1] == 'i'):
		interval = int(''.join(temp[2:]))
	# declare hidden file
	elif (temp[1] == 'h'):
		hiddenFile = ''.join(temp[2:])
	# declare wrapper file
	elif (temp[1] == 'w'):
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
	sys.stderr.write("Invalid mode... Exiting with error code 2...\n")
	exit(2)
except NameError:
	sys.stderr.write\
	("Mode (store/retrieve) not set, please try again or see '--help' for more options.\n")
	exit(2)

# Program exits successfully
exit(0)