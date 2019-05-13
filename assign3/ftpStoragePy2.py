#!/usr/bin/env python2

#WHAT TEAM!? CELTS!
#Paige Meeks redo of the ftp storage covert channel:
#ftp into the given server on the given port, get the
#file permissions, and decode into ASCII
#NOTE: this is Python 2 (denoted by the ...Py2.py)

import ftplib, sys

DEBUG = False

def getServer():
    try:
        server = argv[1]
    except IndexError:
        print("You must pass in a server to FTP into!")
        exit(1)
    return server

def getPort():
    try:
        port = argv[1]
    except IndexError:
        print("CAUTION! A port was not passed in, defaulting to port 21...")
        port = 21
    return port

def getUsername():
    try:
        usr = argv[3]
    except IndexError:
        print("CAUTION! A username was not passed in, defaulting to anonymous login...")
        usr = ""
    return usr

def getPassword():
    try:
        pswrd = argv[4]
    except IndexError:
        print("CAUTION! A username was not passed in, defaulting to anonymous login...")
        pswrd = ""
    return pswrd

###################################################################################################################### main program ###########################
def getAllPaths():
    pass

'''
get all paths
for path in paths
    print full path
    get files in current directory
    try METHOD 7
    try METHOD 10
    append to output
print output
'''

ftp = FTP()
ftp.connect(getServer, getPort)
ftp.login(getUsername, getPassword)

#call some more functions

try:
    ftp.quit()
except:
    ftp.close()

exit(0)