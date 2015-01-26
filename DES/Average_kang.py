from DES_kang import *
from BitVector import *
import random


N = 28   				# number of bit vectors to sample
BIT_POS_SWAP = 40		# arbitrary bit position to flip
max48 = 281470949392383 # max integer value for 48 bit number

###################### Generate N different 64 bit inputs ##########

# Generate two random 32 bit vectors and combine them

max32bit =  int('FFFFFFFF',16)
plaintext = N * [0]
for i in range(0,len(plaintext)):
	left = BitVector(intVal = random.randrange(0,max32bit), size = 32)
	right = BitVector(intVal = random.randrange(0,max32bit), size = 32)
	plaintext[i] = left + right
	
# Change the plaintext sample by one bit
plaintext_changed = N * [0]
#plaintext_changed = plaintext

modbv = BitVector(size = 64)
modbv[BIT_POS_SWAP] = 1
#print modbv
for i in range(0,len(plaintext)):
	#print plaintext_changed[i][BIT_POS_SWAP]
	plaintext_changed[i] = plaintext[i] ^  modbv

# Run DES

#for i in range(0,len(plaintext)):
#	print plaintext[i]
#	print plaintext_changed[i]

key = get_encryption_key()
cipher_unmod = [0] * N
cipher_mod = [0] * N
total = 0

for i in range(0,N):
	cipher_unmod[i] = des('encrypt_nf',plaintext[i],'none',key)		
	cipher_mod[i] = des('encrypt_nf',plaintext_changed[i],'none',key)	

	# xor the two resulting cipher bitvectors to find out how many bits are different
	xorbv = cipher_mod[i] ^ cipher_unmod[i]
	count = xorbv.count_bits() 
	total = total + count
	#print count

average = total/N
print "average diffusion = " + str(average) 

################################# Generate S-box ###########################
FILEOUT = open(sys.argv[1] , 'wb')
for k in range(0,8):
	FILEOUT.write("S" + str(k) + ":" + '\n\n')
	for i in range(0,4):
		row = random.sample(xrange(16),16)
		for j in range(0,16):
			FILEOUT.write(str(row[j]) + '  ')
		FILEOUT.write('\n')
	FILEOUT.write('\n')

############## Generate N different keys for confusion ###########

key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,
50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,22,14,6,61,53,45,37,
29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3]

# Generate N 64 bit keys
max32bit =  int('FFFFFFFF',16)
key = N * [0]
for i in range(0,len(key)):
	left = BitVector(intVal = random.randrange(0,max32bit), size = 32)
	right = BitVector(intVal = random.randrange(0,max32bit), size = 32)
	key[i] = left + right

# Change the key sample by one bit
key_changed = N * [0]

modbv = BitVector(size = 64)
modbv[BIT_POS_SWAP] = 1

for i in range(0,len(key)):
	key_changed[i] = key[i] ^  modbv

	# permute the keys
	key[i] = key[i].permute(key_permutation_1)
	key_changed[i] = key_changed[i].permute(key_permutation_1)


# Generate a random 64 bit input
inputbv = BitVector(intVal = 0)
inputbv = inputbv.gen_rand_bits_for_prime(64)

cipher_unmod = [0] * N
cipher_mod = [0] * N
total = 0

for i in range(0,N):
	cipher_unmod[i] = des('encrypt_nf',inputbv,'none',key[i])		
	cipher_mod[i] = des('encrypt_nf',inputbv,'none',key_changed[i])	

	# xor the two resulting cipher bitvectors to find out how many bits are different
	xorbv = cipher_mod[i] ^ cipher_unmod[i]
	count = xorbv.count_bits() 
	total = total + count
	#print count

average = total/N
print "average confusion = " + str(average) 