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


class Events(UtilsBase):
    def __init__(self, event={}):
        super().__init__("events", events=event)

    def create_event(self, event_object):
        # Change this to different ways of using events/actions
        event_func = event_object.get("event")
        name = event_object.get("name")
        try:
            if "listening" not in event_object:
                event_object["listening"] = False
            if "listeners" not in event_object:
                event_object["listeners"] = {}

            def __handler(data):
                try:
                    event_func(data)
                    action = self.fetch(name)
                    for ln in action.get("listeners").keys():
                        action.get("listeners").get(ln).get("listener")(data)
                    return True
                except:
                    return False

            event_object["handler"] = __handler
            if self.validate_object(event_object, ["name", "event", "handler", "listening", "listeners"]):
                return self.create(event_object)
        except Exception as e:
            raise e
        return False

    def create_listener(self, listener_object):
        pass

    def listener_register(self, listener_object):
        try:
            if self.validate_object(listener_object, ["name", "event_name", "listener"]):
                action = self.fetch(listener_object.get("event_name"))
                action["listeners"][listener_object.get(
                    "name")] = listener_object
                return self.update(action)
            return False
        except Exception as e:
            raise e

    def on(self, name, event_name, handler):
        return self.listener_register({"name": name, "event_name": event_name, "listener": handler})

    def listener_unregister(self, listener_object):
        event_name = listener_object.get("event_name")
        a_name = listener_object.get("action")
        try:
            action = self.fetch(event_name)
            for ln in action.get("listeners"):
                if ln == a_name:
                    del action["listeners"][a_name]
                    break
            return self.update(action)
        except Exception as e:
            raise e

    def get_state(self, event_name):
        try:
            e = self.fetch(event_name)
            if e:
                return e.get("listening")
            return False
        except Exception as e:
            raise e

    def set_state(self, event_name, state):
        try:
            event = self.fetch(event_name)
            event["listening"] = state
            # Stop/Start listening to event
            return self.update(event)
        except Exception as e:
            raise e

    def start(self, event_name):
        return self.set_state({"name": event_name, "listening": True})

    def stop(self, event_name):
        return self.set_state({"name": event_name, "listening": False})

    def send(self, message_object):
        try:
            action = self.fetch(message_object.get("event_name"))
            if action.get("listening"):
                action.get("handler")(message_object.get("message"))
                return True
            return False
        except Exception as e:
            raise e

    def emit(self, event_name, message):
        return self.send({"event_name": event_name, "message": message})


class Actions(UtilsBase):
    """
    Description of ActionsBase

    Attributes:


    """

    def __init__(self, action={}):
        super().__init__("actions", actions=action)


if __name__ == "__main__":
    queue = Queues()


if __name__ == "__main__":
    event = Events()

    def run(data):
        print("Run Event Handler", data)

    event.register_event({"name": "new", "event": run})
    event.register_listener({"name": "new", "action": "run", "listener": run})
    event.listen({"name": "new"})
    event.message({"name": "new", "message": "Testing message"})
    event.stop_listening({"name": "new"})
    event.unregister_listener({"name": "new", "action": "run"})
    event.unregister_event({"name": "new"})

if __name__ == "__main__":
    action = Actions()


__all__ = ["Action", "Events", "Queues"]
