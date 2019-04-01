from ftplib import FTP
dirList = []
METHOD = 7



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
        
    print " "
    for f in range(len(convertBinary)):
        print convertBinary[f]
        
    return convertBinary

def conToInt(fullBinary):
    binaryInt = []
    for l in range(len(fullBinary)):
        binaryInt.append(int(fullBinary[l],2))
        
    print ""
    for y in range(len(binaryInt)):
        print binaryInt[y]
    return binaryInt

def conToASCII(binaryInt):
    ASCIIrep = [] 
    for u in range(len(binaryInt)):
        ASCIIrep.append(chr(binaryInt[u]))
    print ""
    print ASCIIrep
    return ASCIIrep

ftp = FTP('jeangourd.com')
ftp.login(user= 'anonymous', passwd = '')
ftp.retrlines('LIST',dirList.append)
ftp.quit()

for i in range(len(dirList)):
    print dirList[i]
print" "

filePermList = []
for i in range(len(dirList)):
    print dirList[i][0:10]
    filePermList.append(dirList[i][0:10])
    
#############################################################################################################################
    
if(METHOD == 7):
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
    #print ""
    #for l in range(len(filePermList)):
        #print filePermList[l]
            
## Removes the files marked to be ignored  
    for t in range(errorCounter):
        filePermList.remove("ERRONEOUS")

#Creates new list of files with only last 7 permissions included
    permList = []
    for o in range(len(filePermList)):
        permList.append(filePermList[o][3:10])
#Prints a list of file permissions now formatted to last 7 bits     
    print ""
    for y in range(len(permList)):
        print permList[y]
#Runs method to convert list to binary    
    fullBinary = conToBinary(permList)
#Runs method to convert binary list to integer
    binaryInt = conToInt(fullBinary)
#Runs method to convert integers to ASCII characters
    ASCII = conToASCII(binaryInt)
    print ASCII

elif(METHOD == 10):
    longString = ""
    for r in range(len(filePermList)):
        longString = longString + filePermList[0]
