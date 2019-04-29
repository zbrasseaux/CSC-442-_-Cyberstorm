#!/usr/bin/env python

import sys
from PIL import Image

####### Error Codes #######
# 0 : Exited with no issues
# 1 : Invalid flag
<<<<<<< HEAD
# 2 : No MODE set

# global var declarations

# INTERVAL defaults to 1
INTERVAL = 1

FLAG = ''
MODE = ''
METHOD = ''
OFFSET = ''
WRAPPER_FILE = ''
HIDDEN_FILE = ''
=======
# 2 : No mode set

# interval defaults to 1
interval = 1
>>>>>>> 9c079fc6676f4c298599b1594ea56e56e39b921e

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

def test():
<<<<<<< HEAD
	'''some code to test that the different flags work'''
	print('Mode : ' + str(MODE))
	print('Method : ' + str(METHOD))
	print('Interval : ' + str(INTERVAL))
	print('Offset : ' + str(OFFSET))
	print('Hidden File : ' + HIDDEN_FILE)
	print('Wrapper : ' + WRAPPER_FILE)
=======
	print('Mode : ' + str(mode))
	print('Method : ' + str(method))
	print('Interval : ' + str(interval))
	print('Offset : ' + str(offset))
	print('Hidden File : ' + hiddenFile)
	print('Wrapper : ' + wrapper)
>>>>>>> 9c079fc6676f4c298599b1594ea56e56e39b921e

def store():
	return 0

def retrieve():
	return 1
<<<<<<< HEAD
	

##### Main Program #####

def main():
	'''parser to set/change different values'''
	for i in sys.argv[1:]:
		temp = list(i)

		FLAG = ''.join(temp[0:2])

		# help menu
		if (i == '--help'):
			help()
		# store MODE
		elif (FLAG == '-s'):
			MODE = 0
		# retrieve MODE
		elif (FLAG == '-r'):
			MODE = 1
		# bit METHOD
		elif (FLAG == '-b'):
			METHOD =0
		# byte METHOD
		elif (FLAG == '-B'):
			METHOD = 1
		# OFFSET value
		elif (FLAG == '-o'):
			OFFSET = int(''.join(temp[2:]))
		# change default inverval value
		elif (FLAG == '-i'):
			INTERVAL = int(''.join(temp[2:]))
		# declare hidden file
		elif (FLAG == '-h'):
			HIDDEN_FILE = ''.join(temp[2:])
		# declare WRAPPER_FILE file
		elif (FLAG == '-w'):
			WRAPPER_FILE = ''.join(temp[2:])

		# catch-all error statement for invalid options
		else:
			sys.stderr.write("Invalid option : " + i + \
				", please try again, or use --help for more options.\n")
			exit(1)

	# runs retrieve or store based on the MODE
	# includes error handling for errors that I encountered

	try:
		if (MODE == 1):
			retrieve()
		elif (MODE == 0):
			store()
	except NameError:
		sys.stderr.write\
		("Mode (store/retrieve) not set, please try again or see '--help' for more options.\n")
		exit(2)

main()
=======

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
	sys.stderr.write("Invalid mode... Exiting with error code 2...\n")
	exit(2)
except NameError:
	sys.stderr.write\
	("Mode (store/retrieve) not set, please try again or see '--help' for more options.\n")
	exit(2)

>>>>>>> 9c079fc6676f4c298599b1594ea56e56e39b921e
# Program exits successfully
exit(0)