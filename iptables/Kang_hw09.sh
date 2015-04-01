#!/bin/bash
# Firewall for Linux machine using iptables packet filtering modules
#
# Flush rules and reset counters
iptables -F
iptables -X
#
## Place no restriction on outbound packets
iptables -A OUTPUT -j ACCEPT
#
## Block a list of specific ip addresses for all incoming connections
iptables -A INPUT -s 10.10.10.0/255.10.50.0 -j DROP
#
## Block your computer from being pinged by all other hosts
iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
#
## Set up port-forwarding from an unused port of my choice to port 22 on your computer.
iptables -t nat -A PREROUTING -p tcp -d 192.168.0.101 --dport 422 -j DNAT --to 192.168.0.101:22
iptables -A INPUT -i eth0 -p tcp --dport 422 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 422 -m state --state ESTABLISHED -j ACCEPT
#
## Allow for SSH access (port 22) to my machine from only the ecn.purdue.edu domain
iptables -A INPUT -i eth0 -p tcp -s 128.46.4.83 --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
#
## Allow only a single IP address in the internet to access my machine for the HTTP service
iptables -A INPUT -i eth0 -p tcp -s 128.46.4.83 --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 80 -m state --state ESTABLISHED -j ACCEPT
#
## Permit Auth/Ident (port 113) that is used by some services like SMTP and IRC
iptables -A INPUT -p tcp -m tcp --syn --dport 113 -j ACCEPT
## Set policies
iptables -A INPUT -j DROP
iptables -A FORWARD -j DROP
iptables -A OUTPUT -j DROP
#
## View rules
iptables -L
#
## Flush rules and reset because I don't actually want thise firewalls on my computer
iptables -F
iptables -X

