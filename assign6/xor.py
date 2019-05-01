'''
Team Celtics

Link to private GitHub:
https://github.com/zbrasseaux/CSC-442-_-Cyberstorm

If you need access to it, please email any of out members.


Use: This script can be used to either encrypt or decrypt a binary file using a key that is in the same directory.

'''

import sys, string, re

pipedBinary = sys.stdin.read()
byteList1 = []

for i in pipedBinary:
    byteList1.append(i)

byteList2 = []
with open("key2", "rb") as f: # The "key2" can be changed to any key that is needed as long as it is in the same directory as this file
    byte = f.read(1)
    while byte != "":
        byteList2.append(byte)
        byte = f.read(1)


decrypted = [ chr(ord(a) ^ ord(b)) for (a,b) in zip(byteList1, byteList2) ]
print("".join(decrypted))
