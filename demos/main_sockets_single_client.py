import socket
# Socket's Listeners
from taskcontrol.webhooks import Sockets


Socket = Sockets()


def client_handler(messages, socket_client):
    # socket_client.get("server").send("Testing the client message".encode())
    # socket_client.get("server").send(str(messages[0]).encode())
    # print(socket_client.get("server").recv(1024).decode())
    # socket_client.get("server").close()
    print("CLIENT", socket_client.get("host"), socket_client.get("port"))
    


config = {"name": "testclient", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
          "host": "127.0.0.1", "port": 9001, "numbers": 1, "handler": client_handler}
# c = Socket.socket_create(config)
# if c:
#     print("Client started")
#     cl = Socket.socket_connect(config, [b"Testing message from client"])
cl = Socket.socket_connect(config, [b"Testing message from client"])


# c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# c.connect("127.0.0.1", 9001)
# c.send("Hello From Client".decode())
# c.recv(1024).decode()
