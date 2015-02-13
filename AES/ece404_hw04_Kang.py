#!/usr/bin/env/python

import sys
from BitVector import *

def createLookupTable(EncryptorDecrypt):
	
	# Initialize 16x16 Hex Table
	LookupTable = [BitVector(intVal = x, size = 8) for x in range(256)]
	
	# Initialize Modulus Polynomial in GF(2^8)
	modulus = BitVector(bitstring='100011011')
	n = 8
	
	# Encrpyt or Decrypt
	if(EncryptorDecrypt == 'encrypt'):
	
		# Take the multiplicative inverse of each element in the table
		LookupTable = [LookupTable[x].gf_MI(modulus, n) for x in range(256)]
		LookupTable[0] = BitVector(intVal = 0, size = 8)

		# Do bit scrambling with special byte c
		c = BitVector(bitstring='01100011')

		# Initialize an empty 16x16 Hex Table so changed bits don't affect the calculations
		SBox = [BitVector(intVal = x, size = 8) for x in range(256)]

		for byte in range(0,256):
			for i in range(0,8):
				SBox[byte][i] = LookupTable[byte][i] ^ LookupTable[byte][(i + 4) % 8] ^ LookupTable[byte][(i + 5) % 8] ^ LookupTable[byte][(i + 6) % 8] ^ LookupTable[byte][(i + 7) % 8] ^ c[i]
	
	if(EncryptorDecrypt == 'decrypt'):
	
		# Do bit scrambling with special byte d
		d = BitVector(bitstring='00000101')

		# Initialize an empty 16x16 Hex Table so changed bits don't affect the calculations
		SBox = [BitVector(intVal = x, size = 8) for x in range(256)]

		for byte in range(0,256):
			for i in range(0,8):
				SBox[byte][i] = LookupTable[byte][i] ^ LookupTable[byte][(i + 2) % 8] ^ LookupTable[byte][(i + 5) % 8] ^ LookupTable[byte][(i + 7) % 8] ^ d[i]
		
		# Take the multiplicative inverse of each element in the table
		SBox = [SBox[x].gf_MI(modulus, n) for x in range(256)]

	return SBox

def subBytes(LookupTable, stateArray):
	
	# Substitute bytes	
	subbedArray = [LookupTable[stateArray[x][0:4].int_val()*10 + stateArray[x][4:8].int_val()] for x in range(16)]
	return subbedArray

def shiftRows(stateArray):
	
	rows = [stateArray[x::4] for x in range(0,4)]
	for i in range(1,4):
		rows[i] = rows[i][i:] + rows[i][:i]
	array = []
	for i in range(4):
		for j in range(4):
			array.append(rows[j][i])
	
	return array

def main():
	bv = BitVector(intVal = 0)
	stateArray = [bv.gen_rand_bits_for_prime(8) for i in range(16)]
	SBox = createLookupTable('decrypt')
	subbedArray = subBytes(SBox,stateArray)
	shiftArray = shiftRows(stateArray)
	
		
if __name__ == "__main__":
	main()