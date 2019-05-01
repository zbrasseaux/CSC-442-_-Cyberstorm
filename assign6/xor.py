import sys, string, re

###################validation###################

pipedBinary = sys.stdin.read()
byteList1 = []

for i in pipedBinary:
    byteList1.append(i)

# byte = pipedBinary.read(1)
# while byte != "":
#     pipedBinary.append(byte)
#     byte = byteList1.read(1)

byteList2 = []
with open("key2", "rb") as f:
    byte = f.read(1)
    while byte != "":
        byteList2.append(byte)
        byte = f.read(1)


decrypted = [ chr(ord(a) ^ ord(b)) for (a,b) in zip(byteList1, byteList2) ]
print("".join(decrypted))
