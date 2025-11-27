import os

# Get project root directory (SIMPLE-WEB-SERVER/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to static directory
STATIC_DIR = os.path.join(BASE_DIR, "static")


def handle_request(method, path, version, client_socket):
    """
    Main router function.
    """

    # -------------------
    # 1. STATIC FILES
    # -------------------
    if path.startswith("/static/"):
        return serve_static(path, client_socket)

    # -------------------
    # 2. ROOT ROUTE
    # -------------------
    if path == "/" or path == "/index":
        return serve_static("/static/index.html", client_socket)

    # -------------------
    # 404
    # -------------------
    send_404(client_socket)


def serve_static(path, client_socket):
    """
    Serve files from /static directory
    """

    # Remove the /static/ part
    filename = path[len("/static/"):]  
    full_path = os.path.join(STATIC_DIR, filename)

    print("Serving:", full_path)

    if not os.path.exists(full_path):
        return send_404(client_socket)

    # Detect MIME type
    if full_path.endswith(".html"):
        content_type = "text/html"
    elif full_path.endswith(".css"):
        content_type = "text/css"
    elif full_path.endswith(".js"):
        content_type = "application/javascript"
    elif full_path.endswith(".png"):
        content_type = "image/png"
    elif full_path.endswith(".jpg") or full_path.endswith(".jpeg"):
        content_type = "image/jpeg"
    else:
        content_type = "application/octet-stream"

    with open(full_path, "rb") as f:
        content = f.read()

    response_headers = (
        "HTTP/1.1 200 OK\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(content)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode()

    client_socket.sendall(response_headers + content)


def send_404(client_socket):
    """Basic 404 response"""
    response = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        "404 - File Not Found"
    )
    client_socket.send(response.encode())
