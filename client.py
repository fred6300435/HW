import socket,argparse
import time
MAX_SIZE=65534
class DHCP_DISCOVER:
    def buildPacket(self):
        pkg='\x01\x01\x06\x00'
        pkg+='\x11\x22\x33\x44' + ('\x00'*20)
        pkg+='\x01\x02\x03\x04\x05\x06'+('\x00'*202)
        pkg+='\x63\x82\x53\x63'

        pkg+='\x32\x04\xC0\xA8\x01\x64'
        pkg+='\x35\x01\x01'
        pkg+='\x37\x04\x01\x0f\x03\x06'
        pkg+='\xff'
        return pkg
class DHCP_REQUEST:
    def buildPacket(self):
        pkg='\x01\x01\x06\x00'
        pkg+='\x11\x22\x33\x44' + ('\x00'*12)
        pkg+='\xC0\xA8\x01\x01'
        pkg+='\x00\x00\x00\x00'
        pkg+='\x01\x02\x03\x04\x05\x06'+('\x00'*202)
        pkg+='\x63\x82\x53\x63'

        pkg+='\x32\x04\xC0\xA8\x01\x64'
        pkg+='\x35\x01\x03'
        pkg+='\x36\x04\xC0\xA8\x01\x01'
        pkg+='\xff' 
        return pkg


if __name__ == '__main__' :
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)    
    try:    
        sock.bind(('',68))
    except Exception as e:
        print('port 68 in use,,')
        sock.close()
        input('press an key to quit...')
        exit()
    
    print('Start discover')
    data = DHCP_DISCOVER().buildPacket()
    sock.sendto(data, ('255.255.255.255',67))
    time.sleep(1)

    print('wait OFFER')
    data = sock.recvfrom(MAX_SIZE)
    print(data)
    time.sleep(1)
    print('send request')
    data =  DHCP_REQUEST().buildPacket()
    sock.sendto(data , ('255.255.255.255', 67))
    time.sleep(1)
    print('wait ack')
    data = sock.recvfrom(MAX_SIZE)
    print(data)
