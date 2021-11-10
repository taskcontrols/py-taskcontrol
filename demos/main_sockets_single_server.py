import socket
# Socket's Listeners
from taskcontrol.lib.utils import SocketsBase


Socket = SocketsBase()


def server_handler(conn, addr, socket_server):
    print("SERVER", conn, addr)
    conn.send(b"Hello, world from server")
    data = conn.recv(1024)
    print("Received ", str(data))
    # print(conn.recv(1024).decode())
    # conn.send("Test message from server".encode())
    conn.close()


config = {"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
          "host": "127.0.0.1", "port": 9001, "numbers": 1, "handler": server_handler}

# METHOD ONE:
s = Socket.socket_create(config)
if s:
    print("Server started")
    sr = Socket.socket_listen(config.get("name"))
