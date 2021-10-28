import socket
# Socket's Listeners
from taskcontrol.utils import SocketsBase


Socket = SocketsBase()


def client_blocking_handler(messages, socket_object):
    """
    Applies for numbers: 1
    """
    pass


def client_nonblocking_handler(key, mask, sel, socket_object):
    """
    Applies for numbers > 1
    """
    # sock.send("Testing the client message".encode())
    # print(sock.recv(1024).decode())
    # sock.close()
    # print("Test")
    pass


config = {"name": "testclient", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
          "host": "127.0.0.1", "port": 9001, "numbers": 5, "handler": client_nonblocking_handler, "blocking": False}

# c = Socket.socket_create(config)
# if c:
#     print("Client started")
#     cl = Socket.socket_connect(
#         config.get("name"), [b"Test message from client"]
#     )

Socket.socket_connect(
    config, [b"Message 1 from client.", b"Message 2 from client."])
