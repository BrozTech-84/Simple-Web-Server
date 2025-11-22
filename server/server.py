# Entry point for the web server (implementation later)

import socket

HOST = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind to port
server_socket.bind((HOST, PORT))
print("Bound to port", PORT)

#Listen
server_socket.listen(1) 
print("Server is listening...")

#Accept connection
client_socket, client_address = server_socket.accept() 
print("Accepted connection from", client_address)

#Print  raw request
raw_request = client_socket.recv(1024) 
print("Raw request received:") 
print(raw_request.decode())