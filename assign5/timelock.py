'''
Team Celtics

Link to private GitHub:
https://github.com/zbrasseaux/CSC-442-_-Cyberstorm

If you need access to it, please email any of our members.
(Finally fixed that typo. It's been bothering me for ages.)
------------------------------------------------------------------
TimeLock: calculate difference between the current system time
and epoch then MD5 hash the difference and then hash that again
with MD5; then take the first two alpha characters from left-right
and the first two numeric values from right-left of the hash to be
the code; this code is valid for only 60 seconds; NOTE: make this
flexible enough to where alpha and numeric values of the code can
be switched
'''

import sys
import datetime as d
import hashlib as h
import re

debug = True

#different datetime formats
FORMAT1 = "%Y %m %d %H %M %S"
FORMAT2 = "%Y-%m-%d %H:%M:%S"
FORMAT3 = "%Y-%m-%d %H:%M:%S.%f"

#code mode will switch the order of the code (True = first two alpha characters from left-right
#and first numeric characters from right-left; False = vice versa)
CODEMODE = True

SYSTIME = "2020 03 23 18 02 06"
EPOCH = "2017 01 01 00 00 00"

# def main(parameter_list):
#     try:
#         FLAG = sys.argv[1]
#     except IndexError:
#         #call method where epoch is passed
#         return

#     if FLAG == '-ge':
#         EPOCH = t.gmtime()
#     elif FLAG == '-sc':
#         #set datetime
#     else:
#         #call method where epoch is passed


#get epoch (automatically in UTC timezone)
def getEpochTime():
    EPOCH = sys.raw_input()

#get current system time in UTC timezone
def getSysTime():
    d.datetime.utcnow()

#convert string to datetime
def convertTime(convertTime, timeFormat):
    try:
        #to create the datetime, the date string and its corresponding date format must be passed in
        date = d.datetime.strptime(convertTime, timeFormat)
    except ValueError:
        print("Datetime and format did not match!\nDatetime: %s\tFormat: %s" % (convertTime, timeFormat))
        exit()
    #make sure to convert it to 
    if(debug):
        print("Converted date: %s" % date)
    return date

#calculate the elapsed time in seconds
def calculateSeconds(sysTime, epochTime):
    #positive values only to make things simple
    elapsedTime = abs(sysTime - epochTime).total_seconds()
    if(debug):
        print("Elapsed time: %s" % elapsedTime)
    #total_seconds results in the format <seconds>.<milliseconds>
    return elapsedTime

#hash the time in seconds two times with the MD5 hash
def hashMD5(seconds):
    hashWasTaken = h.md5(str(h.md5(str(seconds)))).hexdigest()
    if(debug):
        print("Resulting hash: %s" % hashWasTaken)
    return hashWasTaken

#pick out the desired alphanumeric characters to generate a code
def generateCode(myHash):
    #separate the alpha and numeric characters so we can do some simple splicing
    aplhaCode = re.findall("[a-z]", myHash)
    numericCode = re.findall("[0-9]", myHash)
    if(CODEMODE):
        acode = "".join(aplhaCode[0:2])
        ncode = "".join(numericCode[:-3:-1])
    else:
        acode = "".join(aplhaCode[:-3:-1])
        ncode = "".join(numericCode[0:2])
    code = acode + ncode
    if(debug):
        print("The code: %s" % code)
    return code

def checkTime():
    if(SYSTIME )

sysTime = convertTime(SYSTIME, FORMAT1)
epoch = convertTime(EPOCH, FORMAT1)
seconds = calculateSeconds(sysTime, epoch)
myHash = hashMD5(seconds)
code = generateCode(myHash)