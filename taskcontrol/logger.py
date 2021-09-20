# Logger and timer Base

import logging
from .sharedbase import ClosureBase, UtilsBase
from .interfaces import LogBase


class Logger(LogBase, ClosureBase, UtilsBase):

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


if __name__ == "__main__":
    l = Logger("Test", {})


__all__ = ["Logger"]
