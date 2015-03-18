#!/usr/bin/env python
import socket
import subprocess
import sys
from datetime import datetime

# Clear the screen
subprocess.call('clear', shell=True)

# Ask for input
remoteServer = raw_input("Enter a remote host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)

# Print a banner with information on which host we are about to scan
print "-" * 60
print "Please wait, scanning remote host", remoteServerIP
print "-" * 60

# Check what time the scan started
t1 = datetime.now()

# Scan ports
try:
	for port in range(1,1025):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = sock.connect_ex((remoteServerIP,port))
		if result == 0:
			print "Port {}: \t Open".format(port)
		sock.close()
except KeyboardInterrupt:
	print "User pressed Ctrl+C"
	sys.exit()

except socket.gaierror:
	print "Hostname could not be resolved. Exiting"
	sys.exit()

except socket.error:
	print "Couldn't connect to server"
	sys.exit()

# Checking time end
t2 = datetime.now()

# Time to run script
total = t2 - t1

# Printing information to screen
print 'Scanning Completed in: ',total