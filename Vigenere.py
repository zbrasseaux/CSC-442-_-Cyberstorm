from itertools import starmap, cycle
import sys, string, os
from optparse import OptionParser
import argparse

#adding '-e' and '-d' option in the program.
parser = OptionParser()
parser.add_option("-e", action="store", type="string", dest="key")
parser.add_option("-d", action="store", type="string", dest="key")#"dest" stores the key
(options, args)= parser.parse_args() #.parse_args() return the argment

#encryption fucntion
def encrypt(PlainText, KeyEncrypt):
    #plain text Plain_T into lower case
    Plain_T = PlainText.lower()
    
#decryption function
def decrypt(ct, kd):
    #ctl means encrypted_lowercase text
    ctl=ct.lower()
    

    
