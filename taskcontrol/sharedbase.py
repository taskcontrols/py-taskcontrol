

class SharedBase():

    __instance = None

    def __init__(self):

        """middleware_task_ Structure: name, function, args, kwargs, options"""
        """workflow_kwargs: name, task_instance, task_order, shared, args, kwargs, before, after, log"""
        self.get_shared_tasks, self.set_shared_tasks, self.get_shared_ctx, self.set_shared_ctx, self.get_shared_config, self.set_shared_config, self.get_shared_plugins, self.set_shared_plugins = self.shared_closure()
        if SharedBase.__instance != None:
            pass
        else:
            SharedBase.__instance = self

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SharedBase, cls).__new__(cls)
        return cls.__instance

    def shared_closure(self):
        """middleware_task_ Structure: name, function, args, kwargs, options"""
        """workflow_kwargs: name, task_instance, task_order, shared, args, kwargs, before, after, log"""
        # Allow instance tasks
        tasks = {"taskname": {}}

        """ Results of task runs (shared) """
        # Access results from tasks, shared tasks during a task run
        ctx = {"result": []}

        """  """
        # TODO: Other features
        config = {}

        # TODO: Plugins features
        plugins = {"pluginname": {"taskname": {}}}

        def get_shared_tasks(task_=None):
            if isinstance(task_, str):
                if len(task_.split("shared:")) > 1:
                    task_ = task_.split("shared:")[1]
                return tasks.get(task_)
            elif task_ == 1 and type(task_) == int:
                return tasks
            else:
                return None

        def set_shared_tasks(task=None):
            if type(task) == dict:
                tasks.update(task)
                return True
            return False

        def get_shared_ctx():
            pass

        def set_shared_ctx():
            pass

        def get_shared_config():
            pass

        def set_shared_config():
            pass

        def get_shared_plugins():
            pass

        def set_shared_plugins():
            pass

        return (get_shared_tasks, set_shared_tasks, get_shared_ctx, set_shared_ctx, get_shared_config, set_shared_config, get_shared_plugins, set_shared_plugins)

    @staticmethod
    def getInstance():
        if not SharedBase.__instance:
            SharedBase()
        return SharedBase.__instance
