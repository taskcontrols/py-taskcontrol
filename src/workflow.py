# # Project Workflow
# Goal: Manage Workflow and related middlewares
# TODO: Add Simple scalable plugin system


class SharedTasks():

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
        if SharedTasks.__instance != None:
            # raise Exception("In case erring out is needed - This class is a singleton!")
            pass
        else:
            SharedTasks.__instance = self

        # Option 3: This is okay due to implementation of __new__
        # pass

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SharedTasks, cls).__new__(cls)
            # Note needed currently: Put any initialization code here
        return cls.__instance

    @staticmethod
    def getInstance():
        """ Static access method. """
        if not SharedTasks.__instance:
            SharedTasks()
        return SharedTasks.__instance


class WorkflowBase():

    tasks = {
        "taskname": {}
    }

    plugins = {
        "pluginname": {
            "taskname": {}
        }
    }

    def __init__(self):
        self.shared_tasks = SharedTasks.getInstance()
        # print("Workflow Creating the global object", self.globals)

    def __run_middleware(self, fn, error_obj, log_, *args, **kwargs):

        try:
            if log_:
                print("Workflow running middleware function: ", fn.__name__)
            return True, fn(*args, **kwargs)

        except Exception as e:
            if log_:
                print("Running error for middleware")

            if not hasattr(error_obj, "error"):
                error_obj["error"] = "exit"

            err_enum_ = error_obj.get("error")
            err_next_value_obj_ = error_obj.get("error_next_value")

            if err_enum_ == "next":
                return 'next', (e, err_next_value_obj_)
            elif err_enum_ == "error_handler":
                if not hasattr(error_obj, "error_handler"):
                    return "error_handler", (e, err_next_value_obj_)
                return 'error_handler', error_obj.get("error_handler")(e, err_next_value_obj_)
            elif err_enum_ == "exit":
                raise Exception("error_obj['error'] exit: Error during middleware: ",
                                fn.__name__, str(e))
            else:
                raise Exception(
                    "Error during middleware: flow[options[error]] value error")

    def __get_md_args(self, f, action, log_):

        if action and isinstance(action, dict):
            a, kwa, err_obj = [], {}, {}
            if "args" in action and isinstance(action.get("args"), list):
                a = action.get("args")
            if "kwargs" in action and isinstance(action.get("kwargs"), dict):
                kwa = action.get("kwargs")
            if "options" in action and isinstance(action.get("options"), dict):
                err_obj = action.get("options")

        # TODO: Do clean args here
        return err_obj, a, kwa

    def __setup_run_middleware(self, task_, md_action, log_):

        #       Iterate through before/after for each task_
        #           trigger before functions with next or handle error
        #           with error_handler, next or exit based on options

        actions = task_.get("workflow_kwargs").get(md_action)
        log_ = task_.get("workflow_kwargs").get("log")

        if actions and isinstance(actions, list):
            for action in actions:
                fn = action.get("function")
                err_obj, a, kwa = self.__get_md_args(fn, action, log_)
                self.__run_middleware(fn, err_obj, log_, *a, **kwa)
        elif actions and isinstance(actions, dict):
            err_obj, a, kwa = self.__get_md_args(
                actions.get("function"), actions, log_)
            self.__run_middleware(actions.get("function"),
                                  err_obj, log_, *a, **kwa)

    def clean_args(self, fn, workflow_args, workflow_kwargs, function_args, function_kwargs):

        tpl = fn.__code__.co_varnames
        k_fn_kwa = function_kwargs.keys()
        l_tpl, l_fn_a, l_k_fn_kwa = len(tpl), len(function_args), len(k_fn_kwa)

        if (l_tpl == l_fn_a + l_k_fn_kwa):
            for k in k_fn_kwa:
                if not tpl.index(k) >= l_fn_a:
                    return False
            return True
        return False

    def get_tasks(self, task_=None, shared=False):

        # get shared if shared is requested
        if shared and task_ and isinstance(task_, str):
            return self.shared_tasks.tasks.get(task_)
        elif not shared and task_ and isinstance(task_, str):
            return self.tasks.get(task_)
        return self.tasks

    def set_task(self, fn, function_args, function_kwargs, workflow_args, workflow_kwargs):

        workflow_name = workflow_kwargs.get("name")
        print("Workflow task name to add: ", workflow_name)

        shared = workflow_kwargs.get("shared")

        # set in global or local
        if shared == True:
            if workflow_name not in self.shared_tasks.tasks.keys():
                self.shared_tasks.tasks[workflow_name] = {}
            if not isinstance(self.shared_tasks.tasks[workflow_name], dict):
                self.shared_tasks.tasks.update({workflow_name: {}})

        elif not shared == True:
            if workflow_name not in self.tasks.keys():
                self.tasks[workflow_name] = {}
            if not isinstance(self.tasks[workflow_name], dict):
                self.tasks.update({workflow_name: {}})

        self.tasks[workflow_name].update({
            "task_order": workflow_kwargs.get("task_order"),
            "workflow_args": workflow_args, "workflow_kwargs": workflow_kwargs,
            "function_args": function_args, "function_kwargs": function_kwargs,
            "before": workflow_kwargs.get("before"),
            "after": workflow_kwargs.get("after"),
            "function": fn,
            "log": workflow_kwargs.get("log")
        })

        print("Workflow set_task: Adding Task: ", workflow_name)
        # print("Workflow set_task: ", tasks[kwargs["name"]][kwargs["task_order"]])

    def get_task_attr(self, task_, attr):
        if not task_.get(attr):
            if not task_.get("shared"):
                task_[attr] = self.tasks.get(attr)
            elif task_.get("shared"):
                task_[attr] = self.shared_tasks.tasks.get(attr)
            else:
                raise Exception(
                    "Workflow get_task_attr: shared value and task_ attribute presence error")
        return task_.get(attr)

    def update_task(self, task_):

        # task_ object structure
        # name, args, task_order, shared, before, after, function, function_args, function_kwargs, log
        """workflow_kwargs: name, args, task_order, shared, before, after, log"""

        task_obj = {
            "task_order": self.get_task_attr(task_, "task_order"),
            "workflow_args": self.get_task_attr(task_, "args"),
            "workflow_kwargs": self.get_task_attr(task_, "workflow_kwargs"),
            "function_args": self.get_task_attr(task_, "function_args"),
            "function_kwargs": self.get_task_attr(task_, "fn_args"),
            "before": self.get_task_attr(task_, "before"),
            "after": self.get_task_attr(task_, "after"),
            "function": self.get_task_attr(task_, "function"),
            "log": self.get_task_attr(task_, "log")
        }

        if task_.get("shared") == True:
            self.shared_tasks.tasks.update(task_.get("name"), task_obj)
        elif task_.get("shared") == False:
            self.tasks.update(task_.get("name"), task_obj)

    def run_task(self, task_, shared=None):
        # task_ object structure
        # name, args, task_order, shared, before, after, function, function_args, function_kwargs, log
        """workflow_kwargs: name, args, task_order, shared, before, after, log"""

        task_ = self.get_tasks(task_, shared)
        log_ = task_.get("log")

        if log_:
            print("Workflow task_ found: ", task_)
            # print("The workflow object looks like this: ", task_)

        if task_:
            # TODO: Put in try except block for clean errors

            #       Iterate through before for each task_
            if log_:
                print("Workflow before middlewares for task_ now running: ",
                      task_)
            self.__setup_run_middleware(task_, "before", log_)

            #       Invoke task_
            if log_:
                print("Workflow task_ run: ", task_)
            task_.get("function")(*task_.get("function_args"), **task_.get("function_kwargs"))

            #       Iterate through after for each task_
            if log_:
                print("Workflow after middlewares for task_ now running: ",
                      task_)
            self.__setup_run_middleware(task_, "after", log_)

    def __merge_instance(self, tasks, inst, shared=None, clash_prefix=None):
        for k in tasks.keys():
            for ik in inst.tasks.keys():
                if k == ik:
                    if not clash_prefix:
                        raise Exception(
                            "Workflow merge_instance: clash_prefix not provided")
                    tasks.update(clash_prefix + ik, inst.tasks.get(ik))
                tasks[ik] = inst.tasks.get(ik)
        return tasks

    def merge_instance(self, inst, shared=False, clash_prefix=None):
        if shared == True:
            self.shared_tasks.tasks = self.__merge_instance(
                self.shared_tasks.tasks, inst, clash_prefix)
        elif shared == False:
            self.tasks = self.__merge_instance(
                self.tasks, inst, shared, clash_prefix)


class Tasks(WorkflowBase):

    def add_plugin(self, plugin_inst):
        pass

    def merge(self, inst, shared=False, clash_prefix=None):
        self.merge_instance(inst, shared, clash_prefix)

    def run(self, tasks):

        if isinstance(tasks, str):
            # Iterate task through single task
            print("Workflow task provided being instantiated: ", str(tasks))
            print("Workflow has tasks: ", str(self.tasks.keys()))
            self.run_task(tasks)

        elif isinstance(tasks, list):
            # Iterate task through tasks
            print("Workflow task list provided being instantiated: ", str(tasks))
            print("Workflow has tasks: ", str(self.tasks.keys()))
            [self.run_task(t) for t in self.tasks]

        else:
            print("No workflow or task available to run")

    def apis(self):

        return {
            "get_tasks": self.get_tasks,
            "set_task": self.set_task,
            "update_task": self.update_task,
            "run_task": self.run_task,
            "clean_args": self.clean_args
        }


def workflow(*workflow_args, **workflow_kwargs):

    def get_decorator(fn):
        # print("get_decorator: Decorator init ", "workflow_args: ", workflow_args, "workflow_kwargs: ", workflow_kwargs)
        # print("get_decorator: ", fn)

        def order_tasks(*function_args, **function_kwargs):
            # print("Workflow order_tasks: Decorator init ", "function_args: ", function_args, "function_kwargs: ", function_kwargs)

            t = workflow_kwargs.get("task_instance")
            if not t:
                raise Exception("Task instance not provided")

            # Check before/after middlewares args and kwargs number and validity
            args_normal = t.clean_args(fn, workflow_args, workflow_kwargs, function_args, function_kwargs)

            if not args_normal:
                raise Exception("Args and KwArgs do not match")

            # print((fn, function_args, function_kwargs, workflow_args, workflow_kwargs))
            t.set_task(fn, function_args, function_kwargs, workflow_args, workflow_kwargs)

            print("Workflow order_tasks - Task added: ", workflow_kwargs.get("name"))

        return order_tasks
    return get_decorator


__all__ = ["Tasks", "workflow"]
