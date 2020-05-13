# Actions Base

# Inherit shared and logging

# TODO: Check impact of self on closure


class ActionsBase():
    """
    Description of ActionsBase

    Attributes:
        attr1 (str): Description of 'attr1' 
        attr2 (str): Description of 'attr1' 

    """

    def __init__(self):
        self.action_state, self.register_event, self.register_listener, self.unregister_listener, self.message, self.listen = self.actions_closure()

    def actions_closure(self):

        # list of registered actions/events
        actions = []
        # list of actions/events listeners
        action_listeners = []

        def action_state(self):
            """
            Description of action_state

            Args:
                self (undefined):

            """
            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def register_event(self):
            """
            Description of register_event

            Args:
                self (undefined):

            """
            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def register_listener(self):
            """
            Description of register_listener

            Args:
                self (undefined):

            """
            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def unregister_listener(self):
            """
            Description of unregister_listener

            Args:
                self (undefined):

            """
            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def message(self):
            """
            Description of message

            Args:
                self (undefined):

            """
            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def listen(self):
            """
            Description of listen

            Args:
                self (undefined):

            """
            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        return (action_state, register_event, register_listener, unregister_listener, message, listen)
