# Hooks Base


class SocketsBase():
    pass


# Inherit shared and logging
class HooksBase():

    def __init__(self):
        self.get_hooks, self.set_hooks = self.hooks_closure()
    
    def hooks_closure(self):
        # list of registered web hooks
        hooks = []

        def get_hooks():
            pass

        def set_hooks():
            pass

        return {"get_hooks": get_hooks, "set_hooks": set_hooks}

    def hook_state(self):
        pass

    def service_run(self):
        pass

    def service_stop(self):
        pass

    def register_hook(self):
        pass

    def register_receiver(self):
        pass

    def send(self):
        pass

    def receive(self):
        pass

