# Hooks Base

from dataclasses import dataclass
import abc


# Inherit shared and logging


@dataclass(frozen=True)
class SocketsBase(metaclass=abc.ABCMeta):

    def __init__(self):
        self.get_sockets, self.set_sockets = self.sockets_closure()

    def sockets_closure(self):
        sockets = []

        def get_sockets():
            pass

        def set_sockets():
            pass

        return (get_sockets, set_sockets)

    @abc.abstractmethod
    def socket_create(self):
        raise NotImplementedError

    @abc.abstractmethod
    def socket_delete(self):
        raise NotImplementedError

    @abc.abstractmethod
    def socket_listen(self):
        raise NotImplementedError

    @abc.abstractmethod
    def socket_message(self):
        raise NotImplementedError

    @abc.abstractmethod
    def socket_receive(self):
        raise NotImplementedError


class Sockets(SocketsBase):
    
    def __init__(self):
        self.get_sockets, self.set_sockets = self.sockets_closure()

    def sockets_closure(self):
        sockets = []

        def get_sockets():
            pass

        def set_sockets():
            pass

        return (get_sockets, set_sockets)

    def socket_create(self):
        pass

    def socket_delete(self):
        pass

    def socket_listen(self):
        pass

    def socket_message(self):
        pass

    def socket_receive(self):
        pass


@dataclass(frozen=True)
class HooksBase(metaclass=abc.ABCMeta):

    @classmethod
    def __init__(cls, socketsbase=Sockets):
        cls.get_hooks, cls.set_hooks = cls.hooks_closure()
        cls.sockets = socketsbase

    @classmethod
    def hooks_closure(self):

        # list of registered web hooks
        hooks = []

        def get_hooks():
            pass

        def set_hooks():
            pass

        return {"get_hooks": get_hooks, "set_hooks": set_hooks}

    @abc.abstractmethod
    def hook_state(self):
        raise NotImplementedError

    @abc.abstractmethod
    def service_run(self):
        raise NotImplementedError

    @abc.abstractmethod
    def service_stop(self):
        raise NotImplementedError

    @abc.abstractmethod
    def register_hook(self):
        raise NotImplementedError

    @abc.abstractmethod
    def register_receiver(self):
        raise NotImplementedError

    @abc.abstractmethod
    def send(self):
        raise NotImplementedError

    @abc.abstractmethod
    def receive(self):
        raise NotImplementedError


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

__all__ = ["SocketsBase", "Sockets", "Hooks", "HooksBase"]

