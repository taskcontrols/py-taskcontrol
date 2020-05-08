

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
