# Hooks Base

# TODO: Refactor getters and setters and make code simpler
from .sharedbase import ClosureBase
# Inherit shared and logging
from .interfaces import SocketsBase, HooksBase


class Sockets(SocketsBase, ClosureBase):

    def __init__(self):
        super()
        self.getter, self.setter, self.deleter = self.class_closure(sockets={})

    def socket_create(self, config):
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def socket_delete(self, config):
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def socket_listen(self, config):
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def socket_message(self, config):
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def socket_receive(self, config):
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass


class Hooks(HooksBase, ClosureBase):

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


__all__ = ["Sockets", "Hooks"]
