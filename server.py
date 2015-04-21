import socket
import time
MAX_SIZE=65534

class DHCP_SERVER:
    def buildOfferPacket(self):
        pkg='\x02\x01\06\x00'
        pkg+='\x11\x22\x33\x44'

        pkg+='\x00\x00\x00\x00'
        pkg+='\x00\x00\x00\x00'

        pkg+='\xC0\xA8\x01\x64'
        pkg+='\xC0\xA8\x01\x01'

        pkg+='\x00\x00\x00\x00'
        pkg+='\x01\x02\x03\x04'
        pkg+='\x05\x06\x00\x00'+('\x00'*200)
        pkg+='\x63\x82\x53\x63'
        pkg+='\x35\x01\x02'
        pkg+='\x01\x04\xff\xff\xff\x00'
        pkg+='\x03\x04\xC0\xA8\x01\x01'
        pkg+='\x33\x04\x00\x01\x51\x80'
        pkg+='\x36\x04\xC0\xA8\x01\x01'
        pkg+='\x06\x0C\x09\x07\x0A\x0f\x09\x07\x0A\x10\x09\x07\x0A\x12'
        return pkg
class DHCP_ACK:
    def buildAckPacket(self):
        pkg='\x02\x01\06\x00'
        pkg+='\x11\x22\x33\x44'
        
        pkg+='\x00\x00\x00\x00'
        pkg+='\x00\x00\x00\x00'
        pkg+='\xC0\xA8\x01\x64'
        pkg+='\xC0\xA8\x01\x01'
        
        pkg+='\x00\x00\x00\x00'
        pkg+='\x01\x02\x03\x04'
        pkg+='\x05\x06\x00\x00'+('\x00'*200)
        pkg+='\x63\x82\x53\x63'

        pkg+='\x35\x01\x06'
        pkg+='\x01\x04\xff\xff\xff\x00'
        pkg+='\x03\x04\xC0\xA8\x01\x01'
        pkg+='\x33\x04\x00\x01\x51\x80'
        pkg+='\x36\x04\xC0\xA8\x01\x01'
        pkg+='\x06\x0C\x09\x07\x0A\x0f\x09\x07\x0A\x10\x09\x07\x0A\x12'

        return pkg
if __name__ == '__main__':
    print('server')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(('',67))
    except Exception as e:
        print('port 67 in use,')
        sock.close()
        input('press an key to quit...')
        exit()
    try:       
        data = sock.recvfrom(MAX_SIZE)
        print(data)
        time.sleep(1)
        #offer
        print('sending OFFER')
          
        data=DHCP_SERVER().buildOfferPacket()
        sock.sendto(data,('',68))
        time.sleep(1)        
        try:
            data = sock.recvfrom(MAX_SIZE)
            print(data)
            time.sleep(1)
            #ack
            print('sending ack')
            #data= DHCP_SERVER().buildOfferPacket()
            data=DHCP_ACK().buildAckPacket()
            sock.sendto(data,('',68))
        except:
            traceback.print_exec()
    except:
        traceback.print_exec()
