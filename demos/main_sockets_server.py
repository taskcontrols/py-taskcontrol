
import socket
# Socket's Listeners
from taskcontrol.hooks import Sockets


Socket = Sockets()

def server_handler(socket_server, conn, addr):
    print(conn, addr)
    print(conn.recv(1024).decode())
    conn.send("Test message from server".encode())
    conn.close()

s = Socket.socket_create({"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
                            "host": "127.0.0.1", "port": 9001, "numbers": 1, "handler": server_handler})
if s:
    print("Server started")
sr = Socket.socket_listen(s)

# c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# c.connect("127.0.0.1", 9001)
# c.send("Hello From Client".decode())
# c.recv(1024).decode()

