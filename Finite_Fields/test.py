import sys

FILEOUT = open(sys.argv[1],'w')
num = int(raw_input("Please enter a number less than 50: "))

for i in range(2,num):
	if i % num == 0:
		print('ring')
		FILEOUT.write('ring')
		break
	else:
		print('field')
		FILEOUT.write('field')
FILEOUT.close()