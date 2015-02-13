#!/usr/bin/env/python

import sys
from BitVector import *

def createLookupTable():
	# Initialize 16x16 Hex Table
	LookupTable = [BitVector(intVal = x, size = 8) for x in range(0,256)]
	
	# Initialize Modulus Polynomial in GF(2^8)
	modulus = BitVector(bitstring='100011011')
	n = 8

	# Take the multiplicative inverse of each element in the table
	LookupTable = [LookupTable[x].gf_MI(modulus, n) for x in range(0,256)]
	LookupTable[0] = BitVector(intVal = 0, size = 8)

	# Do bit scrambling with special byte c
	c = BitVector(bitstring='01100011')

	# Initialize an emptey 16x16 Hex Table so changed bits don't affect the calculations
	SBox = [BitVector(intVal = x, size = 8) for x in range(0,256)]

	for byte in range(0,256):
		for i in range(0,8):
			SBox[byte][i] = LookupTable[byte][i] ^ LookupTable[byte][(i + 4) % 8] ^ LookupTable[byte][(i + 5) % 8] ^ LookupTable[byte][(i + 6) % 8] ^ LookupTable[byte][(i + 7) % 8] ^ c[i]

	for i in range(0,256):
		print SBox[i]

def main():
	#bv = BitVector(intVal = 1, size = 8)
	#bv1 = BitVector(intVal = 2, size = 8)
	#print bv
	#print bv1
	#print bv[7] ^ bv1[7]
	createLookupTable()

if __name__ == "__main__":
	main()