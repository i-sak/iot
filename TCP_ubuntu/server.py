#!/usr/bin/env python3

import socket

#HOST = '192.168.0.4'
HOST = '192.168.219.111'
PORT = 11211

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
with conn:
	print("Connected by", addr)
	while True:
		data = conn.recv(1024)
		if not data:
			break
		conn.sendall(data)
