# Hooks Base

import socket
import ast
import sys
from .sharedbase import ClosureBase, UtilsBase
# Inherit shared and logging
from .interfaces import SocketsBase, HooksBase


class Sockets(SocketsBase, ClosureBase, UtilsBase):

    def __init__(self):
        super()
        self.getter, self.setter, self.deleter = self.class_closure(sockets={})

    def socket_create(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        try:
            if self.validate_object(config, values=["name", "protocol", "streammode", "host", "port", "numbers", "handler"]):
                # srv = socket.socket(socket[config.get("protocol")], socket[config.get("streammode")])
                srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                config["server"] = srv
                if "workflow_kwargs" not in config:
                    config["workflow_kwargs"] = {}
                if "shared" not in config["workflow_kwargs"]:
                    config["workflow_kwargs"]["shared"] = False
                s = self.setter("sockets", config, self)
                if s:
                    return config
        except Exception as e:
            raise e
        return False

    def socket_listen(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        try:
            s = self.getter("sockets", config.get("name"))
            if len(s) > 0:
                srv = s[0]
            else:
                raise Exception("Server object not found")
            srv.get("server").bind((srv.get("host"), srv.get("port")))
            srv.get("server").setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.get("server").listen(srv.get("numbers"))
            c = self.socket_accept(srv)
            if c:
                sc = self.setter("sockets", srv, self)
                if sc:
                    return sc
        except Exception as e:
            raise e
        return False

    def socket_accept(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")

        # Process exit not happening in Windows using Keyboard
        # import sys
        # import signal

        # def signal_handler(signal, frame):
        #     sys.exit(1)
        # signal.signal(signal.SIGINT, signal_handler)

        s = self.getter("sockets", config.get("name"))
        if len(s) > 0:
            srv = s[0]
        else:
            raise Exception("Server object not found")
        while True and srv:
            try:
                conn, addr = srv.get("server").accept()

                # IMPORTANT NOTES
                # Sending, Receiving data is Handlers work
                # Closing connection is Handlers work
                srv.get("handler")(srv, conn, addr)
            except Exception as e:
                raise e
        return False

    def socket_connect(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        try:
            if self.validate_object(config, values=["name", "protocol", "streammode", "host", "port", "numbers", "handler", "workflow_kwargs", "server"]):
                s = self.getter("sockets", config.get("name"))
                if len(s) > 0:
                    clt = s[0]
                else:
                    raise Exception("Server object not found")
                clt.get("server").connect((clt.get("host"), clt.get("port")))
                clt.get("handler")(clt)
                sc = self.setter("sockets", clt, self)
                if sc:
                    return sc
        except Exception as e:
            raise e
        return False

    def socket_message(self, socket_object, message):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        return socket_object.send(str(message).encode())

    def socket_receive(self, socket_object):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        msg = socket_object.recv(1024).decode()
        return ast.literal_eval(msg)

    def socket_close(self, socket_object):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        return socket_object.close()

    def socket_delete(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        try:
            self.deleter("sockets", config.get("name"))
        except Exception as e:
            raise e
        return True


class Hooks(HooksBase, ClosureBase, UtilsBase):

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


if __name__ == "__main__":
    Socket = Sockets()

    def server_handler(socket_server, conn, addr):
        print(conn, addr)
        print(conn.recv(1024).decode())
        conn.send("Test message from server".encode())
        conn.close()

    # SERVER CODE
    s = Socket.socket_create({"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
                              "host": "127.0.0.1", "port": 9001, "numbers": 1, "handler": server_handler})
    if s:
        print("Server started")
    sr = Socket.socket_listen(s)

    # CLIENT CODE
    def client_handler(socket_client):
        socket_client.get("server").send("Testing the client message".encode())
        print(socket_client.get("server").recv(1024).decode())
        socket_client.get("server").close()

    c = Socket.socket_create({"name": "testclient", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
                              "host": "127.0.0.1", "port": 9001, "numbers": 1, "handler": client_handler})
    if c:
        print("Client started")
    cl = Socket.socket_connect(c)


if __name__ == "__main__":

    hook = Hooks(socketsbase=Sockets)


__all__ = ["Sockets", "Hooks"]
