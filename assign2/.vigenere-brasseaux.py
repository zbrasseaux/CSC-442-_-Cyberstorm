#!/usr/bin/env python3
import sys

alphabet_length = 26

def strToAscii(inArr):
	temp = []
	for char in inArr:
		temp.append(ord(char))

	return temp

def asciiToStr(inArr):
	temp = ""

	for char in inArr:
		temp = temp + chr(char)

	return temp

def encrypt(key, inString):
	finArr = []

	key = strToAscii(list(key))
	inString = strToAscii(list(inString))

	for i in range(0,len(inString)):
		kval = i%len(key)
		finArr.append((inString[i] + key[kval]) % alphabet_length)

	print(asciiToStr(finArr))

def decrypt(key, inString):
	finArr = []

	key = strToAscii(list(key))
	inString = strToAscii(list(inString))

	for i in range(0,len(inString)):
		kval = i%len(key)
		finArr.append((inString[i] - key[kval]) % alphabet_length)

	print(asciiToStr(finArr))

if (sys.argv[-2] == '-e' or sys.argv[-2] == '--encrypt'):
	inString = input()
	encrypt(sys.argv[-1], inString)

elif (sys.argv[-2] == '-d' or sys.argv[-2] == '--decrypt'):
	inString = input()
	decrypt(sys.argv[-1], inString)

else:
	print("Invalid option, please try again.")
