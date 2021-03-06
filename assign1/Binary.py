'''
Team Celtics

Link to private GitHub:
https://github.com/zbrasseaux/CSC-442-_-Cyberstorm

If you need access to it, please email any of out members.
'''

# Pseudocode
'''
break binary into groups of 7 or 8 (if-elif statements)
convert each block from binary to decimal
convert from decimal to ascii
add to empty string
return final string
'''

import sys

# reading in the file without the newline char
file_input = sys.stdin.read().rstrip()

# empty string that characters will be added to as they are decoded
final_string = ''

# function to split the string into an array of a specific length
# Big-O = n where n = length of instr
def splitStr(instr, length):
	instr = list(instr)
	strArr = []

	for i in range(0,len(instr), length):
		yield instr[i:i + length]

# function to convert each smaller array to a string
# so it can be converted to binary, then to decimal
# so that it can be decoded
def arrToStr(inArr):
	output = ''

	for i in inArr:
		output = output + ''.join(str(i))

	return output

# figures out the appropriate length for the splitStr fxn
# Big-O = 1*n where n = length of standard input
if (len(file_input)%7 == 0):
	input_list = list(splitStr(file_input, 7))
elif (len(file_input)%8 == 0):
	input_list = list(splitStr(file_input, 8))

# if the input is invalid, outputs this message to stderr
else:
	sys.stderr.write("Input file could not be read.\n")
	exit(1)

# an array to hold the chars once in binary form
charArrs = []

# converts each sub list to a string of 1's and 0's
# Big-O = n/7 or n/8 where n = length of standard input
for char in input_list:
	charArrs.append(arrToStr(char))

# converts from binary to int, then to char and
# adds it to an empty string
# Big-O = n/7 or n/8 where n = length of standard input
for char in charArrs:
	temp = int(char, base=2)
	final_string = final_string + chr(temp)

# Final Big-O = 1*n + n/7 + n/7
# 			  = n
# Therefore the runtime is linear
# based on the size of the standard input

# outputs to standard out
sys.stdout.write(final_string + '\n')
exit(0)
