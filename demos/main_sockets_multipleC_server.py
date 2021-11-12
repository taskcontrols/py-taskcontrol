import socket
# Socket's Listeners
from taskcontrol.lib import SocketsBase


Socket = SocketsBase()


def server_blocking_handler(conn, addr, socket_object):
    pass


def server_nonblocking_handler(key, mask, data, sock, conn, addr, socket_object):
    print(conn, addr)
    # print(conn.recv(1024))
    # conn.send("Test message from server".encode())
    # conn.close()


config = {"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
          "host": "127.0.0.1", "port": 9001, "numbers": 5, "handler": server_nonblocking_handler, "blocking": False}

s = Socket.socket_create(config)
if s:
    print("Server started")
    sr = Socket.socket_listen(config.get("name"))
