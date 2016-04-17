#!/usr/bin/env python


import socket

port = 8100
tsfile = open('Test_SD_H264.ts.001', 'r').read()


s = socket.socket()
s.connect(('192.168.18.133', port))
s.send(tsfile)
s.close()

