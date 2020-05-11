

class LoggerBase():

    def __init__(self, name):
        import logging
        self.logger = logging.Logger(name)
        # self.format = None
        # self.handler = None

    def create(self):
        pass
        
    def log(self, level, message):
        pass

    def remove(self):
        pass
