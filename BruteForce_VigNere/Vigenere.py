# Homework 1
# Anthony Kang
# kang144
# 1/22/2015
import sys

if len(sys.argv) is not 3:
	sys.exit('''Needs two command-line arguments, one for '''
             '''the input file and the other for the '''
             '''key file''')

UCASCIIA = 65			# ascii value of upper case A
LCASCIIA = 97			# ascii value of lower case a
UCASCIIZ = 90			# ascii value of upper case Z
LCASCIIZ = 122			# ascii value of lower case z
NUMLETTERS = 26			# number of letters in alphabet

# read in plaintext
PTFILEIN = open(sys.argv[1],'r')
plaintext = PTFILEIN.read()

# read in key
KEYFILEIN = open(sys.argv[2],'r') 
key = KEYFILEIN.read()

# initialize counters
i = 0
j = 0

# initialize encrypt list
encrypt = ''

for i in range(0,len(plaintext)):
	
	# get current key char
	currkeychar = key[j]
	
	# check case and find out the according amount shifted
	if currkeychar.isupper():
		shift = ord(currkeychar) - UCASCIIA
	else:
		shift = ord(currkeychar) - LCASCIIA
	#print str(j) + " " + currkeychar + " " + str(shift)
	
	# loop back to the beggining of the key when reached end of key
	j += 1
	if (j == (len(key) - 1)):
		j = 0

	# get current plain text char
	currptchar = plaintext[i]

	# shift the character
	encryptchar = ord(currptchar) + shift

	# if the shifted ascii value is outside the range, adjust depending on case
	if currptchar.isupper():
		if encryptchar > UCASCIIZ:
			encryptchar -= NUMLETTERS
	else:
		if encryptchar > LCASCIIZ:
			encryptchar -= NUMLETTERS

	# change ascii value back in to character and assign it to encryped list
	encrypt += (chr(encryptchar))

#print encrypt

# Write ciphertext in to output file
FILEOUT = open('output.txt','w')
FILEOUT.write(encrypt + "\n")
FILEOUT.close()

# Close remaining files
PTFILEIN.close()
KEYFILEIN.close()

