import socket
import selectors
from taskcontrol.framework.utils import EPubSubBase, SocketsBase


def run(data):
    print("Running Pubsub ", data)


config = {"name": "new", "handler": run, "queue": None, "maxsize": 10,
          "queue_type": "queue", "processing_flag": False,  "batch_interval": 5, "events": {}}

name = config.get("name")

pb = EPubSubBase()
p = pb.pubsub_create(config)


def invoker(action, obj):
    print("Printing action and object ", action, obj)


def publisher(task=None):
    print("Printing data", pb, task)
    # def client_nonblocking_handler(messages, socket_object):
    #     server_addr = (socket_object.get("host"), socket_object.get("port"))
    #     srv = socket_object.get("server")
    #     srv.connect(server_addr)
    #     for msg in messages:
    #         srv.sendall(msg)
    #     data = srv.recv(1024)
    #     print("Received data ", str(data))

    # print("Running publisher ")
    # pconfig = {"name": "testclient", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
    #                    "host": "127.0.0.1", "port": 9001, "numbers": 5, "handler": client_nonblocking_handler, "blocking": False}
    # Socket = SocketsBase()
    # # Trigger an event in the server based on any application event or manual trigger
    # # Use a socket connect to connect to the publisher server
    # Socket.socket_connect(
    #     pconfig, [b"Message 1 from client.", b"Message 2 from client."])
    # # Close the socket connection
    # Socket = None


def server(task=None):
    print("Printing data ", pb, task)
    # def server_nonblocking_handler(key, mask):
    #     sock = key.fileobj
    #     data = key.data
    #     print(pb)

    # def server_blocking_handler(conn, addr, socket_object):
    #     pass

    # print("Running Publisher message to queue ")
    # # Receive the message from the server

    # srvconfig = {"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
    #              "host": "127.0.0.1", "port": 9001, "numbers": 5, "handler": server_nonblocking_handler, "blocking": False}

    # Socket = SocketsBase()
    #
    # s = Socket.socket_create(config)
    # if s:
    #     print("Server started")
    #     sr = Socket.socket_listen(config.get("name"))
    #
    # # Use a server receive to receive the publisher message
    # # Add to the Queue using the publisher function
    # # Process the Queue items using __process/__schedular
    # # Send message to all the subscriber servers
    # # Close the socket connections for subscriber servers


def subscriber(task=None):
    print("Running subscriber ", pb, task)
    # def server_nonblocking_handler(key, mask):
    #     sock = key.fileobj
    #     data = key.data
    #     print(pb)

    # def server_blocking_handler(conn, addr, socket_object):
    #     pass

    # print("Running Publisher message to queue ")
    # # Receive the message from the server
    #
    # srvconfig = {"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
    #              "host": "127.0.0.1", "port": 9001, "numbers": 5, "handler": server_nonblocking_handler, "blocking": False}
    #
    # Socket = SocketsBase()
    #
    # s = Socket.socket_create(config)
    # if s:
    #     print("Server started")
    #     sr = Socket.socket_listen(config.get("name"))
    #
    # Receive the message from the server
    # Use a server receive to receive the server message
    # Add to the Queue using the publisher function
    # Process the Queue items using __process/__schedular
    # Run the subscriber methods if any
    # Close the socket connections for subscriber servers


if p:
    print("Event registered ", pb.register_event(
        name, {"name": "testingevent", "event": run, "invoker": invoker}))
    print("Event listening ", pb.listen(name, "testingevent"))
    print("Publisher registered ", pb.register_publisher(
        name, {"name": "pubone", "event_name": "testingevent", "publisher": publisher, "invoker": invoker}))
    print("Subscribers registered ", pb.register_subscriber(
        name, {"name": "subone", "event_name": "testingevent", "subscriber": subscriber, "invoker": invoker}))
    print("Event sending ", pb.send({"event_name": "testingevent", "queue_name": "new",
                                     "message": "Testing event testingevent", "publisher": "pubone"}))
