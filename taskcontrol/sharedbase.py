# SHARED BASE

import time
import logging
from .interfaces import TimeBase, LogsBase, CommandBase, ObjectModificationBase


class ClosureBase():
    def class_closure(self, **kwargs):
        closure_val = kwargs

        def getter(key, value=None):
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

        def setter(key, value=None, inst=None):
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

        def deleter(key, value=None):
            if type(value) == str:
                if value != None:
                    closure_val[key].pop(value)
                else:
                    raise TypeError("Problem with " + key +
                                    " Value deleting " + value)
                return True
            elif type(value) == int:
                if value == 1:
                    for v in value:
                        closure_val[key].pop(v)
                return True
            return False

        def log(config):
            pass

        def authenticate(config):
            pass

        def is_authenticated(config):
            pass

        def logout(config):
            pass

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

    def validate_object(self, val_object, values=[]):
        keys = val_object.keys()
        if len(keys) == len(values):
            if type(values) == list:
                for k in values:
                    if k in keys:
                        return True
                    else:
                        return False
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
        return False

    def create(self, config):
        if "workflow_kwargs" not in config:
            config["workflow_kwargs"] = {}
        if "shared" not in config["workflow_kwargs"]:
            config["workflow_kwargs"]["shared"] = False
        try:
            if self.validate_object(config, self.validate_add):
                return self.setter(self.object_name, config, self)[0]
            return False
        except Exception as e:
            raise e

    def fetch(self, name):
        try:
            return self.getter(self.object_name, name)[0]
        except Exception as e:
            raise e

    def update(self, config):
        try:
            o = self.getter(self.object_name, config.get("name"))[0]
            for k, v in config:
                if o.get(k) and (not k == "name"):
                    o[k] = v
            return self.setter(self.object_name, o, self)
        except Exception as e:
            raise e

    def delete(self, name):
        try:
            return self.deleter(self.object_name, name)
        except Exception as e:
            raise e


class TimerBase(TimeBase, ClosureBase, UtilsBase):

    def __init__(self, options, timers={}):
        super()

        if not options and type(options) != dict:
            raise TypeError("Options not provided")

        self.getter, self.setter, self.deleter = self.class_closure(
            timers=timers)

    def time(self, options):

        # options object expected
        # {"name":"name", "logger": "", "format": ""}

        logger = options.get("logger")
        t = self.getter("timers", options.get("name"))

        if len(t) > 0:
            timer = t[0].perf_counter()
        else:
            raise TypeError(
                "Wrong timer name provided. No such timer or multiple names matched")

        if not timer:
            raise ValueError("Did not find timer")
        if logger:
            logger.log(timer)
        return timer


class LogBase(LogsBase, ClosureBase, UtilsBase):

    def __init__(self, name, config):

        self.getter, self.setter, self.deleter = self.class_closure(loggers={})

        # self.setter("loggers", config, self)
        # self.format = None
        # implement handlers and LoggerAdapters
        # self.handler = None
        # _del implementation fn (get from config)
        self._del = lambda x: x

        # delete implementation fn (get from config)
        self.delete = lambda x: x

    def create_logger(self, config):

        # Config object expected
        # { "name":"name", "logger":logger, "level": "debug", "format": "",
        #   "handlers": {"handler": "", "value": ""}, "handlers": [{"handler": "", "value": ""}] }

        logger = self.getter("loggers", config.get("name"))

        # Use config here
        # config contains network info if logging needed to network
        if len(logger) > 1:
            raise ValueError(
                "Number of logger items ({0}) incorrect. Check the logger registeration".format(len(logger)))
        elif len(logger) == 1:
            log = logger[0]
        else:
            log = logging.getLogger(config.get("name"))[0]

        if config.get("handlers") and type(config.get("handlers")) == list:
            for i in config.get("handlers"):
                # {"handler": "FileHandler", "value": None}
                h = getattr(logging, config.get(i["handler"]))(
                    config.get(i["value"]))
                h.setLevel(getattr(logging, config.get("level")))
                log.addHandler(h)
        elif config.get("handlers") and type(config.get("handlers")) == dict:
            h = getattr(logging, config.get("handler"))(config.get("value"))
            h.setLevel(getattr(logging, config.get("level")))
            log.addHandler(h)
        else:
            raise TypeError("Config object handler key error")

        log.setFormatter(log.Formatter(config.get("format")))
        config["logger"] = log
        self.setter("loggers", config, self)

    def delete_logger(self, options):

        # options object expected
        # {"key":"name", "value": ""}

        self.deleter(options.get("key"), options.get("value"))

    def log(self, options):
        # TODO: Concurrency can be added
        # https://docs.python.org/3/howto/logging-cookbook.html

        # options object expected
        # {"name":"name", "level": "debug", "message": ""}

        logger = self.getter("loggers", options.get("name"))
        if (not len(logger) == 0 or not len(logger) > 1) and logger:
            log = logger[0]
        else:
            raise ValueError(
                "Logger items ({0}) incorrect. Check logger".format(len(logger)))

        level = options.get("level")
        message = options.get("message")

        try:
            if level == "debug" and log:
                log.debug(message)
            if level == "info" and log:
                log.info(message)
            if level == "info" and log:
                log.warning(message)
            if level == "error" and log:
                log.error(message)
            if level == "critical" and log:
                log.critical(message)
            return True
        except Exception as e:
            log.raise_error(e, level, message)
            return False


class CommandsBase(CommandBase, ClosureBase, UtilsBase):

    def __init__(self, options, commands={}):
        self.getter, self.setter, self.deleter = self.class_closure(
            commands=commands)

    def create(self, options):
        pass

    def execute(self, options):
        pass

    def close(self, options):
        pass

    def delete(self, options):
        pass


if __name__ == "__main__":
    c = ClosureBase("Test", {})


if __name__ == "__main__":
    s = SharedBase("Test", {})


if __name__ == "__main__":
    t = TimerBase({}, {})


if __name__ == "__main__":
    l = LogBase({}, {})


if __name__ == "__main__":
    c = CommandsBase({}, {})


__all__ = [
    "SharedBase", "ClosureBase",
    "UtilsBase", "TimerBase",
    "LogBase", "CommandsBase"
]
