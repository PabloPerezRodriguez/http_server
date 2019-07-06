import socket
from client_thread import ClientThread

# Create TCP/IP Socket
# socket.AF_INET    --> IPv4
# socket.SOCK_STREAM -> STREAM
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Prevent 'Address already in use'
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind server to port
server_ip = 'localhost'
server_port = 8001
server_address = (server_ip, server_port)
print(f'starting up on {server_ip} port {server_port}')
sock.bind(server_address)

threads = []

while True:
    # Listen for incoming connections
    sock.listen(5)

    # IPs
    client_sock, client_address = sock.accept()
    ip, port = client_address

    # Create thread
    thread = ClientThread(ip, port, client_sock)
    thread.start()

    threads.append(thread)
