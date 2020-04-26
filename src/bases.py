# # Project Workflow


class SharedBase():

    tasks = {"taskname": {}}
    plugins = {"pluginname": {"taskname": {}}}
    ctx = {"result": []}

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


class MiddlewareBase():

    def __get_args(self, f, action, log_):
        if action and isinstance(action, dict):
            args, kwargs, err_obj = [], {}, {}
            if isinstance(action.get("args"), list):
                args = action.get("args")
            if isinstance(action.get("kwargs"), dict):
                kwargs = action.get("kwargs")
            if isinstance(action.get("options"), dict):
                err_obj = action.get("options")
        # TODO: Do clean args here
        return err_obj, args, kwargs

    def run_middleware(self, middleware, error_object, log_, *args, **kwargs):
        try:
            if log_:
                print("Workflow running middleware function: ",
                      middleware.__name__)
            return None, middleware(*args, **kwargs)
        except Exception as e:
            if log_:
                print("Running error for middleware")
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
                raise Exception("error_obj['error'] exit: Error during middleware: ",
                                middleware.__name__, str(e))
            else:
                raise Exception(
                    "Error during middleware: flow[options[error]] value error")

    def run_middlewares(self, middlewares=None, log_=False):
        result = []

        if isinstance(middlewares, list):
            for action in middlewares:
                middleware = action.get("function")
                err_obj, a, kwa = self.__get_args(middleware, action, log_)
                if len(result) > 0:
                    result.append(self.run_middleware(
                        middleware, err_obj, log_, *a, **kwa,
                        error=result[-1].get("error"), fn_result=result[-1].get("fn_result")
                    ))
                else:
                    result.append(self.run_middleware(
                        middleware, err_obj, log_, *a, **kwa, error=None, fn_result=None
                    ))
        elif isinstance(middlewares, dict):
            err_obj, a, kwa = self.__get_args(
                middlewares.get("function"), middlewares, log_
            )
            result.append(self.run_middleware(
                middlewares.get("function"), err_obj, log_, *a, **kwa, error=None, fn_result=None
            ))

        return result

    def init_middlewares(self, task_, md_action=None, log_=False):
        actions = task_.get("workflow_kwargs").get(md_action)
        log_ = task_.get("workflow_kwargs").get("log")
        result = self.run_middlewares(actions, log_)
        return result


class WorkflowBase(SharedBase, MiddlewareBase):
    # task_ object structure
    # name, args, task_order, shared, before, after, function, function_args, function_kwargs, log
    """workflow_kwargs: name, args, task_order, shared, before, after, log"""

    tasks = {"taskname": {}}
    plugins = {"pluginname": {"taskname": {}}}
    ctx = {}

    def __init__(self):
        self.shared_tasks = SharedBase.getInstance()

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
                raise Exception(
                    "Workflow get_attr: shared value and task_ attribute presence error"
                )
        return task_.get(attr)

    def get_tasks(self, task_=None, shared=False):
        if shared and task_ and isinstance(task_, str):
            return self.shared_tasks.tasks.get(task_)
        elif not shared and task_ and isinstance(task_, str):
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

        self.tasks[workflow_name].update({
            "task_order": workflow_kwargs.get("task_order"),
            "workflow_args": workflow_args, "workflow_kwargs": workflow_kwargs,
            "function_args": function_args, "function_kwargs": function_kwargs,
            "before": workflow_kwargs.get("before"),
            "after": workflow_kwargs.get("after"),
            "function": function_,
            "log": workflow_kwargs.get("log")
        })

        print("Workflow set_task: Adding Task: ", workflow_name)
        return True

    def update_task(self, task_):

        # task_obj = self.create_task(task_)

        task_obj = {
            "task_order": self.get_attr(task_, "task_order"),
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

        if not isinstance(type(task_), dict):
            fn = task_.get("function")
            args = task_.get("args")
            kwargs = task_.get("kwargs")
            workflow_args = task_.get("workflow_args")
            workflow_kwargs = task_.get("workflow_kwargs")

        if result:
            result_ = result.get("result")
        if not result:
            result_ = []
            result = {"result": []}
        if not workflow_args:
            workflow_args = []
        if not workflow_kwargs:
            workflow_kwargs = []

        r_ = fn(self.ctx, result_, *args, **kwargs)
        result["result"].append(r_)
        self.ctx["result"] = result.get("result")

        return {"result": result.get("result")}

    def run_task(self, task_, shared=None):

        task_ = self.get_tasks(task_, shared)
        log_ = task_.get("log")

        if isinstance(task_.get("before"), dict):
            before = [task_.get("before")]
        else:
            before = task_.get("before")

        fn_task = {}
        fn_task["function"] = task_.get("function")
        fn_task["args"] = task_.get("workflow_kwargs").get("args")
        fn_task["kwargs"] = task_.get("workflow_kwargs").get("kwargs")
        fn_task["workflow_args"] = task_.get("workflow_args")
        fn_task["workflow_kwargs"] = task_.get("workflow_kwargs")

        after = task_.get("after")
        tasks_to_run_in_task_ = [None, *before, fn_task, *after]

        import functools
        return functools.reduce(self.reducer, tasks_to_run_in_task_)

    def merge_tasks(self, tasks, inst, shared=None, clash_prefix=None):
        for k in tasks.keys():
            for ik in inst.tasks.keys():
                if k == ik:
                    if not clash_prefix:
                        raise Exception(
                            "Workflow merge_instance: clash_prefix not provided")
                    tasks.update(clash_prefix + ik, inst.tasks.get(ik))
                tasks[ik] = inst.tasks.get(ik)

        return tasks
