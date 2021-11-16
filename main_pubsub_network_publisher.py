import socket
import selectors
from taskcontrol.lib import EPubSubBase, SocketsBase


def run(data):
    print("Running Pubsub ", data)


config = {
    "name": "new", "handler": run, "queue": None, "maxsize": 10, "queue_type": "queue",
    "processing_flag": False,  "batch_interval": 5, "events": {}
}

name = config.get("name")

pb = EPubSubBase(validations={}, pubsubs={}, types="epubsub", agent="publisher")
p = pb.pubsub_create(config)


def server(task=None):
    #
    # # Use a server receive to receive the publisher message
    # # Add to the Queue using the publisher function
    # # Process the Queue items using __process/__schedular
    # # Send message to all the subscriber servers
    # # Close the socket connections for subscriber servers
    #
    print("Running server handler ", pb, task)

    def server_nonblocking_handler(key, mask):
        sock = key.fileobj
        data = key.data
        

    # def server_blocking_handler(conn, addr, socket_object):
    #     pass

    # print("Running Publisher message to queue ")
    # # Receive the message from the server
    srvconfig = {"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
                 "host": "127.0.0.1", "port": 9001, "numbers": 5, "handler": server_nonblocking_handler, "blocking": False}

    Socket = SocketsBase()
    s = Socket.socket_create(srvconfig)
    if s:
        print("Server started ")
        sr = Socket.socket_listen(srvconfig.get("name"))


def publisher(task=None):
    print("Running publisher handler ", pb, task)
    # return True

    # Publisher function should send an
    # application event to server queue for processing
    #
    def client_nonblocking_handler(messages, socket_object):
        # Function to handle data from the publisher
        server_addr = (socket_object.get("host"), socket_object.get("port"))
        srv = socket_object.get("server")
        srv.connect(server_addr)
        for msg in messages:
            srv.sendall(msg)
        data = srv.recv(1024)
        print("Received data ", str(data))

    # print("Running publisher ")
    pconfig = {"name": "testclient", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
                       "host": "127.0.0.1", "port": 9002, "numbers": 5, "handler": client_nonblocking_handler, "blocking": False}

    Socket = SocketsBase()
    # # Trigger an event in the server based on any application event or manual trigger
    # # Use a socket connect to connect to the publisher server
    Socket.socket_connect(
        pconfig, [b"Message 1 from server.", b"Message 2 from server."])
    # # Close the socket connection
    # Socket = None


def subscriber(task=None):
    print("Running subscriber handler ", pb, task)

    def server_nonblocking_handler(key, mask):
        # Function to handle data from the subscriber
        sock = key.fileobj
        data = key.data
        print("Subscriber function data ", data)

    # def server_blocking_handler(conn, addr, socket_object):
    #     pass

    # print("Running Publisher message to queue ")
    # # Receive the message from the server
    #
    # # Subscriber Servers Host, Port, Handler (Optional in servr based on need), Protocol of subscriber
    sconfig = {"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
               "host": "127.0.0.1", "port": 9003, "numbers": 5, "handler": server_nonblocking_handler, "blocking": False}

    Socket = SocketsBase()

    s = Socket.socket_create(sconfig)
    if s:
        print("Server Message sent ")
        Socket.socket_connect(
            sconfig, [b"Message 1 from server.", b"Message 2 from server."])
    


if p:
    print("Event registered ", pb.register_event(
        name, {"name": "testingevent", "event": run}))
    print("Event listening ", pb.listen(name, "testingevent"))
    print("Publisher registered ", pb.register_publisher(
        name, {"name": "pubone", "event_name": "testingevent", "publisher": publisher}))
    print("Subscribers registered ", pb.register_subscriber(
        name, {"name": "subone", "event_name": "testingevent", "subscriber": subscriber}))
    print("Event sending (Response Results): ", pb.send({"event_name": "testingevent", "queue_name": "new",
                                                         "message": "Testing event testingevent", "publisher": "pubone"}))
