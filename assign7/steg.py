#!/usr/bin/env python


'''I am currently running the command python steg.py -B -r -o1024 -i8 -wstegged-byte.bmp >> test.txt so I can the the entirety of the output'''
import sys
import binascii
from PIL import Image

####### Error Codes #######
# 0 : Exited with no issues
# 1 : Invalid flag
# 2 : No MODE set
# 3 : No METHOD set

DEBUG = True

# global var declarations
FLAG = ''
MODE = ''
METHOD = ''
OFFSET = ''
INTERVAL = 1
WRAPPER_FILE = ''
HIDDEN_FILE = ''

interval = INTERVAL

sentinelInt = [0, 255, 0, 0, 255, 0]
sentinel = bytearray(sentinelInt)

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
		data = file.read()
		out_bin = bytearray(data)
	return out_bin

#store (-s) a hidden image within an image
def store(offset):
	#get hidden and wrapper binary
	hidden_bin = file_to_bin(hiddenFile)
	wrapper_bin = file_to_bin(wrapper)
	if (method == 1): # Byte method
		i = 0
		#until we reach the end of the hidden message
		while(i < len(hidden_bin)):
			#skip the offset and begin inserting the hidden image
			wrapper_bin[offset] = hidden_bin[i]
			#increase index to the next interval
			offset += interval
			i+=1
		###########################
		#until we reach the end of the setinel
		while(i < len(sentinel)):
			#continue at the place we left off previously and insert the sentinel
			wrapper_bin[offset] = sentinel[i]
			#increase index to the next interval
			offset += interval
			i+=1
		###########################
	elif (method == 0): # Bit method
		i = offset
		j = 0
		#concatenate the hidden message and sentinel so we can insert the message and sentinal at once
		hidden_bin += sentinel
		#until we reach the end of the hidden file (and the sentinel)
		while(j < len(hidden_bin)):
			for k in range(8):
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
	print("Your hidden image has been successfully inserted into the given wrapper file!")

#retrieve (-r) a hidden image from an image
def retrieve():
	#get the wrapper image's binary
	wrapper_bin = file_to_bin(wrapper)
	if(DEBUG):
		print("WRAPPER BEGINS")
		for b in wrapper_bin:
			print(b)
	wrapLength = len(wrapper_bin)
	#wrapIndex 
	wrapIndex = 0
	if(DEBUG):
		print("LENGTH OF WRAPPER")
		print(len(wrapper_bin))

	#array to store the hidden file we are going to retrieve
	hiddenBytes = []

	#create an empty array that we will fill as we match values in the wrapper_bin to the sentinel
	possibleSentinel = [0] * 6
	senIndex = 0
	senLegth = len(sentinel)

	sys.stdout.write("Converting to arrays of binary.\n")

	if (method == 1): # Byte method
		#while we haven't found the sentinel
		while (possibleSentinel != sentinel):
			while(senIndex < senLegth):
				#we did not find the sentinel before EOF
				if(wrapIndex + interval >= wrapLength):
					print("Sentinel was not found... assuming there was no hidden data and exitting...")
					exit(0)
				#not EOF yet
				else:
					#get the byte at the current index			
					wrapByte = wrapper_bin[wrapIndex]
					if(DEBUG):
						print(possibleSentinel)
						print("%s - %s" % (wrapByte, sentinel[senIndex]))
					wrapIndex += interval
					#if the byte matches the sentinel
					if(wrapByte == sentinel[senIndex]):
						# print("MATCH...")
						#then add the byte to the possibleSentinel
						possibleSentinel[senIndex] = wrapByte
						# print(possibleSentinel)
						#and go to the next byte in the possibleSentinel
						senIndex += 1
					#there was no match
					else:
						#reset the possibleSentinel
						possibleSentinel = [0] * 6
						#start over at the first byte of the possibleSentinel
						senIndex = 0
					#append the byte to the hiddenFile regardless if we found a match or not
					hiddenBytes.append(wrapByte)
			###########################
		#once we are here, we must have found a sentinel, so remove it from the hiddenFile
		hiddenBytes = hiddenBytes[:len(hiddenFile)-senLegth]
		print("A hidden file has been retrieved!\n%s" % hiddenFile)

	elif (method == 0): # Bit method
		#while we haven't found the sentinel
		while (possibleSentinel != sentinel):
			wrapByte = 0
			for i in range(8):
				#we did not find the sentinel before EOF
				if(wrapIndex + interval >= wrapLength | wrapIndex >= wrapLength):
					print("Sentinel was not found... assuming there was no hidden data and exitting...")
					exit(0)
				#not EOF yet
				else:
					#preserve the right most bit
					wrapper_bin[wrapIndex] &= 1
					#shift the right most bit over
					wrapper_bin[wrapIndex] <<= (7 - i)
					wrapByte |= wrapper_bin[wrapIndex]
					wrapIndex += interval
			###########################
			#if the byte matches the sentinel
			if(wrapByte == sentinel[senIndex]):
				#then add the byte to the possibleSentinel
				possibleSentinel[senIndex] = wrapByte
				#and go to the next byte in the possibleSentinel
				senIndex += 1
			#there was no match
			else:
				#reset the possibleSentinel
				possibleSentinel = [0] * 6
				#start over at the first byte of the possibleSentinel
				senIndex = 0
			hiddenBytes.append(wrapByte)
		#once we are here, we must have found a sentinel, so remove it from the hiddenFile
		hiddenBytes = hiddenBytes[:len(hiddenBytes)-senLegth]
		print("A hidden file has been retrieved!\n%s" % hiddenFile)
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
# try:
if (mode == 1):
	retrieve()
elif (mode == 0):
	store(offset)
# except IndexError:
# 	sys.stderr.write("Invalid mode... exitting with error code 2...\n")
# 	exit(2)
# except NameError:
# 	sys.stderr.write\
# 	("Mode (store/retrieve) not set, please try again or see '--help' for more options.\n")
# 	exit(2)

# Program exits successfully
exit(0)