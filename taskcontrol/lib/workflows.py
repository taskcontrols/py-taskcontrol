# # Project Workflow

import copy
from taskcontrol.lib.bases import WorkflowBase


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


__all__ = [
    "Tasks", "workflow"
]
