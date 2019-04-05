'''
pass in command line arguments in this order: server, username, password, path, method (10 or 7)

example: python covert.py jeangourd.com anonymous "" ./10 10 >> appendResultToThisFile.txt

appending to the file is not necessary but it will store all of your results so I highly recommend doing it
'''
from ftplib import FTP
import sys

server = sys.argv[1]
user = sys.argv[2]
passwd = sys.argv[3]
directory = sys.argv[4]
METHOD = sys.argv[5]

dirList = []
PRINT = False

#Method to convert incoming data into a binary format
def conToBinary(filePermList):
    convertBinary = []
    for z in range(len(filePermList)):
        tempHolder = ""
        for i in range(len(filePermList[z])):
            if(filePermList[z][i] == "-"):
                tempHolder = tempHolder + "0"
            else:
                tempHolder = tempHolder + "1"
        convertBinary.append(tempHolder)
    if(PRINT):
        print("\nBinary Format:")
        for f in range(len(convertBinary)):
            print(convertBinary[f])  
    return convertBinary

#Method to convert incoming binary data into it's integer form
def conToInt(fullBinary):
    binaryInt = []
    for l in range(len(fullBinary)):
        binaryInt.append(int(fullBinary[l],2))
    if(PRINT):
        print("\nInteger Sum Format:")
        for y in range(len(binaryInt)):
            print(binaryInt[y])
    return binaryInt

#Converts integer number into corresponding ASCII character
def conToASCII(binaryInt):
    ASCIIrep = [] 
    for u in range(len(binaryInt)):
        ASCIIrep.append(chr(binaryInt[u]))
    if (METHOD == "10"):
        print("\nASCII translation for METHOD 10:")
    if (METHOD == "7"):
        print("\nASCII translation for METHOD 7:")
    print (''.join(ASCIIrep))
    return (ASCIIrep)

#Source for code testing, from the madlad himself
ftp = FTP(server)
ftp.login(user, passwd)
ftp.cwd(directory)
ftp.retrlines('LIST',dirList.append)
ftp.quit()

#Cuts incoming file data to strictly the permissions only
filePermList = []
for i in range(len(dirList)):
    #print dirList[i][0:10]
    filePermList.append(dirList[i][0:10])
    
#############################################################################################################################
#7 BIT CODE
if(METHOD == "7"):
## Determines if there is a permission in first 3, marks to ignore if true
    errorCounter = 0
    for i in range(len(filePermList)):
        #print "Running index {} of dirList, value is : {}".format(i, filePermList[i])
        for z in range(0,3):
            #print "Checking index {} of dirlist{}".format(z,i)
            if(filePermList[i][z] != "-"):
                #print"Found illegal value {}, marking index".format(filePermList[i][z])
                filePermList[i] = "ERRONEOUS"
                errorCounter += 1
                break
    if(PRINT):
        print("")
        for l in range(len(filePermList)):
            print(filePermList[l])
            
## Removes the files marked to be ignored  
    for t in range(errorCounter):
        filePermList.remove("ERRONEOUS")
#Creates new list of files with only last 7 permissions included
    permList = []
    for o in range(len(filePermList)):
        permList.append(filePermList[o][3:10])
#Prints a list of file permissions now formatted to last 7 bits
    if(PRINT):
        print("")
        for y in range(len(permList)):
            print(permList[y])
    fullBinary = conToBinary(permList)  #Runs method to convert list to binary  
    binaryInt = conToInt(fullBinary)    #Runs method to convert binary list to integer
    ASCII = conToASCII(binaryInt)   #Runs method to convert integers to ASCII characters
    
################################################################################################
#10 BIT CODE
if(METHOD == "10"):
    longString = []
    for r in range(len(filePermList)):
        longString.append(filePermList[r])
    if(PRINT):
        print("")
        print("String: {}".format(longString))

#Finds if the length is easily broken up into groups of 7, adds zeroes to the last one if not
    lengthString = len(longString)
    modVal = lengthString % 7
    if(PRINT):
        print("Mod Value: {}".format(modVal))
        
    if(modVal != 0):
        addValue = 8-modVal
        if(PRINT):
            print("Modulus is not 0, adding {} to final sequence...".format(addValue))
            print(longString[-1])
            
        longString[-1] = ("-"*addValue) + longString[-1]
        
        if(PRINT):
            print(longString[-1])
            print("\nNew String (still in list format): {}".format(longString))
            
    newString = ""
    for n in range(len(longString)):
        newString += longString[n]
            
    if(PRINT):
        print("New String in comprehensive format: {}".format(newString))
        print("Length%7: {}".format(len(newString)%7))

    bit7Convert = []
    for v in range(len(newString)/7):
        bit7Convert.append(newString[(7*v):(7+(7*v))])
    if(PRINT):
        print("\nConverted to bit7 format: ")
        for b in range(len(bit7Convert)):
            print(bit7Convert[b])
            
#Runs method to convert list to binary    
    fullBinary = conToBinary(bit7Convert)
#Runs method to convert binary list to integer
    binaryInt = conToInt(fullBinary)
#Runs method to convert integers to ASCII characters
    ASCII = conToASCII(binaryInt)
else:
    print("Please enter a 7 or 10 into the METHOD variable, other values will not be accepted.")
    exit(0);
