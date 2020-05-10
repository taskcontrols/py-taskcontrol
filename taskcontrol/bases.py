# # Project Workflow
# Add support for Concurrency

from .sharedbase import SharedBase
from .concurrency import ConcurencyBase
from .actions import ActionsBase
from .logger import LoggerBase
from .plugin import PluginsBase


class WorkflowBase(SharedBase, ConcurencyBase, LoggerBase):

    def __init__(self):
        self.shared_tasks = SharedBase.getInstance()
        self.get_ctx, self.set_ctx, self.get_attr, self.update_task, self.set_tasks, self.parse_tasks, self.get_tasks = self.wf_closure()

    def wf_closure(self):
        """middleware_task_ Structure: name, function, args, kwargs, options"""
        """workflow_kwargs: name, task_instance, task_order, shared, args, kwargs, before, after, log"""

        # Allow instance tasks
        tasks = {"taskname": {}}

        """ Results of task runs (instance) """
        # Access results from tasks, shared tasks during a task run
        # Make context based on taskname
        ctx = {}

        """  """
        # TODO: Other features
        config = {}

        """  """
        # TODO: Plugins features
        plugins = {"pluginname": {"taskname": {}}}

        def get_ctx(keys=None):
            # TODO: Add Auth & Logger
            if keys == 1 and type(keys) == int:
                return ctx
            if type(keys) == str:
                return ctx.get(keys)
            if type(keys) == list:
                cx = {}
                for v in keys:
                    valid_value = ctx.get(v)
                    if valid_value:
                        cx[v] = valid_value
                return cx
            return

        def set_ctx(val=None):
            # TODO: Add Auth & Logger
            if type(val) == dict:
                for i in val.keys():
                    ctx[i] = val[i]
                return True
            elif type(val) == list:
                for l in val:
                    if type(l) == dict:
                        for j in l.keys():
                            ctx[j] = l[j]
                return True
            return False

        def get_config():
            pass

        def set_config():
            pass

        def get_plugins():
            pass

        def set_plugins():
            pass

        def get_attr(task, attr):
            if not task.get(attr):
                if not task.get("shared"):
                    task[attr] = tasks.get(attr)
                elif task.get("shared"):
                    task[attr] = self.shared_tasks.get_shared_tasks(attr)
                else:
                    raise ValueError(
                        "Workflow get_attr: shared value and task attribute presence error"
                    )
            return task.get(attr)

        def update_task(task):

            # # task_obj = self.create_task(task)
            # self.ctx[task.get("name")]["log"] = self.get_attr(task, "log")
            # self.ctx[task.get("name")]["workflow_args"] = self.get_attr(
            #     task, "workflow_args")
            # self.ctx[task.get("name")]["workflow_kwargs"] = self.get_attr(
            #     task, "workflow_kwargs")

            task_obj = {
                "task_order": get_attr(task, "task_order"),
                "workflow_args": get_attr(task, "workflow_args"),
                "workflow_kwargs": get_attr(task, "workflow_kwargs"),
                "function_args": get_attr(task, "function_args"),
                "function_kwargs": get_attr(task, "function_kwargs"),
                "before": get_attr(task, "before"),
                "after": get_attr(task, "after"),
                "function": get_attr(task, "function"),
                "log": get_attr(task, "log")
            }

            if task.get("shared") == True:
                self.shared_tasks.set_shared_tasks(
                    {task.get("name"): task_obj})
            elif task.get("shared") == False:
                tasks.update(task.get("name"), task_obj)

        def set_tasks(function_, function_args, function_kwargs, workflow_args, workflow_kwargs):
            workflow_name = workflow_kwargs.get("name")
            print("Workflow task name to add: ", workflow_name)
            shared = workflow_kwargs.get("shared")

            if shared == True:
                wf = self.shared_tasks.get_shared_tasks(workflow_name)
                if isinstance(wf, dict) and not wf == None:
                    self.shared_tasks.set_shared_tasks({workflow_name: {}})
                if not isinstance(wf, dict):
                    self.shared_tasks.set_shared_tasks({workflow_name: {}})
            elif not shared == True:
                if workflow_name not in tasks.keys():
                    tasks[workflow_name] = {}
                if not isinstance(tasks[workflow_name], dict):
                    tasks.update({workflow_name: {}})

            task = {
                "task_order": workflow_kwargs.get("task_order"),
                "workflow_args": workflow_args, "workflow_kwargs": workflow_kwargs,
                "function_args": function_args, "function_kwargs": function_kwargs,
                "before": workflow_kwargs.get("before"),
                "after": workflow_kwargs.get("after"),
                "function": function_,
                "log": workflow_kwargs.get("log")
            }

            if shared == True:
                self.shared_tasks.set_shared_tasks({workflow_name: task})
            elif shared == False:
                tasks[workflow_name].update(task)

            print("Workflow set_tasks: Adding Task: ", workflow_name)
            return True

        def parse_tasks(task):
            if task == "1" or task == 1:
                return list(tasks.keys())
            if task == "shared:1":
                s_tasks = self.shared_tasks.get_shared_tasks(1).keys()
                return ["shared:"+i for i in list(s_tasks)]
            if task == 1 and type(task) == int:
                return list(tasks.keys())
            return task

        def get_tasks(task=None):
            shared = False
            if isinstance(task, str):
                if len(task.split("shared:")) > 1:
                    shared = True
                    task = task.split("shared:")[1]

                if shared:
                    return self.shared_tasks.get_shared_tasks(task)
                elif not shared:
                    return tasks.get(task)
            return

        return (get_ctx, set_ctx, get_attr, update_task, set_tasks, parse_tasks, get_tasks)

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

    def reducer(self, result, task):
        if isinstance(type(task), dict) or type(task) == dict:
            fn = task.get("function")
            args = task.get("args")
            kwargs = task.get("kwargs")
            workflow_args = task.get("workflow_args")
            workflow_kwargs = task.get("workflow_kwargs")
            log_ = task.get("log")
            if task.get("options") and not task.get("options") == None:
                error_object = task.get("options")
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
            r_ = fn(self.get_ctx(1), result_, *args, **kwargs)
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

        # Applying below for SharedBase Closure support
        # Doesnt work without assigning keys, makes it immutable for dict props/keys
        # Check implementation of getter and setter
        self.set_ctx({"result": result.get("result")})

        return {"result": result.get("result")}

    def run_task(self, task):
        # TODO: Add Auth & Logger
        if task == None:
            return
        if len(task.keys()) == 0:
            return

        log_ = task.get("log")
        t_before = task.get("before")

        if t_before == None:
            t_before = []

        if isinstance(t_before, dict):
            before = [t_before]
        elif isinstance(t_before, list):
            before = t_before
        else:
            raise ValueError("Error: run_task: Definition of before")

        for b in before:
            b["name"] = task.get("name")

        fn_task = {}
        fn_task["name"] = task.get("workflow_kwargs").get("name")
        fn_task["function"] = task.get("function")
        fn_task["args"] = task.get("workflow_kwargs").get("args")
        fn_task["kwargs"] = task.get("workflow_kwargs").get("kwargs")
        fn_task["workflow_args"] = task.get("workflow_args")
        fn_task["workflow_kwargs"] = task.get("workflow_kwargs")

        t_after = task.get("after")

        if t_after == None:
            t_after = []

        if isinstance(t_after, dict):
            after = [t_after]
        elif isinstance(t_after, list):
            after = t_after
        else:
            raise ValueError("Error: run_task: Definition of after")

        for a in after:
            a["name"] = task.get("name")

        tasks_to_run_in_task = [None, *before, fn_task, *after]

        import functools
        return functools.reduce(self.reducer, tasks_to_run_in_task)

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
