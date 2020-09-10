# Logger and timer Base

import logging
import time
from .sharedbase import ClosureBase
from .interfaces import TimeBase, LogBase
# TODO: Refactor getters and setters and make code simpler


class TimerBase(TimeBase, ClosureBase):

    def __init__(self, options, timers={}):
        super()

        if not options and type(options) != dict:
            raise TypeError("Options not provided")

        self.getter, self.setter, self.deleter = self.class_closure(
            timers=timers)

    def time(self, options):
        logger = options.get("logger")
        timer = self.getter("timers", options.get("name"))
        if len(timer) == 1:
            t = timer[0].perf_counter()
        else:
            raise TypeError(
                "Wrong timer name provided. No such timer or multiple names matched")
        if not t:
            raise ValueError("Did not find timer")
        if logger:
            logger.log(t)
        return t


# TODO: Refactor getters and setters and make code simpler

class LoggerBase(LogBase, ClosureBase):

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

    def create(self, config):
        self.setter("loggers", config, self)
        logger = self.getter("loggers", config.get("name"))

        # use config here
        # config contains network info if logging needed to network
        if len(logger) == 0:
            logger[0] = logging.getLogger(config.get("name"))
        log = logger[0]
        if config.get("handlers") and type(config.get("handlers")) == list:
            for i in config.get("handlers"):
                # {"handler": "FileHandler", "value": None}
                h = getattr(logging, config.get(
                    i["handler"])(config.get(i["value"])))
                h.setLevel(getattr(logging, config.get("level")))
                log.addHandler(h)

        log.setFormatter(log.Formatter(config.get("format")))
        self.setter(config.get("name"), log, self)

    def log(self, logger_options):
        logger = self.getter("loggers", logger_options.get("name"))
        level = logger_options.get("level")
        message = logger_options.get("message")

        try:
            if level == "debug" and logger:
                logger[0].debug(message)
            if level == "info" and logger:
                logger[0].info(message)
            if level == "info" and logger:
                logger[0].warning(message)
            if level == "error" and logger:
                logger[0].error(message)
            if level == "critical" and logger:
                logger[0].critical(message)
            return True
        except Exception as e:
            logger[0].raise_error(e, level, message)
            return False
