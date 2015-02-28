from BitVector import *
from PrimeGenerator import *
from BGCD import bgcd
import sys

def generateKey():

	# Given e = 65537
	e = 65537

	# Given modulus n to be 256 bits, generate p and q 
	# p and q are 128 bits
	found = 0
	while(found == 0):
		generator = PrimeGenerator(bits = 128, debug = 0)
		p = generator.findPrime()
		q = generator.findPrime()

		found = 1

		# p and q must be different
		if p == q:
			found = 0

		# p and q two left most bits must be set
		if not (bin(p)[2] and bin(p)[3] and bin(q)[2] and bin(p)[3]):
			found = 0

		# (p-1) and (q-1) must be co-prime to e
		# gcd((p-1),e) and gcd((q-1),e) should be 1
		if (bgcd(p-1,e) != 1) or (bgcd(q-1,e) != 1):
			found = 0

	# compute the modulus n
	n = p * q

	# compute the totient of n
	t_n = (p - 1) * (q - 1)

	# compute d
	bv_modulus = BitVector(intVal = t_n)
	bv = BitVector(intVal = e)
	d = bv.multiplicative_inverse(bv_modulus)
	d = int(d)
	
	# concatanate e and d with n to get public and private keys
	public = [e,n]
	private = [d,n]

	return (public, private,p,q)

def readMessage(myfilename, encrypt_decrypt):

	# find number of bytes in file
	input_text = open(myfilename, 'r+').read()
	num_bytes = len(input_text)
	
	bv = BitVector(filename = myfilename)

	# Split the message in to blocks
	if(encrypt_decrypt == 'encrypt'):
		message_blocks = [bv.read_bits_from_file(128) for x in range((num_bytes/16)+1)]
	elif(encrypt_decrypt == 'decrypt'):
		message_blocks = [int(bv.read_bits_from_file(256)) for x in range((num_bytes/32))]
		return message_blocks
		
	# pad the message with new lines
	new_line = BitVector(textstring = '\n')
	while(len(message_blocks[-1]) < 128):
		message_blocks[-1] = message_blocks[-1] + new_line

	for message in message_blocks:
		message.pad_from_left(128)

	return message_blocks

def encrypt(filename, public):

	# read the message
	message_blocks = readMessage(filename, 'encrypt')
	message = map(int,message_blocks)
	
	# encrpy the message with arithmatic exponential modulation
	encrypt_message = []
	for i in range(len(message)):
		encrypt_message.append(pow(message[i], public[0], public[1]))
	
	printToFile(encrypt_message, sys.argv[3], 'encrypt')
	

def decrypt(filename, private, p, q):

	encrypted_blocks = readMessage(filename, 'decrypt')
	 
	#print message_blocks
	# Using the chinese remainder theorem
	V_p = []
	V_q = []
	for block in encrypted_blocks:
		V_p.append(pow(block, private[0], p))
		V_q.append(pow(block, private[0], q))

	# We need the MI of q and p
	q_bv = BitVector(intVal = q)
	p_bv = BitVector(intVal = p)

	X_p = q * int(q_bv.multiplicative_inverse(p_bv))
	X_q = p * int(p_bv.multiplicative_inverse(q_bv))

	decrypt_message = []
	for i in range(len(encrypted_blocks)):
		decrypt_message.append((( V_p[i]*X_p) + (V_q[i]*X_q) ) % private[1])

	printToFile(decrypt_message, sys.argv[3], 'decrypt')
	

def printToFile(message_block, filename, encrypt_decrypt):
	# Print to file, size of value different for encryption and decryption
	FILEOUT = open(filename, 'wa')
	for message in message_block:
		if(encrypt_decrypt == 'decrypt'):
			bv = BitVector(intVal = message, size = 128)
		else:
			bv = BitVector(intVal = message, size = 256)
		FILEOUT.write(bv.get_text_from_bitvector())



def main():
	if(len(sys.argv) != 4):
		print 'usage: Kang_RSA_hw06.py [-e | -d] input.txt output.txt'
		sys.exit()
	
	# Generate the keys
	keys = generateKey()
	public, private,p,q = keys

	if(sys.argv[1] == '-e'):
		encrypt(sys.argv[2], public)

		# Store the generated public and private keys so it can be used for decryption
		open('public.txt', 'w').write(str(public))
		private_out = open('private.txt', 'wa')
		private_out.write(str(private[0]) + ' ' + str(private[1]))
		open('p.txt', 'w').write(str(p))
		open('q.txt', 'w').write(str(q))

	elif(sys.argv[1] == '-d'):
		
		# get the same keys to use for decryption
		private = map(int,open('private.txt', 'r').readlines()[0].split())
		p = int(open('p.txt','r').read())
		q = int(open('q.txt','r').read())
		decrypt(sys.argv[2], private, p, q)

	else:
		print 'usage: Kang_RSA_hw06.py [-e | -d] input.txt output.txt'
		sys.exit()
	
	
if __name__ == "__main__":
	main()