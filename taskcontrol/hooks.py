# Hooks Base


# Inherit shared and logging
from .interfaces import SocketsBase, HooksBase

class Sockets(SocketsBase):

    def __init__(self):
        self.get_sockets, self.set_sockets = self.sockets_closure()

    def sockets_closure(self):
        sockets = []

        def get_sockets():
            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def set_sockets():
            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        return (get_sockets, set_sockets)

    def socket_create(self):
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def socket_delete(self):
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def socket_listen(self):
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def socket_message(self):
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def socket_receive(self):
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass


class Hooks(HooksBase):

    def __init__(self, socketsbase=Sockets):
        self.get_hooks, self.set_hooks = self.hooks_closure()
        self.sockets = socketsbase

    def hooks_closure(self):

        # list of registered web hooks
        hooks = []

        def get_hooks():
            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def set_hooks():
            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        return {"get_hooks": get_hooks, "set_hooks": set_hooks}

    def hook_state(self):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def service_run(self):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def service_stop(self):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def register_hook(self):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def register_receiver(self):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def send(self):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def receive(self):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

__all__ = ["Sockets", "Hooks"]

