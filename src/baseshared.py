# # Project Workflow


class SharedBase():

    tasks = {
        "taskname": {}
    }

    plugins = {
        "pluginname": {
            "taskname": {}
        }
    }

    __instance = None

    def __init__(self):
        # Option 1:
        if SharedBase.__instance != None:
            # raise Exception("In case erring out is needed - This class is a singleton!")
            pass
        else:
            SharedBase.__instance = self

        # Option 3: This is okay due to implementation of __new__
        # pass

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SharedBase, cls).__new__(cls)
            # Note needed currently: Put any initialization code here
        return cls.__instance

    @staticmethod
    def getInstance():
        """ Static access method. """
        if not SharedBase.__instance:
            SharedBase()
        return SharedBase.__instance

