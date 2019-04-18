import socket
from time import time
import sys
import binascii


address = 'www.jeangourd.com'
port = 31337

covert_bin = ""
covert = ""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))

data = ""

# print(data)

while (data.rstrip("\n") != "EOF"):

	t0 = time()
	data = s.recv(4096)
	t1 = time()

	delta = round(t1 - t0, 3)

	# print(delta)

	if (delta >= .08):
		covert_bin += "1"
	else:
		covert_bin += "0"

	sys.stdout.write(data)
	sys.stdout.flush()

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
print(covert_bin)
