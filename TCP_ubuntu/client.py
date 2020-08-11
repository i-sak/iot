#!/usr/bin/env python3

import socket

#HOST = '192.168.0.4'  # The server's hostname or IP address
HOST = '192.168.219.111'
PORT = 11211        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b'Hello, world')
data = s.recv(1024)

print('Received', repr(data))

