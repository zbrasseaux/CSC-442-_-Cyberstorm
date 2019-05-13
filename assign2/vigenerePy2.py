#!/usr/bin/env python2

#WHAT TEAM!? CELTS!
#Paige Meeks redo of the vigenere cipher:
#take in text to either encrypt or decrypt with a
#given key
#NOTE: this is Python 2 (denoted by the ...Py2.py)

import sys, re

DEBUG = False

###################validation###################
def getMode():
    try:
        #-e for encrypt or -d for decrypt (must have mode)
        mode = sys.argv[1]
    except IndexError:
        print("You must pass in the flag -e (for encryption) or -d (for decryption)")
        exit(1)

    #make sure the flag is either -e, --encryption, -d, or --decryption
    if(mode != "-e" and mode != "--encryption" and mode != "-d" and mode != "--decryption"):
        print("You must pass in the flag -e (for encryption) or -d (for decryption)")
        exit(1)
    
    #if we are encrypting a message, return the value 0
    if(mode == "-e" or mode == "--encryption"):
        return 0
    #at this point, the only other value mode could be is -d or --decryption so return 1
    else:
        return 1

def getKey():
    try:
        #what ever comes after the mode is the key
        key = sys.argv[2]
    except IndexError:
        print ("You must must enter a valid key (must contain at least one alpha)")
        exit(1)

    #make sure there is at least one alpha character in the key that we can encrypt/decrypt by
    if(not re.search("[a-zA-Z]", key)):
        print("You must must enter a valid key (must contain at least one alpha)")
        exit(1)
    #remove all non-alpha characters from key to make things simple
    #first parameter is regex for any non-alpha character, second parameter is the replacement character
    #(which is an empty string in our case), and the third parameter is the input string
    return re.sub("[^a-zA-Z]", "", key).lower()
        
###################main program###################
def main(mode, key):
    while (True):
        try:
            #text we will encrypt/decrypt
            input_text = raw_input()
        except EOFError:
            #EOFError will be caused by ^D so we exit instead of giving a stacktrace
            exit(0)
        #this is what will be printed to the console
        output_text = ''
        #we will use j to interate over the characters of the key
        j = 0
        #iterate over each character of the input text
        for i in range(len(input_text)):
            char = input_text[i]
            #get the case of the character which determines the offset of the ASCII table
            #returns true if character is lowercase and false otherwise
            lwrcase = checkLowercase(char)
            #turn the current character to is lowercase form to make things simple
            char = char.lower()
            #set offset to 97 since that is where the lowercase letters begin in the ASCII table
            offset = 97

            if(not char.isalpha()):
                output_text += char
                continue

            #if we are encrypting
            if(mode == 0):
                #get the index of the encrypted character
                t = ((ord(char) - offset) + (ord(key[j]) - offset)) % 26
            #if we are decrypting
            else:
                #get the index of the decrypted character
                t = ((ord(char) - offset) - (ord(key[j]) - offset) + 26) % 26

            if(DEBUG):
                print(t)

            #get the new character from its index, restore casing, and append it to the end of the output string
            if(lwrcase):
                output_text += chr(t + offset)
            else:
                output_text += chr(t + offset).upper()

            #mod the length of the key so we can iterate over it multiple times
            j = (j + 1) % len(key)
        #print out the encrypted/decrypted message
        print(output_text)

#check the case of the character so we preserve it
def checkLowercase(char):
    #return true if character is lowercase
    if(char.islower()):
        lwrcase = True
    #return false if the character is uppercase
    else:
        lwrcase = False
    return lwrcase

mode = getMode()
key = getKey()

if(DEBUG):
    print("Mode is (0 for encrypt and 1 for decrypt): %s" % mode)
    print("Key is: %s" % key)

main(mode, key)