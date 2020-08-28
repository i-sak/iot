#!/usr/bin/env python3

import socket

HOST = '192.168.219.111'
PORT = 11211

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

client_socket.connect((HOST, PORT)) 


while True: 

    message = input('Enter Message : ')
    if message == 'quit':
    	break

    client_socket.send(message.encode()) 
    data = client_socket.recv(1024) 

    print('Received from the server :',repr(data.decode())) 


client_socket.close() 
