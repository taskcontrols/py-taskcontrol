# # Project Workflow
# Add support for Concurrency


class SharedBase():

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

    __instance = None

    def __init__(self):
        if SharedBase.__instance != None:
            pass
        else:
            SharedBase.__instance = self

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SharedBase, cls).__new__(cls)
        return cls.__instance

    @staticmethod
    def getInstance():
        if not SharedBase.__instance:
            SharedBase()
        return SharedBase.__instance


class ConcurencyBase():
    # asynchronous, needs_join
    def mthread_run(self, function, options):
        pass

    # asynchronous, needs_join
    def mprocess_run(self, function, options):
        pass


class LoggerBase():
    pass


class PluginsBase(SharedBase, ConcurencyBase):

    # add plugin to instance or shared
    def plugin_register(self, name, plugin_instance):
        pass

    # return plugin instance/module
    def plugin_create(self, name, plugin_instance):
        pass


class WorkflowBase(SharedBase, ConcurencyBase, LoggerBase):
    """middleware_task_ Structure: name, function, args, kwargs, options"""
    """workflow_kwargs: name, task_instance, task_order, shared, args, kwargs, before, after, log"""
    # Allow instance tasks
    tasks = {"taskname": {}}

    """ Results of task runs (instance) """
    # Access results from tasks, shared tasks during a task run
    ctx = {}

    """  """
    # TODO: Other features
    config = {}

    """  """
    # TODO: Plugins features
    plugins = {"pluginname": {"taskname": {}}}

    def __init__(self):
        self.shared_tasks = SharedBase.getInstance()

    # def __get_args(self, f, action, log_):
        #     if action and isinstance(action, dict):
        #         args, kwargs, err_obj = [], {}, {}
        #         if isinstance(action.get("args"), list):
        #             args = action.get("args")
        #         if isinstance(action.get("kwargs"), dict):
        #             kwargs = action.get("kwargs")
        #         if isinstance(action.get("options"), dict):
        #             err_obj = action.get("options")
        #     # TODO: Do clean args here
        #     return err_obj, args, kwargs

    # Check before/after middlewares args and kwargs number and validity
    def clean_args(self, function_, function_args, function_kwargs):
        arg_list = function_.__code__.co_varnames
        k_fn_kwa = function_kwargs.keys()
        l_tpl, l_fn_a, l_k_fn_kwa = len(arg_list), len(
            function_args), len(k_fn_kwa)

        if (l_tpl == l_fn_a + l_k_fn_kwa):
            for k in k_fn_kwa:
                if not arg_list.index(k) >= l_fn_a:
                    return False
            return True
        return False

    def get_attr(self, task_, attr):
        if not task_.get(attr):
            if not task_.get("shared"):
                task_[attr] = self.tasks.get(attr)
            elif task_.get("shared"):
                task_[attr] = self.shared_tasks.tasks.get(attr)
            else:
                raise ValueError(
                    "Workflow get_attr: shared value and task_ attribute presence error"
                )
        return task_.get(attr)

    def parse_tasks(self, task_):
        if task_ == "1" or task_ == 1:
            return list(self.tasks.keys())
        if task_ == "shared:1":
            s_tasks = self.shared_tasks.tasks.keys()
            return ["shared:"+i for i in list(s_tasks)]
        if task_ == 1 and type(task_) == int:
            return list(self.tasks.keys())
        return task_

    def get_tasks(self, task_=None):
        shared = False
        if isinstance(task_, str):
            if len(task_.split("shared:")) > 1:
                shared = True
                task_ = task_.split("shared:")[1]

            if shared:
                return self.shared_tasks.tasks.get(task_)
            elif not shared:
                return self.tasks.get(task_)
        return self.tasks

    def set_task(self, function_, function_args, function_kwargs, workflow_args, workflow_kwargs):
        workflow_name = workflow_kwargs.get("name")
        print("Workflow task name to add: ", workflow_name)
        shared = workflow_kwargs.get("shared")

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

        task_ = {
            # task run not configured for ordered run
            "task_order": workflow_kwargs.get("task_order"),
            # workflow args are getting duplicated
            # consider saving it in ctx
            "workflow_args": workflow_args, "workflow_kwargs": workflow_kwargs,
            "function_args": function_args, "function_kwargs": function_kwargs,
            "before": workflow_kwargs.get("before"),
            "after": workflow_kwargs.get("after"),
            "function": function_,
            "log": workflow_kwargs.get("log")
        }

        if shared == True:
            self.shared_tasks.tasks[workflow_name].update(task_)
        elif shared == False:
            self.tasks[workflow_name].update(task_)

        print("Workflow set_task: Adding Task: ", workflow_name)
        return True

    def update_task(self, task_):

        # task_obj = self.create_task(task_)
        self.ctx[task_.get("name")]["log"] = self.get_attr(task_, "log")
        self.ctx[task_.get("name")]["workflow_args"] = self.get_attr(
            task_, "workflow_args")
        self.ctx[task_.get("name")]["workflow_kwargs"] = self.get_attr(
            task_, "workflow_kwargs")

        task_obj = {
            # task run not configured for ordered run
            "task_order": self.get_attr(task_, "task_order"),
            # workflow args are getting duplicated
            # consider saving it in ctx
            "workflow_args": self.get_attr(task_, "workflow_args"),
            "workflow_kwargs": self.get_attr(task_, "workflow_kwargs"),
            "function_args": self.get_attr(task_, "function_args"),
            "function_kwargs": self.get_attr(task_, "function_kwargs"),
            "before": self.get_attr(task_, "before"),
            "after": self.get_attr(task_, "after"),
            "function": self.get_attr(task_, "function"),
            "log": self.get_attr(task_, "log")
        }

        if task_.get("shared") == True:
            self.shared_tasks.tasks.update(task_.get("name"), task_obj)
        elif task_.get("shared") == False:
            self.tasks.update(task_.get("name"), task_obj)

    def reducer(self, result, task_):
        if isinstance(type(task_), dict) or type(task_) == dict:
            fn = task_.get("function")
            args = task_.get("args")
            kwargs = task_.get("kwargs")
            workflow_args = task_.get("workflow_args")
            workflow_kwargs = task_.get("workflow_kwargs")
            log_ = task_.get("log")
            if task_.get("options") and not task_.get("options") == None:
                error_object = task_.get("options")
            else:
                error_object = {}
        else:
            raise TypeError("Object not a dictionary type")

        if args == None or not isinstance(args, list) or not type(args) == list:
            raise TypeError("Args not a dictionary type")
        if kwargs == None or not isinstance(kwargs, dict) or not type(kwargs) == dict:
            raise TypeError("Kwargs not a dictionary type")
        if workflow_args == None or not isinstance(workflow_args, list) or not type(workflow_args) == list:
            workflow_args = []
        if workflow_kwargs == None or not isinstance(workflow_kwargs, dict) or not type(workflow_kwargs) == dict:
            workflow_kwargs = {}

        if result:
            result_ = result.get("result")
        if not result:
            result_ = []
            result = {"result": []}

        try:
            r_ = fn(self.ctx, result_, *args, **kwargs)
        except (Exception) as e:
            if log_:
                print("reducer: Running error for middleware")

            if not hasattr(error_object, "error"):
                error_object["error"] = "exit"

            e_enum = error_object.get("error")
            e_next_value = error_object.get("error_next_value")
            e_return = {"error": e, "next": e_next_value}

            if e_enum == "next":
                return e_return
            elif e_enum == "error_handler":
                if not hasattr(error_object, "error_handler"):
                    return e_return
                return {"error": e, "next": error_object.get("error_handler")(e, e_next_value)}
            elif e_enum == "exit":
                raise Exception("Error during middleware: error_obj['error'] exit",
                                fn.__name__, str(e))
            else:
                raise TypeError(
                    "Error during middleware: flow[options[error]] value error")

        result["result"].append(r_)
        self.ctx["result"] = result.get("result")

        return {"result": result.get("result")}

    def run_task(self, task_):
        if task_ == None:
            return
        if len(task_.keys()) == 0:
            return

        log_ = task_.get("log")
        t_before = task_.get("before")

        if t_before == None:
            t_before = []

        if isinstance(t_before, dict):
            before = [t_before]
        elif isinstance(t_before, list):
            before = t_before
        else:
            raise ValueError("Error: run_task: Definition of before")

        for b in before:
            b["name"] = task_.get("name")

        fn_task = {}
        fn_task["name"] = task_.get("workflow_kwargs").get("name")
        fn_task["function"] = task_.get("function")
        fn_task["args"] = task_.get("workflow_kwargs").get("args")
        fn_task["kwargs"] = task_.get("workflow_kwargs").get("kwargs")
        fn_task["workflow_args"] = task_.get("workflow_args")
        fn_task["workflow_kwargs"] = task_.get("workflow_kwargs")

        t_after = task_.get("after")

        if t_after == None:
            t_after = []

        if isinstance(t_after, dict):
            after = [t_after]
        elif isinstance(t_after, list):
            after = t_after
        else:
            raise ValueError("Error: run_task: Definition of after")

        for a in after:
            a["name"] = task_.get("name")

        tasks_to_run_in_task_ = [None, *before, fn_task, *after]

        import functools
        return functools.reduce(self.reducer, tasks_to_run_in_task_)

    def merge_tasks(self, tasks, inst, shared=None, clash_prefix=None):
        for k in tasks.keys():
            for ik in inst.tasks.keys():
                if k == ik:
                    if not clash_prefix:
                        raise TypeError(
                            "Workflow merge_instance: clash_prefix not provided")
                    tasks.update(clash_prefix + ik, inst.tasks.get(ik))
                tasks[ik] = inst.tasks.get(ik)

        return tasks
