import socket

port = 9224

loc_req = "POST /vodadi HTTP/1.1\r\n"\
"User-Agent: VSS User-Agent/1.0\r\n"\
"Host: CDNServer\r\n"\
"Content-Type: text/xml\r\n"\
"Content-Length: 268\r\n"\
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n"\
"<LocateRequest>\r\n"\
"   <Object>star_00000000000015336127_DerivativeFile_Suffix=bw_2.0_</Object>\r\n"\
"   <TransferRate>0</TransferRate>\r\n"\
"   <IngressCapacity>37500000</IngressCapacity>\r\n"\
"   <TransferDelay>5000</TransferDelay>\r\n"\
"</LocateRequest>\r\n";

reqlen = 460
tran_req = "GET /12345ABCD0006 HTTP/1.1\r\n"\
"User-Agent: VSS User-Agent/1.0\r\n"\
"Host: 192.168.1.6\r\n"\
"Transfer-Delay: 5000\r\n"\
"Range: bytes=0-%d\r\n"\
"Ingress-Capacity: 375000000\r\n" % reqlen

s = socket.socket()
s.connect(('192.168.19.8', port))
s.send(loc_req)
print s.recv(1024)
s.close()

s = socket.socket()
s.connect(('192.168.19.8', port))
s.send(tran_req)
while True:
    rev_len = s.recv(1024)
    if len(rev_len) <= 0:
        break
    print rev_len

s.close()

