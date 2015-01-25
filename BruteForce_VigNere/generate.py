import itertools
import binascii
from BitVector import *

array = ["".join(seq) for seq in itertools.product("01", repeat=8)]
for i in range(0,len(array)):
	print array[i]
	bv = BitVector(bitstring=array[i])
	print bv



#for i in range(1,len(array)):
#	print '0b'+str(array[i])



#a =  bin(int(binascii.hexlify('hello'), 16))
#n = int('0b1010', 2)
#print binascii.unhexlify('%x' % n)