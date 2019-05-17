#!/usr/bin/env python2

#WHAT TEAM!? CELTS!
#Paige Meeks redo of steg:
#implements both the bit and byte methods of storing
#and retrieving the hidden data
#NOTE: this is Python 2 (denoted by the ...Py2.py)

import sys

#NOTE: both debug modes need to be turned off as to output just the image
DEBUG = False
#extreme debug will print out a lot of information (it's best to direct the output to a text file when this is enabled)
XDEBUG = False

#marks the end of the hidden file
SENTINEL = bytearray([0, 255, 0, 0, 255, 0])

#variables to store the user's parameters
method = 0
mode = 0
offset = 0
interval = 1
wrapperFile = ""
hiddenFile = ""

######################################################################################################## retrieve parameters ########################
'''
python steg.py -(bB) -(sr) -o<val> [-i<val>] -w<val> [-h<val>]
    -b          use bit method
    -B          use byte method
    -s          store/hide data
    -r          retrieve stored/hidden data
    -o<val>     set offset to <val>
    -i<val>     set interval to <val>
    -w<val>     set wrapper file to <val>
    -h<val>     set hidden file to <val>
'''

def getParameters():
    # parser to set/change different values
    for i in sys.argv[1:]:
        global method
        global mode
        global offset
        global interval
        global wrapperFile
        global hiddenFile

        temp = list(i)

        flag = ''.join(temp[0:2])

        #bit method
        if (flag == '-b'):
            method = 0
            if(DEBUG):
                print("method: %s" % method)
        #byte method
        elif (flag == '-B'):
            method = 1
            if(DEBUG):
                print("method: %s" % method)
        #store mode
        elif (flag == '-s'):
            mode = 0
            if(DEBUG):
                print("mode: %s" % mode)
        #retrieve mode
        elif (flag == '-r'):
            mode = 1
            if(DEBUG):
                print("mode: %s" % mode)
        #offset value
        elif (flag == '-o'):
            offset = int(''.join(temp[2:]))
            if(DEBUG):
                print("offset: %s" % offset)
        #interval value
        elif (flag == '-i'):
            interval = int(''.join(temp[2:]))
            if(DEBUG):
                print("interval: %s" % interval)
        #declare wrapper file
        elif (flag == '-w'):
            wrapperFile = ''.join(temp[2:])
            if(DEBUG):
                print("wrapper: %s" % wrapperFile)
        #declare hidden file
        elif (flag == '-h'):
            hiddenFile = ''.join(temp[2:])
            if(DEBUG):
                print("hidden: %s" % hiddenFile)
        # catch-all error statement for invalid options
        else:
            print("ERROR! Invalid option : " + i + ". Please try again...\n")
            exit(1)

############################################################################################################### main program ########################

def readFile(file):
    #open the file and read it as binary
    with open(file, "rb") as f:
        #this spits out string representation of byte objects
        rawFile = f.read()
        #create a byte array which converts the string byte objects to decimals
        byteFile = bytearray(rawFile)
        if(XDEBUG):
            print("Byte array of %s" % file)
            for i in byteFile:
                print(byteFile[i])
    return byteFile

def retrieve(wrapperFileData, method, mode, offset, interval):

    #make array of the maximum hidden file size to store the hidden data in
    hiddenData = [0] * maxHiddenFileSize(wrapperFileData)
    #skip the offset
    wrapperFileData = wrapperFileData[offset:]

    #byte method
    if(method == 1):
        i = 0
        j = 0
        #while we haven't reached the end of the wrapper file
        while(i + interval < len(wrapperFileData)):
            #store the value of the wrapper file at the current interval into the output array
            hiddenData[j] = wrapperFileData[i]
            #increment by the interval
            i += interval
            #but only move over one position for the hidden data
            j+=1
            #first check if there are at least 6 bytes in the hidden data array and then check if the sentinel has been found
            if(j >= (len(SENTINEL)-1) and bytearray(hiddenData[j-6:j]) == SENTINEL):
                if(DEBUG):
                    print "A sentinel was found!"
                return hiddenData[:-6]
        #if we have reached here, then a sentinel was not found
        print("Sentinel was not found! Exiting...")
        exit(0)


    #bit method
    else:
        i = 0
        j = 0
        #while we haven't reached the end of the wrapper file
        while(i + interval < len(wrapperFileData) or i < len(wrapperFileData)):
            byte = 0
            #go through each bit of the byte
            for k in range(8):
                #preserve the LSB
                wrapperFileData[i] &= 1
                #shift the LSB bit over
                wrapperFileData[i] <<= (7 - k)
                #preserve the byte for the next cycle
                byte |= wrapperFileData[i]
                #increment by the interval
                i += interval
            #add the byte to the hidden data
            hiddenData[j] = byte
            #go to the next position of the hidden data array
            j+=1
            #check if the sentinel has been found
            if(j >= (len(SENTINEL)-1) and bytearray(hiddenData[j-6:j]) == SENTINEL):
                if(DEBUG):
                    print "A sentinel was found!"
                return hiddenData[:-6]
        #if we have reached here, then a sentinel was not found
        print("Sentinel was not found! Exiting...")
        exit(0)

    if(XDEBUG):
        print("Hidden data")
        for l in range(len(hiddenData)):
            print(hiddenData[l])

def store(wrapperFileData, hiddenFileData, method, mode, offset, interval):

    if(DEBUG):
        print("wrapper file length: %s" % len(wrapperFileData))
        print("hidden file length: %s" % len(hiddenFileData))

    #byte method
    if(method == 1):
        i = 0
        #while we haven't reached the end of the possible hidden file
        while i < len(hiddenFileData):
            #hide data in the wrapper, skipping its header data
            wrapperFileData[offset] = hiddenFileData[i]
            #increase to next interval
            offset += interval
            i+=1
        i = 0
        #pick up where you left off
        while i < len(SENTINEL):
            #and insert the sentinel
            wrapperFileData[offset] = SENTINEL[i]
            #increase to the next interval
            offset += interval
            i+=1
        if(DEBUG):
            print("The data was successfully stored in bytes into the wrapper file!")
    #bit method
    else:
        #append the sentinel to the hidden file data so you can insert it in one go
        hiddenFileData += SENTINEL
        i = offset
        j = 0
        #while the end of the hidden file has not been reached
        while j < len(hiddenFileData):
            #for each byte
            for k in range(8):
                #isolate the seven most significant bits (MSB)
                wrapperFileData[i] &= 11111110
                #isolate the MSB of the hiiden byte and store it in the least significant bit (LSB) of the wrapper byte
                wrapperFileData[i] |= ((hiddenFileData[j] & 10000000) >> 7)
                #shit the hidden byte to the left
                hiddenFileData[j] <<= 1
                #increase the index by the interval
                i += interval
            j+=1
        if(DEBUG):
            print("The data was successfully stored in bits into the wrapper file!")

    if(XDEBUG):
        print("Wrapper file date after hidden file has been stored")
        for i in wrapperFileData:
            print(wrapperFileData[i])

#find the maximum size of a hidden file you can hide in a given wrapper file
def maxHiddenFileSize(wrapperFileData):
    return ((len(wrapperFileData) - offset)//interval)

#find the minimum size of a wrapper file you can use to hide a given hidden file
def minWrapperSize(hiddenFileData):
    return (len(hiddenFileData) * interval + offset)

#main program that calls all of the helper methods
def main():
    #get user parameters
    getParameters()

    #get the wrapper file in bytes
    if(wrapperFile != ""):
        wrapperFileData = readFile(wrapperFile)
    #get the hidden file in bytes
    if(hiddenFile != ""):
        hiddenFileData = readFile(hiddenFile)

    #retrieve data
    if(mode == 1):
        #output this to an image file
        print(bytearray(retrieve(wrapperFileData, method, mode, offset, interval)))
    #store data
    else:
        #output this to an image file
        print(bytearray(store(wrapperFileData, hiddenFileData, method, mode, offset, interval)))

    if(DEBUG):
        print("End of program")

main()