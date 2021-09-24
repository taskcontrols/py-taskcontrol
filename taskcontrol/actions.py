# Queue Events Actions Base

from .sharedbase import ClosureBase, UtilsBase, LogBase


class Queue():
    pass


class Event(UtilsBase):
    pass


class Action(UtilsBase):
    """
    Description of ActionsBase

    Attributes:


    """

    def __init__(self):
        super()
        self.getter, self.setter, self.deleter = ClosureBase().class_closure(
            actions={})

    def action_state(self, event_object):
        """
        Description of action_state

        Args:
            event_object (dict):
            { "name": "eventactionstate" }

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        try:
            ev = self.getter("actions", event_object.get("name"))
            if len(ev) > 0:
                e = ev[0]
                if e.get("listening"):
                    return e.get("listening")
        except Exception as e:
            raise e
        return False

    def register_event(self, event_object):
        """
        Description of register_event

        Args:
            event_object (dict):
            { "name": "name", "event": function, "listening": True/False, listeners: {} }

        """
        try:
            event_func = event_object.get("event")
            event_object["listening"] = False
            if "listeners" not in event_object:
                event_object["listeners"] = {}
            if "workflow_kwargs" not in event_object:
                event_object["workflow_kwargs"] = {}
            if "shared" not in event_object["workflow_kwargs"]:
                event_object["workflow_kwargs"]["shared"] = False

            def handler(data):
                try:
                    event_func(data)
                    action = self.getter(
                        "actions", event_object.get("name"))[0]
                    for ln in action.get("listeners").keys():
                        action.get("listeners").get(ln).get("listener")(data)
                    return True
                except:
                    return False

            event_object["handler"] = handler
            if self.validate_object(event_object, ["name", "event", "handler", "listening", "listeners", "workflow_kwargs"]):
                # TODO: Add Logger

                # TODO: Add Authentication
                # if not is_authenticated():
                #     raise Exception("Not authenticated")
                ev = self.setter("actions", event_object, self)
                if ev:
                    return ev
                return False
        except Exception as e:
            raise e
        return False

    def unregister_event(self, event_object):
        """
        Description of unregister_listener

        Args:
            event_object (dict):
            { "name": "name" }

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        try:
            ev = self.deleter("actions", event_object.get("name"))
            if ev:
                print("Unregistered Action Event " + event_object.get("name"))
                return ev
        except Exception as e:
            raise e
        return False

    def register_listener(self, listener_object):
        """
        Description of register_listener

        Args:
            listener_object (dict):
            { "name": "name", "action": "eventactionname", "listener": function }

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        try:
            act = self.getter("actions", listener_object.get("name"))
            if len(act) > 0:
                action = act[0]
            else:
                raise Exception("Event not present")
            action["listeners"][listener_object.get(
                "action")] = listener_object
            ev = self.setter("actions", action, self)
            if ev:
                return ev
        except Exception as e:
            raise e
        return False

    def unregister_listener(self, listener_object):
        """
        Description of unregister_listener

        Args:
            listener_object (dict):
            { "action": "name", "name": "eventname" }

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        try:
            act = self.getter("actions", listener_object.get("name"))
            if len(act) > 0:
                action = act[0]
            else:
                raise Exception("Event not present")
            for i, ln in enumerate(action.get("listeners")):
                if ln == listener_object.get("action"):
                    del action["listeners"][listener_object.get("action")]
                    break
            ev = self.setter("actions", action, self)
            if ev:
                print("Unregistered Action Listener " +
                      listener_object.get("action"))
                return ev
        except Exception as e:
            raise e
        return False

    def message(self, message_object):
        """
        Description of message

        Args:
            message_object (dict):
            {"name": "eventactionname", "message": object}

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        try:
            act = self.getter("actions", message_object.get("name"))
            if len(act) > 0:
                action = act[0]
            else:
                raise Exception("Event not present")
            if action.get("listening"):
                action.get("handler")(message_object.get("message"))
                return True
        except Exception as e:
            raise e
        return False

    def listen(self, event_object):
        """
        Description of listen

        Args:
            event_object (dict):
            { "name": "eventactionname" }

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        try:
            act = self.getter("actions", event_object.get("name"))
            if len(act) > 0:
                action = act[0]
            else:
                raise Exception("Error in name")

            action["listening"] = True
            ev = self.setter("actions", action, self)
            if ev:
                return ev
        except Exception as e:
            raise e
        return False

    def stop_listening(self, event_object):
        """
        Description of stop_listening

        Args:
            event_object (dict):
            { "name": "eventactionname" }

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        try:
            action = self.getter("actions", event_object.get("name"))[0]
            action["listening"] = False
            e = self.setter("actions", action, self)
            if e:
                return e
        except Exception as e:
            raise e
        return False


if __name__ == "__main__":
    action = Action()

    def run(data):
        print("Run Event Handler", data)

    action.register_event({"name": "new", "event": run})
    action.register_listener({"name": "new", "action": "run", "listener": run})
    action.listen({"name": "new"})
    action.message({"name": "new", "message": "Testing message"})
    action.stop_listening({"name": "new"})
    action.unregister_listener({"name": "new", "action": "run"})
    action.unregister_event({"name": "new"})


__all__ = ["Action", "Event", "Queue"]
