#!/usr/bin/env python2
import sys, string, re

mode = sys.argv[1] #-e for encrypt or -d for decrypt (must have tag)

key = sys.argv[2] #what ever comes after the tag is the key

if not re.search("[a-zA-Z]", key): #make sure there is at least one alpha character in the key that we can encrypt/decrypt by
    print "You must must enter a valid key (must contain at least one alpha )"
    exit()

while (True):
    try:
        input_text = raw_input() #text we will encrypt/decrypt
    except EOFError: #EOFError will be caused by ^D so we exit instead of giving a stacktrace
        print "Bye!"
        exit()
    output_text = '' #this is what will be printed to the console
    j = 0 #we will use j to interate over the characters of the key
    for i in range(len(input_text)):
        while not key[j].isalpha(): #skip all of the non-alpha characters in the key
            j += 1
        if (input_text[i].isalpha() and (mode == "-e" or mode == "-E")): #if the current character is an alpha character and we are encrypting the input
            output_text += string.ascii_letters[(string.letters.index(input_text[i]) + string.letters.index(key[j])) % 52]
        elif (input_text[i].isalpha() and (mode == "-d" or mode == "-D")): #if the current character is an alpha character and we are decrypting the input
            output_text += string.ascii_letters[(52 + string.letters.index(input_text[i]) - string.letters.index(key[i])) % 52]
        elif not input_text[i].isalpha(): #if the current character is not an alpha character
            output_text += input_text[i] #simply add it to the output text since we do not encrypt/decrypt non-alpha characters
        else: #if this check has been reached, then a flag was not given or it was incorrect
            print "You must pass in the flag -e (for encryption) or -d (for decryption)"
            exit()
        j += 1
        j = j % len(key) #% length of the key so we can iterate over it multiple times
    print output_text #print out the encrypted/decrypted message
