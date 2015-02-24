from BitVector import *
import os

# NOTE: The file is read within the encrypt and decrypt methods
#       The files are opened within the methods and the the methods also create the output file


class RC4:

    # Initialize state vector
    S = [x for x in range(256)]

    def __init__(self, key_string):
        self.key_string = key_string

        # initialize T
        split = [0] * len(key_string)
        for i in range(len(key_string)):
            split[i] = BitVector(textstring=key_string[i])
            split[i] = int(split[i])
        T = []
        while (len(T) < 256):
            T.extend(split)
        T = T[0:256]

        # permute S         
        j = 0
        for i in range(256):
            j = (j + self.S[i] + T[j]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]

    def encrypt(self, image):
        
        # open the file, and read in the data, disregarding the header
        picture = []
        with open(image,'r') as myfile:
            lines = myfile.readlines()
            for i in range(5,len(lines)):
                for j in range(len(lines[i])):
                    picture.append(ord(lines[i][j]))
        
        i = 0
        j = 0
        byte = 0
        encrypt = []
        
        # get the permuted S array
        encryptS = self.S[:]

        # generate byte stream and XOR, stopping when every byte has been XORed
        while(True):
            i = (i + 1) % 256
            j = (j + (encryptS)[i]) % 256
            encryptS[i], encryptS[j] = encryptS[j], encryptS[i]
            k = (encryptS[i] + encryptS[j]) % 256
            encrypt.append(encryptS[k] ^ picture[byte])
            byte = byte + 1
            if (byte == len(picture)):
                break
        
        # create file and write to it
        fname = 'encrypted_tiger.ppm'
        with open(fname, 'wba') as outfile:
            for x in lines[0:5]:
                outfile.write(x)
            outfile.write(bytearray(encrypt))
        
        return encrypt

    def decrypt(self, image):

        # open the file, and read in the data, disregarding the header
        picture = []
        with open(image,'r') as myfile:
            lines = myfile.readlines()
            for i in range(5,len(lines)):
                for j in range(len(lines[i])):
                    picture.append(ord(lines[i][j]))
        
        i = 0
        j = 0
        byte = 0
        decrypt = []

        # get the permuted S array
        decryptS = self.S[:]
        
        # generate byte stream and XOR, stopping when every byte has been XORed
        while(True):
            i = (i + 1) % 256
            j = (j + (decryptS)[i]) % 256
            decryptS[i], decryptS[j] = decryptS[j], decryptS[i]
            k = (decryptS[i] + decryptS[j]) % 256
            decrypt.append(decryptS[k] ^ picture[byte])
            byte = byte + 1
            if (byte == len(picture)):
                break
        
        # create file and write to it
        fname = 'decrypted_tiger.ppm'
        with open(fname, 'wba') as outfile:
            for x in lines[0:5]:
                outfile.write(x)
            outfile.write(bytearray(decrypt))

        return decrypt             


def main():
    rc4Cipher = RC4('thisisjustatestkeyforthealgorithm')
    encrypt = rc4Cipher.encrypt('Tiger2.ppm')
    decrypt = rc4Cipher.decrypt('encrypted_tiger.ppm')

    # Commparing orignal picture with decrypted picture
    picture = []
    with open('Tiger2.ppm','r') as myfile:
        lines = myfile.readlines()
        for i in range(5,len(lines)):
            for j in range(len(lines[i])):
                picture.append(ord(lines[i][j]))

    if(picture == decrypt):
        print ('RC4 is awesome')
    else:
        print ('something wrong')

if __name__ == "__main__":
    main()