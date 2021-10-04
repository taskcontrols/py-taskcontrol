# Hooks Base

import ast
import time
import sys
import types
import socket
import selectors
import copy
from .sharedbase import ClosureBase, UtilsBase
# Inherit shared and logging
from .interfaces import SocketsBase, HooksBase, SshBase, PubSubBase
from .actions import Queues, Events, EPubSub


class Sockets(UtilsBase, SocketsBase):

    validations = {
        "create": ["name", "protocol", "streammode", "host", "port", "numbers", "handler", "blocking", "nonblocking_data", "nonblocking_timeout", "server"],
        "add": ["name", "protocol", "streammode", "host", "port", "numbers", "handler", "blocking", "nonblocking_data", "nonblocking_timeout", "workflow_kwargs", "server"],
        "fetch": ["name"],
        "update": ["name"],
        "delete": ["name"]
    }

    def __init__(self, socket={}):
        super().__init__("sockets", validations=self.validations, sockets=socket)

    def socket_create(self, socket_object):
        socket_object.update({
            "blocking": socket_object.get("blocking", True),
            "nonblocking_data": socket_object.get("nonblocking_data", None),
            "nonblocking_timeout": socket_object.get("nonblocking_timeout", 1),
            "server": socket_object.get("server", None)
        })
        if self.validate_object(socket_object, values=self.validations.get("create")):
            srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_object.update({"server": srv})
            return self.create(socket_object)
        raise ValueError

    def socket_listen(self, socket_name):
        sel = selectors.DefaultSelector()
        socket_object = self.fetch(socket_name)
        blocking = socket_object.get("blocking", False)
        srv = socket_object.get("server")
        srv.bind((socket_object.get("host"), socket_object.get("port")))
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.listen(socket_object.get("numbers", 1))
        srv.setblocking(blocking)
        if not blocking:
            sel.register(srv, selectors.EVENT_READ, data=None)
        socket_object.update({"server": srv, "selectors": sel})
        self.socket_accept(socket_object)
        return True

    def socket_accept(self, socket_object):
        srv = socket_object.get("server")
        sel = socket_object.get("selectors")
        blocking = socket_object.get("blocking")
        while True and srv:
            if blocking:
                try:
                    conn, addr = srv.accept()

                    # IMPORTANT NOTES
                    # Sending, Receiving data is Handlers work
                    # Closing connection is Handlers work
                    socket_object.get("handler")(conn, addr, socket_object)
                    try:
                        if conn:
                            conn.close()
                    except Exception as e:
                        pass
                    print("Closing connection to client", str(addr))
                except KeyboardInterrupt:
                    print("Exiting due to keyboard interrupt")
                except Exception as e:
                    raise e
            else:
                def accept_wrapper(sock):
                    try:
                        # Should be ready to read
                        conn, addr = sock.accept()  # Should be ready to read
                        print("accepted connection from", addr)
                        # conn.setblocking(False)
                        data = types.SimpleNamespace(
                            addr=addr, inb=b"", outb=b"")
                        events = selectors.EVENT_READ | selectors.EVENT_WRITE
                        sel.register(conn, events, data=data)
                        return True
                    except Exception as e:
                        print("Error in service connection: accept_wrapper")
                        # raise e
                        return False

                def service_connection(key, mask):
                    try:
                        sock = key.fileobj
                        data = key.data
                        if mask & selectors.EVENT_READ:
                            # Should be ready to read
                            recv_data = sock.recv(1024)
                            if recv_data:
                                data.outb += recv_data
                            else:
                                print("closing connection to", data.addr)
                                sel.unregister(sock)
                                sock.close()
                        if mask & selectors.EVENT_WRITE:
                            if data.outb:
                                print("echoing", repr(
                                    data.outb), "to", data.addr)
                                # Should be ready to write
                                sent = sock.send(data.outb)
                                data.outb = data.outb[sent:]
                        # sock.close()
                        return True
                    except Exception as e:
                        print("Error in service connection: service_connection")
                        # raise e
                        return False
                try:
                    while True:
                        events = sel.select(timeout=None)
                        for key, mask in events:
                            if key.data is None:
                                accept_wrapper(key.fileobj)
                            else:
                                service_connection(key, mask)
                except KeyboardInterrupt:
                    print("Caught keyboard interrupt, exiting")
                    sys.exit(0)
                finally:
                    sel.close()

        print("Server connection to client closed")
        socket_object.update({"server": srv, "selectors": sel})
        return self.update(socket_object)

    def socket_multi_server_connect(self, socket_object, messages=[]):
        connections = socket_object.get("numbers", 1)
        server_addr = (socket_object.get("host"), socket_object.get("port"))
        sel = selectors.DefaultSelector()
        blocking = socket_object.get("blocking", False)

        def service_connection(key, mask):
            sock = key.fileobj
            data = key.data
            if mask & selectors.EVENT_READ:
                recv_data = sock.recv(1024)  # Should be ready to read
                if recv_data:
                    print("Received ", repr(recv_data),
                          " from connection ", data.connid)
                    data.recv_total += len(recv_data)
                if not recv_data or data.recv_total == data.msg_total:
                    print("Closing connection ", data.connid)
                    sel.unregister(sock)
                    sock.close()
            if mask & selectors.EVENT_WRITE:
                if not data.outb and data.messages:
                    data.outb = data.messages.pop(0)
                if data.outb:
                    print("Sending ", repr(data.outb),
                          " to connection ", data.connid)
                    # Should be ready to write
                    sent = sock.send(data.outb)
                    data.outb = data.outb[sent:]

        for i in range(0, connections):
            connid = i + 1
            print("Starting connection ", connid, " to ", server_addr)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(blocking)
            sock.connect_ex(server_addr)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(
                connid=connid,
                msg_total=sum(len(m) for m in messages),
                recv_total=0,
                messages=list(messages),
                outb=b"",
            )
            sel.register(sock, events, data=data)
        try:
            while True:
                events = sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        service_connection(key, mask)
                # Check for a socket being monitored to continue.
                if not sel.get_map():
                    break
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            sel.close()

    def socket_connect(self, socket_object, messages=[]):
        connections = socket_object.get("numbers", 1)
        server_addr = (socket_object.get("host"), socket_object.get("port"))
        sel = selectors.DefaultSelector()
        blocking = socket_object.get("blocking", False)
        if connections == 0:
            raise ValueError
        elif connections < 2:
            o = self.socket_create(socket_object)
            if o:
                s = self.fetch(socket_object.get("name"))
                srv = s.get("server")
                srv.connect(server_addr)
                srv.sendall(b"Hello, world from client")
                data = srv.recv(1024)
                print("Received ", str(data))
                s.get("handler")(messages, s)
                try:
                    s.get("server").close()
                except Exception:
                    pass
        else:
            o = socket_object
            o["selectors"] = sel
            self.socket_multi_server_connect(o, messages)

    def socket_close(self, socket_object):
        return socket_object.close()

    def socket_delete(self, socket_object):
        try:
            return self.delete(socket_object.get("name"))
        except Exception as e:
            raise e

    def send(self, socket_object, message):
        return socket_object.send(str(message).encode())

    def receive(self, socket_object):
        msg = socket_object.recv(1024).decode()
        return ast.literal_eval(msg)


class IPubSub(EPubSub):

    def __init__(self, pubsubs={}, type="ipubsub"):
        super().__init__(pubsubs=pubsubs, type="ipubsub")
        self.v = ["name", "handler", "queue", "maxsize",
                  "queue_type", "batch_interval", "processing_flag", "events", "workflow_kwargs"]
        self.ev = ["name", "pubsub_name", "publishers", "subscribers"]


class Hooks(UtilsBase, HooksBase):

    def __init__(self, socketsbase=Sockets):
        super()
        self.getter, self.setter, self.deleter = self.class_closure(hooks={})
        self.sockets = socketsbase

    def hook_state(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def service_run(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def service_stop(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def register_hook(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def register_receiver(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def send(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def receive(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass


class SSH(UtilsBase, SshBase):

    def __init__(self, pubsub={}):
        super().__init__("pubsubs", pubsubs=pubsub)

    def create(self, options):
        pass

    def connect(self, options):
        pass

    def execute(self, options):
        pass

    def close(self, options):
        pass


if __name__ == "__main__":
    Socket = Sockets()


if __name__ == "__main__":
    hook = Hooks(socketsbase=Sockets)


if __name__ == "__main__":
    ssh = SSH()


__all__ = ["Sockets", "Hooks"]
