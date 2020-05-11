
import logging

class LoggerBase():

    def __init__(self, name, config):
        self.create(name, config)
        # self.format = None
        # implement handlers and LoggerAdapters
        # self.handler = None
        # del implementation fn
        self.delt = lambda x: x
        # delete implementation fn
        self.delete = lambda x: x

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
        # self.logger.config.stopListening()
        # self.delt(1)
        pass

    def __delete__(self, instance):
        # self.logger = None
        # self.format = None
        # self.handler = None
        
        # self.delete(1)
        pass
