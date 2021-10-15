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
        self.v = ["name", "maxsize", "queue_type", "queue", "workflow_kwargs"]
        super().__init__("queues", validations={
            "add": self.v, "create": self.v, "update": self.v, "delete": ["name"]}, queues=queues)

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
        self.v = ["name", "event", "handler", "listening",
                  "listeners", "workflow_kwargs"]
        super().__init__("events", validations={
            "add": self.v, "create": self.v, "update": self.v, "delete": ["name"]}, events=event)

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

    type = "epubsub"
    # agent options: application, publisher, server, subscriber
    # TODO: Implement threading/processing
    # application (in application events, simple app event architecture)
    # publisher, server, subscriber (in network system application events, clientagent-server architecture)
    agent = "application"

    def __init__(self, pubsubs={}, type="epubsub", agent="server"):
        self.v = ["name", "handler", "queue", "maxsize",
                  "queue_type", "batch_interval", "processing_flag", "events", "workflow_kwargs"]
        self.ev = ["name", "pubsub_name",
                   "publishers", "subscribers", "handler"]
        self.type = type
        self.agent = agent
        super().__init__("pubsubs", validations={
            "add": self.v, "create": self.v, "update": self.v, "delete": ["name"]}, pubsubs=pubsubs)
        # self.__schedular()

    def __process(self, name):
        o = self.fetch(name)
        h = o.get("handler")
        r = None
        try:
            while True:
                t = o["queue"].get(o.get("name"))
                if t:
                    r = self.__publish_handler(t)
                else:
                    break
        except Exception as e:
            o["queue"].add(t)
        o["processing_flag"] = False
        u = self.update(o)
        if u:
            return r
        return False

    def __schedular(self):
        while True:
            pb = self.fetch(1)
            for k in pb:
                # TODO: Add Threading/Processing
                try:
                    if pb[k].get("processing_flag") == False:
                        pb[k]["processing_flag"] = True
                        u = self.update(dict([[k, pb[k]]]))
                        if u:
                            r = self.__process(k)
                            if not r:
                                raise Exception
                except Exception as e:
                    raise e
            time.sleep(pb.get(k).get("batch_interval"))

    def __handler(self, task, handler):
        r = handler(task)
        if r:
            return True
        return False

    def __publish_handler(self, message_object):
        o = self.fetch(message_object.get("queue_name"))
        h = o.get("handler")
        if not h:
            def h(message_object): return print(
                "Message Object ", message_object)
        e = o.get("events").get(message_object.get("event_name"))
        if e:
            r = False
            if self.agent == "publisher":
                # Get Handler
                pb_hdlr = e.get("handler", h)
                # Invoke Handler
                if pb_hdlr:
                    print("Running Handler pb_hdlr")
                    r = self.__handler(message_object, pb_hdlr)
            elif self.agent == "subscriber":
                # Get Handler
                sb_hdlr = e.get("handler", h)
                # Invoke Handler
                if sb_hdlr:
                    print("Running Handler sb_hdlr")
                    r = self.__handler(message_object, sb_hdlr)
            else:
                r = []
                # Get Handler
                srv_hdlr = e.get("handler", h)
                # Invoke Handler
                print("Running Handler srv_hdlr")
                u1 = self.__handler(message_object, srv_hdlr)
                # Get all subscriber handlers
                if not u1:
                    print("Return Error U1")
                srv_pbh = e.get("publishers").get(
                    message_object.get("publisher")).get("handler", h)
                # Invoke Publisher
                print("Running Handler srv_pbh")
                u2 = self.__handler(message_object, srv_pbh)
                if not u2:
                    print("Return Error U2")
                sbs = e.get("subscribers")
                for sb in sbs:
                    # Get individual handler
                    srv_sb_hdlr = sbs[sb].get("handler", h)
                    # Invoke all handlers
                    print("Running Handler srv_sb_hdlr")
                    tmpres = self.__handler(message_object, srv_sb_hdlr)
                    r.append(tmpres)
            return r
        return False

    def pubsub_create(self, config):
        # "name", "handler", "queue", "maxsize", "queue_type", "processing_flag", "batch_interval", "events"
        if not "name" in config:
            raise TypeError

        o = {
            "name": config.get("name"),
            "handler": config.get("handler", lambda message_object: print(str(message_object))),
            "maxsize": config.get("maxsize", 10),
            "queue": config.get("queue", None),
            "queue_type": config.get("queue_type", "list"),
            "batch_interval": 5,
            "processing_flag": False,
            "workflow_kwargs": {},
            "events": {}
        }

        u = self.queue_create({
            "name": config.get("name"),
            "maxsize": config.get("maxsize"),
            "queue_type": config.get("queue_type")
        })
        if u:
            o["queue"] = u
            if self.validate_object(o, self.validate_create):
                return self.create(o)
        return False

    def pubsub_delete(self, pubsub_name):
        return self.delete(pubsub_name)

    def queue_create(self, config):
        # "name", "queue", "maxsize", "queue_type"
        qConfig = config
        tmpQ = Queues()
        q = tmpQ.new(qConfig)
        qConfig["queue"] = q
        qs = tmpQ.create(qConfig)
        if qs:
            return tmpQ
        return False

    def queue_delete(self, pubsub_name):
        """
        publisher_object: name, event_name, publisher
        """
        o = self.fetch(pubsub_name)
        o["queue"] = None
        return self.update(o)

    def register_publisher(self, pubsub_name, publisher_object):
        """
        publisher_object: name, event_name, publisher
        """
        p = self.fetch(pubsub_name)
        p["events"][publisher_object.get("event_name")]["publishers"].update(dict([
            [publisher_object.get("name"), publisher_object]
        ]))
        return self.update(p)

    def register_subscriber(self, pubsub_name, subscriber_object):
        """
        subscriber_object: name, event_name, subscriber
        """
        s = self.fetch(pubsub_name)
        s["events"][subscriber_object.get("event_name")]["subscribers"].update(dict([
            [subscriber_object.get("name"), subscriber_object]
        ]))
        return self.update(s)

    def register_event(self, pubsub_name, event_object):
        e = self.fetch(pubsub_name)
        e["events"].update(dict([
            [
                event_object.get("name"), {
                    "name": event_object.get("name"),
                    "publishers": event_object.get("publishers", {}),
                    "subscribers": event_object.get("subscribers", {})
                }
            ]
        ]))
        return self.update(e)

    def unregister_event(self, pubsub_name, event_object):
        try:
            p = self.fetch(pubsub_name)
            del p["events"][event_object.get("name")]
            return self.update(p)
        except Exception as e:
            pass
        return False

    def unregister_publisher(self, pubsub_name, publisher_object):
        try:
            p = self.fetch(pubsub_name)
            del p["events"][publisher_object.get(
                "event_name")]["publishers"][publisher_object.get("name")]
            return self.update(p)
        except Exception as e:
            print("Exception during Publisher unregister ", e)
        return False

    def unregister_subscriber(self, pubsub_name, subscriber_object):
        try:
            p = self.fetch(pubsub_name)
            del p["events"][subscriber_object.get(
                "event_name")]["subscribers"][subscriber_object.get("name")]
            return self.update(p)
        except Exception as e:
            pass
        return False

    def send(self, message_object):
        # message_object: queue_name, event_name, publisher_name, message
        # Events (Publisher-Subscriber, WebHooks) Mode:
        #       publisher, server[forsubscribers]
        # TODO: Consider send for subscriber for Client-Server (Server-Agent) Mode or (Subscriber having feedback) or (Subscriber app in Dual) Mode
        u = self.__publish_handler(message_object)
        if u:
            return True
        return False

    def receive(self, message_object):
        # message_object: queue_name, event_name, publisher_name, message
        # server[forpublishers], subscribers
        # TODO: Consider receive for Client-Server (Server-Agent) or (Publisher having feedback) or (Publisher app in Dual) Mode
        u = self.__publish_handler(message_object)
        if u:
            return True
        return False


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
        print("Run Action Handler ->", data)

    c = event.event_register({"name": "new", "event": run})
    if c:
        event.listener_register(
            {"name": "run", "event_name": "new", "listener": run})
        event.on("new", "runner", lambda data: print(
            "Second Listener running -> ", data))
        event.start("new")
        print("'new' event state is", event.get_state("new"))
        event.set_state("new", False)
        print("'new' event state is", event.get_state("new"))
        event.set_state("new", True)
        print("'new' event state is", event.get_state("new"))
        event.send({"event_name": "new", "message": "Testing message"})
        event.emit("new", "Testing message")
        event.listener_register({"event_name": "new", "name": "run"})
        event.stop("new")
        event.event_unregister("new")


if __name__ == "__main__":
    action = Actions()


if __name__ == "__main__":

    def run(data):
        print("Running Pubsub")

    def publisher(data):
        print("Running publisher", data)

    def subscriber(data):
        print("Running subscriber", data)

    config = {"name": "new", "handler": run, "queue": None, "maxsize": 10,
              "queue_type": "queue", "processing_flag": False,  "batch_interval": 5, "events": {}}
    name = config.get("name")

    pb = EPubSub()
    p = pb.pubsub_create(config)

    if p:
        print("Event register", pb.register_event(
            name, {"name": "testevent", "event": run}))
        print("Publish register", pb.register_publisher(
            name, {"name": "pubone", "event_name": "testevent", "publisher": publisher}))
        print("Subscribers register", pb.register_subscriber(
            name, {"name": "subone", "event_name": "testevent", "subscriber": subscriber}))
        print("Subscribers register", pb.register_subscriber(
            name, {"name": "subtwo", "event_name": "testevent", "subscriber": subscriber}))
        print("Event sending", pb.send({"event_name": "testevent",
                                        "message": "Testing event testevent"}))
        print("Publisher unregister", pb.unregister_publisher(
            name, {"name": "pubone", "event_name": "testevent"}))
        print("Subscriber unregister", pb.unregister_subscriber(
            name, {"name": "subone", "event_name": "testevent"}))
        print("Subscriber unregister", pb.unregister_subscriber(
            name, {"name": "subtwo", "event_name": "testevent"}))
        print("Pubsub Object ", pb.fetch(name))
        print("Pubsub Object Deleted ", pb.pubsub_delete(name))
        print("Pubsub Object ", pb.fetch(name))


__all__ = ["Actions", "Events", "Queues", "EPubSub"]
