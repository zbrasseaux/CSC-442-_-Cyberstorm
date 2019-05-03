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

DEBUG = False

# global var declarations
interval = 1
sentinelInt = [0, 255, 0, 0, 255, 0]
sentinel = bytearray(sentinelInt)
# print(type(sentinel[0]))

def asciiout(h):
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
		
	# open files
	wrap = open(wrapper, 'rb')
	hide = open(hiddenFile, 'rb')

	# Get size of file to hide
	head_len = os.path.getsize(hiddenFile)
	# Get sizes of file to wrap the hidden in
	wrap_len = os.path.getsize(wrapper)

	# check to see if wrapper can hold the file
	if ((method == 1) and (head_len * interval + offset + 6) > wrap_len):
		print("Wrapper too small, must be at least " \
			+ str(head_len * interval + offset + 6) + " bytes")
		exit()
	elif ((method == 0) and (head_len * interval * 8 + offset + 6 * 8) > wrap_len):
		print("Wrapper too small, must be at least " \
			+ str(head_len * interval + offset + 6) + " bytes")
		exit()

	# print the header
	sys.stdout.buffer.write(wrap.read(offset)) 

	sys.stdout.flush()

	# Using byte method
	if (method == 1):
		for i in range(0, head_len):
			sys.stdout.flush()                
			asciiout(ord(hide.read(1)))        
			wrap.seek(wrap.tell() + 1)     
			for j in range(interval): 
				asciiout(ord(wrap.read(1)))  

		for i in range(6):
			sys.stdout.flush()                
			asciiout(sentinel[i])           
			wrap.seek(wrap.tell() + 1)  
			for j in range(interval):    
				asciiout(ord(wrap.read(1))) 
			
		next_byte = wrap.read(1)   
		while next_byte != b'': 
			sys.stdout.flush()     
			asciiout(ord(next_byte))  
			next_byte = wrap.read(1)

	# Using bit method
	else:
		for i in range(0, head_len):           
			sys.stdout.flush()             
			h = ord(hide.read(1))               
			for j in range(8):    
				# read the next wrapper bit            
				w = ord(wrap.read(1))             
				w &= 0b11111110                 
				w |= ((h & 0b10000000) >> 7)     
				asciiout(w)                     
				h = h + 1   
				# output ascii
				sys.stdout.buffer.write(wrap.read(interval))
				sys.stdout.flush()

		for i in range(6):                    
			sys.stdout.flush()          
			h = sentinel[i]                    
			for j in range(8):    
				# read the next wrapper bit            
				w = ord(wrap.read(1))        
				w &= 0b11111110              
				w |= ((h & 0b10000000) >> 7)   
				asciiout(w)      
				h = h + 1     
				# output ascii     
				sys.stdout.buffer.write(wrap.read(interval)) 
				sys.stdout.flush()
			
		next_byte = wrap.read(1)     
		while next_byte != b'':     
			sys.stdout.flush()      
			asciiout(ord(next_byte))    
			next_byte = wrap.read(1)

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
	hiddenFile = []
	possibleSentinel = [0] * 6
	senIndex = 0
	senLegth = len(sentinel)

	sys.stdout.write("Converting to arrays of binary.\n")

	if (method == 1): # Byte method
		while (possibleSentinel != sentinel): #while we haven't found the sentinel
			while(senIndex < senLegth):
				if(wrapIndex + interval >= wrapLength): #we did not find the sentinel before EOF
					print("Sentinel was not found... assuming there was no hidden data and exitting...")
					exit(0)
				else:
					wrapByte = wrapper_bin[wrapIndex]
					if(DEBUG):
						print(possibleSentinel)
						print("%s - %s" % (wrapByte, sentinel[senIndex]))
					wrapIndex += interval
					if(wrapByte == sentinel[senIndex]):
						possibleSentinel[senIndex] = wrapByte
						senIndex += 1
					else:
						possibleSentinel = [0] * 6
						senIndex = 0
					hiddenFile.append(wrapByte)
			###########################
		hiddenFile = hiddenFile[:len(hiddenFile)-senLegth]
		print("CONGRATS")

	elif (method == 0): # Bit method
		while (possibleSentinel != sentinel): #while we haven't found the sentinel
			wrapByte = 0
			for i in range(8):
				if(wrapIndex + interval >= wrapLength | wrapIndex >= wrapLength): #we did not find the sentinel before EOF
					print("Sentinel was not found... assuming there was no hidden data and exitting...")
					exit(0)
				else:
					wrapper_bin[wrapIndex] &= 1
					wrapper_bin[wrapIndex] <<= (7 - i)
					wrapByte |= wrapper_bin[wrapIndex]
					wrapIndex += interval
			###########################
			if(wrapByte == sentinel[senIndex]):
				possibleSentinel[senIndex] = wrapByte
				senIndex += 1
			else:
				possibleSentinel = [0] * 6
				senIndex = 0
			hiddenFile.append(wrapByte)
		hiddenFile = hiddenFile[:len(hiddenFile)-senLegth]
		print("CONGRATS")
	else:
		sys.stderr.write\
		("Method (bit/byte) not set, please try again or see '--help' for more options.\n")
		exit(3)

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