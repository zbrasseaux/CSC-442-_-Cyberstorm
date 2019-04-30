###################################################################################
# Group Assignment #5
# Celt's Members: Addison Abercrombie, Ankit Aryal, Sai Betgeri, Zachary Brasseaux,
#                 Trenton Choate, Richard Lebell, Paige Meeks
# Desc: This program is designed to take in an epoch time and create a password
#       based on the difference of these times.
###################################################################################

import time
import sys
import datetime
import hashlib
import calendar
from pytz import timezone
import pytz
import os.path

##################################################################################
# Functions
##################################################################################

#Returns boolean for if the timezone at the given date is in Daylight Savings Time
def is_dst(zonename, now):
    tz = pytz.timezone(zonename)
    return now.astimezone(tz).dst() != datetime.timedelta(0)

#Parse md5 by first 2 characters and last 2 integers
def Parse_Int_Char(s):
    c1 = ''
    c2 = ''
    i1 = 0
    i2 = 0
    count = 0
    for c in reversed(s):
        if(c.isalpha()):
            count += 1
            if(count == 1):
                c1 = c
            if(count == 2):
                c2 = c

    count = 0
    for i in s:
        if(i.isdigit()):
            count += 1
            if(count == 1):
                i1 = i
            if(count == 2):
                i2 = i
    print(i1 + i2  + c1 + c2)


#Parse md5 by first 2 integers and last 2 characters
def Parse_Char_Int(s):
    c1 = ''
    c2 = ''
    i1 = 0
    i2 = 0
    count = 0
    for c in s:
        if(c.isalpha()):
            count += 1
            if(count == 1):
                c1 = c
            if(count == 2):
                c2 = c

    count = 0
    for i in reversed(s):
        if(i.isdigit()):
            count += 1
            if(count == 1):
                i1 = i
            if(count == 2):
                i2 = i
    print(c1 + c2  + i1 + i2)

#encode provided string into md5 and encode that md5 to md5
def encode_md5(x):
    h = hashlib.md5(x.encode())
    h1 = h.hexdigest()
    h = hashlib.md5(h1.encode())
    h2 = h.hexdigest()
    return h2


##################################################################################
# Main
##################################################################################

#Take input from terminal for epoch time
if len(sys.argv) > 1:
    epoch = sys.argv[1]
else:
    epoch = input()

#specify currenttime with a string in Y m d H M S format or the current date with
#datetime.datetime.now(), both are options are directly below, choose only one.

currenttime = datetime.datetime.now()
#currenttime = "2017 01 01 00 00 00"

if(type(currenttime) is not str):
    currenttime_date = currenttime
else:
    #Set string to Datetime format
    currenttime_date = datetime.datetime.strptime(currenttime, "%Y %m %d %H %M %S")


#Set string to Datetime format
epoch_date = datetime.datetime.strptime(epoch, "%Y %m %d %H %M %S")

difference = currenttime_date - epoch_date


#If in Daylight Savings Time, take into account the hour in seconds
dst = is_dst("America/Chicago", currenttime_date)
if(dst):
    dst_seconds = 1 * 60 * 60
else:
    dst_seconds = 0

#Subtract the modulo 60 of the difference to get the starting time of the current time interval
seconds_To_Encode = str((int(difference.total_seconds())-dst_seconds)-((int(difference.total_seconds())-dst_seconds)%60))

#Encode the result twice with md5
h2 = encode_md5(seconds_To_Encode)

#Parse the resulting md5 string and print
Parse_Char_Int(h2)
