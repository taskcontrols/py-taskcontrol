

class LoggerBase():

    def __init__(self, name):
        import logging
        self.logger = logging.Logger(name)
        # self.format = None
        # self.handler = None
        # del implementation fn
        self.delt = lambda x: x
        # delete implementation fn
        self.delete = lambda x: x

    def create(self):
        pass

    def log(self, level, message):
        pass

    def __del__(self):
        # self.delt(1)
        pass

    def __delete__(self, instance):
        # self.logger = None
        # self.format = None
        # self.handler = None

        # self.delete(1)
        pass
