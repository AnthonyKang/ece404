from BitVector import *
from PrimeGenerator import *
from BGCD import bgcd

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
	print t_n
	d = int(d)
		
	print p
	print q

	# concatanate e and d with n to get public and private keys
	#public = (e << len(bin(n)) - 2) + n
	#private = (d << len(bin(n)) - 2) + n
	public = [e,n]
	private = [d,n]

	return (public, private)

def readMessage(myfilename):
	bv = BitVector(filename = myfilename)

def main():
	print "hi"
	generator = PrimeGenerator(bits = 128, debug = 0)
	prime = generator.findPrime()
	prime = generator.findPrime()
	#print bin(prime)

	keys = generateKey()
	public, private = keys
	print pow(123123123123123, public[0], public[1])
	


	#print bgcd(1231231231,10)

if __name__ == "__main__":
	main()