import sys
import math

def is_prime(n):
    if n % 2 == 0 and n > 2: 
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
	num = 51
	FILEOUT = open(sys.argv[1], 'w')
	while (num > 50):
		num = int(raw_input("Please enter a number less than 50: "))
	if(is_prime(num)):
		print "field"
		FILEOUT.write("field")
	else:
		print "ring"
		FILEOUT.write("ring")

	FILEOUT.close()
 
if __name__ == "__main__":
    main()