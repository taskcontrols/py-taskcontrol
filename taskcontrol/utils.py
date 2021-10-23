# SHARED BASE

import time
import ast
import time
import sys
import types
import socket
import selectors
import copy
import logging
import re
from typing import Dict, List
from threading import Thread, Lock
from multiprocessing import Process, Array, Value, Manager
from collections import deque
from queue import Queue, LifoQueue, PriorityQueue, SimpleQueue
from .interfaces import ObjectModificationBase, SocketsBase, HooksBase, SshBase
from .interfaces import PubSubsBase, TimeBase, LogsBase, CommandsBase, PicklesBase


class ClosureBase():
    def class_closure(self, **kwargs):
        closure_val = kwargs

        def getter(key, value=None):
            try:
                if (type(value) == int and value == 1) or (type(value) == str and value == "1"):
                    keys = closure_val[key]
                    val = []
                    for t in keys:
                        if t:
                            val.append(closure_val[key].get(t))
                    return val
                elif type(value) == str:
                    val = closure_val[key].get(value)
                    if val:
                        return [val]
                    return []
                elif type(value) == list:
                    vl = []
                    for tk in value:
                        if int(tk) == 1:
                            for i in closure_val[key].keys():
                                vl.append(closure_val[key].get(i))
                        elif tk in closure_val[key].keys():
                            vl.append(closure_val[key].get(tk))
                    return vl
                return []
            except Exception as e:
                print("Error in Getter ", e)
                return False

        def setter(key, value=None, inst=None):
            try:
                if type(value) == dict and inst != None:
                    if inst.__class__.__name__ == "SharedBase":
                        closure_val[key].update({value.get("name"): value})
                    elif value.get("workflow_kwargs").get("shared") == True:
                        inst.shared.setter(key, value, inst.shared)
                    elif value.get("workflow_kwargs").get("shared") == False:
                        closure_val[key].update({value.get("name"): value})
                    return True
                else:
                    raise TypeError("Problem with " + key +
                                    " Value setting " + str(value))
            except Exception as e:
                print("Error in Setter ", e)
                return False

        def deleter(key, value=None):
            try:
                if type(value) == str:
                    if value != None:
                        closure_val[key].pop(value)
                    else:
                        return False
                    return True
                elif type(value) == int:
                    if value == 1:
                        for v in value:
                            closure_val[key].pop(v)
                    return True
                return False
            except Exception as e:
                print("Exception in delete ", e)
                return False

        return (getter, setter, deleter)


class SharedBase(ClosureBase):

    __instance = None

    def __init__(self):
        super().__init__()
        self.getter, self.setter, self.deleter = self.class_closure(
            tasks={}, ctx={}, plugins={}, config={}, workflow={}
        )
        if SharedBase.__instance != None:
            pass
        else:
            SharedBase.__instance = self

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SharedBase, cls).__new__(cls)
        return cls.__instance

    @staticmethod
    def getInstance():
        if not SharedBase.__instance:
            return SharedBase()
        return SharedBase.__instance


class UtilsBase(ObjectModificationBase):
    object_name = None

    def __init__(self, object_name="", validations={}, **kwargs):
        self.object_name = object_name
        self.validate_create = validations.get("create", ["name"])
        self.validate_fetch = validations.get("fetch", ["name"])
        self.validate_add = validations.get("add", ["name"])
        self.validate_update = validations.get("update", ["name"])
        self.validate_delete = validations.get("delete", ["name"])
        self.getter, self.setter, self.deleter = ClosureBase().class_closure(
            **kwargs)

    def append_update_dict(self, main_object, update_object):
        for k in update_object:
            if k in main_object:
                main_object.update(dict([[k, update_object.get(k)]]))
            else:
                main_object.append(dict([[k, update_object.get(k)]]))
        return main_object

    def validate_object(self, val_object, values=[]):
        keys = val_object.keys()
        if len(keys) == len(values):
            if type(values) == list:
                for k in values:
                    if k in keys:
                        continue
                    else:
                        return False
                return True
            elif type(values) == dict:
                v_keys = values.keys()
                for v in v_keys:
                    if v in keys:
                        for k in keys:
                            if type(values.get(v)) == type(val_object.get(k)):
                                continue
                            else:
                                return False
                    else:
                        return False
                return True
        return False

    def list_search(self, list_object, params):
        arr = []
        for idx, l in enumerate(list_object):
            for w in params:
                if w.type == "exact":
                    if l == w.param:
                        arr.append({"row": idx, "item": l})
                if w.type == "reg-match":
                    p = re.compile(w.get("pattern"))
                    if re.search(p, w.get("param")):
                        arr.append({"row": idx, "item": l})
                elif w.type == "reg-search" or w.type == "contains":
                    p = re.compile(w.get("pattern"))
                    if re.search(p, w.get("param")):
                        arr.append({"row": idx, "item": l})
        return arr

    def create(self, config):
        config["workflow_kwargs"] = config.get("workflow_kwargs", {})
        config["workflow_kwargs"]["shared"] = config.get(
            "workflow_kwargs").get("shared", False)
        try:
            if self.validate_object(config, self.validate_add):
                return self.setter(self.object_name, config, self)
            return False
        except Exception as e:
            print("Fetch error ", e)
            return False

    def fetch(self, name):
        try:
            return self.getter(self.object_name, name)[0]
        except Exception as e:
            print("Fetch error ", e)
            return False

    def update(self, config):
        try:
            o = self.getter(self.object_name, config.get("name"))[0]
            for k in config:
                if o.get(k) and (not k == "name"):
                    o[k] = o.get(k)
            return self.setter(self.object_name, o, self)
        except Exception as e:
            print("Fetch error ", e)
            return False

    def delete(self, name):
        try:
            return self.deleter(self.object_name, name)
        except Exception as e:
            print("Fetch error ", e)
            return False


class ConcurencyBase(UtilsBase):

    # consider adding concurrency futures
    def futures_run(self):
        pass

    # consider adding asyncio lib
    def asyncio_run(self):
        pass

    # asynchronous, needs_join
    def mthread_run(self, function, options):
        """
        Description of mthread_run

        Args:
            self (undefined):
            function (undefined):
            options (undefined):

        """
        # options structure
        # # args, kwargs, needs_join, share_value

        # Test this instance of MThreading for lock and other params

        result = None

        if type(options) == dict:
            # # Keeping following to be user responsibility
            # # Check addition later
            # share_value = options.get("share_value")
            pass

        daemon = options.get("daemon", True)
        if type(daemon) != bool:
            daemon = True

        args = options.get("args", [])
        if type(args) != list:
            args = []

        kwargs = options.get("kwargs", {})
        if type(kwargs) != dict:
            kwargs = {}

        need_lock = options.get("lock")
        if need_lock:
            lock = Lock()

        if lock:
            args = (lock, *args)
        else:
            arg = (*args,)

        worker = Thread(
            target=function,
            args=arg,
            kwargs={"result": result, **kwargs}
        )
        worker.setDaemon(daemon)
        worker.start()

        if options.get("needs_join") or options.get("needs_join") == None:
            worker.join()
            return {"result": result}

        return {"worker": worker, "result": result}

    # asynchronous, needs_join
    def mprocess_run(self, function, options):
        """
        Description of mprocess_run

        Args:
            self (undefined):
            function (undefined):
            options (undefined):

        """
        # options structure
        # args, kwargs, needs_join

        # Test this instance of MProcessing for lock and other params

        result = None

        # # Check need here. Create a common one outside by user
        # # Consider if you want to handle this (Negative currently)

        # # share_value, share_array, share_queue, share_pipe, share_lock, share_rlock,
        # # share_manager, share_pool, share_connection, share_event,
        # # share_semaphore, share_bounded_semaphore

        if type(options) == dict:
            # # Keeping following to be user responsibility
            # # Check addition later
            # share_value = options.get("share_value")
            # share_array = options.get("share_array")

            args = options.get("args", [])
            if type(args) != list:
                args = []

            kwargs = options.get("kwargs", {})
            if type(kwargs) != dict:
                kwargs = {}

        daemon = options.get("daemon", True)
        if type(daemon) != bool:
            daemon = True

        worker = Process(
            target=function,
            args=(*args,),
            kwargs={**kwargs}
        )
        worker.daemon = daemon
        worker.start()

        if options.get("needs_join") or options.get("needs_join") == None:
            result = worker.join()
            return {"result": result}

        terminate = options.get("terminate")
        if type(terminate) != bool or terminate == True:
            worker.terminate()
            return {"result": result}

        return {"worker": worker, "result": result}

    # asynchronous, needs_join
    def mprocess_pool_run(self, function, options):
        pass

    def run_concurrently(self, function, options):
        mode = options.get("mode")
        if mode:
            if mode == "process":
                return self.mprocess_run(function, options)
            if mode == "process_pool":
                return self.mprocess_pool_run(function, options)
            if mode == "thread":
                return self.mthread_run(function, options)
            if mode == "async":
                pass
            if mode == "futures":
                pass
        return None


class TimerBase(UtilsBase, TimeBase):

    def __init__(self, timers={}):
        self.v = ["name", "_start_time", "_elapsed_time",
                  "_accumulated", "workflow_kwargs"]
        super().__init__("timers",
                         validations={"add": self.v, "fetch": self.v, "create": self.v,
                                      "update": self.v, "delete": ["name"]},
                         timers=timers)

    def timer_create(self, config):
        config.update({
            "_start_time": 0.0,
            "_elapsed_time": 0.0,
            "_accumulated": 0.0
        })
        print(config)
        u = self.create(config)
        if u:
            return True
        return False

    def time(self):
        return time.perf_counter()

    def elapsed_time(self, name):
        t = self.fetch(name)
        if not t:
            raise TypeError("Timer not present")
        else:
            return t.get("_elapsed_time")

    def curent_elapsed_time(self, name):
        t = self.fetch(name)
        if not t:
            raise ValueError("Timer not started")
        return time.perf_counter() - t.get("_start_time", 0.0)

    def reset(self, name):
        t = self.fetch(name)
        if t:
            t.update({
                "_start_time": 0.0,
                "_elapsed_time": 0.0,
                "_accumulated": 0.0
            })
            return True
        return False

    def start(self, name):
        # options object : {"name":"name", "timer": None}
        t = self.fetch(name)
        if not t:
            raise ValueError("Timer not present")
        t.update({
            "_start_time": self.time(),
            "_elapsed_time": 0.0
        })
        u = self.update(t)
        if u:
            return t["_start_time"]
        return False

    def stop(self, name):
        # options object : {"name":"name", "timer": None}
        t = self.fetch(name)
        if not t or not t.get("_start_time"):
            raise ValueError("Timer not present")
        elapsed_time = time.perf_counter() - t.get("_start_time")
        t.update({
            "_start_time": 0.0,
            "_elapsed_time": elapsed_time,
            "_accumulated": t["_accumulated"] + elapsed_time
        })
        u = self.update(t)
        if u:
            return elapsed_time
        raise Exception("Couldnot stop")


class FileReaderBase(UtilsBase):

    def __init__(self, validations={}, fileobjects={}):
        if validations:
            self.v = validations
        else:
            self.v = ["name", "file", "mode", "encoding", "workflow_kwargs"]

        super().__init__("fileobjects", validations={
            "add": self.v,
            "fetch": self.v,
            "create": self.v,
            "update": self.v,
            "delete": self.v
        }, fileobjects=fileobjects)

    def file_open(self, config):
        try:
            f = self.create(config)
            if f:
                return open(file=config.get("file"), mode=config.get("mode", "a+"), encoding=config.get("encoding", "utf-8"))
            raise Exception
        except Exception as e:
            return False

    def file_read(self, obj, way, char=None):
        try:
            if way == "read":
                if char:
                    return obj.read(char)
                else:
                    return obj.read()
            elif way == "readlines":
                return obj.readlines()
            elif way == "file":
                a = []
                for i in obj:
                    a.append(a)
                return a
            return True
        except Exception as e:
            return False

    def file_write(self, obj, items, way):
        try:
            if way == "write":
                obj.write(items)
            elif way == "writelines":
                obj.writelines(items)
            self.close_file(obj)
            return True
        except Exception as e:
            return False

    def file_close(self, obj):
        try:
            obj.close()
            return True
        except Exception as e:
            return False

    def row_insert(self, name, item, row=-1):
        c = self.fetch(name)
        try:
            if row == -1:
                c.update({"mode": "a+"})
                o = self.open_file(c)
                return self.file_write(o, item, "write")
            else:
                c.update({"mode": "w+"})
                o = self.open_file(c)
                f = self.file_read(o, "readlines")
                f.insert(row, item)
                return self.file_write(o, f, "writelines")
        except Exception as e:
            return False

    def row_append(self, name, item):
        c = self.fetch(name)
        try:
            c.update({"mode": "a+"})
            o = self.open_file(c)
            return self.file_write(o, item, "write")
        except Exception as e:
            return False

    def row_update(self, name, item, row=-1):
        c = self.fetch(name)
        c.update({"mode": "w+"})
        o = self.open_file(c)
        f = self.file_read(o, "readlines")
        try:
            if row == -1:
                f[len(f)-1] = item
            else:
                f[row] = item
            return self.file_write(o, f, "writelines")
        except Exception as e:
            return False

    def row_delete(self, name, row=-1):
        c = self.fetch(name)
        c.update({"mode": "w+"})
        o = self.open_file(c)
        f = self.file_read(o, "readlines")
        try:
            if row == -1:
                item = f.pop()
            else:
                item = f.pop(row)
            u = self.file_write(o, f, "writelines")
            if not u:
                raise Exception
            return item
        except Exception as e:
            return False

    def row_search(self, name, params):
        # exact, reg-match, reg-search, contains
        c = self.fetch(name)
        c.update({"mode": "r"})
        o = self.open_file(c)
        fir_lines = self.file_read(o, "readlines")
        arr = self.list_search(fir_lines, params)
        u = self.file_close(o)
        if not u:
            raise ValueError
        return arr


class CSVReaderBase(FileReaderBase):

    def __init__(self, validations={}, csvs={}):
        if validations:
            self.vd = validations
        else:
            self.v = ["name", "file", "mode", "encoding",
                      "seperator", "workflow_kwargs"]
            self.vd = {
                "add": self.v,
                "fetch": self.v,
                "create": self.v,
                "update": self.v,
                "delete": self.v
            }

        super().__init__(validations=self.vd, fileobjects=csvs)

    def rowitem_insert(self, name, head, item, params):
        a = self.row_search(name, params)

    def rowitem_fetch(self, name, head, params):
        a = self.row_search(name, params)

    def rowitem_update(self, name, head, item, params):
        a = self.row_search(name, params)

    def rowitem_delete(self, name, head, params):
        a = self.row_search(name, params)


class LogBase(UtilsBase, LogsBase):

    def __init__(self, loggers={}):
        self.v = ["name", "handlers", "logger", "workflow_kwargs"]
        self.fv = ["name", "file", "mode", "encoding",
                   "seperator", "workflow_kwargs"]
        super().__init__("loggers",
                         validations={"add": self.v, "fetch": self.v, "create": self.v,
                                      "update": self.v, "delete": ["name"]},
                         loggers=loggers)

        self.log_handlers = CSVReaderBase(validations={
            "add": self.fv,
            "fetch": self.fv,
            "create": self.fv,
            "update": self.fv,
            "delete": self.fv
        }, csvs={})

        # self.setter("loggers", config, self)
        # self.format = None
        # implement handlers and LoggerAdapters
        # self.handler = None
        # _del implementation fn (get from config)
        self._del = lambda x: x

        # delete implementation fn (get from config)
        self.delete = lambda x: x

    def logger_create(self, config):
        # Config object expected
        # { "name":"name",
        #   "handlers": {"handler": {"type": "file", "file": "filename.log"}, "format": "", "level": logging.INFO},
        #   "handlers": [{"handler": {"type": "file", "file": "filename.log"}, "format": "", "level": logging.DEBUG}]
        # }

        # Use config here. config contains network info if logging needed to network
        try:
            log = logging.getLogger(config.get("name"))
            if not config.get("handlers"):
                raise TypeError("Handlers Object not provided in config")

            if type(config.get("handlers")) == list:
                for hdlrs in config.get("handlers"):
                    if type(hdlrs) != dict:
                        raise ValueError(
                            "Error One in Configs list " + hdlrs.get("name"))
                    if config.get("handlers").get("handler").get("type") == "file":
                        h = logging.FileHandler(config.get("handlers").get(
                            "handler").get("file", "./demos/logs/logfile.log"))
                    elif config.get("handler").get("type") == "stream":
                        h = logging.StreamHandler()
                    if not h:
                        raise ValueError(
                            "Error in Config dict " + config.get("name"))
                    h.setLevel(config.get("level", logging.INFO))
                    fmt = logging.Formatter(
                        config.get("handlers").get(
                        "handler").get("format", "%(levelname)s - %(asctime)s - %(name)s - %(message)s"))
                    h.setFormatter(fmt)
                    log.addHandler(h)
            elif type(config.get("handlers")) == dict:
                if config.get("handlers").get("handler").get("type") == "file":
                    h = logging.FileHandler(config.get("handlers").get(
                        "handler").get("file", "./demos/logs/logfile.log"))
                elif config.get("handler").get("type") == "stream":
                    h = logging.StreamHandler()
                if not h:
                    raise ValueError(
                        "Error in Config dict " + config.get("name"))
                h.setLevel(config.get("level", logging.INFO))
                fmt = logging.Formatter(
                    config.get("handlers").get(
                        "handler").get("format", "%(levelname)s - %(asctime)s - %(name)s - %(message)s"))
                h.setFormatter(fmt)
                log.addHandler(h)
            else:
                raise TypeError
        except Exception as e:
            print("Error in creation of logger ", e)
            return False
        config.update({"logger": log})
        u = self.create(config)
        print(config)
        if u:
            return True
        return False

    def logger_delete(self, logger_name):
        # options object : {"name": "name"}
        u = self.delete(logger_name)
        if u:
            return True
        return False

    def log(self, options):
        # TODO: Concurrency can be added
        # https://docs.python.org/3/howto/logging-cookbook.html
        # options object : {"name":"name", "level": "debug", "message": ""}

        l = self.fetch(options.get("name"))
        log = l.get("logger")
        level = options.get("level", "info")
        message = options.get("message")
        try:
            if level == "critical":
                log.debug(message)
            elif level == "error":
                log.info(message)
            elif level == "info":
                log.warning(message)
            elif level == "warning":
                log.error(message)
            elif level == "debug":
                log.critical(message)
            else:
                raise Exception
            return True
        except Exception as e:
            # log.raise_error(e, level, message)
            print(log, level, message, e)
            return False


class PickleBase(UtilsBase, PicklesBase):
    # Consider PickleBase class for ORM and Authentication
    def __init__(self, pickles={}):
        self.v = ["name", "workflow_kwargs"]
        super().__init__(
            "pickles", validations={"add": self.v, "create": self.v, "update": self.v, "delete": ["name"]},
            pickles=pickles
        )

    def connection(self, config):
        pass

    def insert(self, name, config):
        pass

    def find(self, name, config):
        pass

    def update(self, name, config):
        pass

    def delete(self, name, config):
        pass


class CommandBase(UtilsBase, CommandsBase):

    def __init__(self, object_name="commands", validations={}, commands={}):
        self.v = ["name", "workflow_kwargs"]
        super().__init__(object_name, validations=self.v, commands=commands)

    def create(self, options):
        pass

    def execute(self, options):
        pass

    def close(self, options):
        pass

    def delete(self, options):
        pass


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

    def listen(self, event_name):
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


class Sockets(UtilsBase, SocketsBase):

    def __init__(self, socket={}):
        self.v = {
            "create": ["name", "protocol", "streammode", "host", "port", "numbers", "handler", "blocking", "nonblocking_data", "nonblocking_timeout", "server"],
            "add": ["name", "protocol", "streammode", "host", "port", "numbers", "handler", "blocking", "nonblocking_data", "nonblocking_timeout", "workflow_kwargs", "server"],
            "fetch": ["name"],
            "update": ["name"],
            "delete": ["name"]
        }
        super().__init__("sockets", validations=self.v, sockets=socket)

    def socket_create(self, socket_object):
        socket_object.update({
            "blocking": socket_object.get("blocking", True),
            "nonblocking_data": socket_object.get("nonblocking_data", None),
            "nonblocking_timeout": socket_object.get("nonblocking_timeout", 1),
            "server": socket_object.get("server", None)
        })
        if self.validate_object(socket_object, values=self.validations.get("create")):
            srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_object.update({"server": srv})
            return self.create(socket_object)
        raise ValueError

    def socket_listen(self, socket_name):
        sel = selectors.DefaultSelector()
        socket_object = self.fetch(socket_name)
        blocking = socket_object.get("blocking", False)
        srv = socket_object.get("server")
        srv.bind((socket_object.get("host"), socket_object.get("port")))
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.listen(socket_object.get("numbers", 1))
        srv.setblocking(blocking)
        if not blocking:
            sel.register(srv, selectors.EVENT_READ, data=None)
        socket_object.update({"server": srv, "selectors": sel})
        self.socket_accept(socket_object)
        return True

    def socket_accept(self, socket_object):
        srv = socket_object.get("server")
        sel = socket_object.get("selectors")
        blocking = socket_object.get("blocking")
        while True and srv:
            if blocking:
                try:
                    conn, addr = srv.accept()

                    # IMPORTANT NOTES
                    # Sending, Receiving data is Handlers work
                    # Closing connection is Handlers work
                    socket_object.get("handler")(conn, addr, socket_object)
                    try:
                        if conn:
                            conn.close()
                    except Exception as e:
                        pass
                    print("Closing connection to client", str(addr))
                except KeyboardInterrupt:
                    print("Exiting due to keyboard interrupt")
                except Exception as e:
                    raise e
            else:
                def accept_wrapper(sock):
                    try:
                        # Should be ready to read
                        conn, addr = sock.accept()  # Should be ready to read
                        print("accepted connection from", addr)
                        # conn.setblocking(False)
                        data = types.SimpleNamespace(
                            addr=addr, inb=b"", outb=b"")
                        events = selectors.EVENT_READ | selectors.EVENT_WRITE
                        sel.register(conn, events, data=data)
                        return True
                    except Exception as e:
                        print("Error in service connection: accept_wrapper")
                        # raise e
                        return False

                def service_connection(key, mask):
                    try:
                        sock = key.fileobj
                        data = key.data
                        if mask & selectors.EVENT_READ:
                            # Should be ready to read
                            recv_data = sock.recv(1024)
                            if recv_data:
                                data.outb += recv_data
                            else:
                                print("closing connection to", data.addr)
                                sel.unregister(sock)
                                sock.close()
                        if mask & selectors.EVENT_WRITE:
                            if data.outb:
                                print("echoing", repr(
                                    data.outb), "to", data.addr)
                                # Should be ready to write
                                sent = sock.send(data.outb)
                                data.outb = data.outb[sent:]
                        # sock.close()
                        return True
                    except Exception as e:
                        print("Error in service connection: service_connection")
                        # raise e
                        return False
                try:
                    while True:
                        events = sel.select(timeout=None)
                        for key, mask in events:
                            if key.data is None:
                                accept_wrapper(key.fileobj)
                            else:
                                service_connection(key, mask)
                except KeyboardInterrupt:
                    print("Caught keyboard interrupt, exiting")
                    sys.exit(0)
                finally:
                    sel.close()

        print("Server connection to client closed")
        socket_object.update({"server": srv, "selectors": sel})
        return self.update(socket_object)

    def socket_multi_server_connect(self, socket_object, messages=[]):
        connections = socket_object.get("numbers", 1)
        server_addr = (socket_object.get("host"), socket_object.get("port"))
        sel = selectors.DefaultSelector()
        blocking = socket_object.get("blocking", False)

        def service_connection(key, mask):
            sock = key.fileobj
            data = key.data
            if mask & selectors.EVENT_READ:
                recv_data = sock.recv(1024)  # Should be ready to read
                if recv_data:
                    print("Received ", repr(recv_data),
                          " from connection ", data.connid)
                    data.recv_total += len(recv_data)
                if not recv_data or data.recv_total == data.msg_total:
                    print("Closing connection ", data.connid)
                    sel.unregister(sock)
                    sock.close()
            if mask & selectors.EVENT_WRITE:
                if not data.outb and data.messages:
                    data.outb = data.messages.pop(0)
                if data.outb:
                    print("Sending ", repr(data.outb),
                          " to connection ", data.connid)
                    # Should be ready to write
                    sent = sock.send(data.outb)
                    data.outb = data.outb[sent:]

        for i in range(0, connections):
            connid = i + 1
            print("Starting connection ", connid, " to ", server_addr)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(blocking)
            sock.connect_ex(server_addr)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(
                connid=connid,
                msg_total=sum(len(m) for m in messages),
                recv_total=0,
                messages=list(messages),
                outb=b"",
            )
            sel.register(sock, events, data=data)
        try:
            while True:
                events = sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        service_connection(key, mask)
                # Check for a socket being monitored to continue.
                if not sel.get_map():
                    break
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            sel.close()

    def socket_connect(self, socket_object, messages=[]):
        connections = socket_object.get("numbers", 1)
        server_addr = (socket_object.get("host"), socket_object.get("port"))
        sel = selectors.DefaultSelector()
        blocking = socket_object.get("blocking", False)
        if connections == 0:
            raise ValueError
        elif connections < 2:
            o = self.socket_create(socket_object)
            if o:
                s = self.fetch(socket_object.get("name"))
                srv = s.get("server")
                srv.connect(server_addr)
                srv.sendall(b"Hello, world from client")
                data = srv.recv(1024)
                print("Received ", str(data))
                s.get("handler")(messages, s)
                try:
                    s.get("server").close()
                except Exception:
                    pass
        else:
            o = socket_object
            o["selectors"] = sel
            self.socket_multi_server_connect(o, messages)

    def socket_close(self, socket_object):
        return socket_object.close()

    def socket_delete(self, socket_object):
        try:
            return self.delete(socket_object.get("name"))
        except Exception as e:
            raise e

    def send(self, socket_object, message):
        return socket_object.send(str(message).encode())

    def receive(self, socket_object):
        msg = socket_object.recv(1024).decode()
        return ast.literal_eval(msg)


class EPubSub(UtilsBase, PubSubsBase):

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
        if e and e.get("listening"):
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
                r1 = self.__handler(message_object, srv_hdlr)
                # Get all subscriber handlers
                if not r1:
                    print("Return Error R1")
                srv_pbh = e.get("publishers").get(
                    message_object.get("publisher")).get("handler", h)
                # Invoke Publisher
                print("Running Handler srv_pbh")
                r2 = self.__handler(message_object, srv_pbh)
                if not r2:
                    print("Return Error R2")
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
        qConfig = copy.copy(config)
        tmpQ = Queues()
        qConfig["queue"] = tmpQ.new(qConfig)
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
                    "listening": False,
                    "publishers": event_object.get("publishers", {}),
                    "subscribers": event_object.get("subscribers", {})
                }
            ]
        ]))
        return self.update(e)

    def listen(self, pubsub_name, event_name):
        e = self.fetch(pubsub_name)
        e["events"].get(event_name).update({"listening": True})
        return self.update(e)

    def stop(self, pubsub_name, event_name):
        e = self.fetch(pubsub_name)
        e["events"].get(event_name).update({"listening": False})
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


class IPubSub(EPubSub):

    server = None

    def __init__(self, validations={}, pubsubs={}, type="ipubsub", agent="server", socketsbase=Sockets):
        super().__init__(pubsubs=pubsubs, type=type, agent=agent)
        self.v = ["name", "handler", "queue", "maxsize",
                  "queue_type", "batch_interval", "processing_flag", "events", "workflow_kwargs"]
        self.ev = ["name", "pubsub_name", "publishers", "subscribers"]
        self.server = socketsbase()

    def __multilistener_server(self, config):
        c = copy.copy(config.get("handler", lambda key, mask, data, sock, conn, addr,
                                 socket_object: print(key, mask, data, sock, conn, addr, socket_object)))

        def server_nonblocking_handler(key, mask, data, sock, conn, addr, socket_object):
            print(conn, addr)
            # print(conn.recv(1024))
            # conn.send("Test message from server".encode())
            # conn.close()
            c(key, mask, data, sock, conn, addr, socket_object)

        config["handler"] = server_nonblocking_handler
        sc = self.server.socket_create(config)

        if sc:
            print("Server started ")
            sl = self.server.socket_listen(config.get("name"))
            if sl:
                return self.server
        return False

    def publisher_socket(self, config):
        c = copy.copy(config.get("handler", lambda key, mask, sel,
                                 socket_object: print(key, mask, sel, socket_object)))

        def client_nonblocking_handler(key, mask, sel, socket_object):
            """
            Applies for numbers > 1
            """
            # sock.send("Testing the client message".encode())
            # print(sock.recv(1024).decode())
            # sock.close()
            # print("Test")
            c(key, mask, sel, socket_object)

        config["handler"] = client_nonblocking_handler
        self.server = config
        return self.server

    def subscriber_socket(self, config):
        return self.__multilistener_server(config)

    def server_socket(self, config):
        return self.__multilistener_server(config)


class Actions(UtilsBase):

    def __init__(self, action={}):
        super().__init__("actions", actions=action)


class Hooks(UtilsBase, HooksBase):

    server = None

    def __init__(self, validations={}, hooks={}, socketsbase=Sockets):
        self.v = validations
        super().__init__("hooks", validations=self.v, hooks=hooks)
        self.server = socketsbase()

    def hook_state(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def service_run(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def service_stop(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def register_hook(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def register_receiver(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def send(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def receive(self, config):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass


class Webhooks(UtilsBase):

    def __init__(self, action={}):
        super().__init__("actions", actions=action)


class SSH(CommandBase, SshBase):

    server = None

    def __init__(self, validations={}, pubsub={}, socketsbase=Sockets):
        self.v = validations
        super().__init__("pubsubs", validations=self.v, pubsubs=pubsub)
        self.server = socketsbase()

    def create(self, options):
        pass

    def connect(self, options):
        pass

    def execute(self, options):
        pass

    def close(self, options):
        pass


if __name__ == "__main__":
    c = ClosureBase("Test", {})


if __name__ == "__main__":
    concurrency = ConcurencyBase()


if __name__ == "__main__":
    s = SharedBase("Test", {})


if __name__ == "__main__":
    t = TimerBase({}, {})


if __name__ == "__main__":
    l = LogBase({}, {})


if __name__ == "__main__":
    c = CommandsBase({}, {})


if __name__ == "__main__":
    Socket = Sockets()


if __name__ == "__main__":

    config = {"name": "test", "maxsize": 10,
              "queue_type": "queue", "queue": None}
    queue = Queues()
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

    print("\nActions:\nDemonstrating Action and Action Listeners")
    event = Events()

    def run(data):
        print("Run Action Handler ->", data)

    c = event.event_register({"name": "new", "event": run})
    if c:
        event.listener_register(
            {"name": "run", "event_name": "new", "listener": run})
        event.on("new", "runner", lambda data: print(
            "Second Listener running -> ", data))
        event.listen("new")
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

    def run(data):
        print("Running Pubsub ", data)

    def publisher(data):
        print("Running publisher ", data)

    def subscriber(data):
        print("Running subscriber ", data)

    config = {"name": "new", "handler": run, "queue": None, "maxsize": 10,
              "queue_type": "queue", "processing_flag": False,  "batch_interval": 5, "events": {}}
    name = config.get("name")

    pb = EPubSub()
    p = pb.pubsub_create(config)

    if p:
        print("Event register ", pb.register_event(
            name, {"name": "testevent", "event": run}))
        print("Event listen ", pb.listen(name, "testevent"))
        print("Publish register ", pb.register_publisher(
            name, {"name": "pubone", "event_name": "testevent", "publisher": publisher}))
        print("Subscribers register ", pb.register_subscriber(
            name, {"name": "subone", "event_name": "testevent", "subscriber": subscriber}))
        print("Subscribers register ", pb.register_subscriber(
            name, {"name": "subtwo", "event_name": "testevent", "subscriber": subscriber}))
        print("Event sending ", pb.send(
            {"event_name": "testevent", "queue_name": "new", "message": "Testing event testevent", "publisher": "pubone"}))
        print("Publisher unregister ", pb.unregister_publisher(
            name, {"name": "pubone", "event_name": "testevent"}))
        print("Subscriber unregister ", pb.unregister_subscriber(
            name, {"name": "subone", "event_name": "testevent"}))
        print("Subscriber unregister ", pb.unregister_subscriber(
            name, {"name": "subtwo", "event_name": "testevent"}))
        print("Pubsub Object PRINT FROM SCRIPT: ", pb.fetch(name))
        print("Event unlisten ", pb.stop(name, "testevent"))
        print("Pubsub Object Deleted ", pb.pubsub_delete(name))
        print("Pubsub Object ", pb.fetch(name))


if __name__ == "__main__":

    action = Actions()


if __name__ == "__main__":

    hook = Hooks(socketsbase=Sockets)


if __name__ == "__main__":

    webhook = Webhooks(socketsbase=Sockets)


if __name__ == "__main__":

    ssh = SSH()


__all__ = [
    "SharedBase", "ClosureBase", "UtilsBase",
    "TimerBase", "FileReaderBase", "CSVBase",
    "LogBase", "CommandBase",
    "ConcurencyBase", "Queues",
    "Events", "Sockets",
    "Actions", "Hooks", "Webhooks",
    "EPubSub", "IPubSub", "SSH"
]


# 1, 3, 5, (26)
