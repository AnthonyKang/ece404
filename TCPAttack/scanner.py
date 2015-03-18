#!/usr/bin/env python
from socket import * 

ports = [22,80,139,445]

if __name__ == '__main__':
    target = raw_input('Enter host to scan: ')
    targetIP = gethostbyname(target)
    print 'Starting scan on host ', targetIP

    #scan reserved ports
    for i in range(20, 1025):
    #for i in ports:
        s = socket(AF_INET, SOCK_STREAM)
        timeout = s.settimeout(0.1)
        if(timeout == None):
            print 'Port %d: closed' % (i,)
        result = s.connect_ex((targetIP, i))

        if(result == 0) :
            print 'Port %d: OPEN' % (i,)
        s.close()
