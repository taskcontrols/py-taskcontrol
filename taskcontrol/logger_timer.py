# Logger and timer Base

import logging
import time


class TimerBase():

    def __init__(self):
        pass
    
    def time(self):
        pass
    
    def log(self, file):
        pass


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

