# # Project Workflow
# Add support for Concurrency

import copy
from taskcontrol.lib.utils import ClosureBase, SharedBase, UtilsBase, ConcurencyBase, TimerBase, LogBase, CommandsBase
from taskcontrol.lib.utils import EventsBase, QueuesBase, SocketsBase, HooksBase, ActionsBase
from taskcontrol.lib.utils import EPubSubBase, IPubSubBase, WebhooksBase, SSHBase
from taskcontrol.lib.authentication import AuthenticationBase
from taskcontrol.lib.orm import SQLORMBase
from taskcontrol.lib.interfaces import PluginsInterface


class PluginBase(UtilsBase, PluginsInterface):

    # return plugin instance/module (plugin_instance)
    def plugin_create(self, name, task_instance):

        # TODO: Apply multiple instances (Allow seperate and merged instances)
        # Low priority
        if type(task_instance) != dict:
            raise TypeError("plugins definition has an issue")

        if type(task_instance) == dict:
            if not task_instance.get("config"):
                raise ValueError("config definition has an issue")
            if not task_instance.get("ctx"):
                raise ValueError("ctx definition has an issue")
            if not task_instance.get("plugins"):
                raise ValueError("internal plugins definition has an issue")
            if not task_instance.get("shared"):
                raise ValueError("shared definition has an issue")
            if not task_instance.get("tasks"):
                raise ValueError("tasks definition has an issue")
            if not task_instance.get("workflows"):
                raise ValueError("workflows definition has an issue")

        if type(name) == str:
            return {
                name: {
                    "config": task_instance.get("config"),
                    "ctx": task_instance.get("ctx"),
                    "plugins": task_instance.get("plugins"),
                    "shared": task_instance.get("shared"),
                    "tasks": task_instance.get("tasks"),
                    "workflows": task_instance.get("workflows")
                }
            }


class WorkflowBase(ClosureBase, ConcurencyBase, PluginBase, UtilsBase):

    def __init__(self):
        super().__init__()
        # ConcurencyBase.__init__(self)
        # PluginsBase.__init__(self)
        self.shared = SharedBase.getInstance()
        self.getter, self.setter, self.deleter = self.class_closure(
            tasks={}, plugins={}, ctx={})
        """middleware_task_ Structure: name, function, args, kwargs, options"""
        """workflow_kwargs: name, task_instance, task_order, shared, args, kwargs, before, after, log"""

    def clean_args(self, function_, function_args, function_kwargs):

        arg_list = function_.__code__.co_varnames
        fnc_kwa_keys = function_kwargs.keys()

        len_tpl, len_fnc_args, len_fnc_kwa_keys = len(arg_list), len(
            function_args), len(fnc_kwa_keys)

        if arg_list[1] == "result" and arg_list[0] == "ctx":
            if (len_tpl == len_fnc_args + len_fnc_kwa_keys + 2):
                for k in fnc_kwa_keys:
                    if not arg_list.index(k) >= len_fnc_args:
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
            args = task.get("workflow_args", [])
            kwargs = task.get("workflow_kwargs", {})
            workflow_args = task.get("workflow_args", [])
            workflow_kwargs = task.get("workflow_kwargs", {})
            log_ = task.get("log")
            if task.get("options") and task.get("options") != None:
                error_object = task.get("options")
            else:
                error_object = {}
        else:
            raise TypeError("Object not a dictionary type")

        if not result:
            result = {"result": []}
        result_ = result.get("result", [])

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
        t_before = task.get("workflow_kwargs").get("before", [])

        if isinstance(t_before, dict) or type(t_before) == dict:
            t_before.update({
                "name": task.get("name"),
                "workflow_args": task.get("workflow_args"),
                "workflow_kwargs": task.get("workflow_kwargs")
            })
            before = [t_before]
        elif isinstance(t_before, list) or type(t_before) == list:
            for idx, item in enumerate(t_before):
                t_before[idx].update({
                    "name": task.get("name"),
                    "workflow_args": task.get("workflow_args"),
                    "workflow_kwargs": task.get("workflow_kwargs")
                })
            before = t_before
        else:
            raise ValueError("Error: run_task: Definition of before")

        fn_task = {
            "name": task.get("name"),
            "args": task.get("args"),
            "kwargs": task.get("kwargs"),
            "function": task.get("function"),
            "workflow_args": task.get("workflow_args"),
            "workflow_kwargs": task.get("workflow_kwargs"),
            "log": task.get("log")
        }

        t_after = task.get("workflow_kwargs").get("after", [])

        if isinstance(t_after, dict) or type(t_after) == dict:
            t_after.update({
                "name": task.get("name"),
                "workflow_args": task.get("workflow_args"),
                "workflow_kwargs": task.get("workflow_kwargs")
            })
            after = [t_after]
        elif isinstance(t_after, list) or type(t_after) == list:
            for idx, item in enumerate(t_after):
                t_after[idx].update({
                    "name": task.get("name"),
                    "workflow_args": task.get("workflow_args"),
                    "workflow_kwargs": task.get("workflow_kwargs")
                })
            after = t_after
        else:
            raise ValueError("Error: run_task: Definition of after")

        tasks_to_run_in_task = [None, *before, fn_task, *after]

        import functools
        return functools.reduce(self.reducer, tasks_to_run_in_task)



class Tasks(WorkflowBase):

    def __init__(self):
        super().__init__()
    
    def plugin_register(self, plugin_instance):
        pass

    def merge(self, inst, shared=False, clash_prefix=None):
        pass

    def create_workflow(self, name, workflows, options):
        pass

    def get_all_tasks(self, tasks, tsk=[]):
        if type(tasks) == int:
            if tasks == 1:
                l = self.getter("tasks", 1)
                for i in l:
                    tsk.append(i)
        elif type(tasks) == str:
            if tasks.count("shared:1"):
                l = self.shared.getter("tasks", 1)
                for i in l:
                    tsk.append(i)
            elif tasks.count("shared:"):
                l = self.shared.getter("tasks", tasks.split("shared:")[1])
                for i in l:
                    tsk.append(i)
            elif tasks.count("1"):
                l = self.getter("tasks", 1)
                for i in l:
                    tsk.append(i)
            else:
                l = self.getter("tasks", tasks)
                for i in l:
                    tsk.append(i)
        elif type(tasks) == list:
            for t in tasks:
                tsk = self.get_all_tasks(t, tsk)
        return tsk

    def run(self, tasks=["1"]):
        # "1", 1, "shared:1", "shared:task", "task"
        result = []

        tsk = self.get_all_tasks(tasks, [])

        if len(tsk) > 0:
            for tk in tsk:
                if type(tsk) == dict:
                    return result.append(self.run_task(tk))
                elif type(tsk) == list:
                    for task in tsk:
                        result.append(self.run_task(task))
                    return result
        else:
            print("No workflow or task available to run")
        return result


def workflow(*work_args, **work_kwargs):

    def get_decorator(function_):

        def add_tasks(*function_args, **function_kwargs):
            if not work_kwargs.get("name"):
                raise TypeError("Name Argument or task instance not provided")
            if type(work_kwargs.get("args")) != list:
                work_kwargs["args"] = work_kwargs.get("args", [])
            if type(work_kwargs.get("kwargs")) != dict:
                work_kwargs["kwargs"] = work_kwargs.get("kwargs", {})

            t = work_kwargs["task_instance"]
            work_kwargs.update({
                "task_order": work_kwargs.get("task_order", 1),
                "before": work_kwargs.get("before", []),
                "after": work_kwargs.get("after", []),
                "shared": work_kwargs.get("shared", False),
                "options": work_kwargs.get("options", {}),
                "log": work_kwargs.get("log", False)
            })

            args_normal = t.clean_args(function_, work_kwargs["args"], work_kwargs["kwargs"])
            if args_normal == None or args_normal == False:
                raise Exception("Args and Kwargs do not match")

            # function_, args, kwargs, work_args, work_kwargs
            fn_task = {
                "name": work_kwargs.get("name"),
                "task_order": work_kwargs.get("task_order"),
                "function": function_,
                "workflow_args": work_args,
                "workflow_kwargs": work_kwargs,
                "log": work_kwargs.get("log")
            }
            t.setter("tasks", fn_task, t)

            # print("Workflow add_tasks - Task added: ",
            #       work_kwargs.get("name"))
            # print("Workflow add_tasks - Task Present: ", t.getter("tasks", 1))

        return add_tasks()
    return get_decorator


if __name__ == "__main__":
    plugin = PluginBase()


__all__ = [
    "ClosureBase", "SharedBase", "UtilsBase", "ConcurencyBase",
    "TimerBase", "LogBase", "CommandsBase", "EventsBase", "QueuesBase", "SocketsBase",
    "HooksBase", "ActionsBase", "EPubSubBase", "IPubSubBase", "WebhooksBase",
    "SSHBase", "AuthenticationBase", "SQLORMBase", "PluginBase", "WorkflowBase",
    "Tasks", "workflow"
]
