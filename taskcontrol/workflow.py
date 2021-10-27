# # Project Workflow

from taskcontrol.interfaces import AuthsBase, SocketsBase, HooksBase, SQLBase, LogsBase, TimeBase, CommandsBase
from taskcontrol.bases import WorkflowBase, PluginBase
from taskcontrol.bases import Queues, Actions, Events, Hooks
from taskcontrol.bases import Sockets, EPubSub, IPubSub, SSH
from taskcontrol.bases import ConcurencyBase, AuthenticationBase
from taskcontrol.bases import LogBase, TimerBase, UtilsBase, CommandBase, SQLORM


class Tasks(WorkflowBase):

    def __init__(self):
        super().__init__()
        #     print(self.shared.getter("tasks", 1))

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

    def run(self, tasks):
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


def workflow(*workflow_args, **workflow_kwargs):

    def get_decorator(function_):

        def add_tasks(*function_args, **function_kwargs):
            # print((function_, function_args, function_kwargs, workflow_args, workflow_kwargs))
            if type(workflow_kwargs.get("args")) != list:
                workflow_kwargs["args"] = []
            if type(workflow_kwargs.get("kwargs")) != dict:
                workflow_kwargs["kwargs"] = {}

            workflow_kwargs.update({
                "args": workflow_kwargs.get("args", []),
                "kwargs": workflow_kwargs.get("kwargs", {})
            })

            t = workflow_kwargs.get("task_instance")
            if not t:
                raise TypeError("Task instance not provided")

            if not workflow_kwargs.get("name"):
                raise TypeError("Name Argument not provided")

            workflow_kwargs.update({
                "before": workflow_kwargs.get("before", []),
                "after": workflow_kwargs.get("after", []),
                "shared": workflow_kwargs.get("shared", False),
                "options": workflow_kwargs.get("options", {}),
                "log": workflow_kwargs.get("log", False)
            })

            args = []
            if len(workflow_kwargs["args"]) > 0:
                for i in workflow_kwargs["args"]:
                    args.append(i)

            kwargs = {}
            if len(workflow_kwargs["kwargs"]) > 0:
                for i in workflow_kwargs["kwargs"].keys():
                    kwargs.update(workflow_kwargs["kwargs"][i])

            # if len(function_kwargs) > 0:
            #     kwargs.update(**function_kwargs)

            args_normal = t.clean_args(
                function_, workflow_kwargs["args"], workflow_kwargs["kwargs"])

            if args_normal == None or args_normal == False:
                raise Exception("Args and Kwargs do not match")

            # function_, args, kwargs, workflow_args, workflow_kwargs

            fn_task = {
                "name": workflow_kwargs.get("name"),
                "task_order": workflow_kwargs.get("task_order"),
                "function": function_,
                "args": workflow_kwargs.get("args"),
                "kwargs": workflow_kwargs.get("kwargs"),
                "workflow_args": workflow_args,
                "workflow_kwargs": workflow_kwargs,
                "log": workflow_kwargs.get("log")
            }
            t.setter("tasks", fn_task, t)

            # print("Workflow add_tasks - Task added: ",
            #       workflow_kwargs.get("name"))
            # print("Workflow add_tasks - Task Present: ", t.getter("tasks", 1))

        return add_tasks()
    return get_decorator


__all__ = [
    "SocketsBase", "HooksBase", "LogsBase",
    "TimeBase", "SQLBase", "AuthsBase",
    "CommandsBase", "PluginsBase",
    "PluginBase", "UtilsBase", "CommandBase", "ConcurencyBase",
    "LogBase", "TimerBase", "AuthenticationBase",
    "SQLORM", "Actions", "Events", "Queues", "Sockets",
    "Hooks", "Webhooks", "EPubSub", "IPubSub", "SSH",
    "Tasks", "workflow"
]
