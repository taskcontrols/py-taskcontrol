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
from typing import Dict, List, Type
import threading
import multiprocessing
# from threading import Thread, Lock
# from multiprocessing import Process, Array, Value, Manager
from queue import Queue, LifoQueue, PriorityQueue, SimpleQueue
from taskcontrol.lib.interfaces import ObjectModificationInterface, SocketsInterface, HooksInterface, SSHInterface, FileReaderInterface, CSVReaderInterface
from taskcontrol.lib.interfaces import QueuesInterface, EventsInterface, PubSubsInterface, TimeInterface, LogsInterface, CommandsInterface, PicklesInterface


class ClosureBase():
    """
    `ClosureBase` class to create true privacy for closure_val dict object \n
    LIBRARY CORE: Do not modify \n
    Use for creating closures, if need for your app or use case. \n

    ##### Instance Methods
    @`class_closure()` -> `(@getter, @setter, @deleter)`
    """

    def class_closure(self, **kwargs):
        """
        `class_closure` Function to store needed objects private in instances in `truely private and immutable` object \n
        `LIBRARY CORE`: `do not modify` \n
        Use for creating closures, if need for your app or use case. Function invocation returns a `getter`, `setter`, and `deleter` tuple for the variable `closure_val` \n
        `kwargs`: type(dict) \n
        kwargs are of type dict that can be used for storing true immutable private values. \n
        They are modifiable only using `getter`, `setter`, and `deleter` functions returned by the `class_closure` function after invocation. \n
        """
        """
        private, immutable variable closure_val
        """
        closure_val = kwargs

        def getter(key, value=None):
            """
            Function `getter` gets the `value` (key name or list of key names) from the `key` dict object stored inside `closure_val` \n
            { `key` (str), `value` (str) or (list) or (int -> 1) } \n
            #### args definition: \n
            `key`: type(str) \n
            key is the key of the dict object you want to fetch from `closure_val`. Read details of fetch using `closure_val object structure` and `usage` details below. \n
            `value`: type(list) or type(str) or type(int -> 1) \n
            value is key of the dict object stored in `key` of `closure_val` \n
            #### closure_val object structure:
            `closure_val` = \n
            `{"keyone":{"value_one":{},"value_two":[]},"keytwo":{"value_one":1,"value_two":"myvalue"}}`
            #### usage:
            `getter(key="keyone", value=["value_one", "value_two"])` \n
            `getter(key="keyone", value="value_one")` \n
            `getter(key="keyone", value=1)` \n
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
            Function `setter` is used to set a dict value `value` to key named `key` in `closure_val` \n
            { `key` (str), `value` (str) or (list) or (int -> 1) } \n
            #### args definition: \n
            `key`: type(str) \n
            key is the key of the dict object you want to fetch from `closure_val`. Read details of fetch using `closure_val object structure` and `usage` details below. \n
            `value`: type(dict) \n
            value is key of the dict object stored in `key` of `closure_val` \n
            { name, **other_keys } \n
            `inst`: type(instance) \n
            inst is instance of your own `ClosureBase` extended class object used to stored the `key` and `value` in a private, immutable dict `closure_val` \n
            #### closure_val object structure:
            `closure_val` = \n
            `{"keyone":{"value_one":{},"value_two":[]},"keytwo":{"value_one":1,"value_two":"myvalue"}}`
            #### usage:
            `setter(key="keyone", value={"value_one":[], "value_two":10})` \n
            `setter(key="keyone", value={"value_one":"test","value_two":True})` \n
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
            Function `deleter` is used to delete the value or list of values (`value` argument) from the `key` dict stored in the `closure_val` (dict) \n
            { `key` (str), `value` (str) or (int -> 1) } \n
            #### args definition: \n
            `key`: type(str) \n
            key is the key of the dict object you want to fetch from `closure_val`. Read details of fetch using `closure_val object structure` and `usage` details below. \n
            `value`: type(dict) \n
            value is key of the dict object stored in `key` of `closure_val` \n
            #### closure_val object structure:
            `closure_val` = \n
            `{"keyone":{"value_one":{},"value_two":[]},"keytwo":{"value_one":1,"value_two":"myvalue"}}`
            #### usage:
            `deleter(key="keyone", value="value_one")` \n
            `deleter(key="keyone", value=1)` \n
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
    """
    SharedBase class is used to share a common instance across different objects across module. Follows a singleton pattern \n

    ##### Static Methods
    @`getInstance` \n
    Usage: \n
    `SharedBase.getInstance()`
    """
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


class RThreadBase(threading.Thread):
    """
    `RThreadBase`
    """

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, daemon=False, Verbose=None):
        threading.Thread.__init__(self, group=group, target=target,
                                  name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._return = None

    def run(self):
        """
        .run() function is used to store returns to fetch from a join implementation
        """
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        """
        .join() function can be used to get returns from a join implementation

        """
        threading.Thread.join(self, *args, timeout=-1)
        return self._return


class RProcessBase(multiprocessing.Process):
    """
    `RProcessBase`
    """
    # https://analyticsindiamag.com/run-python-code-in-parallel-using-multiprocessing/

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, daemon=False, Verbose=None):
        multiprocessing.Process.__init__(self, group=group, target=target,
                                         name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._return = None

    def run(self):
        """
        .run() function is used to store returns to fetch from a join implementation
        """
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        """
        .join() function can be used to get returns from a join implementation
        """
        multiprocessing.Process.join(self, *args, timeout=-1)
        return self._return


class ConcurencyBase():
    """
    `ConcurencyBase` allows working with different ways of working with concurrency \n

    ##### Instance Methods
    @staticmethod Futures: `ConcurencyBase.futures` [todo]
    @staticmethod Asyncio: `ConcurencyBase.asyncio` [todo]
    @staticmethod Thread: `ConcurencyBase.thread`
    @staticmethod Process: `ConcurencyBase.process`

    """
    @staticmethod
    def futures():
        """
        Description of thread
        asynchronous & 

        Args:

        """
        pass

    @staticmethod
    def asyncio():
        """
        Description of asyncio
        asynchronous & 

        Args:

        """
        pass

    @staticmethod
    def thread(group=None, target=None, name=None, args=(), kwargs={}, daemon=False, options={}):
        """
        Description of thread \n
        asynchronous & \n
        needs 'join': Value Options [True, False] \n

        { `name` (str), `group` (), `target` (function), `args` (list) or (tuple), `kwargs` (dict), `daemon` (bool), `options` (dict) } \n

        ##### process args and kwargs definitions 
        `name`: str \n
        [Default is None] \n
        `group`: \n
        [Default is None] \n
        `target`: type(function) \n
        `args`: list / tuple \n
        [Default is blank tuple () ] \n
        `kwargs`: dict \n
        [Default is blank dict {}] \n
        `daemon`: bool \n
        [Default is bool False] \n
        `options`: dict \n
        { `lock` (bool), `share_value` (str), `needs_return` (bool), `join` (bool), `terminate` (bool), `Verbose` () } \n

        """
        # https://analyticsindiamag.com/run-python-code-in-parallel-using-multiprocessing/
        if type(options) != dict:
            raise TypeError

        if options.get("lock"):
            lock = threading.Lock()
            arg = (*args,)
            kwarg = {**kwargs, "lock": lock}
        else:
            arg = (*args,)
            kwarg = {**kwargs}

        # share_value = options.get("share_value")
        if options.get("needs_return", True):
            T = RThreadBase
        else:
            T = threading.Thread

        worker = T(
            group=group, target=target,
            name=name, args=(*arg,),
            kwargs={**kwarg}, daemon=daemon
        )
        worker.setDaemon(daemon)
        worker.start()

        print("[BUG] Print needed bug from python interpretor or Windows Hacked. Checking .join ",
              options.get("join", True))
        if options.get("join", True):
            result = worker.join()
        return {"worker": worker, "result": result}

    @staticmethod
    def process(group=None, target=None, name=None, args=(), kwargs={}, daemon=False, options={}):
        """
        Description of process \n
        asynchronous &  \n
        needs 'join': Value Options [ True, False ] \n

        { `name` (str), `group` (), `target` (function), `args` (list) or (tuple), `kwargs` (dict), `daemon` (bool), `options` (dict) }` \n

        ##### process args and kwargs definitions 
        `name`: str \n
        [Default is None] \n
        `group`: \n
        [Default is None] \n
        `target`: type(function) \n
        `args`: list / tuple \n
        [Default is blank tuple () ] \n
        `kwargs`: dict \n
        [Default is blank dict {}] \n
        `daemon`: bool \n
        [Default is bool False] \n
        `options`: \n
        { `lock` (bool), `share_value` (str), `needs_return` (bool), `join` (bool), `terminate` (bool), `Verbose` () } \n

        """
        if type(options) != dict:
            raise TypeError

        # # Check need here. Create a common one outside by user
        # # Consider if you want to handle this (Negative currently)

        # # share_value, share_array, share_queue, share_pipe, share_lock, share_rlock,
        # # share_manager, share_pool, share_connection, share_event,
        # # share_semaphore, share_bounded_semaphore

        # share_value = options.get("share_value")
        # share_array = options.get("share_array")
        # worker = Process(
        #     group=group, target=target,
        #     name=name, args=(*args,),
        #     kwargs={**kwargs}, daemon=daemon
        # )

        if options.get("lock"):
            lock = threading.Lock()
            arg = (*args,)
            kwarg = {**kwargs, "lock": lock}
        else:
            arg = (*args,)
            kwarg = {**kwargs}

        # share_value = options.get("share_value")
        if options.get("needs_return", True):
            P = RProcessBase
        else:
            P = multiprocessing.Process

        worker = P(
            group=group, target=target,
            name=name, args=(*arg,),
            kwargs={**kwarg}, daemon=daemon
        )
        worker.daemon = daemon
        worker.start()

        result = {}
        if options.get("terminate", True):
            worker.terminate()
        else:
            result.update({"worker": worker})
        if options.get("join", True):
            res = worker.join()
            result.update({"result": res})
        return result

    @staticmethod
    def process_pool(function, args=(), kwargs={}, options={}):
        """
        Description of process_pool
        asynchronous and needs 'join':True or False
        https://stackoverflow.com/questions/8804830/python-multiprocessing-picklingerror-cant-pickle-type-function

        { `args` (list), `kwargs` (dict), `options` (dict) } \n

        ##### process_pool args and kwargs 

        `args`: type(list) \n
        [Default is empty tuple ()] \n
        `kwargs`: type(dict) \n
        [Default is empty dict {}] \n
        `options`: type(dict) \n
        { `processes` (int), `mode` (str) } \n
            -- `processes`: type(int) \n
            [Default is int 1]
            -- `mode`: type(dict) \n
            Value Options [ apply, apply_async, map, map_async, manager ] \n
            [Default is str apply]
        """
        if type(options) != dict:
            raise TypeError

        mode = options.get("mode", "apply")

        def init(l):
            global lock
            lock = l

        if options.get("lock"):
            lock = multiprocessing.Lock()
            pool = multiprocessing.Pool(processes=options.get(
                "processes", 1), initializer=init, initargs=(lock,))
        else:
            pool = multiprocessing.Pool(processes=options.get("processes", 1))

        callback = options.get("processes", lambda *args,
                               **kwargs: print("Callback run ", args, kwargs))
        error_callback = options.get(
            "processes", lambda *args, **kwargs: print("Error Callback run ", args, kwargs))

        # https://towardsdatascience.com/parallelism-with-python-part-1-196f0458ca14
        if mode == "apply":
            # apply(func[, args[, kwds]]) (This is implemented as apply_async( ... ).get())
            result = [pool.apply(function, args=a, kwds=kwargs)
                      for a in args]
        elif mode == "map":
            # map(func, iterable[, chunksize]) (This is implemented as map_async( ... ).get())
            result = [pool.map(
                function, iterable=args, chunksize=options.get("chunksize", 1)
            )]
        elif mode == "apply_async":
            # TODO: apply_async(func[, args[, kwds[, callback[, error_callback]]]])
            output = [pool.apply_async(
                function, args=[a], kwds=kwargs,
                callback=callback, error_callback=error_callback
            ) for a in args]
            result = [p.get() for p in output]
        elif mode == "map_async":
            # TODO: map_async(func, iterable[, chunksize[, callback[, error_callback]]])
            result = [pool.map_async(
                function, iterable=args,
                callback=callback, error_callback=error_callback
            ).get()]
        elif mode == "manager":
            # manager = multiprocessing.Manager()
            # res = manager.dict()
            result = []

        if options.get("join"):
            pool.close()
            pool.join()
        return result


class UtilsBase(ObjectModificationInterface):
    """
    `UtilsBase` class is used for extending most common logics around the taskcontrols library. \n

    ##### Instance Methods
    Provides a `validate_object` to validate an dictionary object to verify a specific list of keys
    @`validate_object` \n
    @`append_update_dict` \n
    Provides a `create`, `fetch`, `update`, and `delete` functions to modify private stored objects (implementation of ClosureBase) in the instance \n
    @`create` \n
    @`fetch` \n
    @`update` \n
    @`delete` \n

    ClosureBase Implemented (Not Inherited) Available Methods: \n
    Provides a `getter`, `setter`, and `delete` functions not due to inheritence due to the ClosureBase implementation within \n
    @`getter` \n
    @`setter` \n
    @`deleter` \n

    """

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

    @staticmethod
    def dictify_xml(r, root=True):
        """
        """
        if root:
            return {r.tag: dictify(r, False)}
        d = copy(r.attrib)
        if r.text:
            d["_text"] = r.text
        for x in r.findall("./*"):
            if x.tag not in d:
                d[x.tag] = []
            d[x.tag].append(dictify(x, False))
        return d

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

    @staticmethod
    def csv_to_json():
        """

        """
        # https://dzone.com/articles/full-stack-development-tutorial-sending-pandas-dat
        pass

    @staticmethod
    def csv_to_xml():
        """

        """
        # https://dzone.com/articles/using-python-pandas-for-log-analysis
        # https://pbpython.com/pdf-reports.html
        pass

    @staticmethod
    def string_to_json(string):
        """
        """
        return json.loads(string)

    @staticmethod
    def json_to_string(json):
        """
        """
        return str(json)

    @staticmethod
    def iterate(function, iterations):
        """
        `.iterate()` function can be used to iterate the same function n (`iterations`) number of times \n
        { `function` (function) or (str), `count` (int) } \n

        ##### Arguments
        `function`: type(function) \n
        The function name that is stored in the instance or the function that needs to be run \n

        `iterations`: type(str) \n
        Counts or iterations or frequency of repetition of a task

        """
        if not hasattr(function, '__call__'):
            raise TypeError
        try:
            r = []
            for i in range(iterations):
                r.append(function())
            return r
        except Exception as e:
            return False

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
        `.create` function helps create a key stored in the list of all objects \n
        { `config` (dict) }

        `config`: type(dict) \n
        { `name` (str), `workflow_kwargs` (dict), ...your object structure... }
        ##### config structure details below
        `name`: type(str) \n
        `workflow_kwargs`: type(dict) is optional key \n
        -- `shared`: type(bool) \n
        `any-other-keys-you-need-to-specify-and-store`: any other keys you need to specify and store \n

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
        `.fetch` function helps fetch a key stored in the list of all objects \n
        { `name` (str) } \n
        `name`: type(str) \n
        Name of the key to be fetched from the all the stored objects 
        """
        try:
            return self.getter(self.object_name, name)[0]
        except Exception as e:
            print("Fetch error ", e)
            return False

    def update(self, config):
        """
        `.update` function helps update a key stored in the list of all objects \n
        { `config` (dict) } \n

        `config`: type(dict) \n
        { `name` (str), `workflow_kwargs` (dict), ...your object structure... }
        ##### config structure details below
        `name`: type(str) \n

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
        `.delete` function helps deleting a key stored in the list of all objects \n
        { `name` (str) } \n
        `name`: type(str) \n
        Name of the key to be deleted from the all the stored objects 
        """
        try:
            return self.deleter(self.object_name, name)
        except Exception as e:
            print("Fetch error ", e)
            return False


class TimerBase(UtilsBase, TimeInterface):
    """
    `TimerBase` class is used for time execution captures of specific programing logic you need \n

    ##### Instance Methods
    @`timer_create`
    @`time`
    @`elapsed_time`
    @`curent_elapsed_time`
    @`reset`
    @`start`
    @`stop`
    """

    def __init__(self, timers={}):
        """
        Instantiation for timers in the instance \n
        `timers` objects in keys \n
        single timer object: { `name`, `_start_time`, `_elapsed_time`, `_accumulated` } \n

        """
        self.v = ["name", "_start_time", "_elapsed_time",
                  "_accumulated", "workflow_kwargs"]
        super().__init__("timers",
                         validations={"add": self.v, "fetch": self.v, "create": self.v,
                                      "update": self.v, "delete": ["name"]},
                         timers=timers)

    def timer_create(self, config):
        """
        `.timer_create()` function creates and stores an timer config into the `TimerBase` instance \n
        { `config` (dict) }
        { `name` (str), `_start_time` (float), `_elapsed_time` (float), `_accumulated` (float), `workflow_kwargs` (dict): { `shared` (bool) } }

        ##### Argument details
        `name`: type(str) \n
        `_start_time`: type(int) optional \n
        `_elapsed_time`: type(int) optional \n
        `_accumulated`: type(int) optional \n

        """
        if not config.get("name"):
            raise TypeError("Name argument has to be provided")

        config.update({
            "_start_time": config.get("_start_time", 0.0),
            "_elapsed_time": config.get("_elapsed_time", 0.0),
            "_accumulated": config.get("_accumulated", 0.0)
        })
        u = self.create(config)
        if u:
            return True
        return False

    def time(self):
        """
        `.time()` function returns an pure python timer `time.perf_counter` instance \n
        """
        return time.perf_counter()

    def elapsed_time(self, name):
        """
        `.elapsed_time()` function returns the stored elapsed time of the timer name instance requested \n

        { `name` (str) }
        `name`: type(str) \n
        Name of the timer instance's last elapsed time to return stored after a stop method last used for the name of the instance stored. \n
        Will return 0 if the timer instance has been started and has not been stopped atleast once. \n
        """
        t = self.fetch(name)
        if not t:
            raise TypeError("Timer not present")
        else:
            return t.get("_elapsed_time")

    def curent_elapsed_time(self, name):
        """
        `.curent_elapsed_time()` function returns the elapsed time of the timer name requested \n

        { `name` (str) }
        `name`: type(str) \n
        Name of the timer instance's current elapsed time to return from the instance stored in the instance \n
        """
        t = self.fetch(name)
        if not t:
            raise ValueError("Timer not started")
        return time.perf_counter() - t.get("_start_time", 0.0)

    def reset(self, name):
        """
        `.reset()` function resets the timer \n

        { `name` (str) }
        `name`: type(str) \n
        Name of the timer instance to reset that is stored in the instance \n
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
        `.start()` function starts the timer \n

        { `name` (str) }
        `name`: type(str) \n
        Name of the timer instance to start that is stored in the instance \n
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
        `.stop()` function stops the timer \n

        { `name` (str) }
        `name`: type(str) \n
        Name of the timer instance to stop that is stored in the instance \n
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
    """
    `FileReaderBase` class can be used to read, write, append to a file. \n
    FileReaderBase class can also be used to insert, update, append, delete rows in a file and to search rows in a file that match a regex pattern. \n
    [todo] row methods to be modified \n

    ##### Instance Methods
    @`exists` \n
    @`is_file` \n
    @`file_store` \n
    @`file_read` \n
    @`file_write` \n
    @`file_append` \n
    @`row_insert` \n
    @`row_append` \n
    @`row_update` \n
    @`row_delete` \n
    @`row_search` \n

    """

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

    def file_store(self, config):
        try:
            return self.create(config)
        except:
            return False

    def file_read(self, name, way, index=None):
        """

        """
        config = self.fetch(name)
        with open(config.get("file"), mode="r", encoding=config.get("encoding")) as obj:
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
                obj.close()
                return False
            except Exception as e:
                return False

    def file_write(self, name, items, way):
        """

        """
        config = self.fetch(name)
        with open(config.get("file"), mode="w+", encoding=config.get("encoding")) as obj:
            try:
                if way == "write":
                    obj.write(items)
                elif way == "writeline":
                    obj.writeline(items)
                elif way == "writelines":
                    obj.writelines(items)
                obj.close()
                return True
            except Exception as e:
                return False

    def file_append(self, name, items, way):
        """

        """
        config = self.fetch(name)
        with open(config.get("file"), mode="a", encoding=config.get("encoding")) as obj:
            try:
                if way == "write":
                    obj.write(items)
                elif way == "writeline":
                    obj.writeline(items)
                elif way == "writelines":
                    obj.writelines(items)
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
    """
    `CSVReaderBase` class can be used to read, write, append to a file. \n
    CSVReaderBase class can also be used to insert, update, append, delete rows in a file and to search rows in a file that match a regex pattern. \n
    [todo] row methods to be modified \n

    ##### Instance Methods
    @`exists` \n
    @`is_file` \n
    @`file_store` \n
    @`file_read` \n
    @`file_write` \n
    @`file_append` \n
    @`row_insert` \n
    @`row_append` \n
    @`row_update` \n
    @`row_delete` \n
    @`row_search` \n

    """

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
    """
    `LogBase` class is used to store logger instances and log data to file using predefined loggers \n

    ##### Instance Methods:
    @`logger_create`
    @`log`
    """

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
        `.logger_create` is use to create and store a logger instance in the LogBase instance \n

        `config`: type(dict) \n
        `{ "name":"name",
           "handlers": {"handler": {"type": "file", "file": "filename.log"}, "format": "", "level": logging.INFO},
           "handlers": [{"handler": {"type": "file", "file": "filename.log"}, "format": "", "level": logging.DEBUG}]
        }`
        """

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
        `.log` is used to make a log

        `options`: type(dict) \n
        { `name` (str), `level` (str), `message` (str)} \n

        ##### Argument specifications: \n
        Value Options for `level`: [ critical, error, info, warning, debug ] [Default is str info] \n

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
    """
    `PicklesBase` class is used for managing and working with Pickle files \n

    ##### Instance Methods:
    @`row_insert`
    @`row_append`
    @`row_update`
    @`row_delete`
    @`search`
    @`connection`
    """
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
    """
    `CommandsBase` class allows for running commands you specify programmatically. \n
    All ways of `subprocess.call`, `subprocess.popen`, `subprocess.run`, `os.popen` [todo] are intended to be supported. \n

    ##### Instance Methods:
    @`exists`
    @`path`
    @`execute`

    ##### Static Instance Methods (UtilsBase Inherited)
    @`iterate` \n

    """

    def __init__(self, object_name="commands", validations={}, commands={}):
        """
        { `object_name` (str), `validations` (dict), `commands` (dict) } \n
        ##### Definition details \n
        `object_name`: type(str) \n
        instance name of the object [Default: "commands"] \n
        `validations`: type(dict) \n
        { `create` (list), `add` (list), `fetch` (list), `update` (list), `delete` (list) } \n
        `commands`: type(dict) \n
        command object: { `name` (str), `command` (str), `options`(dict -> options:arguments) } \n
        """
        self.v = ["name", "command", "options", "workflow_kwargs"]
        super().__init__(object_name, validations={
            "add": self.v, "create": self.v, "update": self.v, "delete": ["name"]}, commands=commands)

    def exists(self, command):
        """
        `command`: type(str) \n
        command [Executable or command that needs to be checked for presence]
        """
        return shutil.which(command) is not None

    def path(self, command):
        """
        `command`: type(str) \n
        command [Executable or command that needs to be path mapped]
        """
        return shutil.which(command)

    def execute(self, command, mode="subprocess_popen", stdin_mode=False, options={}):
        """
        `TODO`: ReWrite for inclusion of all arguments \n
        #### `.execute` ARGUMENTS \n
        `command`: type(str) or type(list) \n
        Any command or command with arguments and options as a list \n
        `stdin_mode`: type(bool) \n
        Get input value for the shell \n
        Value Options: [ True, False ] [Default is bool False] \n
        `mode`: type(str) \n
        Value Options: [ subprocess_call [TODO - Unfunctional], subprocess_popen, subprocess_run, os_popen, os_system ] [Default is str subprocess_popen] \n
        `options`: type(dict) \n
        Details of the same in the section `option Object keys details` below. \n
        `options` object that are needed for `subprocess` or `os` functions \n


        #### `option` object keys Details: \n

        for `subprocess_call` [TODO - Unfunctional] which calls the `subprocess.call()` function: \n
        { `args`:command argument and/or options, `stdin, stdout, stderr, bufsize, universal_newlines, executable, shell, cwd, env,
        preexec_fn, close_fds, startupinfo, creationflags, restore_signals, start_new_session, pass_fds, timeout`
        } \n

        * for `subprocess_popen` which calls the `subprocess.Popen()` function: \n
        { `args`:command argument and/or options, `stdin, stdout, stderr, universal_newlines, bufsize, executable, close_fds, shell, cwd, env, start_new_session, text` }
            -- `POSIX` ONLY \n
        { `preexec_fn, restore_signals, group, extra_groups, pass_fds, umask, user` }
            -- `WINDOWS` ONLY \n
        { `startupinfo`, `creationflags` } \n\n

        * for `subprocess_run` which calls the `subprocess.run()` function: \n
        { `args`:command argument and/or options, `stdin, stdout, stderr, universal_newlines, input, bufsize, executable, preexec_fn, close_fds,
        shell, cwd, env, startupinfo, creationflags, restore_signals, start_new_session,
        pass_fds, capture_output, check, encoding, errors, text, timeout`
        } \n\n

        * for `os_popen` which calls the `os.popen()` function: \n
        { `args` (str): command argument and/or options, `mode` (str), `buffsize` (int) } \n

        * for `os_system` which calls the `os.system()` function: \n
        { `command` (str), `args` (str): command argument and/or options } \n

        """
        # https://www.cyberciti.biz/faq/python-run-external-command-and-get-output/
        try:
            if self.exists(command):
                if mode == "subprocess_call" or mode == "subprocess_popen" or mode == "subprocess_run":
                    stdin = options.get("stdin", subprocess.PIPE)
                    stdout = options.get("stdout", subprocess.PIPE)
                    stderr = options.get("stderr", subprocess.PIPE)
                    universal_newlines = options.get(
                        "universal_newlines", True)
                    bufsize = options.get("bufsize", 0)
                    preexec_fn = options.get("preexec_fn", None)
                    close_fds = options.get("close_fds", False)
                    shell = options.get("shell", True)
                    cwd = options.get("cwd", None)
                    env = options.get("env", None)
                    startupinfo = options.get("startupinfo", None)
                    creationflags = options.get("creationflags", 0)
                    restore_signals = options.get("restore_signals", True)
                    start_new_session = options.get("start_new_session", True)
                    pass_fds = options.get("pass_fds", None)
                    timeout = options.get("timeout", 60)
                    executable = options.get("executable", None)
                    text = options.get("text", True)
                    group = options.get("group", "")
                    extra_groups = options.get("extra_groups", "")
                    user = options.get("user", "")
                    umask = options.get("umask", "")
                    capture_output = options.get("capture_output", True)
                    check = options.get("check", False)
                    encoding = options.get("encoding", None)
                    errors = options.get("errors", None)
                    cargs = options.get("args", [])
                    stdin_input = options.get("stdin_input", None)
                    input = options.get("input", None)
                    result = None

                if mode == "subprocess_call":
                    proc = subprocess.call(
                        [command, *cargs],
                        stdin=stdin, stdout=stdout, stderr=stderr,
                        bufsize=bufsize, universal_newlines=universal_newlines,
                        executable=executable, shell=shell,
                        cwd=cwd, env=env

                        # preexec_fn=preexec_fn, close_fds=close_fds,
                        # startupinfo=startupinfo, creationflags=creationflags,
                        # restore_signals=restore_signals, start_new_session=start_new_session,
                        # pass_fds=pass_fds, timeout=timeout
                    )
                    if stdin_mode:
                        pass
                elif mode == "subprocess_popen":
                    # a = {
                    #     "stdin": stdin, "stdout": stdout, "stderr": stderr,
                    #     "universal_newlines": universal_newlines, "bufsize": bufsize,
                    #     "executable": executable, "close_fds": close_fds, "shell": shell,
                    #     "cwd": cwd, "env": env, "start_new_session": start_new_session, "text": text
                    # }
                    # l = ("unneeded_key")
                    # # # POSIX ONLY
                    # # preexec_fn=preexec_fn, restore_signals=restore_signals,
                    # # # group=group, extra_groups=extra_groups,
                    # # pass_fds=pass_fds, umask=umask,
                    # # # user=user
                    # # # WINDOWS ONLY
                    # # startupinfo=startupinfo, creationflags=creationflags
                    # list(map(a.__delitem__, filter(a.__contains__, l)))

                    proc = subprocess.Popen(
                        [command, *cargs],
                        stdin=stdin, stdout=stdout, stderr=stderr,
                        universal_newlines=universal_newlines, bufsize=bufsize,
                        executable=executable, close_fds=close_fds, shell=shell,
                        cwd=cwd, env=env, start_new_session=start_new_session, text=text
                    )
                    if stdin_mode:
                        result = proc.communicate(input=stdin_input)[0]
                        proc.stdin.close()
                    if options.get("wait"):
                        proc.wait()
                elif mode == "subprocess_run":
                    a = {
                        "stdin": stdin, "stdout": stdout, "stderr": stderr,
                        "universal_newlines": universal_newlines,
                        "input": input, "bufsize": bufsize, "executable": executable,
                        "preexec_fn": preexec_fn, "close_fds": close_fds, "shell": shell,
                        "cwd": cwd, "env": env, "startupinfo": startupinfo,
                        "creationflags": creationflags, "restore_signals": restore_signals,
                        "start_new_session": start_new_session, "pass_fds": pass_fds,
                        "capture_output": capture_output, "check": check, "encoding": encoding,
                        "errors": errors, "text": text, "timeout": timeout
                    }
                    if not input and stdin_input:
                        rm = ["input", "executable", "preexec_fn", "close_fds", "shell", "cwd", "env", "startupinfo",
                              "creationflags", "restore_signals", "start_new_session", "pass_fds",
                              "capture_output", "check", "encoding", "errors", "text"]
                        {a.pop(r) for r in rm}
                        proc = subprocess.run([command, *cargs], **a)
                        # # Following has Error in implementation
                        # # TODO: Following does not send input from the PIPE - .communicate and stdin.write does not work
                        # # # # - Following does not capture the Output from the PIPE
                        # # # # - Have to use input instead of std_input to send and get the stdin and stdout
                        # # # #
                        if stdin_mode:
                            # result = proc.communicate(input=stdin_input)
                            # proc.stdin.write(stdin_input)
                            # proc.stdin.close()
                            pass
                    elif input and not stdin_input:
                        rm = ["stdin", "executable", "preexec_fn", "close_fds", "shell", "cwd", "env", "startupinfo",
                              "creationflags", "restore_signals", "start_new_session", "pass_fds",
                              "capture_output", "check", "encoding", "errors", "text", "timeout"]
                        {a.pop(r) for r in rm}
                        proc = subprocess.run([command, *cargs], **a)
                    else:
                        raise Exception("input and stdin_input not provided")
                elif mode == "os_popen":
                    proc = os.popen(" ".join([command, *options.get("args", [])]), mode=options.get(
                        "mode", "r"), buffering=options.get("buffsize", 1))
                elif mode == "os_system":
                    proc = os.system(
                        " ".join([command, *options.get("args", [])]))
                else:
                    raise Exception("Raising Exception due to wrong option")
                return proc, result
        except Exception as e:
            print("Raising Exception due to error ", e)
            return False

    def shell(self, file, target="", options={}):
        """
        file: bash shell `.sh`, powershell `.ps1` `.psm` `.ps1xml`, bat `.bat` file
        `target`: local, remote
        `options`: { dir, remote { ip, port, protocol } }

        """
        # https://docs.microsoft.com/en-us/powershell/scripting/windows-powershell/ise/how-to-write-and-run-scripts-in-the-windows-powershell-ise?view=powershell-7.2
        try:
            if target == "local":
                return self.execute(
                    file,
                    mode="subprocess_call",
                    stdin_mode=options.get("stdin_mode", False),
                    options=options.get("options")
                )
            elif target == "remote":
                pass
            else:
                raise Exception
        except Exception as E:
            return False


class QueuesBase(UtilsBase, QueuesInterface):
    """
    `QueuesBase` allows you to create a list of queues to work with \n
    All ways of `list`, `Queue`, `LifoQueue`, `PriorityQueue`, `SimpleQueue` are supported \n

    ##### Instance Methods:
    @`new`
    @`add`
    @`get`
    """
    tmp = {}

    def __init__(self, queues={}):
        """
        `queues`: type(dict) \n
        { `name` (str), `maxsize` (int), `queue_type` (str), `queue` (`queue` instance) } \n
        """
        self.v = ["name", "maxsize", "queue_type", "queue", "workflow_kwargs"]
        super().__init__("queues", validations={
            "add": self.v, "create": self.v, "update": self.v, "delete": ["name"]}, queues=queues)

    def new(self, config):
        """
        Create or define a new `queue` using `.new` \n
        `config`: type(dict) following queues dict \n
        { `name` (str), `maxsize` (int), `queue_type` (str), `queue` (`queue` instance) } \n
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
        Add an `queue` from `.add` \n 
        { `name` (str), `item` (list), `index` (int), `nowait` (bool) } \n
        `name`: type(str) \n
        name of the queue to be added \n
        `item`: type() \n
        item to be added \n
        `index`: type(int) \n 
        index of the item to be added
        [Default is int `0`] \n
        `nowait`: type(bool) \n
        whether there should be any wait (python lang queue/deque definition of nowait) \n
        Value Options: [ True, False ] [Default is bool `True`] \n
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
        Get an `queue` from the instance using `.get` \n
        { `name` (str), `index` (int), `nowait` (bool) } \n
        `name`: type(str) \n
        name of the queue to fetch \n
        `index`: type(int) \n
        index of the item to fetch [Default is  int `0`] \n
        `nowait`: type(bool) \n
        on the fly redefinition of whether there should be any wait (python lang queue/deque definition of nowait) \n
        Value Options: [ True, False ] [Default is bool `True`] \n
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
    """
    `EventsBase` class can be used to work with events \n
    [TODO] Implementation of Asynchronous behaviour using concurrency class \n

    ##### Instance Methods:
    @`event_register`
    @`event_unregister`
    @`listener_register`
    @`on`
    @`listener_unregister`
    @`get_state`
    @`set_state`
    @`listen`
    @`stop`
    @`send`
    @`emit`

    """

    def __init__(self, event={}):
        """

        """
        self.v = ["name", "event", "handler", "listening",
                  "listeners", "workflow_kwargs"]
        super().__init__("events", validations={
            "add": self.v, "create": self.v, "update": self.v, "delete": ["name"]}, events=event)

    def event_register(self, event_object):
        """
        Create or define an event using `.event_register` \n
        `event_object`: type(dict) \n
        { `name` (str), `event` (function), `listening` (bool), `listeners` (dict) } \n

        ##### event_object Keyword Arguments Details
        `event`: type(func) \n
        Function to execute when event is invoked \n
        `listening`: type(bool) \n
        If function needs to be listening to events \n
        `listeners`: type(dict) \n
        Dictionary of listener objects \n
        TODO: This is blocking event object. Needs to allow non-blocking and non-blocking multithreaded / multiprocess
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
        Create or define an event using `.event_unregister` \n
        { `event_name` (str) } \n

        ##### Arguments Details
        `event_name`: type(str) \n
        """
        print("Deleting event: ", event_name)
        return self.delete(event_name)

    def listener_register(self, listener_object):
        """
        Create or define an event using `.listener_register` \n
        { `listener_object` (dict) } \n

        ##### Arguments Details
        `listener_object`: type(dict) \n
        { `name` (str), `event_name` (str), `listener` (bool) } \n

        ##### listener_object Keyword Arguments
        `name`: type(str) \n
        `event_name`: type(str) \n
        `listener`: type(bool) \n
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
        Create or define an event using `.on` \n
        { `event_name` (str), `name` (str), `handler` (function) } \n

        ##### Arguments Details
        `event_name`: type(str) \n
        `name`: type(str) \n
        `handler`: type(function) \n

        """
        return self.listener_register({"name": name, "event_name": event_name, "listener": handler})

    def listener_unregister(self, listener_object):
        """
        Listen to an event using `.listener_unregister` \n
        { `listener_object` (dict) } \n

        ##### Arguments Details
        `listener_object`: type(dict) \n
        { `name` (str), `event_name` (str) } \n

        ##### listener_object Keyword Argument Details
        `name`: type(str) \n
        `event_name`: type(str) \n 
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
        Get an event state using `.get_state` \n
        { `event_name` (str) } \n

        ##### Arguments Details
        `event_name`: type(str) \n

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
        Set an event state using `.set_state` \n
        { `event_name` (str), `state` (bool) } \n

        ##### Arguments Details
        `event_name` type(str): \n
        `state` type(bool): \n
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
        Listen an event using `.listen` \n
        { `event_name` (str) } \n

        ##### Arguments Details
        `event_name` type(str): \n
        """
        return self.set_state(event_name, True)

    def stop(self, event_name):
        """
        Stop Listening to an event using `.stop` \n
        { `event_name` (str) } \n

        ##### Arguments Details
        `event_name` type(str): \n
        """
        return self.set_state(event_name, False)

    def send(self, message_object):
        """
        Send an event using `.send` \n
        { `message_object` (dict) } \n

        ##### Arguments Details
        `message_object` type(dict): \n
        { `event_name` (str), `message` (any object) } \n

        ##### `message_object` Keyword Arguments Details
        `event_name`: type(str) \n
        `message`: type(any object) \n

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
        Emit an event using `.emit` \n
        { `event_name` (str), `message` (any object) } \n

        ##### Arguments Details
        `event_name`: type(str): \n

        `message` type(any object): \n

        """
        return self.send({"event_name": event_name, "message": message})


class SchedularBase(UtilsBase):
    """
    `SchedularBase` class can be used to work with schedulars

    ##### Private Instance Methods
    @`__runschedular` \n
    @`__schedular` \n

    ##### Instance Methods
    @`manual` \n
    @`start` \n
    @`stop` \n

    ##### Static Instance Methods (UtilsBase Inherited)
    @`iterate` \n

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

    def __runschedular(self, name, func, interval, *args, **kwargs):
        """
        `__runschedular` function \n
        { `name` (str), `func` (function), `interval` (int) }

        `name`: type(str) \n

        `func`: type(function) \n

        `interval`: type(int) \n

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
        `__schedular` function \n
        { `sch` (dict) } \n

        """
        if sch.get("interval") == "repeated" and sch.get("active") == True:
            sobj = self.__runschedular(
                sch.get("name"), sch.get("function"), sch.get("time"),
                args=[*sch.get("args", [])],
                kwargs={**sch.get("kwargs", {})}
            )
        if sch.get("interval") == "iterate" and sch.get("active") == True:
            sobj = self.iterate(
                sch.get("function"), sch.get("time"),
                args=[*sch.get("args", [])],
                kwargs={**sch.get("kwargs", {})}
            )
        elif sch.get("interval") == "single" and sch.get("active") == True:
            sobj = sch.get("function")(
                args=[*sch.get("args", [])],
                kwargs={**sch.get("kwargs", {})}
            )
        if sobj:
            return sobj
        return False

    def manual(self, name):
        """
        `.manual` function \n
        { `name` (str) } \n
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
        `.start` function \n
        { `name` (str) } \n

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
        `.stop` function \n
        { `name` (str) } \n

        """
        sc = self.fetch(name)
        if sc:
            sc.update({"active": False, "schedular": None})
            u = self.update(sc)
            if u:
                return True
        return False


class SocketsBase(UtilsBase, SocketsInterface):
    """
    `SocketsBase` class is used to work with sockets \n
    SocketsBase works with any type of protocol supported by Python sockets \n

    ##### Instance Methods
    @`socket_create`
    @`socket_listen`
    @`socket_accept`
    @`socket_multi_server_connect`
    @`socket_connect`
    @`socket_close`
    @`socket_delete`
    @`send`
    @`receive`

    """

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
        if self.validate_object(socket_object, values=self.v.get("create")):
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
                def accept_wrapper(sock, self):
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

                def service_connection(key, mask, sel, self):
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
                                accept_wrapper(key.fileobj, self)
                            else:
                                if srv.get("handler", None):
                                    srv.get("handler")(
                                        key, mask, socket_object, self)
                                else:
                                    service_connection(key, mask, sel, self)
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

        def service_connection(key, mask, self):
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
                        service_connection(key, mask, self)
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
            sobject.get("handler")(messages, sobject, self)
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
    `EPubSubBase` class to work with a socket/ network based `Publish-Server-Subscriber` event architecture within an application \n
    EPubSubBase runs a queue in all `Publisher`, `Server`, and `Subscriber` event object instances \n

    ##### Private Instance Methods
    @`__process`
    @`__schedular`
    @`__handler`
    @`__publish_handler`
    @`__receive_handler`

    ##### Instance Methods
    @`pubsub_create`
    @`pubsub_delete`
    @`queue_create`
    @`queue_delete`
    @`register_publisher`
    @`unregister_publisher`
    @`register_subscriber`
    @`unregister_subscriber`
    @`register_event`
    @`unregister_event`
    @`listen`
    @`stop`
    @`send`
    @`receive`

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
            "add": self.v, "fetch": self.v, "create": self.v, "update": self.v, "delete": ["name"]
        }, pubsubs=pubsubs)
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
        e = o.get("events").get(message_object.get("event_name"))
        if e and e.get("listening"):
            try:
                r = []
                srv_h = o.get("handler")
                if srv_h:
                    print("Trying PubSub Handler Run: ", srv_h.__name__)
                    r0 = self.__handler(message_object, srv_h)
                    # Get all subscriber handlers
                    if not r0:
                        print("Return Error R0 ", srv_h.__name__)
                    r.append(r0)
                # Get Handler
                srv_hdlr = e.get("handler")
                # Invoke Handler
                if srv_hdlr:
                    print("Trying PubSub Main Handler Run: ", srv_hdlr.__name__)
                    r1 = self.__handler(message_object, srv_hdlr)
                    # Get all subscriber handlers
                    if not r1:
                        print("Return Error R1 ", srv_hdlr.__name__)
                    r.append(r1)
                srv_pb = e.get("publishers").get(
                    message_object.get("publisher"))
                if srv_pb:
                    srv_pbh = srv_pb.get("publisher", None)
                    # Invoke Publisher
                    if srv_pbh:
                        print("Trying PubSub Publisher Handler Run: ",
                              srv_pbh.__name__)
                        r2 = self.__handler(message_object, srv_pbh)
                        if not r2:
                            print("Return Error R2 ", srv_pbh.__name__)
                        r.append(r2)
                sbs = e.get("subscribers")
                if sbs:
                    r3 = []
                    for sb in sbs:
                        # Get individual handler
                        srv_sb_hdlr = sbs[sb].get("subscriber", None)
                        if srv_sb_hdlr:
                            # Invoke all handlers
                            print("Trying PubSub Subscriber Handler Run: ",
                                  srv_sb_hdlr.__name__)
                            tmpres = self.__handler(
                                message_object, srv_sb_hdlr)
                            if not tmpres:
                                print("Return Error tmpres ",
                                      srv_sb_hdlr.__name__)
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
                    "handler": event_object.get("handler", lambda x: True),
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
    """
    `IPubSubBase` class to work with a socket/ network based `Publish-Server-Subscriber` server architecture across servers \n
    IPubSubBase runs a queue in all `Publisher`, `Server`, and `Subscriber` sockets \n

    ##### Private Instance Methods
    @`__process`
    @`__schedular`
    @`__handler`
    @`__publish_handler`
    @`__receive_handler`

    ##### Instance Methods
    @`pubsub_create`
    @`pubsub_delete`
    @`queue_create`
    @`queue_delete`
    @`register_publisher`
    @`unregister_publisher`
    @`register_subscriber`
    @`unregister_subscriber`
    @`register_event`
    @`unregister_event`
    @`listen`
    @`stop`
    @`send`
    @`receive`
    @`publisher_socket`
    @`subscriber_socket`
    @`server_socket`

    """
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
        super().__init__(validations={
            "add": self.v,
            "fetch": self.v,
            "create": self.v,
            "update": self.v,
            "delete": ["name"]
        }, pubsubs=pubsubs, types=types, agent=agent)
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
        e = o.get("events").get(message_object.get("event_name"))
        if e and e.get("listening"):
            try:
                r = []
                srv_h = o.get("handler")
                if srv_h:
                    print("Trying PubSub Handler Run: ", srv_h.__name__)
                    r0 = self.__handler(message_object, srv_h)
                    # Get all subscriber handlers
                    if not r0:
                        print("Return Error R0 ", srv_h.__name__)
                    r.append(r0)
                # Get Handler
                srv_hdlr = e.get("handler")
                # Invoke Handler
                if srv_hdlr:
                    print("Trying PubSub Main Handler Run: ", srv_hdlr.__name__)
                    r1 = self.__handler(message_object, srv_hdlr)
                    # Get all subscriber handlers
                    if not r1:
                        print("Return Error R1 ", srv_hdlr.__name__)
                    r.append(r1)
                srv_pb = e.get("publishers").get(
                    message_object.get("publisher"))
                if srv_pb:
                    srv_pbh = srv_pb.get("publisher", None)
                    # Invoke Publisher
                    if srv_pbh:
                        print("Trying PubSub Publisher Handler Run: ",
                              srv_pbh.__name__)
                        r2 = self.__handler(message_object, srv_pbh)
                        if not r2:
                            print("Return Error R2 ", srv_pbh.__name__)
                        r.append(r2)
                sbs = e.get("subscribers")
                if sbs:
                    r3 = []
                    for sb in sbs:
                        # Get individual handler
                        srv_sb_hdlr = sbs[sb].get("subscriber", None)
                        if srv_sb_hdlr:
                            # Invoke all handlers
                            print("Trying PubSub Subscriber Handler Run: ",
                                  srv_sb_hdlr.__name__)
                            tmpres = self.__handler(
                                message_object, srv_sb_hdlr)
                            if not tmpres:
                                print("Return Error tmpres ",
                                      srv_sb_hdlr.__name__)
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
                    "handler": event_object.get("handler", lambda x: True),
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

        # def server_nonblocking_handler(key, mask, self):
        #     sock = key.fileobj
        #     data = key.data
        #     print("Sending data ", str(data))
        #     d = self.string_to_json(data)
        #     print("Sending data ", d, d.__name__)
        #
        # srvconfig = {"name": "test", "protocol": socket.AF_INET, "streammode": socket.SOCK_STREAM,
        #          "host": "127.0.0.1", "port": 9001, "numbers": 1, "handler": server_nonblocking_handler, "blocking": False}
        #
        # Socket = SocketsBase()
        # s = Socket.socket_create(srvconfig)
        # if s:
        #     # sr = Socket.socket_listen(srvconfig.get("name"))
        #     print("Server started ")
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
    """
    `ActionsBase` class to work with actions within the application \n

    ##### Instance Methods

    """

    def __init__(self, action={}):
        """

        """
        super().__init__("actions", actions=action)


class HooksBase(UtilsBase, HooksInterface):
    """
    `HooksBase` class [TODO] to work with hooks \n
    ##### Instance Methods

    """
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
    """
    `WebhooksBase` class [todo] for working with a webhooks server \n

    ##### Instance Methods

    """

    def __init__(self, action={}):
        """

        """
        super().__init__("actions", actions=action)


class SSHBase(CommandsBase, SSHInterface):
    """
    `SSHBase` class is used to work with `ssh`, `scp`. Needs `OpenSSH` installed \n

    ##### Instance Methods
    @`connect`
    @`execute`
    @`close`

    ##### Static Instance Methods (UtilsBase Inherited)
    @`iterate` \n

    """
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


__all__ = [
    "SharedBase", "ClosureBase", "UtilsBase",
    "TimerBase", "FileReaderBase", "CSVReaderBase",
    "LogBase", "CommandsBase", "PicklesBase",
    "ConcurencyBase", "QueuesBase", "EventsBase",
    "ActionsBase", "SocketsBase", "HooksBase",
    "WebhooksBase", "EPubSubBase", "IPubSubBase",
    "SSHBase"
]
