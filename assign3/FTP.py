#!/usr/bin/env python
import sys
from ftplib import FTP
import os

#python.py -m/a
#Input scheme: python.py -m/a website username password port path method
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
    if(PRINT == True):
        print("\nBinary Format:")
        for f in range(len(convertBinary)):
            print(convertBinary[f])  
    return convertBinary

#Method to convert incoming binary data into it's integer form
def conToInt(fullBinary):
    binaryInt = []
    for l in range(len(fullBinary)):
        binaryInt.append(int(fullBinary[l],2))
    if(PRINT == True):
        print("\nInteger Sum Format:")
        for y in range(len(binaryInt)):
            print(binaryInt[y])
    return binaryInt

#Converts integer number into corresponding ASCII character
def conToASCII(binaryInt):
    ASCIIrep = [] 
    for u in range(len(binaryInt)):
        ASCIIrep.append(chr(binaryInt[u]))
    #print("\nASCII translation:")
    print (''.join(ASCIIrep))
    return (ASCIIrep)

################################################################################################
def BIT7(filePermList, PRINT):
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
    if(PRINT == True):
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
    if(PRINT == True):
        print("")
        for y in range(len(permList)):
            print(permList[y])
    fullBinary = conToBinary(permList)  #Runs method to convert list to binary  
    binaryInt = conToInt(fullBinary)    #Runs method to convert binary list to integer
    ASCII = conToASCII(binaryInt)   #Runs method to convert integers to ASCII characters
################################################################################################



################################################################################################
#10 BIT CODE
def BIT10(filePermList, PRINT):
    longString = []
    for r in range(len(filePermList)):
        longString.append(filePermList[r])
        
    if(PRINT == True):
        print("")
        print("String: {}".format(longString))  
    newString = ""
    for n in range(len(longString)):
        newString += longString[n]  

    if(PRINT == True):
        print("New String in comprehensive format: {}".format(newString))
        print("Length%7: {}".format(len(newString)%7))

#Converts the now finished string of 10 bit to groups of 7 bits
    bit7Convert = []
    for v in range(len(newString)/7):
        bit7Convert.append(newString[(7*v):(7+(7*v))])
    if(PRINT == True):
        print("\nConverted to bit7 format: ")
        for b in range(len(bit7Convert)):
            print(bit7Convert[b])
#Finds if the length is easily broken up into groups of 7, adds zeroes to the last one if not
    lengthString = len(longString)
    modVal = lengthString % 7
    if(PRINT == True):
        print("Mod Value: {}".format(modVal))

    if(modVal != 0):
        addValue = 8-modVal
        if(PRINT == True):
            print("Modulus is not 0, adding {} to final sequence...".format(addValue))
            print(longString[-1])

        longString[-1] = ("-"*addValue) + longString[-1]  

        if(PRINT == True):
            print(longString[-1])
            print("\nNew String (still in list format): {}".format(longString))
#Runs method to convert list to binary    
    fullBinary = conToBinary(bit7Convert)
#Runs method to convert binary list to integer
    binaryInt = conToInt(fullBinary)
#Runs method to convert integers to ASCII characters
    ASCII = conToASCII(binaryInt)



############################ MAIN CODE #############################################

def getData():
    dirList = []
    ftp.retrlines('LIST',dirList.append)
    filePermList = []
    for i in range(len(dirList)):
        #print dirList[i][0:10]
        filePermList.append(dirList[i][0:10])
    return filePermList

def getConnectionInfo():
    try:
        WEBSITE = sys.argv[2]
    except(IndexError):
        WEBSITE = raw_input("Please enter the website to connect to")
    try:
        USERNAME = sys.argv[3]
    except(IndexError):
        USERNAME = raw_input("Please enter the username")
    try:
        PASSWORD = sys.argv[4]
    except(IndexError):
        PASSWORD = raw_input("Please enter the password")
    try:
        PORT = sys.argv[5]
    except(IndexError):
        PORT = raw_input("Please enter the port to connect with, or type default")
    try:
        PATH = sys.argv[6]
    except(IndexError):
        PATH = raw_input("Please enter the path, or type default")
    try:
        METHOD = sys.argv[7]
    except(IndexError):
        METHOD = raw_input("Please enter the method of decryption")
    connectionData = [WEBSITE,USERNAME,PASSWORD,PORT,PATH,METHOD]
    return connectionData

try:
    connectType = sys.argv[1]
    connectionInfo = getConnectionInfo()
except(IndexError):
    print("Did not specify manual or auto, defaulting to auto")
    connectionInfo = getConnectionInfo()
    connectType = '-r'
if(PRINT):
	print("Website: {}".format(connectionInfo[0]))
	print("Username: {}".format(connectionInfo[1]))
	print("Password: {}".format(connectionInfo[2]))
	print("Port: {}".format(connectionInfo[3]))
	print("Path: {}".format(connectionInfo[4]))
	print("Method: {}".format(connectionInfo[5]))
ftp = FTP()
if(connectionInfo[3] == 'default'):
    ftp.connect(connectionInfo[0])
else:
    ftp.connect(connectionInfo[0],connectionInfo[3])
ftp.login(user = connectionInfo[1], passwd = connectionInfo[2])
if(connectionInfo[4] == 'default'):
    print("No set path to direct to")
else:

    ftp.cwd(str(connectionInfo[4]))

if(connectType == '-r'):
    serverData = getData()
elif(connectType == '-m'):
    manual = True
    while(manual == True):
        command = raw_input("Please enter a command")
        if(command == '-r'):
            serverData = getData()
            manual = False
        else:
            try:
                ftp.voidcmd(command)
            except():
                print("Did not work")
ftp.close()
if(int(connectionInfo[5]) == 7):
    BIT7(serverData,PRINT)
elif(int(connectionInfo[5]) == 10):
    BIT10(serverData,PRINT)
else:
    print("Please enter a 7 or 10 into the METHOD variable, other values will not be accepted.")

    exit(0);
