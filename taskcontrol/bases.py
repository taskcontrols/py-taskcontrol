# # Project Workflow
# Add support for Concurrency

from .sharedbase import ClosureBase, SharedBase
from .concurrency import ConcurencyBase
from .actions import ActionsBase
from .hooks import Sockets, Hooks
from .authentication import AuthBase
from .logger_timer import LoggerBase
from .plugin import PluginsBase


class WorkflowBase(ClosureBase, ConcurencyBase, PluginsBase):

    def __init__(self):
        self.shared = SharedBase.getInstance()
        self.getter, self.setter, self.deleter = self.class_closure(
            tasks={}, plugins={}, ctx={})
        """middleware_task_ Structure: name, function, args, kwargs, options"""
        """workflow_kwargs: name, task_instance, task_order, shared, args, kwargs, before, after, log"""

    def clean_args(self, function_, function_args, function_kwargs):

        arg_list = function_.__code__.co_varnames
        k_fn_kwa = function_kwargs.keys()

        l_tpl, l_fn_a, l_k_fn_kwa = len(arg_list), len(
            function_args), len(k_fn_kwa)

        if arg_list[1] == "result" and arg_list[0] == "ctx":
            if (l_tpl == l_fn_a + l_k_fn_kwa + 2):
                for k in k_fn_kwa:
                    if not arg_list.index(k) >= l_fn_a:
                        return False
                return True
        else:
            raise TypeError(
                "First two args of a function/middleware has to be ctx and result")
        return False

    def merge_tasks(self, tasks, inst, shared=None, clash_prefix=None):
        pass

    def reducer(self, result, task):

        if type(task) == dict:
            if len(task.keys()) == 0:
                raise TypeError("Task structure error")
            fn = task.get("function")
            args = task.get("args")
            kwargs = task.get("kwargs")
            workflow_args = task.get("workflow_args")
            workflow_kwargs = task.get("workflow_kwargs")
            log_ = task.get("log")
            if task.get("options") and task.get("options") != None:
                error_object = task.get("options")
            else:
                error_object = {}
        else:
            raise TypeError("Object not a dictionary type")

        if args == None or type(args) != list:
            raise TypeError("Args not a list type")
        if kwargs == None or type(kwargs) != dict:
            raise TypeError("Kwargs not a dictionary type")
        if workflow_args == None or type(workflow_args) != list:
            workflow_args = []
        if workflow_kwargs == None or type(workflow_kwargs) != dict:
            workflow_kwargs = {}

        if result:
            result_ = result.get("result")
        if not result:
            result_ = []
            result = {"result": []}

        try:
            r_ = fn(self.getter("ctx", 1), result_, *args, **kwargs)
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

        result["result"].append(
            {"result": r_, "function": fn.__name__, "name": task.get("name")})

        return {"result": result.get("result")}

    def run_task(self, task):
        if task == None:
            return {"result": "Task not found error", "type": str(type(task))}
        log_ = task.get("log")
        t_before = task.get("workflow_kwargs").get("before")

        if t_before == None:
            t_before = []

        if isinstance(t_before, dict) or type(t_before) == dict:
            t_before.update({"name": task.get("name")})
            t_before.update({"workflow_args": task.get("workflow_args")})
            t_before.update(
                {"workflow_kwargs": task.get("workflow_kwargs")})
            before = [t_before]
        elif isinstance(t_before, list) or type(t_before) == list:
            for idx, item in enumerate(t_before):
                t_before[idx].update({"name": task.get("name")})
                t_before[idx].update(
                    {"workflow_args": task.get("workflow_args")})
                t_before[idx].update(
                    {"workflow_kwargs": task.get("workflow_kwargs")})
            before = t_before
        else:
            raise ValueError("Error: run_task: Definition of before")

        for b in before:
            b["name"] = task.get("name")

        fn_task = {}
        fn_task["name"] = task.get("name")
        fn_task["args"] = task.get("args")
        fn_task["kwargs"] = task.get("kwargs")
        fn_task["function"] = task.get("function")
        fn_task["workflow_args"] = task.get("workflow_args")
        fn_task["workflow_kwargs"] = task.get("workflow_kwargs")
        fn_task["log"] = task.get("log")

        t_after = task.get("workflow_kwargs").get("after")

        if t_after == None:
            t_after = []

        if isinstance(t_after, dict) or type(t_after) == dict:
            t_after.update({"name": task.get("name")})
            t_after.update({"workflow_args": task.get("workflow_args")})
            t_after.update(
                {"workflow_kwargs": task.get("workflow_kwargs")})
            after = [t_after]
        elif isinstance(t_after, list) or type(t_after) == list:
            for idx, item in enumerate(t_after):
                t_after[idx].update({"name": task.get("name")})
                t_after[idx].update(
                    {"workflow_args": task.get("workflow_args")})
                t_after[idx].update(
                    {"workflow_kwargs": task.get("workflow_kwargs")})
            after = t_after
        else:
            raise ValueError("Error: run_task: Definition of after")

        for a in after:
            a["name"] = task.get("name")

        tasks_to_run_in_task = [None, *before, fn_task, *after]

        import functools
        return functools.reduce(self.reducer, tasks_to_run_in_task)


__all__ = ["WorkflowBase", "PluginsBase"]
