import socket
import threading
import os
import sys
import time

target_host = "127.0.0.1"
target_port = 11234

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect((target_host,target_port))

byebye = 0

def handle_send():
		
	while True:
		content = input()
		co = content.encode('ascii')
		if byebye == 1:
			exit()
			break;
		else:
			client.send(co)
			
def handle_receive():
	
	while True:
		response = client.recv(4096)
		re = response.decode('ascii')
		print(re + "\n")
		
		if re=="password:":
			os.system("stty -echo")
			response = client.recv(4096)
			re = response.decode('ascii')
			print(re + "\n")
			if re=="wrong password!":
				os.system("stty echo")
			elif re=="login success!":
				os.system("stty echo")
			else:
				os.system("stty echo")
				
		elif re=="bye":
			global byebye
			byebye = 1
			print("exit")
			break;
	
	
	
send_handler = threading.Thread(target=handle_send,args=())
send_handler.start()
	
receive_handler  = threading.Thread(target=handle_receive,args=())
receive_handler.start()
	
while True:
	if byebye == 1:
		sys.exit()
