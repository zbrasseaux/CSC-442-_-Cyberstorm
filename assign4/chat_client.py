'''
Team Celtics

Link to private GitHub:
https://github.com/zbrasseaux/CSC-442-_-Cyberstorm

If you need access to it, please email any of out members.
'''

# Library imports
import socket
from time import time
import sys
import binascii


# For best results use wired connection

# address and ports
address = 'jeangourd.com'
port = 31337

# empty strings to be filled with data
covert_bin = ""
covert = ""

# initializing connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))

# allows for the recieving of packets
data = s.recv(4096)

# accepts and iterated through the overt message
while (data.rstrip("\n") != "EOF"):
	sys.stdout.write(data)
	sys.stdout.flush()

	# calculates time between characters
	t0 = time()
	data = s.recv(4096)
	t1 = time()

	# rounds the time to 3 decimal places
	delta = round(t1 - t0, 3)

<<<<<<< HEAD
	# determines a one or a zero for the time
	if (delta >= .07): # can be changed in the future to improve accuracy
=======
	if (delta >= .095): # can be changed in the future to improve accuracy
>>>>>>> 9c079fc6676f4c298599b1594ea56e56e39b921e
		covert_bin += "1"
	else:
		covert_bin += "0"

# terminates the connection
s.close()

i = 0
while (i < len(covert_bin)):

	# process one byte at a time
	b = covert_bin[i:i + 8]
	# convert it to ASCII
	n = int("0b{}".format(b), 2)

	# attempt to convert binary to ascii chars
	# if it fails, it uses '?'
	try:
		covert += binascii.unhexlify("{0:x}".format(n))
	except TypeError:
		covert += "?"
	
	# stop at the string "EOF"
	i += 8

# outputs the final string w/o the 'EOF?'
print(covert.rstrip("EOF?"))
