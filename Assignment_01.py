'''
Ankit Aryal
Assignmrnt 1 rough. 
'''

import os
import sys


#if no file is specified:

print ("Enter some binary numbers: ")
Data = sys.stdin.readline()



Data = Data[:-1]

n = 7

if len(Data) % 8 == 0:
    n = 8

groups = []

result =[]

while Data:

    
    groups.append(Data[:n])

    Data = Data[n:]

print(groups)

j = 0 

while j < len(groups):

    #actual conversion. 
    convert = int((groups[j]), 2)

    j += 1

    result.append(convert)

print(''.join(map(chr,result)))
