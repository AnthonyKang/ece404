from Kang_RSA_hw06 import *
from BitVector import *
from solve_pRoot import *

def main():

	# generate 3 sets of keys with e = 3
	public1, private1, p1, q1, d = generateKey(3)
	public2, private2, p2, q2, d = generateKey(3)
	public3, private3, p3, q3, d = generateKey(3)

	
	# encrpyt the given plaintext with each of the three public keys
	encrypt1 = encrypt(sys.argv[1], public1, 'bf_encrypt1.txt')
	open('bf_encrypt1.txt', 'w').write('\nn = ' + str(public1[1]))
	encrypt2 = encrypt(sys.argv[1], public2, 'bf_encrypt2.txt')
	open('bf_encrypt2.txt', 'w').write('\nn = ' + str(public2[1]))
	encrypt3 = (sys.argv[1], public3, 'bf_encrypt3.txt')
	open('bf_encrypt3.txt', 'w').write('\nn = ' + str(public3[1]))

	print public1[0]
	# Apply the chinese remainder theorem
	N = public1[1] * public2[1] * public3[1]
	
	N_1 = N/public1[1]
	bv_modulus = BitVector(intVal = public1[1])
	bv = BitVector(intVal = N_1)
	d_1 = int(bv.multiplicative_inverse(bv_modulus))

	N_2 = N/public2[1]
	bv_modulus = BitVector(intVal = public2[1])
	bv = BitVector(intVal = N_2)
	d_2 = int(bv.multiplicative_inverse(bv_modulus))

	N_3 = N/public3[1]
	bv_modulus = BitVector(intVal = public3[1])
	bv = BitVector(intVal = N_3)
	d_3 = int(bv.multiplicative_inverse(bv_modulus))

	M = []
	#print N
	#print (encrypt1[1]*N_1*d_1) 
	#print (encrypt1[1]*N_1*d_1) % N
	
	for i in range(len(encrypt1)):
		X = (encrypt1[1]*N_1*d_1) % N
		X += (encrypt2[1]*N_2*d_2) % N
		#print X
		X += (encrypt3[1]*N_3*d_3) % N
		M.append(solve_pRoot(3,X))
	
	FILEOUT = open(argv[2], 'wa')
	for message in M:
		bv = BitVector(intVal = message, size = 128)
		FILEOUT.write(bv.get_hex_string_from_bitvector())
	for message in M:
		bv = BitVector(intVal = message, size = 128)
		FILEOUT.write(bv.get_text_from_bitvector())


if __name__ == '__main__':
	main()