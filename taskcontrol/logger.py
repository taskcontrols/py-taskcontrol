# Logger and timer Base

import logging
from .sharedbase import ClosureBase
from .interfaces import LogBase
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

    def create_logger(self, config):

        # Config object expected
        # {"name":"name", "handlers": {"handler": "", "value": ""}, "format": ""}

        self.setter("loggers", config, self)
        logger = self.getter("loggers", config.get("name"))

        # Use config here
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

    def delete_logger(self, options):

        # options object expected
        # {"key":"name", "value": ""}

        self.deleter(options.get("key"), options.get("value"))

    def log(self, options):

        # options object expected
        # {"name":"name", "level": "debug", "message": ""}

        logger = self.getter("loggers", options.get("name"))
        level = options.get("level")
        message = options.get("message")

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
