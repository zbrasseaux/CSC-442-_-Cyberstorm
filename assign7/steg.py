#!/usr/bin/env python


'''I am currently running the command python steg.py -B -r -o1024 -i8 -wstegged-byte.bmp >> test.txt so I can the the entirety of the output'''
import sys
import binascii
import os

####### Error Codes #######
# 0 : Exited with no issues
# 1 : Invalid flag
# 2 : No MODE set
# 3 : No METHOD set

DEBUG = True

# global var declarations
interval = 1
sentinelInt = [0, 255, 0, 0, 255, 0]
sentinel = bytearray(sentinelInt)
# print(type(sentinel[0]))

def printr(h):
	sys.stdout.buffer.write(bytes([h]))

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
		# print(out_bin[0])
	return out_bin

#store (-s) a hidden image within an image
def store():
		
	wrap = open(wrapper, 'rb')
	hide = open(hiddenFile, 'rb')

	h_size = os.path.getsize(hiddenFile)
	# Get sizes of file to hide
	w_size = os.path.getsize(wrapper)

	if ((method == 1) and (h_size * interval + offset + 6) > w_size):
		print("Wrapper too small, must be at least " + str(h_size * interval + offset + 6) + " bytes")
		exit()
	elif ((method == 0) and (h_size * interval * 8 + offset + 6 * 8) > w_size):
		print("Wrapper too small, must be at least " + str(h_size * interval + offset + 6) + " bytes")
		exit()
	# Make sure given wrapper is large enough to store the hidden file inside
		
	# At this point, ready to hide file
	sys.stdout.buffer.write(wrap.read(offset))         # Print header
	sys.stdout.flush()

	if (method == 1):
		# Using byte method

		for i in range(h_size):
			sys.stdout.flush()                 # flush it
			printr(ord(hide.read(1)))          # print a byte of the hidden file
			wrap.seek(wrap.tell() + 1)         # skip a byte of the wrapper
			for j in range(interval):            # 
				printr(ord(wrap.read(1)))  # print 'i' bytes of the wrapper

		for i in range(6):
			sys.stdout.flush()                    # flush it
			printr(sentinel[i])                   # print raw byte of sentinel
			wrap.seek(wrap.tell() + 1)            # skip a byte of the wrapper
			for j in range(interval):               # 
				printr(ord(wrap.read(1)))     # print 'i' bytes of the wrapper
			
		next_byte = wrap.read(1)                   #
		while next_byte != b'':                    #
			sys.stdout.flush()                 #
			printr(ord(next_byte))             #
			next_byte = wrap.read(1)           # print the rest of the wrapper
	else:
		# Using bit method

		for i in range(h_size):                           #
			sys.stdout.flush()                        # Flush it
			h = ord(hide.read(1))                     # Get next byte to hide
			for j in range(8):                        # 
				w = ord(wrap.read(1))             # ^ Read next wrapper byte
				w &= 0b11111110                   # ^ Set LSB to 0
				w |= ((h & 0b10000000) >> 7)      # ^ Shift MSB of h to LSB of w
				printr(w)                         # ^ Print raw byte
				h <<= 1                           # ^ Shift in next byte of h
				sys.stdout.buffer.write(wrap.read(interval)) # Skip interval
				sys.stdout.flush()

		for i in range(6):                                #
			sys.stdout.flush()                        # Flush it
			h = sentinel[i]                           # Get next byte of sentinel
			for j in range(8):                        # 
				w = ord(wrap.read(1))             # ^
				w &= 0b11111110                   # ^
				w |= ((h & 0b10000000) >> 7)      # ^
				printr(w)                         # ^
				h <<= 1                           # ^
				sys.stdout.buffer.write(wrap.read(interval)) # Skip interval
				sys.stdout.flush()
			
		next_byte = wrap.read(1)                   #
		while next_byte != b'':                    #
			sys.stdout.flush()                 #
			printr(ord(next_byte))             #
			next_byte = wrap.read(1)           # print the rest of the wrapper
	# except NameError:
	# 	print("Hidden file not set.")
	# 	exit()

#retrieve (-r) a hidden image from an image
def retrieve():
	wrapper_bin = file_to_bin(wrapper)[offset:]
	if(DEBUG):
		for b in wrapper_bin:
			print(b)
	wrapLength = len(wrapper_bin)
	wrapIndex = 0
	if(DEBUG):
		print(len(wrapper_bin))
	hiddenBytes = []
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
		hiddenBytes = hiddenBytes[:len(hiddenBytes)-senLegth]
		print("A hidden file has been retrieved!\n%s" % hiddenBytes)

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
		print("A hidden file has been retrieved!\n%s" % hiddenBytes)
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
		val = ''.join(temp[2:])
		offset = int(val)
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
	store()
# except IndexError:
# 	sys.stderr.write("Invalid mode... exitting with error code 2...\n")
# 	exit(2)
# except NameError:
# 	sys.stderr.write\
# 	("Mode (store/retrieve) not set, please try again or see '--help' for more options.\n")
# 	exit(2)

# Program exits successfully
exit(0)