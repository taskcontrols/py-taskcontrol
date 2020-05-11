# Hooks Base

# Inherit shared and logging
class HooksBase():

    # list of registered web hooks
    hooks = []

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

