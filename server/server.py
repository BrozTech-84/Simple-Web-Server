# ...existing code...
import socket
import traceback
import os

def get_content_type(filename):
    if filename.endswith(".html"):
        return "text/html"
    elif filename.endswith(".css"):
        return "text/css"
    elif filename.endswith(".js"):
        return "application/javascript"
    elif filename.endswith(".png"):
        return "image/png"
    elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
        return "image/jpeg"
    elif filename.endswith(".svg"):
        return "image/svg+xml"
    elif filename.endswith(".woff") or filename.endswith(".woff2"):
        return "font/woff2"
    elif filename.endswith(".ttf"):
        return "font/ttf"
    else:
        return "application/octet-stream"


def parse_request_line(request_text):
    if not request_text:
        raise ValueError("Empty request")
    first_line = request_text.split("\r\n", 1)[0]
    parts = first_line.split(" ")
    if len(parts) < 3:
        raise ValueError(f"Invalid request line: {first_line!r}")
    method, path, version = parts[0], parts[1], " ".join(parts[2:])
    return method, path, version


def parse_headers(request_text):
    lines = request_text.split("\r\n")
    headers = {}
    for line in lines[1:]:
        if line == "":
            break
        if ": " in line:
            key, value = line.split(": ", 1)
            headers[key] = value
    return headers

def read_request(client_socket, max_size=65536):
    buffer = b""
    client_socket.settimeout(1.0)
    try:
        while b"\r\n\r\n" not in buffer and len(buffer) < max_size:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            buffer += chunk
    except socket.timeout:
        pass
    finally:
        client_socket.settimeout(None)
    return buffer.decode("utf-8", errors="replace")

HOST = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server_socket.bind((HOST, PORT))
except OSError as e:
    print("Failed to bind:", e)
    print("If the port is in use, change PORT or stop the process using it.")
    raise

print("Bound to port", PORT)
server_socket.listen(5)
print("Server is listening...")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from", client_address)
        try:
            raw_request = read_request(client_socket)
            if not raw_request:
                print("Empty request received, closing connection.")
                client_socket.close()
                continue

            print("Raw request received:")
            print(raw_request)

            try:
                method, path, version = parse_request_line(raw_request) 
                headers = parse_headers(raw_request)    
            except ValueError as e:
                print("Failed to parse request:", e)
                response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nBad Request"
                client_socket.send(response.encode("utf-8"))
                client_socket.close()
                continue

            print("\nParsed Request Line:", method, path, version)
            print("Parsed Headers:", headers)

            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello!"
            client_socket.send(response.encode("utf-8"))
        except Exception:
            print("Error handling connection:")
            traceback.print_exc()
        finally:
            client_socket.close()

except KeyboardInterrupt:
    print("\nServer shutting down...")
finally:
    server_socket.close()

# ===========================
# Serve Static Files
# ===========================

if path.startswith("/static/"):
    file_path = path.lstrip("/")  # remove leading slash
    full_path = os.path.join(os.getcwd(), file_path)

    if os.path.exists(full_path) and os.path.isfile(full_path):
        # Read file as binary
        with open(full_path, "rb") as f:
            body = f.read()

        content_type = get_content_type(full_path)

        
        # Send headers
        header = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
        )

        client_socket.sendall(header.encode() + body)
    
    else:
        # File not found
        body = b"404 Not Found"
        header = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
        )
        
        client_socket.sendall(header.encode() + body)
        