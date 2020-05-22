# Logger and timer Base

import logging
import time


class TimerBase():

    def __init__(self, options, timer=None):
        if not options and type(options) != dict:
            raise TypeError("Options not provided")

        if not timer:
            # do timer instantiation
            # get all function assignations
            timer = None
            self.get_timer, self.set_timer = self.timer_closure(options, timer)
        else:
            # get all function assignations
            self.get_timer, self.set_timer = self.timer_closure(options, timer)

    def timer_closure(self, options, timer):
        timers = {}

        def times():
            pass

        return times

    def time(self, options):
        logger = options.get("logger")
        timer = self.get_timer(options.get("name"))
        t = timer.perf_counter()
        if logger:
            logger.log(t)
        return t

class LoggerBase():

    def __init__(self, name, config):

        self.get_logger, self.set_logger = self.logger_closure()

        self.create(name, config)
        # self.format = None
        # implement handlers and LoggerAdapters
        # self.handler = None
        # del implementation fn (get from config)
        self.delt = lambda x: x
        # delete implementation fn (get from config)
        self.delete = lambda x: x

    def logger_closure(self):

        logger = []

        def get_logger(self):
            pass

        def set_logger(self):
            pass

        return {"get_logger": get_logger, "set_logger": set_logger}

    def create(self, name, config):

        self.logger = logging.Logger(name)
        # use config here
        # config contains network info if logging needed to network
        # self.logger.setLevel(logging.DEBUG)
        # self.logger.setLevel(logging.DEBUG)

    def log(self, level, message):

        if level == "debug":
            self.logger.debug(message)
        if level == "info":
            self.logger.info(message)
        if level == "info":
            self.logger.warning(message)
        if level == "error":
            self.logger.error(message)
        if level == "critical":
            self.logger.critical(message)

    def __del__(self):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")

        # self.logger.config.stopListening()
        # self.delt(1)
        pass

    def __delete__(self, instance):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")

        # self.logger = None
        # self.format = None
        # self.handler = None

        # self.delete(1)
        pass
