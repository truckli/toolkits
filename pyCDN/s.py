import socket
import string 
import struct
import time 

host = socket.gethostname()
port = 9224
transfer_ip_base = (192<<24)|(168<<16)|(19<<8)|(133)
req_seq = 0
#Set to 1 if handles tranfer on this machine, 0 if redirect to another CDN server
local_avail = 0

def handle_loc(sock, req):
    global req_seq
    global transfer_ip_base 
    global local_avail

    if local_avail == 1:
	transfer_ip_str = sock.getsockname()[0]
	transfer_port = 9224
    else:
	transfer_ip = transfer_ip_base + (req_seq<<8)
	transfer_ip_str = socket.inet_ntoa(struct.pack('I',socket.ntohl(transfer_ip)))
	transfer_port = 8100


    loc_rsp = "HTTP/1.1 201 Created\r\n"\
            "Server: CDNServer/1.0\r\n"\
            "Cache_Control: no-cache\r\n"\
            "Content-Type: text/xml\r\n" "Content-Length: "\
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n"\
            "<LocateResponse>\r\n"\
            "   <TransferPort>%s:%d</TransferPort>\r\n"\
            "   <TransferID>123456ABCDEF</TransferID>\r\n"\
            "   <TransferTimeout>500</TransferTimeout>\r\n"\
            "   <AvailableRange>0-88888888888888</AvailableRange>\r\n"\
            "   <OpenForWrite>no</OpenForWrite>\r\n"\
            "</LocateResponse>\r\n" % (transfer_ip_str, transfer_port)
    sock.send(loc_rsp)
    req_seq = (req_seq+1)%1

def send_junk(sock, datalen, pktlen):
    junk_base = string.lowercase
    junk = junk_base.ljust(pktlen, '#')
    junk_rem = junk_base.ljust(datalen % pktlen, '!')
    npkt = datalen / pktlen
    for i in range(0, npkt):
	time.sleep(0.1)
        sock.send(junk)

    sock.send(junk_rem)


def handle_tran(sock, req):
    start = req.find('bytes=')
    start += len('bytes=')
    end = req.find('-', start)
    start_pos = int(req[start:end])
    start = end + 1
    end = req.find('\r', start)
    end_pos = int(req[start:end])
    range_len = end_pos - start_pos + 1
    print 'Requesting range %d - %d' % (start_pos, end_pos)
    tran_rsp = "HTTP/1.1 206 Partial Content\r\n"\
            "Server: CDNServer/1.0\r\n"\
            "Content-Range: bytes %d-%d/1530000\r\n"\
            "Content-Type: application/octet-stream\r\n"\
            "Transfer-Encoding: chunked\r\n"\
            "Cache-Control: no-cache\r\n\r\n%X\r\n" % (start_pos, end_pos, range_len)
    sock.send(tran_rsp)
    send_junk(sock, range_len, 1316)
    sock.send('\r\n0\r\nThank you')
    


s = socket.socket()
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('', port))
s.listen(5)

while True:
    c, addr = s.accept()
    print 'Got connection from', addr

    while True:
	req = c.recv(512)
	if len(req) > 0:break
	print 'Fail to recv message :'

    if req.find('POST') >= 0: 
        handle_loc(c, req)
	c.close()
    elif req.find('GET') >= 0:
	while True:
	    handle_tran(c, req)
	    req = c.recv(512)
	    if len(req) <= 0 or req.find('GET')<0:
		c.close()
		break
    else:
	print 'Unknown message of %d bytes :' % len(req)
	print req
	c.close()
	continue



