# Logger and timer Base

import logging
import time
from .sharedbase import ClosureBase
# TODO: Refactor getters and setters and make code simpler


class TimerBase(ClosureBase):

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
            raise TypeError("Wrong timer name provided. No such timer or multiple names matched")
        if not t:
            raise ValueError("Did not find timer")
        if logger:
            logger.log(t)
        return t


# TODO: Refactor getters and setters and make code simpler

class LoggerBase(ClosureBase):

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
        # logger.setLevel(config.get("level"))
        # logger.setLevel(config.get("level"))

    def log(self, logger_options):
        logger = self.getter("loggers", logger_options.get("name"))
        level = logger_options.get("level")
        message = logger_options.get("message")
        try:
            if level == "debug" and logger:
                logger.debug(message)
            if level == "info" and logger:
                logger.info(message)
            if level == "info" and logger:
                logger.warning(message)
            if level == "error" and logger:
                logger.error(message)
            if level == "critical" and logger:
                logger.critical(message)
            return True
        except Exception as e:
            logger.raise_error(e, level, message)
            return False
