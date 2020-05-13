# # Project Workflow


from sys import path
path.append('./')

from .bases import WorkflowBase, PluginsBase
from .hooks import SocketsBase, HooksBase
from .authentication import AuthenticationBase, AuthBase
from .concurrency import ConcurencyBase
from .logger_timer import LoggerBase, TimerBase


class Tasks(WorkflowBase):

    # add plugin to instance or shared
    def plugin_register(self, plugin_instance):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")

        if type(plugin_instance) != dict:
            raise TypeError("plugins definition has an issue")
        if type(plugin_instance) == dict:
            # if not plugin_instance.get("config"):
            #     raise ValueError("config definition has an issue")
            # if not plugin_instance.get("ctx"):
            #     raise ValueError("ctx definition has an issue")
            # if not plugin_instance.get("plugins"):
            #     raise ValueError("internal plugins definition has an issue")
            # if not plugin_instance.get("shared"):
            #     raise ValueError("shared definition has an issue")
            # if not plugin_instance.get("tasks"):
            #     raise ValueError("tasks definition has an issue")
            pass

    def merge(self, inst, shared=False, clash_prefix=None):

        # TODO: Add Logger

        # TODO: Add Authentication
        # if not is_authenticated():
        #     raise Exception("Not authenticated")
        if shared == True:
            # Check this based on new closure ways
            # TODO: Tests pending
            self.shared.tasks = self.merge_tasks(
                self.shared.tasks, inst, shared, clash_prefix
            )
        elif shared == False:
            # Check this based on new closure ways
            # TODO: Tests pending
            self.tasks = self.merge_tasks(
                self.tasks, inst, shared, clash_prefix
            )

    def run(self, tasks):

        # print("Workflow task list provided being instantiated: ", str(tasks))
        # add this to context (shared/local check design)
        result = []

        if isinstance(tasks, str) or type(tasks) == int:
            tasks = self.parse_tasks(tasks)

        if isinstance(tasks, str):
            # Iterate task through single task
            task_ = self.get_tasks(tasks)
            if not task_ == None:
                result.append(self.run_task(task_))
        elif isinstance(tasks, list):
            # Iterate task through tasks
            # reduce is a better and easier way. Compare looping ways
            for task_ in tasks:
                t = self.get_tasks(task_)
                if not t == None:
                    result.append(self.run_task(t))
        else:
            print("No workflow or task available to run")
        return result


def workflow(*workflow_args, **workflow_kwargs):

    # print("get_decorator: Decorator init ", "workflow_args: ", workflow_args, "workflow_kwargs: ", workflow_kwargs)

    def get_decorator(function_):

        # print("get_decorator: ", function_)
        def add_tasks(*function_args, **function_kwargs):

            # print("Workflow add_tasks: Decorator init ", "function_args: ", function_args, "function_kwargs: ", function_kwargs)
            # print((function_, function_args, function_kwargs, workflow_args, workflow_kwargs))
            workflow_kwargs.update({"function_args": function_args})
            workflow_kwargs.update({"function_kwargs": function_kwargs})

            t = workflow_kwargs.get("task_instance")
            if not t:
                raise TypeError("Task instance not provided")

            if not workflow_kwargs.get("name"):
                raise TypeError("Name Argument not provided")

            if not workflow_kwargs.get("args"):
                workflow_kwargs["args"] = []
            if not workflow_kwargs.get("kwargs"):
                workflow_kwargs["kwargs"] = {}

            if not workflow_kwargs.get("before"):
                workflow_kwargs["before"] = []
            if not workflow_kwargs.get("after"):
                workflow_kwargs["after"] = []
            if not workflow_kwargs.get("options"):
                workflow_kwargs["options"] = {}
            if not workflow_kwargs.get("log"):
                workflow_kwargs["log"] = False

            args = []
            if len(workflow_args):
                args.append(*workflow_args)
            if len(function_args):
                args.append(*function_args)

            kwargs = {}
            if len(workflow_args):
                kwargs.update(**workflow_kwargs)
            if len(function_args):
                kwargs.update(**function_kwargs)

            args_normal = t.clean_args(
                function_, workflow_kwargs["args"], workflow_kwargs["kwargs"])

            if args_normal == None:
                raise Exception("Args and Kwargs do not match")

            # TODO: Add Logger

            # TODO: Add Authentication
            # if not is_authenticated():
            #     raise Exception("Not authenticated")

            t.set_tasks(
                function_, args, kwargs,
                workflow_args, workflow_kwargs
            )

            print("Workflow add_tasks - Task added: ",
                  workflow_kwargs.get("name"))
        return add_tasks()
    return get_decorator


__all__ = ["Tasks", "workflow", "AuthenticationBase",
           "SocketsBase", "TimerBase", "LoggerBase"]
