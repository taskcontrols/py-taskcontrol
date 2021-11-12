# SHARED BASE

import ast
import time
import sys
import types
import socket
import selectors
import copy
import logging
import re
import pickle
# import yaml
import csv
import os
import sys
import shutil
import subprocess
import json
import argparse
from genericpath import exists
from pathlib import Path
from collections import defaultdict
from xml.etree import cElementTree as ET
from collections import deque
from typing import Dict, List
from threading import Thread, Lock
from multiprocessing import Process, Array, Value, Manager
from queue import Queue, LifoQueue, PriorityQueue, SimpleQueue
from taskcontrol.lib.interfaces import ObjectModificationInterface, SocketsInterface, HooksInterface, SSHInterface, FileReaderInterface, CSVReaderInterface
from taskcontrol.lib.interfaces import QueuesInterface, EventsInterface, PubSubsInterface, TimeInterface, LogsInterface, CommandsInterface, PicklesInterface


class ClosureBase():
    def class_closure(self, **kwargs):
        """

        """
        closure_val = kwargs

        def getter(key, value=None):
            """

            """
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
            """

            """
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
            """

            """
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
        """

        """
        super().__init__()
        self.getter, self.setter, self.deleter = self.class_closure(
            workflows={}, tasks={}, plugins={}, ctx={}, configs={},
            loggers={}, orms={}, auth={}, timers={}, files={}, pickles={},
            queues={}, events={}, sockets={},
            epubsubs={}, ipubsubs={}, webhooks={},
            cmds={}, ssh={}
        )
        if SharedBase.__instance != None:
            pass
        else:
            SharedBase.__instance = self

    def __new__(cls):
        """

        """
        if cls.__instance is None:
            cls.__instance = super(SharedBase, cls).__new__(cls)
        return cls.__instance

    @staticmethod
    def getInstance():
        """

        """
        if not SharedBase.__instance:
            return SharedBase()
        return SharedBase.__instance


class ConcurencyBase():
    """

    """
    # consider adding concurrency futures
    @staticmethod
    def futures():
        """

        """
        pass

    # consider adding asyncio lib
    @staticmethod
    def asyncio():
        """

        """
        pass

    # asynchronous, needs_join
    @staticmethod
    def mthread(function, options):
        """
        Description of mthread

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
    @staticmethod
    def mprocess(function, options):
        """
        Description of mprocess

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
    @staticmethod
    def mprocess_pool(function, options):
        """

        """
        pass

    @staticmethod
    def concurrency(function, options):
        """

        """
        mode = options.get("mode")
        if mode:
            if mode == "process":
                return ConcurencyBase.mprocess(function, options)
            if mode == "process_pool":
                return ConcurencyBase.mprocess_pool(function, options)
            if mode == "thread":
                return ConcurencyBase.mthread(function, options)
            if mode == "async":
                return ConcurencyBase.asyncio(function, options)
            if mode == "futures":
                return ConcurencyBase.futures(function, options)
        return None


class UtilsBase(ObjectModificationInterface):
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
        """

        """
        for k in update_object:
            if k in main_object:
                main_object.update(dict([[k, update_object.get(k)]]))
            else:
                main_object.append(dict([[k, update_object.get(k)]]))
        return main_object

    def validate_object(self, val_object, values=[]):
        """

        """
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
        """

        """
        arr = []
        for idx, l in enumerate(list_object):
            for w in params:
                if w.type == "exact":
                    if l == w.param:
                        arr.append({"row": idx, "item": l})
                if w.type == "reg-match":
                    p = re.compile(w.get("pattern"))
                    if re.match(p, w.get("param")):
                        arr.append({"row": idx, "item": l})
                elif w.type == "reg-search" or w.type == "contains":
                    p = re.compile(w.get("pattern"))
                    if re.search(p, w.get("param")):
                        arr.append({"row": idx, "item": l})
        return arr

    def list_modify(self, list_object, fnc, params=None):
        """

        """
        if not params:
            return map(fnc, list_object)
        arr = []
        for idx, l in enumerate(list_object):
            for w in params:
                if w.type == "exact":
                    if l == w.param:
                        arr.append({"row": idx, "item": fnc(l)})
                if w.type == "reg-match":
                    p = re.compile(w.get("pattern"))
                    if re.match(p, w.get("param")):
                        arr.append({"row": idx, "item": fnc(l)})
                elif w.type == "reg-search" or w.type == "contains":
                    p = re.compile(w.get("pattern"))
                    if re.search(p, w.get("param")):
                        arr.append({"row": idx, "item": fnc(l)})
        return arr

    def create(self, config):
        """

        """
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
        """

        """
        try:
            return self.getter(self.object_name, name)[0]
        except Exception as e:
            print("Fetch error ", e)
            return False

    def update(self, config):
        """

        """
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
        """

        """
        try:
            return self.deleter(self.object_name, name)
        except Exception as e:
            print("Fetch error ", e)
            return False


class TimerBase(UtilsBase, TimeInterface):

    def __init__(self, timers={}):
        """

        """
        self.v = ["name", "_start_time", "_elapsed_time",
                  "_accumulated", "workflow_kwargs"]
        super().__init__("timers",
                         validations={"add": self.v, "fetch": self.v, "create": self.v,
                                      "update": self.v, "delete": ["name"]},
                         timers=timers)

    def timer_create(self, config):
        """

        """
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
        """

        """
        return time.perf_counter()

    def elapsed_time(self, name):
        """

        """
        t = self.fetch(name)
        if not t:
            raise TypeError("Timer not present")
        else:
            return t.get("_elapsed_time")

    def curent_elapsed_time(self, name):
        """

        """
        t = self.fetch(name)
        if not t:
            raise ValueError("Timer not started")
        return time.perf_counter() - t.get("_start_time", 0.0)

    def reset(self, name):
        """

        """
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
        """

        """
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
        """

        """
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


class FileReaderBase(UtilsBase, FileReaderInterface):

    def __init__(self, validations={}, fileobjects={}):
        """

        """
        if len(validations):
            self.v = validations
        else:
            # self.v = ["name", "file", "mode", "encoding", "workflow_kwargs"]
            self.v = ["name", "file", "mode", "workflow_kwargs"]

        super().__init__("fileobjects", validations={
            "add": self.v,
            "fetch": self.v,
            "create": self.v,
            "update": self.v,
            "delete": ["name"]
        }, fileobjects=fileobjects)

    def exists(self, file_path):
        """

        """
        return os.path.exists(file_path)

    def is_file(self, file_path):
        """

        """
        path = Path(file_path)
        return path.is_file()

    @staticmethod
    def csv_to_dict(csvfile):
        """

        """
        return csv.DictReader(open(csvfile))

    @staticmethod
    def yml_to_dict(ymlfile):
        """

        """
        # with open(ymlfile) as inf:
        #     content = yaml.load(inf, Loader=yaml.Loader)
        #     return content
        pass

    @staticmethod
    def xml_to_dict(node):
        """

        """
        # # https://stackoverflow.com/questions/2148119/how-to-convert-an-xml-string-to-a-dictionary
        # d = {t.tag: {} if t.attrib else None}
        # children = list(t)
        # if children:
        #     dd = defaultdict(list)
        #     for dc in map(FileReaderBase.xml_to_dict, children):
        #         for k, v in dc.items():
        #             dd[k].append(v)
        #     d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
        # if t.attrib:
        #     d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
        # if t.text:
        #     text = t.text.strip()
        #     if children or t.attrib:
        #         if text:
        #             d[t.tag]['#text'] = text
        #     else:
        #         d[t.tag] = text
        # return d
        return {'tag': node.tag, 'text': node.text, 'attrib': node.attrib, 'children': {child.tag: FileReaderBase.xml_to_dict(child) for child in node}}

    @staticmethod
    def json_to_dict(node):
        """

        """
        return json.loads(node)

    @staticmethod
    def dict_to_json(node):
        """

        """
        return json.dumps(node)

    @staticmethod
    def dict_to_xml(diction):
        """

        """
        try:
            basestring
        except NameError:
            basestring = str

        def _to_etree(diction, root):
            if not diction:
                pass
            elif isinstance(diction, basestring):
                root.text = diction
            elif isinstance(diction, dict):
                for k, v in diction.items():
                    assert isinstance(k, basestring)
                    if k.startswith('#'):
                        assert k == '#text' and isinstance(v, basestring)
                        root.text = v
                    elif k.startswith('@'):
                        assert isinstance(v, basestring)
                        root.set(k[1:], v)
                    elif isinstance(v, list):
                        for e in v:
                            _to_etree(e, ET.SubElement(root, k))
                    else:
                        _to_etree(v, ET.SubElement(root, k))
            else:
                raise TypeError('invalid type: ' + str(type(diction)))
        assert isinstance(diction, dict) and len(diction) == 1
        tag, body = next(iter(diction.items()))
        node = ET.Element(tag)
        _to_etree(body, node)
        return ET.tostring(node)

    # def dictify_xml(r,root=True):
    #     if root:
    #         return {r.tag : dictify(r, False)}
    #     d=copy(r.attrib)
    #     if r.text:
    #         d["_text"]=r.text
    #     for x in r.findall("./*"):
    #         if x.tag not in d:
    #             d[x.tag]=[]
    #         d[x.tag].append(dictify(x,False))
    #     return d

    @staticmethod
    def dict_to_csv(csv_filename, headers=[], diction_list=[]):
        """

        """
        try:
            with open(csv_filename, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                # Every data in the list will be a
                #       dictionary with matching columns
                for data in diction_list:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

    @staticmethod
    def dict_yml(yml_filename, diction):
        """

        """
        pass

    def file_open(self, name):
        """

        """
        config = self.fetch(name)
        try:
            # return open(config.get("file"), config.get("mode"), config.get("encoding"))
            return open(config.get("file"), config.get("mode"))
        except Exception as e:
            return False

    def file_read(self, obj, way, index=None):
        """

        """
        try:
            if way == "read":
                if index:
                    return obj.read(index)
                else:
                    return obj.read()
            elif way == "readline":
                if index:
                    return obj.readline(index)
                else:
                    return obj.readline()
            elif way == "readlines":
                return obj.readlines()
            elif way == "file":
                a = []
                for i in obj:
                    a.append(i)
                return a
            return False
        except Exception as e:
            return False

    def file_write(self, obj, items, way):
        """

        """
        try:
            if way == "write":
                obj.write(items)
            elif way == "writeline":
                obj.writeline(items)
            elif way == "writelines":
                obj.writelines(items)
            return True
        except Exception as e:
            return False

    def file_close(self, obj):
        """

        """
        try:
            obj.close()
            return True
        except Exception as e:
            return False

    def row_insert(self, name, item, row=None):
        """

        """
        # c = self.fetch(name)
        # try:
        #     if row == None:
        #         c.update({"mode": "a"})
        #         o = self.file_open(c)
        #         w = self.file_write(o, item, "writeline")
        #         print(w)
        #         u = self.file_close(o)
        #         if not u:
        #             raise Exception
        #         return True
        #     else:
        #         c.update({"mode": "w"})
        #         o = self.file_open(c)
        #         f = self.file_read(o, "readlines")
        #         f.insert(row, item)
        #         print(f)
        #         w = self.file_write(o, f, "write")
        #         u = self.file_close(o)
        #         if not u:
        #             raise Exception
        #         return True
        # except Exception as e:
        #     return False
        pass

    def row_append(self, name, item):
        """

        """
        # c = self.fetch(name)
        # try:
        #     c.update({"mode": "a+"})
        #     o = self.file_open(c)
        #     w = self.file_write(o, item, "write")
        #     u = self.file_close(o)
        #     if not u:
        #         raise Exception
        # except Exception as e:
        #     return False
        pass

    def row_update(self, name, item, row=-1):
        """

        """
        # c = self.fetch(name)
        # c.update({"mode": "w+"})
        # o = self.file_open(c)
        # f = self.file_read(o, "readlines")
        # try:
        #     if row == -1:
        #         f[len(f)-1] = item
        #     else:
        #         f[row] = item
        #     w = self.file_write(o, f, "writelines")
        #     u = self.file_close(o)
        #     if not u:
        #         raise Exception
        # except Exception as e:
        #     return False
        pass

    def row_delete(self, name, row=-1):
        """

        """
        # c = self.fetch(name)
        # c.update({"mode": "w+"})
        # o = self.file_open(c)
        # f = self.file_read(o, "readlines")
        # try:
        #     if row == -1:
        #         item = f.pop()
        #     else:
        #         item = f.pop(row)
        #     w = self.file_write(o, f, "writelines")
        #     u = self.file_close(o)
        #     if not u:
        #         raise Exception
        #     return item
        # except Exception as e:
        #     return False
        pass

    def row_search(self, name, params):
        """

        """
        # exact, reg-match, reg-search, contains
        c = self.fetch(name)
        c.update({"mode": "r"})
        o = self.file_open(c)
        fir_lines = self.file_read(o, "readlines")
        arr = self.list_search(fir_lines, params)
        u = self.file_close(o)
        if not u:
            raise ValueError
        return arr


class CSVReaderBase(FileReaderBase, CSVReaderInterface):

    def __init__(self, csvs={}):
        """

        """
        self.v = ["name", "file", "mode", "encoding",
                  "seperator", "heads", "workflow_kwargs"]
        self.vd = {
            "add": self.v,
            "fetch": self.v,
            "create": self.v,
            "update": self.v,
            "delete": self.v
        }
        super().__init__(validations=self.vd, fileobjects=csvs)

    def csv_to_json():
        """

        """
        # https://dzone.com/articles/full-stack-development-tutorial-sending-pandas-dat
        pass

    def csv_to_xml():
        """

        """
        # https://dzone.com/articles/using-python-pandas-for-log-analysis
        # https://pbpython.com/pdf-reports.html
        pass

    def row_insert(self, name, head, params):
        """

        """
        return False

    def row_fetch(self, name, head, params):
        """

        """
        return False

    def row_update(self, name, params):
        """

        """
        return False

    def row_delete(self, name, head):
        """

        """
        return False


class LogBase(UtilsBase, LogsInterface):

    def __init__(self, loggers={}):
        """

        """
        self.v = ["name", "handlers", "logger", "workflow_kwargs"]
        self.fv = ["name", "file", "mode", "encoding",
                   "seperator", "workflow_kwargs"]
        super().__init__("loggers",
                         validations={"add": self.v, "fetch": self.v, "create": self.v,
                                      "update": self.v, "delete": ["name"]},
                         loggers=loggers)

        # self.log_handlers = CSVReaderBase(validations={
        #     "add": self.fv,
        #     "fetch": self.fv,
        #     "create": self.fv,
        #     "update": self.fv,
        #     "delete": self.fv
        # }, csvs={})

        # self.setter("loggers", config, self)
        # self.format = None
        # implement handlers and LoggerAdapters
        # self.handler = None
        # _del implementation fn (get from config)
        self._del = lambda x: x

        # delete implementation fn (get from config)
        self.delete = lambda x: x

    def logger_create(self, config):
        """

        """
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
                            "handler").get("path", "./logs/") + config.get("name") + "_" + config.get("handlers").get(
                            "handler").get("file", "logfile.log"))
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
                        "handler").get("path", "./logs/") + config.get("name") + "_" + config.get("handlers").get(
                        "handler").get("file", "logfile.log"))
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
            return False
        config.update({"logger": log})
        u = self.create(config)
        if u:
            return True
        return False

    def log(self, options):
        """

        """
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
            log.error("Exception occurred " + str(e) + " " +
                      level + " " + message, exc_info=True)
            return False


class PicklesBase(UtilsBase, PicklesInterface):
    # Consider PickleBase class for ORM and Authentication
    def __init__(self, pickles={}):
        """

        """
        self.v = ["name", "workflow_kwargs"]
        super().__init__(
            "pickles", validations={"add": self.v, "create": self.v, "update": self.v, "delete": ["name"]},
            pickles=pickles
        )

    def row_insert(self, config):
        """

        """
        pass

    def row_append(self, config):
        """

        """
        pass

    def row_update(self, config):
        """

        """
        pass

    def row_delete(self, config):
        """

        """
        pass

    def search(self, config):
        """

        """
        pass

    def connection(self, config):
        """

        """
        pass


class CommandsBase(UtilsBase, CommandsInterface):

    def __init__(self, object_name="commands", validations={}, commands={}):
        """
        object_name: command [Default: "commands". Instance's object_name used for differentiating class object instances] \n
        validations: create, add, fetch, update, delete \n
        commands: type(command) -> name, command, options(options:arguments) \n
        """
        self.v = ["name", "command", "options", "workflow_kwargs"]
        super().__init__(object_name, validations=self.v, commands=commands)

    def exists(self, command):
        """
        command: command [Executable or command that needs to be checked for presence]
        """
        return shutil.which(command) is not None

    def path(self, command):
        """
        command: command [Executable or command that needs to be path mapped]
        """
        return shutil.which(command)

    def execute(self, command, mode="subprocess_call", stdin_mode=False, stdin_options={}, *args):
        """
        command: command [Default: "commands"] \n
        stdin_mode: True/False [Default: False. Get input value.] \n
        stdin_options: [Options object that will be requested for Stdin] \n
        mode: str("subprocess_call", "subprocess_popen", "subprocess_run", "os_popen") [Default: "subprocess_call"] \n
        args: list(args to be passed to command) \n
        """
        try:
            if self.exists(command):
                if mode == "subprocess_call":
                    r = subprocess.call([command, *args])
                elif mode == "subprocess_popen":
                    stream = subprocess.Popen([command, *args],
                                              stdin=subprocess.PIPE,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE,
                                              universal_newlines=True,
                                              bufsize=0)
                    if stdin_mode:
                        ssh.stdin.write("uname -a\n")
                        ssh.stdin.close()
                    r = stream.read()
                elif mode == "subprocess_run":
                    process = subprocess.run([command, *args],
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             universal_newlines=True)
                    r = process.stdout
                elif mode == "os_popen":
                    stream = os.popen([command, *args])
                    r = stream.read()
                elif mode == "os_popen":
                    stream = os.popen([command, *args])
                    r = stream.read()
                return r
            raise Exception
        except Exception:
            return False


class QueuesBase(UtilsBase, QueuesInterface):
    tmp = {}

    def __init__(self, queues={}):
        """
        queues: type(queue) -> [name, maxsize, queue_type, queue] \n
        """
        self.v = ["name", "maxsize", "queue_type", "queue", "workflow_kwargs"]
        super().__init__("queues", validations={
            "add": self.v, "create": self.v, "update": self.v, "delete": ["name"]}, queues=queues)

    def new(self, config):
        """
        config: type(queue)
        """
        if self.validate_object(config, values=["name", "maxsize", "queue_type", "queue"]):
            if config.get("queue_type") == "queue":
                return Queue(maxsize=config.get("maxsize"))
            elif config.get("queue_type") == "deque":
                return deque([], maxlen=config.get("maxsize"))
            else:
                return []

    def add(self, name, item, index=0, nowait=True):
        """
        name: name \n
        item: type(item) [] \n
        index: [Default: 0] \n
        nowait: True/False [Default: True] \n
        """
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
        """
        name: name \n
        index: [Default: 0] \n
        nowait: True/False [Default: True] \n
        """
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


class EventsBase(UtilsBase, EventsInterface):

    def __init__(self, event={}):
        """

        """
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
        """

        """
        print("Deleting event: ", event_name)
        return self.delete(event_name)

    def listener_register(self, listener_object):
        """

        """
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
        """

        """
        return self.listener_register({"name": name, "event_name": event_name, "listener": handler})

    def listener_unregister(self, listener_object):
        """

        """
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
        """

        """
        try:
            e = self.fetch(event_name)
            if e:
                return e.get("listening")
            return False
        except Exception as e:
            raise e

    def set_state(self, event_name, state):
        """

        """
        try:
            event = self.fetch(event_name)
            event["listening"] = state
            # Stop/Start listening to event
            return self.update(event)
        except Exception as e:
            raise e

    def listen(self, event_name):
        """

        """
        return self.set_state(event_name, True)

    def stop(self, event_name):
        """

        """
        return self.set_state(event_name, False)

    def send(self, message_object):
        """

        """
        try:
            action = self.fetch(message_object.get("event_name"))
            if action.get("listening"):
                action.get("handler")(message_object.get("message"))
                return True
            return False
        except Exception as e:
            raise e

    def emit(self, event_name, message):
        """

        """
        return self.send({"event_name": event_name, "message": message})


class SchedularBase(UtilsBase):
    """
    SchedularBase
    """
    #  EventsBase Send events for running schedular at a specific interval or time or day or manually

    def __init__(self, schedulars={}):
        # type of schedular: time, timestamp, days (Type of schedular)
        # time: secs, timestamp, days. the interval value the schedular should run
        # flag: True, False. if the schedular is running currently
        # function: The function to run for schedular
        # active: True, False, if the schedular can be run or not
        # interval: single, multiple. if this is a single or multiple run
        self.v = ["name", "active", "interval", "type",
                  "time", "function", "schedular", "flag", "workflow_kwargs"]
        super().__init__("schedulars",
                         validations={"add": self.v, "fetch": self.v, "create": self.v,
                                      "update": self.v, "delete": ["name"]},
                         schedulars=schedulars)

    def __runschedular(self, name, func, interval):
        """
        name:
        func:
        interval:
        """
        try:
            o = self.fetch(name)
            if o.get("flag") == False:
                o.update({"flag": True})
                s = self.update(o)
                if s:
                    res = func()
                    o = self.fetch(name)
                    if o.get("flag") == True:
                        o.update({"flag": False})
                        s = self.update(o)
                        if s:
                            if o.get("type") == "time":
                                dTime = interval
                            if o.get("type") == "timestamp":
                                dTime = 24 * 60 * 60
                            if o.get("type") == "days":
                                dTime = interval * 24 * 60 * 60
                            time.sleep(dTime)
                            self.__timebased(name, func, interval)
            return False
        except Exception as e:
            return False

    def __schedular(self, sch):
        """
        sch
        """
        if sch.get("interval") == "repeated" and sch.get("active") == True:
            sobj = self.__runschedular(
                sch.get("name"), sch.get("function"), sch.get("time"))
        elif sch.get("interval") == "single" and sch.get("active") == True:
            sobj = sch.get("function")()
        if sobj:
            return sobj
        return False

    def manual(self, name):
        """

        """
        try:
            o = self.fetch(name)
            if o.get("flag") == False:
                o.update({"flag": True})
                s = self.update(o)
                if s:
                    res = o.get("function")()
                    o.update({"flag": False})
                    s = self.update(o)
                    if s:
                        return res
            return False
        except Exception as e:
            return False

    def start(self, name):
        """

        """
        sch = self.fetch(name)
        sobj = self.__schedular(sch)
        if sobj:
            if sch:
                sch.update({"active": True, "schedular": sobj})
                u = self.update(sch)
                if u:
                    return True
        return False

    def stop(self, name):
        """

        """
        sc = self.fetch(name)
        if sc:
            sc.update({"active": False, "schedular": None})
            u = self.update(sc)
            if u:
                return True
        return False


class SocketsBase(UtilsBase, SocketsInterface):

    def __init__(self, socket={}):
        """
        socket: 
        """
        self.v = {
            "create": ["name", "protocol", "streammode", "host", "port", "numbers", "handler", "blocking", "nonblocking_data", "nonblocking_timeout", "server"],
            "add": ["name", "protocol", "streammode", "host", "port", "numbers", "handler", "blocking", "nonblocking_data", "nonblocking_timeout", "workflow_kwargs", "server"],
            "fetch": ["name"],
            "update": ["name"],
            "delete": ["name"]
        }
        super().__init__("sockets", validations=self.v, sockets=socket)

    def socket_create(self, socket_object):
        """
        socket_object:
        """
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
        """
        socket_name: 
        """
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
        """
        socket_object:
        """
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

                def service_connection(key, mask, sel):
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
                            # return False
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
                                if srv.get("handler", None):
                                    srv.get("handler")(
                                        key, mask, socket_object)
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
        """
        socket_object:
        messages:
        """
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
        """
        socket_object:
        messages
        """
        sobject = self.fetch(socket_object.get("name"))
        if not sobject:
            sobject = self.socket_create(socket_object)
        connections = sobject.get("numbers", 1)
        server_addr = (sobject.get("host"), sobject.get("port"))
        sel = selectors.DefaultSelector()
        blocking = sobject.get("blocking", False)
        if connections == 0:
            raise ValueError
        elif connections < 2:
            # if s:
            #     # s = self.fetch(socket_object.get("name"))
            #     # srv = s.get("server")
            #     # srv.connect(server_addr)
            #     # srv.sendall(b"Hello, world from client")
            #     # data = srv.recv(1024)
            #     # print("Received ", str(data))
            #     s.get("handler")(messages, s)
            #     try:
            #         s.get("server").close()
            #     except Exception:
            #         pass
            sobject.get("handler")(messages, sobject)
            try:
                sobject.get("server").close()
            except Exception:
                pass
        else:
            o = sobject
            o["selectors"] = sel
            self.socket_multi_server_connect(o, messages)

    def socket_close(self, socket_name):
        """
        socket_object:
        """
        try:
            s = self.fetch(socket_name)
            s["server"].close()
            return self.update(s)
        except Exception as e:
            return e

    def socket_delete(self, socket_object):
        """
        socket_object
        """
        try:
            return self.delete(socket_object.get("name"))
        except Exception as e:
            raise e

    def send(self, socket_object, message):
        """
        socket_object:
        message
        """
        return socket_object.send(str(message).encode())

    def receive(self, socket_object):
        """
        socket_object
        """
        msg = socket_object.recv(1024).decode()
        return ast.literal_eval(msg)


class EPubSubBase(UtilsBase, PubSubsInterface):
    """
    EPubSubBase
    """
    type = "epubsub"
    # agent options: application, publisher, server, subscriber
    # TODO: Implement threading/processing
    # application (in application events, simple app event architecture)
    # publisher, server, subscriber (in network system application events, clientagent-server architecture)
    agent = "application"

    def __init__(self, validations={}, pubsubs={}, types="epubsub", agent="application"):
        """
        validations={}
        pubsubs={}
        types="epubsub"
        agent="application"
        """
        self.v = ["name", "handler", "queue", "maxsize",
                  "queue_type", "batch_interval", "processing_flag", "events", "workflow_kwargs"]
        self.ev = ["name", "pubsub_name",
                   "publishers", "subscribers", "handler"]
        self.type = types
        self.agent = agent
        super().__init__("pubsubs", validations={
            "add": self.v, "create": self.v, "update": self.v, "delete": ["name"]}, pubsubs=pubsubs)
        # self.__schedular()

    def __process(self, name):
        """
        name: 
        """
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
        """
        No Input
        """
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
        """
        task:
        handler:
        """
        r = handler(task)
        if r:
            return True
        return False

    def __publish_handler(self, message_object):
        """
        message_object: 
        """
        o = self.fetch(message_object.get("queue_name"))
        h = o.get("handler")
        if not h:
            def h(message_object): return print(
                "Message Object ", message_object)
        e = o.get("events").get(message_object.get("event_name"))
        if e and e.get("listening"):
            try:
                r = []
                # Get Handler
                srv_hdlr = e.get("handler", None)
                # Invoke Handler
                if srv_hdlr:
                    print("Trying PubSub Main Handler Run: ", srv_hdlr.__name__)
                    r1 = self.__handler(message_object, srv_hdlr)
                    # Get all subscriber handlers
                    if not r1:
                        print("Return Error R1")
                    r.append(r1)
                srv_pb = e.get("publishers").get(
                    message_object.get("publisher"))
                if srv_pb:
                    srv_pbh = srv_pb.get("handler", None)
                    # Invoke Publisher
                    if srv_pbh:
                        print("Trying PubSub Publisher Handler Run: ",
                              srv_pbh.__name__)
                        r2 = self.__handler(message_object, srv_pbh)
                        if not r2:
                            print("Return Error R2")
                        r.append(r2)
                sbs = e.get("subscribers")
                if sbs:
                    r3 = []
                    for sb in sbs:
                        # Get individual handler
                        srv_sb_hdlr = sbs[sb].get("subscriber", h)
                        # Invoke all handlers
                        print("Trying PubSub Subscriber Handler Run: ",
                              srv_sb_hdlr.__name__)
                        tmpres = self.__handler(message_object, srv_sb_hdlr)
                        r3.append(tmpres)
                    r.append(r3)
                return r
            except Exception as e:
                return e
        return False

    def __receive_handler(self, message_object):
        """

        """
        pass

    def pubsub_create(self, config):
        """

        """
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
        """

        """
        return self.delete(pubsub_name)

    def queue_create(self, config):
        """

        """
        # "name", "queue", "maxsize", "queue_type"
        qConfig = copy.copy(config)
        tmpQ = QueuesBase()
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
        """
        event_object: name, publishers, subscribers
        """
        e = self.fetch(pubsub_name)
        e["events"].update(dict([
            [
                event_object.get("name"), {
                    "name": event_object.get("name"),
                    "listening": event_object.get("listening", False),
                    "publishers": event_object.get("publishers", {}),
                    "subscribers": event_object.get("subscribers", {})
                }
            ]
        ]))
        return self.update(e)

    def listen(self, pubsub_name, event_name):
        """

        """
        e = self.fetch(pubsub_name)
        e["events"].get(event_name).update({"listening": True})
        return self.update(e)

    def stop(self, pubsub_name, event_name):
        """

        """
        e = self.fetch(pubsub_name)
        e["events"].get(event_name).update({"listening": False})
        return self.update(e)

    def unregister_event(self, pubsub_name, event_object):
        """

        """
        try:
            p = self.fetch(pubsub_name)
            del p["events"][event_object.get("name")]
            return self.update(p)
        except Exception as e:
            pass
        return False

    def unregister_publisher(self, pubsub_name, publisher_object):
        """

        """
        try:
            p = self.fetch(pubsub_name)
            del p["events"][publisher_object.get(
                "event_name")]["publishers"][publisher_object.get("name")]
            return self.update(p)
        except Exception as e:
            print("Exception during Publisher unregister ", e)
        return False

    def unregister_subscriber(self, pubsub_name, subscriber_object):
        """

        """
        try:
            p = self.fetch(pubsub_name)
            del p["events"][subscriber_object.get(
                "event_name")]["subscribers"][subscriber_object.get("name")]
            return self.update(p)
        except Exception as e:
            pass
        return False

    def send(self, message_object):
        """

        """
        # message_object: queue_name, event_name, publisher_name, message
        # Events (Publisher-Subscriber, WebHooks) Mode:
        #       publisher, server[forsubscribers]
        # TODO: Consider send for subscriber for Client-Server (Server-Agent) Mode or (Subscriber having feedback) or (Subscriber app in Dual) Mode
        return self.__publish_handler(message_object)

    def receive(self, message_object):
        """

        """
        # message_object: queue_name, event_name, publisher_name, message
        # server[forpublishers], subscribers
        # TODO: Consider receive for Client-Server (Server-Agent) or (Publisher having feedback) or (Publisher app in Dual) Mode
        return self.__receive_handler(message_object)


class IPubSubBase(EPubSubBase):

    type = "ipubsub"
    # agent options: application, publisher, server, subscriber
    # TODO: Implement threading/processing
    # application (in application events, simple app event architecture)
    # publisher, server, subscriber (in network system application events, clientagent-server architecture)
    agent = "server"

    def __init__(self, validations={}, pubsubs={}, types="ipubsub", agent="server", socketsbase=SocketsBase):
        """
        validations: "add", "fetch", "create", "update", "delete" \n
        pubsubs: {"name" : "name", "handler", "queue", "maxsize", "queue_type", "batch_interval", "processing_flag", "events", "workflow_kwargs"} \n
        types: ipubsub (Options: ipubsub, epubsub) \n
        agent: server (Options: publisher, server, subscriber) \n
        socketsbase: SocketsBase (class)
        """
        self.v = ["name", "handler", "queue", "maxsize",
                  "queue_type", "batch_interval", "processing_flag", "events", "workflow_kwargs"]
        self.ev = ["name", "pubsub_name",
                   "publishers", "subscribers", "handlers"]
        self.type = types
        self.agent = agent
        # Object Structure: Publishers, Subscribers, PubSubServer
        self.server = socketsbase()
        super().__init__("pubsubs", validations={
            "add": self.v,
            "create": self.v,
            "update": self.v,
            "delete": ["name"]
        }, pubsubs=pubsubs, types=types, agent=agent)
        # self.__schedular()

    def __process(self, name):
        """
        name: name
        """
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
        """
        No Input
        """
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
        """
        task: "task" object
        handler: Function
        """
        r = handler(task)
        if r:
            return True
        return False

    def __publish_handler(self, message_object):
        """
        message_object: 
        """
        o = self.fetch(message_object.get("queue_name"))
        h = o.get("handler", None)
        if not h:
            def h(message_object): return print(
                "Message Object ", message_object)
        e = o.get("events").get(message_object.get("event_name"))
        if e and e.get("listening"):
            try:
                r = []
                # Get Handler
                srv_hdlr = e.get("handler", None)
                # Invoke Main Handler
                if srv_hdlr:
                    print("Trying PubSub Main Handler Run: ", srv_hdlr.__name__)
                    r1 = self.__handler(message_object, srv_hdlr)
                    if not r1:
                        print("Return Error R1")
                    r.append(r1)
                srv_pb = e.get("publishers").get(
                    message_object.get("publisher"))
                if srv_pb:
                    srv_pbh = srv_pb.get("handler", None)
                    # Invoke Publisher Handler
                    if srv_pbh:
                        print("Trying PubSub Publisher Handler Run: ",
                              srv_pbh.__name__)
                        r2 = self.__handler(message_object, srv_pbh)
                        if not r2:
                            print("Return Error R2")
                        r.append(r2)
                # Get all Subscriber Handlers
                sbs = e.get("subscribers")
                if sbs:
                    r3 = []
                    for sb in sbs:
                        # Get Individual Handler
                        srv_sb_hdlr = sbs[sb].get("subscriber", h)
                        # Invoke all Subscribers Handlers
                        print("Trying PubSub Subscriber Handler Run: ",
                              srv_sb_hdlr.__name__)
                        tmpres = self.__handler(message_object, srv_sb_hdlr)
                        r3.append(tmpres)
                    r.append(r3)
                return r
            except Exception as e:
                return e
        return False

    def __receive_handler(self, message_object):
        """
        message_object: 
        """
        pass

    def pubsub_create(self, config):
        """
        config: "name", "handler", "queue", "maxsize", "queue_type", "processing_flag", "batch_interval", "events"
        """
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

        s = self.server.create(
            dict([[config.get("name"), {
                "publishers": config.get("publishers", {}),
                "server": config.get("server", {}),
                "subscribers": config.get("subscribers", {})
            }]])
        )

        if u and s:
            o["queue"] = u
            if self.validate_object(o, self.validate_create):
                return self.create(o)
        return u and s

    def pubsub_delete(self, pubsub_name):
        """
        pubsub_name: name
        """
        p = self.delete(pubsub_name)
        s = False
        if p:
            s = self.server.delete(pubsub_name)
        return p and s

    def queue_create(self, config):
        """
        config: "name", "queue", "maxsize", "queue_type"
        """
        qConfig = copy.copy(config)
        tmpQ = QueuesBase()
        qConfig["queue"] = tmpQ.new(qConfig)
        qs = tmpQ.create(qConfig)
        if qs:
            return tmpQ
        return False

    def queue_delete(self, pubsub_name):
        """
        pubsub_name: name
        """
        o = self.fetch(pubsub_name)
        o["queue"] = None
        return self.update(o)

    def register_publisher(self, pubsub_name, publisher_object, publisher_server={}):
        """
        pubsub_name: name
        publisher_object: name, event_name, publisher (function)
        publisher_server: type(socket_object)
        """
        try:
            p = self.fetch(pubsub_name)
            p["events"][publisher_object.get("event_name")]["publishers"].update(dict([
                [publisher_object.get("name"), publisher_object]
            ]))

            s = self.server.fetch(pubsub_name)
            if not s and publisher_server:
                u = self.server.create(publisher_server)
                if not u:
                    raise TypeError
                s = self.server.fetch(pubsub_name)

            spb_object = {
                "action": "register_publisher",
                "message_object": copy.copy(publisher_object),
                "source": s
            }

            if self.agent == "publisher" or self.agent == "subscriber":
                # if send event to server
                # if not registered, then register
                sh = s.socket_connect({
                    "name": s.get("name")
                }, str(spb_object))
            elif self.agent == "server":
                # if send event to publisher and subscribers, if present
                # if not registered, then register
                spb = s.get("publishers").get(publisher_object.get("name"))
                if spb:
                    sh = spb.socket_connect({
                        "name": s.get("name")
                    }, str(spb_object))
            else:
                pass
            if p:
                return self.update(p)
            return False
        except Exception as e:
            return e

    def register_subscriber(self, pubsub_name, subscriber_object, subscriber_socket={}):
        """
        pubsub_name: name
        subscriber_object: name, event_name, subscriber (function)
        subscriber_socket: type(socket_object)
        """
        try:
            sc = self.fetch(pubsub_name)
            sc["events"][subscriber_object.get("event_name")]["subscribers"].update(dict([
                [subscriber_object.get("name"), subscriber_object]
            ]))
            s = self.server.fetch(pubsub_name)
            if not s and subscriber_socket:
                u = self.server.create(subscriber_socket)
                if not u:
                    raise TypeError
                s = self.server.fetch(pubsub_name)

            ssb_object = {
                "action": "register_subscriber",
                "message_object": copy.copy(subscriber_socket),
                "source": s
            }

            if self.agent == "publisher" or self.agent == "subscriber":
                # if send event to server
                # if not registered, then register
                sh = s.socket_connect({
                    "name": s.get("name")
                }, str(ssb_object))
            elif self.agent == "server":
                # if send event to publisher and subscribers, if present
                # if not registered, then register
                ssb = s.get("subscribers").get(subscriber_socket.get("name"))
                if ssb:
                    sh = ssb.socket_connect({
                        "name": s.get("name")
                    }, str(ssb_object))
            else:
                pass
            if sc:
                return self.update(sc)
            return False
        except Exception as e:
            return e

    def register_event(self, pubsub_name, event_object, event_socket={}):
        """
        pubsub_name: name
        event_object: name, listening, publishers [type(publisher_object)], subscribers [type(subscriber_object)]
        event_socket: type(socket_object)
        """
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
        s = self.server.fetch(pubsub_name)
        if not s and event_socket:
            u = self.server.create(event_socket)
            if not u:
                raise TypeError
            s = self.server.fetch(pubsub_name)

        se_object = {
            "action": "register_event",
            "message_object": copy.copy(event_socket),
            "source": s
        }

        if self.agent == "publisher" or self.agent == "subscriber":
            # if send event to server
            # if not registered, then register
            sh = s.socket_connect({
                "name": s.get("name")
            }, str(se_object))
        elif self.agent == "server":
            # if send event to publisher and subscribers, if present
            # if not registered, then register
            spb = s.get("publishers")
            if spb:
                sh = []
                for t in spb:
                    sh.append(spb.get(t.get("name")).socket_connect({
                        "name": t.get("name")
                    }, str(se_object)))
            ssb = s.get("subscribers")
            if ssb:
                sh = []
                for t in ssb:
                    sh.append(ssb.get(t.get("name")).socket_connect({
                        "name": t.get("name")
                    }, str(se_object)))
        else:
            pass

        if e:
            return self.update(e)
        return False

    def listen(self, pubsub_name, event_name):
        """
        pubsub_name:
        event_name: 
        """
        e = self.fetch(pubsub_name)
        e["events"].get(event_name).update({"listening": True})
        s = self.server.fetch(pubsub_name)
        se_object = {
            "action": "listen",
            "message_object": {"pubsub_name": pubsub_name, "event_name": event_name},
            "source": s
        }
        sh = s.socket_connect({
            "name": s.get("name")
        }, str(se_object))
        if e and sh:
            return self.update(e)
        return False

    def stop(self, pubsub_name, event_name):
        """
        pubsub_name:
        event_name: 
        """
        e = self.fetch(pubsub_name)
        e["events"].get(event_name).update({"listening": False})
        s = self.server.fetch(pubsub_name)
        se_object = {
            "action": "stop",
            "message_object": {"pubsub_name": pubsub_name, "event_name": event_name},
            "source": s
        }
        sh = s.socket_connect({
            "name": s.get("name")
        }, str(se_object))
        if e and sh:
            return self.update(e)
        return False

    def unregister_event(self, pubsub_name, event_object):
        """
        pubsub_name:
        event_object: 
        """
        try:
            p = self.fetch(pubsub_name)
            s = self.server.fetch(pubsub_name)
            se_object = {
                "action": "register_event",
                "message_object": {"pubsub_name": pubsub_name, "event_name": event_object.get("name")},
                "source": s
            }

            if self.agent == "publisher" or self.agent == "subscriber":
                # if send event to server
                # if not registered, then register
                sh = s.socket_connect({
                    "name": s.get("name")
                }, str(se_object))
            elif self.agent == "server":
                # if send event to publisher and subscribers, if present
                # if not registered, then register
                spb = s.get("publishers")
                if spb:
                    sh = []
                    for t in spb:
                        sh.append(spb.get(t.get("name")).socket_connect({
                            "name": t.get("name")
                        }, str(se_object)))
                ssb = s.get("subscribers")
                if ssb:
                    sh = []
                    for t in ssb:
                        sh.append(ssb.get(t.get("name")).socket_connect({
                            "name": t.get("name")
                        }, str(se_object)))
            else:
                pass
            del p["events"][event_object.get("name")]
            if p:
                return self.update(p)
            return False
        except Exception as e:
            return e

    def unregister_publisher(self, pubsub_name, publisher_object):
        """
        pubsub_name:
        publisher_object: 
        """
        try:
            p = self.fetch(pubsub_name)
            s = self.server.fetch(pubsub_name)
            spb_object = {
                "action": "register_publisher",
                "message_object": {"pubsub_name": pubsub_name, "event_name": publisher_object.get("name")},
                "source": s
            }

            if self.agent == "publisher" or self.agent == "subscriber":
                # if send event to server
                # if not registered, then register
                sh = s.socket_connect({
                    "name": s.get("name")
                }, str(spb_object))
            elif self.agent == "server":
                # if send event to publisher and subscribers, if present
                # if not registered, then register
                spb = s.get("publishers").get(publisher_object.get("name"))
                if spb:
                    sh = spb.socket_connect({
                        "name": s.get("name")
                    }, str(spb_object))
            else:
                pass
            del p["events"][publisher_object.get(
                "event_name")]["publishers"][publisher_object.get("name")]
            if p:
                return self.update(p)
            return False
        except Exception as e:
            print("Exception during Publisher unregister ", e)
        return False

    def unregister_subscriber(self, pubsub_name, subscriber_object):
        """
        pubsub_name:
        subscriber_object: 
        """
        try:
            p = self.fetch(pubsub_name)
            s = self.server.fetch(pubsub_name)
            ssb_object = {
                "action": "register_subscriber",
                "message_object": {"pubsub_name": pubsub_name, "event_name": subscriber_object.get("name")},
                "source": s
            }

            if self.agent == "publisher" or self.agent == "subscriber":
                # if send event to server
                # if not registered, then register
                sh = s.socket_connect({
                    "name": s.get("name")
                }, str(ssb_object))
            elif self.agent == "server":
                # if send event to publisher and subscribers, if present
                # if not registered, then register
                ssb = s.get("subscribers").get(subscriber_object.get("name"))
                if ssb:
                    sh = ssb.socket_connect({
                        "name": s.get("name")
                    }, str(ssb_object))
            else:
                pass
            del p["events"][subscriber_object.get(
                "event_name")]["subscribers"][subscriber_object.get("name")]
            if p:
                return self.update(p)
            return False
        except Exception as e:
            return e

    def send(self, message_object):
        """
        message_object: 
        """
        # message_object: queue_name, event_name, publisher_name, message
        # Events (Publisher-Subscriber, WebHooks) Mode:
        #       publisher, server[forsubscribers]
        # TODO: Consider send for subscriber for Client-Server (Server-Agent) Mode or (Subscriber having feedback) or (Subscriber app in Dual) Mode
        return self.__publish_handler(message_object)

    def receive(self, message_object):
        """
        message_object: 
        """
        # message_object: queue_name, event_name, publisher_name, message
        # server[forpublishers], subscribers
        # TODO: Consider receive for Client-Server (Server-Agent) or (Publisher having feedback) or (Publisher app in Dual) Mode
        return self.__receive_handler(message_object)

    def __multilistener_server(self, config):
        """
        config: 
        """
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
        """
        config: 
        """
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
        """
        config: 
        """
        return self.__multilistener_server(config)

    def server_socket(self, config):
        """
        config: 
        """
        return self.__multilistener_server(config)


class ActionsBase(UtilsBase):

    def __init__(self, action={}):
        """

        """
        super().__init__("actions", actions=action)


class HooksBase(UtilsBase, HooksInterface):

    server = None

    def __init__(self, validations={}, hooks={}, socketsbase=SocketsBase):
        """

        """
        self.v = validations
        super().__init__("hooks", validations=self.v, hooks=hooks)
        self.server = socketsbase()

    def hook_state(self, config):
        """

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def service_run(self, config):
        """

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def service_stop(self, config):
        """

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def register_hook(self, config):
        """

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def register_receiver(self, config):
        """

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def send(self, config):
        """

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass

    def receive(self, config):
        """

        """
        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        pass


class WebhooksBase(UtilsBase):

    def __init__(self, action={}):
        """

        """
        super().__init__("actions", actions=action)


class SSHBase(CommandsBase, SSHInterface):

    server = None

    def __init__(self, validations={}, pubsub={}, socketsbase=SocketsBase):
        """

        """
        self.v = validations
        super().__init__("pubsubs", validations=self.v, pubsubs=pubsub)
        self.server = socketsbase()

    def connect(self, options):
        """

        """
        pass

    def execute(self, options):
        """

        """
        pass

    def close(self, options):
        """

        """
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
    Socket = SocketsBase()


if __name__ == "__main__":

    config = {"name": "test", "maxsize": 10,
              "queue_type": "queue", "queue": None}
    queue = QueuesBase()
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
    event = EventsBase()

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

    pb = EPubSubBase()
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

    action = ActionsBase()


if __name__ == "__main__":

    hook = HooksBase(socketsbase=SocketsBase)


if __name__ == "__main__":

    webhook = WebhooksBase(socketsbase=SocketsBase)


if __name__ == "__main__":

    ssh = SSHBase()


__all__ = [
    "SharedBase", "ClosureBase", "UtilsBase",
    "TimerBase", "FileReaderBase", "CSVBase",
    "LogBase", "CommandsBase", "PicklesBase",
    "ConcurencyBase", "QueuesBase", "EventsBase",
    "ActionsBase", "SocketsBase", "HooksBase",
    "WebhooksBase", "EPubSubBase", "IPubSubBase",
    "SSHBase"
]


# 1, 3, 5, (26)
