import socket

def parse_headers(request_text):
    lines = request_text.split("\r\n")
    headers = {}
    for line in lines[1:]:
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value
        if line == "":
            break
    return headers

HOST = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
print("Bound to port", PORT)

server_socket.listen(5)
print("Server is listening...")

try:
    while True:  # 🔹 Keep server alive for multiple requests
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from", client_address)

        raw_request_bytes = client_socket.recv(1024)
        raw_request = raw_request_bytes.decode()

        print("Raw request received:")
        print(raw_request)

        headers = parse_headers(raw_request)
        print("\nParsed Headers Dictionary:")
        print(headers)

        # Simple response
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello!"
        client_socket.send(response.encode("utf-8"))
        client_socket.close()

except KeyboardInterrupt:
    print("\nServer shutting down...")
    server_socket.close()
