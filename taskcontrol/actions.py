# Queue Events Actions Base

from typing import List
from .interfaces import ObjectModificationBase
from .sharedbase import ClosureBase, UtilsBase, LogBase
from collections import deque
from queue import Queue


class Queues(UtilsBase):
    tmp = {}

    def __init__(self, queues={}):
        super().__init__("queues", queues=queues)

    def new(self, config):
        if self.validate_object(config, values=["maxsize", "queue_type"]):
            if config.get("queue_type") == "queue":
                return Queue(config.get("maxsize"))
            elif config.get("queue_type") == "deque":
                return deque([], maxlen=config.get("maxsize"))
            else:
                return []

    def add(self, name, item):
        o = self.fetch(name)
        o.insert(item)
        return self.update(o)

    def remove(self, name, item):
        o = self.fetch(name)
        u = o.remove(item)
        return u, self.update(o)

    def pop(self, name, index):
        o = self.fetch(name)
        u = o.pop(index)
        return u, self.update(o)

    def next(self, name):
        if name not in self.tmp:
            self.tmp[name] = self.fetch(name)
        if isinstance(self.tmp.get(name), List):
            return self.tmp.get(name).shift()
        return self.tmp.get(name).next()


class Event(UtilsBase):
    def __init__(self, event={}):
        super().__init__("events", events=event)

    def create_event(self, event_object):
        pass

    def create_listener(self, event_object):
        pass

    def listener_register(self, listener_object):
        try:
            return
        except Exception as e:
            raise e

    def listener_unregister(self, listener_object):
        try:
            return
        except Exception as e:
            raise e

    def start(self, event_object):
        try:
            return
        except Exception as e:
            raise e

    def stop(self, event_object):
        try:
            return
        except Exception as e:
            raise e

    def get_state(self, event_object):
        try:
            return False
        except Exception as e:
            raise e

    def send(self, message_object):
        try:
            return True
        except Exception as e:
            raise e

    def receive(self, message_object):
        try:
            return True
        except Exception as e:
            raise e


class Action(UtilsBase):
    """
    Description of ActionsBase

    Attributes:


    """

    def __init__(self, action={}):
        super()
        self.getter, self.setter, self.deleter = ClosureBase().class_closure(
            actions=action)

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
            ev = self.getter("actions", event_object.get("name"))[0]
            if ev.get("listening"):
                return ev.get("listening")
            return False
        except Exception as e:
            raise e

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
                return self.setter("actions", event_object, self)
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
            return self.deleter("actions", event_object.get("name"))
        except Exception as e:
            raise e

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
            action = self.getter("actions", listener_object.get("name"))[0]
            action["listeners"][listener_object.get(
                "action")] = listener_object
            return self.setter("actions", action, self)
        except Exception as e:
            raise e

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
            action = self.getter("actions", listener_object.get("name"))[0]
            for i, ln in enumerate(action.get("listeners")):
                if ln == listener_object.get("action"):
                    del action["listeners"][listener_object.get("action")]
                    break
            return self.setter("actions", action, self)
        except Exception as e:
            raise e

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
            action = self.getter("actions", message_object.get("name"))[0]
            if action.get("listening"):
                action.get("handler")(message_object.get("message"))
                return True
            return False
        except Exception as e:
            raise e

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
            action = self.getter("actions", event_object.get("name"))[0]
            action["listening"] = True
            return self.setter("actions", action, self)
        except Exception as e:
            raise e

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
            return self.setter("actions", action, self)
        except Exception as e:
            raise e


if __name__ == "__main__":
    queue = Queue()


if __name__ == "__main__":
    event = Event()


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


__all__ = ["Action", "Event", "Queues"]
