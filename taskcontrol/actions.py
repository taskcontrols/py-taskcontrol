# Queue Events Actions Base

import time
from typing import Dict, List
from .interfaces import PubSubBase
from .sharedbase import ClosureBase, UtilsBase, LogBase
from collections import deque
from queue import Queue, LifoQueue, PriorityQueue, SimpleQueue


class Queues(UtilsBase):
    tmp = {}

    def __init__(self, queues={}):
        v = ["name", "maxsize", "queue_type", "queue", "workflow_kwargs"]
        super().__init__("queues", validations={
            "add": v, "create": v, "update": v, "delete": ["name"]}, queues=queues)

    def new(self, config):
        if self.validate_object(config, values=["name", "maxsize", "queue_type", "queue"]):
            if config.get("queue_type") == "queue":
                return Queue(maxsize=config.get("maxsize"))
            elif config.get("queue_type") == "deque":
                return deque([], maxlen=config.get("maxsize"))
            else:
                return []

    def add(self, name, item, index=0, nowait=True):
        q = self.fetch(name)
        o = q["queue"]
        if isinstance(o, List) or isinstance(o, deque):
            if not q.get("maxsize") == len(o):
                o.append(item)
            else:
                return False
        elif isinstance(o, Queue) or isinstance(o, LifoQueue) or isinstance(o, PriorityQueue):
            if not q.get("maxsize") == o.qsize():
                o.put(item, nowait)
            else:
                return False
        elif isinstance(o, SimpleQueue):
            try:
                o.put(item)
            except Exception as e:
                return False
        q["queue"] = o
        return self.update(q)

    def get(self, name, index=0, nowait=True):
        q = self.fetch(name)
        o = q["queue"]
        u = None
        if type(o) == List:
            if len(o):
                u = o.pop(index)
        elif isinstance(o, Queue) or isinstance(o, SimpleQueue):
            if not o.empty():
                u = o.get(nowait)
        elif isinstance(o, LifoQueue) or isinstance(o, PriorityQueue):
            if not o.empty():
                u = o.get()
        elif isinstance(o, deque):
            if o:
                if index == 0:
                    u = o.popleft()
                else:
                    u = o.pop()
        q["queue"] = o
        c = self.update(q)
        if c:
            return u


class Events(UtilsBase):
    def __init__(self, event={}):
        v = ["name", "event", "handler", "listening",
             "listeners", "workflow_kwargs"]
        super().__init__("events", validations={
            "add": v, "create": v, "update": v, "delete": ["name"]}, events=event)

    def event_register(self, event_object):
        """
        event_object: name (str), event (func), listening (bool), listeners (dict)
            event (func): function to execute when event is invoked
            listening (bool): if function needs to be listening to events
            listeners (dict): dictionary of listener objects
        TODO: This is blocking event object. Needs to allow non-blocking and non-blocking multithreaded/multiprocess
        """
        # Change this to different ways of using events/actions
        event_func = event_object.get("event")
        name = event_object.get("name")
        try:
            if "listening" not in event_object:
                event_object["listening"] = False
            if "listeners" not in event_object:
                event_object["listeners"] = {}
            if "workflow_kwargs" not in event_object:
                event_object["workflow_kwargs"] = {}

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
            if self.validate_object(event_object, self.validate_create):
                print("Creating event: ", event_object.get("name"))
                return self.create(event_object)
        except Exception as e:
            raise e
        return False

    def event_unregister(self, event_name):
        print("Deleting event: ", event_name)
        return self.delete(event_name)

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

    def on(self, event_name, name, handler):
        return self.listener_register({"name": name, "event_name": event_name, "listener": handler})

    def listener_unregister(self, listener_object):
        event_name = listener_object.get("event_name")
        a_name = listener_object.get("name")
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
        return self.set_state(event_name, True)

    def stop(self, event_name):
        return self.set_state(event_name, False)

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

    def __init__(self, action={}):
        super().__init__("actions", actions=action)


class EPubSub(UtilsBase):

    def __init__(self, pubsubs={}):
        self.v = [
            "name", "handler", "queues",
            "maxsize", "queue_type", "events"
        ]
        self.ev = ["name", "publishers", "subscribers"]
        super().__init__("pubsubs", {}, pubsubs=pubsubs)

    def __handler(self, task, handler):
        handler(task)
        return True

    def queue_create(self, config):
        # "name", "handler", "queue", "events"
        if not "name" in config:
            raise TypeError

        o = {"name": config.get("name"),
             "handler": config.get("handler", lambda message_object: print(str(message_object))),
             "queue": config.get("queue", None),
             "maxsize": config.get("maxsize", 10),
             "queue_type": config.get("queue_type", None),
             "batch_interval": 60,
             "events": dict([
                 [
                     config.get("events").get("name"), {
                         "name": config.get("events").get("name"),
                         "publishers": config.get("events").get("publishers", {}),
                         "subscribers": config.get("events").get("subscribers", {})
                     }
                 ]
             ])}

        if self.validate_object(o, self.validate_create):
            tmpQ = Queues()
            q = tmpQ.new({
                "name": config.get(),
                "maxsize": config.get("maxsize"),
                "queue_type": config.get("queue_type", "list")
            })
            config["queues"][config.get("name")].update({"queue":  q})
            print("config", config)
            u = tmpQ.create(q)
            if u:
                self.__process()
                return True
            return False

    def register_publisher(self, queue_name, publisher_object):
        q = self.fetch(queue_name)
        q["events"][publisher_object.get("event_name")]["publishers"].update(dict([
            [publisher_object.get("name"), publisher_object]
        ]))
        return self.update(q)

    def register_subscriber(self, queue_name, subscriber_object):
        s = self.fetch(queue_name)
        s["events"][subscriber_object.get("event_name")]["subscribers"].update(dict([
            [subscriber_object.get("name"), subscriber_object]
        ]))
        return self.update(s)

    def register_event(self, queue_name, event_object):
        e = self.fetch(queue_name)
        e["events"].update(dict([
            [
                event_object.get("event_name"), {
                    "name": event_object.get("name"),
                    "publishers": event_object.get("publishers", {}),
                    "subscribers": event_object.get("subscribers", {})
                }
            ]
        ]))
        return self.update(e)

    def __process(self, name):
        o = self.fetch(name)
        h = o.get("handler")
        t = o["queue"].pop(0)
        r = None
        try:
            r = self.__handler(t, h)
        except Exception as e:
            o["queue"].add(t)
        u = self.update(o)
        if u:
            return r

    def __schedular(self):
        pb = self.fetch("pubsubs")
        for k in pb:
            # Put into thread
            while True:
                try:
                    time.sleep(pb.get(k).get("batch_interval"))
                    self.__process(k)
                except Exception as e:
                    raise e

    def send(self, message_object):
        # message_object: queue_name, event_name, publisher_name, message
        pass

    def receive(self, message_object):
        # message_object: queue_name, event_name, publisher_name, message
        pass


if __name__ == "__main__":
    queue = Queues()

    config = {"name": "test", "maxsize": 10,
              "queue_type": "queue", "queue": None}

    q = queue.new(config)
    config["queue"] = q
    # print(config)
    c = queue.create(config)
    print(c, queue.validate_add)
    print(queue.add("test", "test1"))
    print(queue.add("test", "test2"))
    print(queue.add("test", "test3"))
    print(queue.add("test", "test4"))
    print(queue.add("test", "test5"))
    print(queue.add("test", "test6"))
    print(queue.add("test", "test7"))
    print(queue.add("test", "test8"))
    print(queue.add("test", "test9"))
    print(queue.add("test", "test10"))
    print(queue.add("test", "test11"))
    print(queue.add("test", "test10"))
    print(queue.get("test"))
    print(queue.get("test"))
    print(queue.get("test"))
    print(queue.get("test"))
    print(queue.get("test"))
    print(queue.get("test"))
    print(queue.get("test"))
    print(queue.get("test"))
    print(queue.get("test"))
    print(queue.get("test"))
    print(queue.get("test"))
    print(queue.get("test"))


if __name__ == "__main__":
    event = Events()

    def run(data):
        print("Run Event Handler", data)

    event.register_event({"name": "new", "event": run})
    event.register_listener(
        {"event_name": "new", "name": "run", "listener": run})
    event.listen({"name": "new"})
    event.message({"event_name": "new", "message": "Testing message"})
    event.stop_listening({"event_name": "new"})
    event.unregister_listener({"event_name": "new", "action": "run"})
    event.unregister_event({"name": "new"})


if __name__ == "__main__":
    action = Actions()


if __name__ == "__main__":
    epb = EPubSub()


__all__ = ["Actions", "Events", "Queues", "EPubSub"]
