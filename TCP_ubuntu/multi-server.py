#!/usr/bin/env python3

import socket
from _thread import *

def threaded(client_socket, addr):
	print('Connected by : ', addr[0], ':', addr[1])
	
	while True :

		try:
			data=client_socket.recv(1024) # data recive
			
			# no data ->> break
			if not data :
				print('Disconneted by ' +addr[0], ':', addr[1])
				break
			print('Received from '+addr[0],':',addr[1],data.decode())
			client_socket.send(data)
		except ConnectionResetError as e:
			print('Disconnected by '+ addr[0], ':', addr[1])
			break

	client_socket.close()

HOST = '192.168.219.111'
PORT = 11211

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 

print('server start')

while True: 

    print('wait')

    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr)) 

server_socket.close() 
