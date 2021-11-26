import json
import socket
import selectors
from taskcontrol.lib import IPubSubBase, SocketsBase


def run(data):
    print("Running Pubsub ", data)


config = {
    "name": "new", "handler": run, "queue": None, "maxsize": 10, "queue_type": "queue",
    "processing_flag": False,  "batch_interval": 5, "events": {}
}

name = config.get("name")

pb = IPubSubBase(types="ipubsub", agent="server")
p = pb.pubsub_create(config)


def server(task=None, handler=lambda x: x):
    #
    # # Use a server receive to receive the publisher message
    # # Add to the Queue using the publisher function
    # # Process the Queue items using __process/__schedular
    # # Send message to all the subscriber servers
    # # Close the socket connections for subscriber servers
    #
    print("Running server handler ", pb, task)

    def server_nonblocking_handler(key, mask, self):
        sock = key.fileobj
        data = key.data
        print("Sending data ", str(data))
        d = self.string_to_json(data)
        print("Sending data ", d, d.__name__)
        # Parse message
        # Run authentication
        # Run checks
        # Check event
        # Publisher:
        #   # Add event to queue if event
        #   # Process event of addition of publisher if event is register publisher
        #   # Process event of addition of subscriber if event is register subscriber_from_publisher
        #   # Process event of addition of event if event is event
        # Subscriber:
        #   # Process event of addition of subscriber if event is register subscriber_from_subscriber
        #   # Process event of addition of event if event is event

    # def server_blocking_handler(conn, addr, socket_object):
    #     pass
    #
    # print("Running Publisher message to queue ")
    # # Receive the message from the server

    srvconfig = {"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
                 "host": "127.0.0.1", "port": 9001, "numbers": 1, "handler": server_nonblocking_handler, "blocking": False}

    Socket = SocketsBase()
    s = Socket.socket_create(srvconfig)
    if s:
        # sr = Socket.socket_listen(srvconfig.get("name"))
        print("Server started ")
        return True
    return False


def publisher(task=None, handler=lambda x: x):
    print("Running publisher handler ", pb, task)

    # Publisher function should send an
    # application event to server queue for processing
    #
    def client_nonblocking_handler(messages, socket_object, self):
        # Function to handle data from the publisher
        s = self.fetch(socket_object.get("name"))
        srv = s.get("server")
        server_addr = (socket_object.get("host"), socket_object.get("port"))
        srv.connect(server_addr)
        srv.sendall(b"Hello, world from client")
        data = srv.recv(1024)
        print("Received ", str(data))
        # Do whatever with received data
        try:
            s.get("server").close()
        except Exception:
            pass

    # # print("Running publisher ")
    # pconfig = {"name": "testclient", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
    #                    "host": "127.0.0.1", "port": 9002, "numbers": 1, "handler": client_nonblocking_handler, "blocking": False}

    # Socket = SocketsBase()
    # s = Socket.socket_create(pconfig)
    # if s:
    #     Socket.socket_connect(
    #         pconfig, [b"Message 1 from server.", b"Message 2 from server."])
    #     print("Server Message sent to Publisher ")
    # # # Trigger an event in the server based on any application event or manual trigger
    # # # Use a socket connect to connect to the publisher server

    # # Close the socket connection
    # Socket = None


def subscriber(task=None, handler=lambda x: x):
    print("Running subscriber handler ", pb, task)

    def server_nonblocking_handler(messages, socket_object, self):
        # Function to handle data from the subscriber
        s = self.fetch(socket_object.get("name"))
        srv = s.get("server")
        server_addr = (socket_object.get("host"), socket_object.get("port"))
        srv.connect(server_addr)
        srv.sendall(b"Hello, world from client")
        data = srv.recv(1024)
        print("Received ", str(data))
        # Do whatever with received data
        try:
            s.get("server").close()
        except Exception:
            pass

    # def server_blocking_handler(conn, addr, socket_object):
    #     pass
    #
    # print("Running Publisher message to queue ")
    # # Receive the message from the server
    #
    # # Subscriber Servers Host, Port, Handler (Optional in servr based on need), Protocol of subscriber
    sconfig = {"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
               "host": "127.0.0.1", "port": 9003, "numbers": 1, "handler": server_nonblocking_handler, "blocking": False}

    Socket = SocketsBase()
    s = Socket.socket_create(sconfig)
    if s:
        Socket.socket_connect(
            sconfig, [b"Message 1 from server.", b"Message 2 from server."])
        print("Server Message sent to Subscriber ")
    #
    # Receive the message from the server
    # Use a server receive to receive the server message
    # Add to the Queue using the publisher function
    # Process the Queue items using __process/__schedular
    # Run the subscriber methods if any
    # Close the socket connections for subscriber servers


if p:
    print("Event registered ", pb.register_event(
        name, {"name": "testingevent", "handler": server}))
    print("Event listening ", pb.listen(name, "testingevent"))
    print("Publisher registered ", pb.register_publisher(
        name, {"name": "pubone", "event_name": "testingevent", "publisher": publisher}))
    print("Subscribers registered ", pb.register_subscriber(
        name, {"name": "subone", "event_name": "testingevent", "subscriber": subscriber}))
    print("Event sending (Response Results): ", pb.send({"event_name": "testingevent", "queue_name": "new",
                                                         "message": "Testing event testingevent", "publisher": "pubone"}))
