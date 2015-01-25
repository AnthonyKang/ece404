# Homework 1
# Anthony Kang
# kang144
# 1/22/2015

# This script is just a modification of DeCryptForFun. Instead of asking the user for a key
# It tries every possible bit permutation for a 16 bit block size, then returns the key

PassPhrase = "Hopes and dreams of a million years"

import sys
import os
from BitVector import *                                         #(A)
import re

if len(sys.argv) is not 3:                                      #(B)
    sys.exit('''Needs two command-line arguments, one for '''
             '''the encrypted file and the other for the '''
             '''decrypted output file''')

BLOCKSIZE = 16                                                  #(C)
numbytes = BLOCKSIZE / 8                                        #(D)

# Reduce the passphrase to a bit array of size BLOCKSIZE:
bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)                      #(E)
for i in range(0,len(PassPhrase) / numbytes):                   #(F)
    textstr = PassPhrase[i*numbytes:(i+1)*numbytes]             #(G)
    bv_iv ^= BitVector( textstring = textstr )                  #(H)

# Create a bitvector from the ciphertext hex string:
FILEIN = open(sys.argv[1])                                      #(I)
encrypted_bv = BitVector( hexstring = FILEIN.read() )           #(J)

# Test every possible permutation
FILEOUT = open(sys.argv[2], 'w')  
for k in range(0,2**BLOCKSIZE):

    # Creates the BitVector given the integer value
    key_bv = BitVector(intVal = k, size = 16)                     #(P)
    
    # Create a bitvector for storing the output plaintext bit array:
    msg_decrypted_bv = BitVector( size = 0 )                        #(T)

    # Carry out differential XORing of bit blocks and decryption:
    previous_decrypted_block = bv_iv                                #(U)
    for i in range(0, len(encrypted_bv) / BLOCKSIZE):               #(V)
        bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]              #(W)
        temp = bv.deep_copy()                                       #(X)
        bv ^=  previous_decrypted_block                             #(Y)
        previous_decrypted_block = temp                             #(Z)
        bv ^=  key_bv                                               #(a)
        msg_decrypted_bv += bv                                      #(b)

    # If Babe Ruth is found in the output then we have found the key and we can exit
    outputtext = msg_decrypted_bv.getTextFromBitVector()            #(c)
    search = re.search('Babe Ruth', outputtext)
    if search:
        FILEOUT.write(outputtext + '\n')
        FILEOUT.write("key = ")
        FILEOUT.write(str(unichr(int(key_bv[0:8]))))
        FILEOUT.write(str(unichr(int(key_bv[9:16]))))
        sys.exit("Found Key")
        
    
FILEOUT.close()                                                 #(f)
