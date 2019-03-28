#!/usr/bin/env python2

#CELTS GITHUB
#https://github.com/zbrasseaux/CSC-442-_-Cyberstorm

import sys, string, re

###################validation###################
try:
    mode = sys.argv[1] #-e for encrypt or -d for decrypt (must have tag)
except IndexError:
    print "You must pass in the flag -e (for encryption) or -d (for decryption)"
    exit()

if mode != "-e" and mode != "--encryption" and mode != "-d" and mode != "--decryption": #make sure the flag is either -e, --encryption, -d, or --decryption
    print "You must pass in the flag -e (for encryption) or -d (for decryption)"
    exit()

try:
    key = sys.argv[2] #what ever comes after the tag is the key
except IndexError:
    print "You must must enter a valid key (must contain at least one alpha)"
    exit()

if not re.search("[a-zA-Z]", key): #make sure there is at least one alpha character in the key that we can encrypt/decrypt by
    print "You must must enter a valid key (must contain at least one alpha)"
    exit()
################################################

while (True):
    try:
        input_text = raw_input() #text we will encrypt/decrypt
    except EOFError: #EOFError will be caused by ^D so we exit instead of giving a stacktrace
        exit()
    output_text = '' #this is what will be printed to the console
    j = 0 #we will use j to interate over the characters of the key
    for i in range(len(input_text)):
        while not key[j].isalpha(): #skip all of the non-alpha characters in the key
            j += 1
        if (input_text[i].isalpha() and (mode == "-e" or mode == "--encryption")): #if the current character is an alpha character and we are encrypting the input
            temp = string.ascii_letters[(string.letters.index(input_text[i]) + string.letters.index(key[j])) % 26]
            #(for the line above) get the index of the current input character and the key, mod it by 26, and get the letter at the resulting index
            if input_text[i].isupper():
                output_text += temp.upper()
            else:
                output_text += temp
        elif (input_text[i].isalpha() and (mode == "-d" or mode == "--decryption")): #if the current character is an alpha character and we are decrypting the input
            temp = string.ascii_letters[(26 + string.letters.index(input_text[i]) - string.letters.index(key[j])) % 26]
            #(for the line above) add 26 (to ensure the result is positive), get the index of the current input character minus the key,
            #mod it by 26, and get the letter at the resulting index
            if input_text[i].isupper():
                output_text += temp.upper()
            else:
                output_text += temp
        elif not input_text[i].isalpha(): #if the current character is not an alpha character
            output_text += input_text[i] #simply add it to the output text since we do not encrypt/decrypt non-alpha characters          

        j += 1
        j = j % len(key) #% length of the key so we can iterate over it multiple times
    print output_text #print out the encrypted/decrypted message
