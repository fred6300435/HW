import socket
import threading
import time
import datetime

bind_ip = "127.0.0.1"
bind_port =11111 

users = ["fred", "qqq", "aaa"]
passwords = ["fred", "qqq", "aaa"]
login_state = [0,0,0]
login_ip = ["127.0.0.1","127.0.0.1","127.0.0.1"]
login_port = [bind_port,bind_port,bind_port]
towho = [-1,-1,-1]
message = ["", "", ""]

broad = [-1,-1,-1]
bmessage = ""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.bind((bind_ip,bind_port))

server.listen(5)
	
print("[*] Listening on "+ bind_ip +":" + str(bind_port))	
def handle_client(client_socket,ipadd,portadd):
		
	#----- login -----#
	logincheck = 1
	sendlock = 1
	while logincheck!=0:
	
		content = "login:"
		co = content.encode('ascii')
		client_socket.send(co)
		
		request = client_socket.recv(1024)
		re = request .decode('ascii')
		print("[*] login:" + re)
		
		for i in range(len(users)):
			if re==users[i]:
				uid = i
				
				content = "password:"
				co = content.encode('ascii')
				client_socket.send(co)
				
				request = client_socket.recv(1024)
				re = request .decode('ascii')
				
				if  re==passwords[uid] :
					logincheck = 0
					content = "login success!"
					co = content.encode('ascii')
					client_socket.send(co)
					login_state[uid] = 1
					login_ip[uid] = ipadd
					login_port[uid] = portadd
					print("[*]"+users[uid]+ str(uid) +" login from address:"+login_ip[uid] +":"+ str(login_port[uid]))
				else:
					logincheck = 3
				break;
			else:
				logincheck = 2
								
		if logincheck == 3:
			content = "wrong password!"
			co = content.encode('ascii')
			client_socket.send(co)
			
		elif logincheck==2:
			content = "user not exist!"
			co = content.encode('ascii')
			client_socket.send(co)	
		
		
	content = "Messenger Start!!"
	co = content.encode('ascii')
	client_socket.send(co)
	
	global bmessage
		
	while True:
		
		request = client_socket.recv(1024)
		re = request .decode('ascii')
		print("[*] Received:" + re)
		if re=="listuser":
			for i in range(len(users)):
				if login_state[i] == 1:
					onlineuser  = users[i] + "\n"
					on = onlineuser.encode('ascii')			
					client_socket.send(on)

		elif re=="logout":
			content = "bye"
			co = content.encode('ascii')
			client_socket.send(co)
			client_socket.close()
			login_state[uid] = 0
			break;
		
		elif re[0:4]=="talk":
			sendlock = 1
			print(re[5:])
			for i in range(len(users)):
				if re[5:]==users[i]:
					while sendlock == 1:
						print("to "+users[i])
						request = client_socket.recv(1024)
						re = request .decode('ascii')
						print(re)
						current = datetime.datetime.now()
						message[uid] = message[i] +re + " from " + str(current)
						towho[uid] = i
						time.sleep(1)
						if re=="bye":
							sendlock = 0
								
		elif re[0:9]=="broadcast":
			print(re[10:])
			current = datetime.datetime.now()
			bmessage = re[10:] + "  from " + str(current)
			for i in range(len(users)):
				towho[i] = -2
		else:
			content = "wrong comment!"
			co = content.encode('ascii')
			client_socket.send(co)
				
			
def client_listen(client_socket,ipadd,portadd):
	lock = 0
	while lock == 0:
		for i in range(len(users)):
			if(ipadd == login_ip[i] and portadd == login_port[i]):
				lock = 1			
				uid = i
				break;
	
	while True:
		
		for i in range(len(users)):
			time.sleep(1)
			
			if towho[i] == uid:
				content = users[i] + ":"+ message[i]
				co = content.encode('ascii')
				client_socket.send(co)
				towho[i] = -1
				message[i] = ""
			elif towho[uid] == -2:
				content2 = "broadcast:"
				co2 = content2.encode('ascii')
				client_socket.send(co2)
				print(users[uid] + "send broadcast package1")
				content3 = bmessage
				co3 = content3.encode('ascii')
				client_socket.send(co3)
				print(users[uid] + "send broadcast package2")
				towho[uid] = -1
				
				
			
while True:
	
	client_socket,addr = server.accept()
	print("[*] Accept connection from:"+ addr[0] +":" + str(addr[1]))
	
	
	client_handler = threading.Thread(target=handle_client,args=(client_socket,addr[0],addr[1],))
	client_handler.start()
	
	client_listener = threading.Thread(target=client_listen,args=(client_socket,addr[0],addr[1],))
	client_listener.start()
