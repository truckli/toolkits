#!/usr/bin/python

from os import system, path
from time import sleep
import sys
from subprocess import Popen, PIPE


if len(sys.argv) < 2:
    print 'Usage: %s [config_file]' % sys.argv[0]
    checkfile = 'ip_addr_config'
    print 'Default config file is \"%s\"' % checkfile
else:
    checkfile = sys.argv[1]

if not path.isfile(checkfile):
    print 'config file %s does not exist' % checkfile
    sys.exit(1)

ip_list = []

try:
    file = open(checkfile, 'r')
    for ip_addr in file:
        if ip_addr.find('.') > 0:
            ip_list.append(ip_addr.strip())
    file.close()
except IOError:
    print 'Failed to open config file \"%s\".' % checkfile
    sys.exit(1)

if ip_list == []:
    print 'config file %s does not specify any IP addresses' % checkfile
    sys.exit(1)



pipe_list = []
for ip_addr in ip_list:
    pipe_list.append(Popen(['ping', '-i', '.2', '-c', '3', ip_addr], stdout=PIPE))

sleep(1)
system("killall ping")

for ip_addr, pipe in zip(ip_list, pipe_list):
    lines = pipe.stdout.readlines()
    found = False
    for line in lines:
        if line.find('ttl') >= 0 and line.find(ip_addr) >= 0:
            found = True
            break
    if found:
        print '%s : success' % ip_addr
    else:
        print '%s : Fail' % ip_addr
    




