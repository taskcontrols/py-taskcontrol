# SHARED BASE

# TODO: Refactor getters and setters and make code simpler

class SharedBase():

    __instance = None

    def __init__(self):
        """middleware_task_ Structure: name, function, args, kwargs, options"""
        """workflow_kwargs: name, task_instance, task_order, shared, args, kwargs, before, after, log"""
        self.get_shared_tasks, self.set_shared_tasks, self.delete_shared_tasks, self.get_shared_ctx, self.set_shared_ctx, self.get_shared_config, self.set_shared_config, self.get_shared_plugins, self.set_shared_plugins, self.get_shared_workflows, self.set_shared_workflows, self.disable_shared_workflows = self.shared_closure()
        if SharedBase.__instance != None:
            pass
        else:
            SharedBase.__instance = self

    def __new__(cls):

        if cls.__instance is None:
            cls.__instance = super(SharedBase, cls).__new__(cls)
        return cls.__instance

    # TODO: Refactor getters and setters and make code simpler
    def shared_closure(self):
        """middleware_task_ Structure: name, function, args, kwargs, options"""
        """workflow_kwargs: name, task_instance, task_order, shared, args, kwargs, before, after, log"""
        # Allow instance tasks
        tasks = {"taskname": {}}

        # Allow instance tasks
        # Consider persisting this to DB
        # DB Persistance for Pugins? Managed how?
        # TODO: Allow running tasks as ordered runs
        workflows = {
            "workflowname": {"tasks": [], "auth_exceptions": [], "disabled": True}
        }

        """ Results of task runs (shared) """
        # Access results from tasks, shared tasks during a task run
        ctx = {"result": []}

        """  """
        # TODO: Other features
        config = {}

        # TODO: Plugins features
        plugins = {"pluginname": {"taskname": {}}}

        def get_shared_workflows():

            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def set_shared_workflows():

            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def disable_shared_workflows():

            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def get_shared_tasks(task_=None):

            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            if isinstance(task_, str):
                if len(task_.split("shared:")) > 1:
                    task_ = task_.split("shared:")[1]
                return tasks.get(task_)
            elif task_ == 1 and type(task_) == int:
                return tasks
            else:
                return None

        def set_shared_tasks(task=None):

            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            if type(task) == dict:
                tasks.update(task)
                return True
            return False

        def delete_shared_tasks(task_=None):
            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            if type(task_) == str:
                if len(task_.split("shared:")) > 1:
                    task = task_.split("shared:")[1]
                else:
                    task = task_
            if task == 1 or task == "1":
                for t in tasks:
                    tasks.pop(t, None)
            if type(task) == str and task != "1":
                tasks.pop(task, None)
            if type(task) == list and len(task) > 0:
                for t in task:
                    if type(t) == str and t in tasks.keys():
                        tasks.pop(t, None)

        def get_shared_ctx():

            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def set_shared_ctx():

            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def get_shared_config():

            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def set_shared_config():

            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def get_shared_plugins():

            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        def set_shared_plugins():

            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")
            pass

        return (get_shared_tasks, set_shared_tasks, delete_shared_tasks, get_shared_ctx, set_shared_ctx, get_shared_config, set_shared_config, get_shared_plugins, set_shared_plugins, get_shared_workflows, set_shared_workflows, disable_shared_workflows)

    @staticmethod
    def getInstance():
        if not SharedBase.__instance:
            SharedBase()
        return SharedBase.__instance
