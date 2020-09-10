# Actions Base

from .sharedbase import ClosureBase

# Inherit shared and logging

# TODO: Check impact of self on closure
# TODO: Refactor getters and setters and make code simpler


class ActionsBase(ClosureBase):
    """
    Description of ActionsBase

    Attributes:
        getter (fn): Description of 'getter' 
        setter (fn): Description of 'setter'
        deleter (fn): Description of 'deleter'

    """

    def __init__(self):
        super()
        self.getter, self.setter, self.deleter = self.class_closure(
            actions=[], action_listeners=[])

    def action_state(self, key):
        """
        Description of action_state

        Args:
            key (string):

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        state = self.getter("actions", key)
        if state and len(state) == 1:
            return state[0] # send back state
        return False

    def register_event(self, event_object):
        """
        Description of register_event

        Args:
            event_object (dict):

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        e = self.setter("actions", event_object)
        if e:
            return e
        return False

    def unregister_event(self, event_object):
        """
        Description of unregister_listener

        Args:
            event_object (dict):

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        e = self.deleter("actions", event_object)
        if e:
            return e
        return False

    def register_listener(self, listener_object):
        """
        Description of register_listener

        Args:
            listener_object (dict):

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        e = self.setter("action_listeners", listener_object)
        if e:
            return e
        return False

    def unregister_listener(self, listener_object):
        """
        Description of unregister_listener

        Args:
            listener_object (dict):

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        e = self.setter("action_listeners", listener_object)
        if e:
            return e
        return False

    def message(self, msg_object):
        """
        Description of message

        Args:
            msg_object (dict):

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        action = self.getter("actions", msg_object.get("key"))
        action[0].send(msg_object.get("message")) # use send or related function TODO

    def listen(self, options):
        """
        Description of listen

        Args:
            options (dict):

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        action = self.getter("actions", options.get("key"))
        action[0].listen(options) # use listen or related function TODO
