from Kang_hw08 import *
targetIP = '128.46.75.62'
spoofIP = '192.168.0.103'
rangStart = 20
rangEnd = 1025
port = 110
Tcp = TcpAttack(spoofIP, targetIP)
#Tcp.scanTarget(rangStart,rangEnd)
Tcp.attackTarget(port)