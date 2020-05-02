# Actions and Hooks Base
# TODO: Create structure


# Inherit shared and logging
class ActionsBase():

    # list of registered actions/events
    actions = []
    # list of actions/events listeners
    action_listeners = []

    def action_state(self):
        pass

    def register_event(self):
        pass

    def register_listener(self):
        pass

    def unregister_listener(self):
        pass

    def message(self):
        pass

    def listen(self):
        pass


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

