#!/usr/bin/env python2

#WHAT TEAM!? CELTS!
#Paige Meeks redo of timelock:
#description...
#NOTE: this is Python 2 (denoted by the ...Py2.py)

import sys
import datetime as d
import hashlib as h
import re
import pytz

debug = True

#different datetime formats
FORMAT1 = "%Y %m %d %H %M %S"
FORMAT2 = "%Y-%m-%d %H:%M:%S"
FORMAT3 = "%Y-%m-%d %H:%M:%S.%f"

#code mode will switch the order of the code (True = first two alpha characters from left-right
#and first numeric characters from right-left; False = vice versa)
CODEMODE = True

EPOCH = "1999 12 31 23 59 59"
SYSTIME = "2013 05 06 07 43 25"

#get epoch
def getEpochTime():
    global EPOCH
    EPOCH = sys.raw_input()

#get current system time
def getSysTime():
    global SYSTIME
    d.datetime.now()

#convert string to datetime
def convertTime(convertTime, timeFormat):
    try:
        #to create the datetime, the date string and its corresponding date format must be passed in
        date = d.datetime.strptime(convertTime, timeFormat)
    except ValueError:
        print("Datetime and format did not match!\nDatetime: %s\tFormat: %s" % (convertTime, timeFormat))
        exit()
    if(debug):
        print("Original date: %s" % date)
    #make sure to convert it from Central to UTC
    localDate = pytz.timezone('America/Chicago').localize(date, is_dst = True)
    dateUTC = localDate.astimezone(pytz.utc)
    if(debug):
        print("Converted UTC date: %s" % dateUTC)
    return dateUTC

#calculate the elapsed time in seconds
def calculateSeconds(sysTime, epochTime):
    #positive values only to make things simple
    elapsedTime = abs(sysTime - epochTime).total_seconds()
    if(debug):
        print("Elapsed time: %s" % elapsedTime)
    #total_seconds results in the format <seconds>.<milliseconds>
    return elapsedTime

#hash the time in seconds two times with the MD5 hash
def hashMD5(elapsedTime):
    seconds = elapsedTime - (elapsedTime % 60)
    print("Seconds before hash: %s" % seconds)
    hashWasTaken = h.md5(str(int(seconds)).encode())
    hash1 = hashWasTaken.hexdigest()
    hashWasTaken = h.md5(hash1.encode())
    hash2 = hashWasTaken.hexdigest()
    if(debug):
        print("Resulting hash: %s" % hash2)
    return hash2

#pick out the desired alphanumeric characters to generate a code
def generateCode(myHash):
    #separate the alpha and numeric characters so we can do some simple splicing
    aplhaCode = re.findall("[a-f]", myHash)
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

sysTime = convertTime(SYSTIME, FORMAT1)
epoch = convertTime(EPOCH, FORMAT1)
seconds = calculateSeconds(sysTime, epoch)
myHash = hashMD5(seconds)
code = generateCode(myHash)