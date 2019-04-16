'''
Team Celtics

Link to private GitHub:
https://github.com/zbrasseaux/CSC-442-_-Cyberstorm

If you need access to it, please email any of out members.
'''

import socket
from time import time
import sys
import binascii


# For best results use wired connection

address = 'www.jeangourd.com'
port = 31337

covert_bin = ""
covert = ""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))

data = s.recv(4096)

while (data.rstrip("\n") != "EOF"):
	sys.stdout.write(data)
	sys.stdout.flush()

	t0 = time()
	data = s.recv(4096)
	t1 = time()

	delta = round(t1 - t0, 3)

	if (delta >= .07): # can be changed in the future to improve accuracy
		covert_bin += "1"
	else:
		covert_bin += "0"

s.close()

i = 0
while (i < len(covert_bin)):

	# process one byte at a time
	b = covert_bin[i:i + 8]
	# convert it to ASCII
	n = int("0b{}".format(b), 2)

	try:
		covert += binascii.unhexlify("{0:x}".format(n))
	except TypeError:
		covert += "?"
	
	# stop at the string "EOF"
	i += 8

print(covert.rstrip("EOF?"))
