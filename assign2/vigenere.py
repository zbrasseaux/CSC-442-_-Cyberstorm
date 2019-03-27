#!/usr/bin/env python3
import sys

def cipher(key, inString):
	print(key, inString)

if (sys.argv[-2] == '-e' or sys.argv[-2] == '--encrypt'):
	inString = input()
	cipher(sys.argv[-1], inString)

elif (sys.argv[-2] == '-d' or sys.argv[-2] == '--decrypt'):
	inString = input()
	cipher(sys.argv[-1], inString)

else:
	print("Invalid option, please try again.")
