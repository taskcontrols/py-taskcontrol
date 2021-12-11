# # Project Workflow
# Add support for Concurrency

import copy
from taskcontrol.lib.utils import ClosureBase, SharedBase, UtilsBase, ConcurencyBase, TimerBase, LogBase, CommandsBase
from taskcontrol.lib.utils import EventsBase, QueuesBase, SocketsBase, HooksBase, ActionsBase
from taskcontrol.lib.utils import EPubSubBase, IPubSubBase, WebhooksBase, SSHBase
from taskcontrol.lib.orm import SQLORMBase, AuthenticationBase
from taskcontrol.lib.interfaces import PluginsInterface


class PluginBase(UtilsBase, PluginsInterface):
    """
    `PluginsBase` class to create a plugin. Retuns a verified plugins object \n
    Allow invocation of workflow [todo] or task from within plugin \n

    ##### Instance Methods
    @`plugin_create` \n

    """

    # return plugin instance/module (plugin_instance)
    def plugin_create(self, name, definition):
        """
        Define and Create a plugin using plugin_create \n
        { `name` (str), `definition` (dict) }
        `name`: type(str) \n
        Name of the plugin to create \n
        `definition`: type(dict) \n
        Definition of the plugin object \n
        { `config` (dict), `ctx` (dict), `plugins` (dict), `shared` (dict),  `tasks` (dict),  `workflows` (dict), menu_command (dict) (bool) (None) } \n
            `config`: type(dict)
            `ctx`: type(dict)
            `plugins`: type(dict)
            `shared`: type(dict)
            `tasks`: type(dict)
            `workflows`: type(dict)
            `menu_command`: type(dict) or type(None) or type(bool) \n

            menu_command options: \n
            { `title` (str), `command` (dict), `required` (bool), `nargs` (int) (str), `help` (str) }

        """

        # TODO: Apply multiple instances (Allow seperate and merged instances)
        # Low priority
        if type(definition) != dict:
            raise TypeError("plugins definition has an issue")

        if type(definition) == dict:
            if not definition.get("config"):
                raise ValueError("config definition has an issue")
            if not definition.get("ctx"):
                raise ValueError("ctx definition has an issue")
            if not definition.get("plugins"):
                raise ValueError("internal plugins definition has an issue")
            if not definition.get("shared"):
                raise ValueError("shared definition has an issue")
            if not definition.get("tasks"):
                raise ValueError("tasks definition has an issue")
            if not definition.get("workflows"):
                raise ValueError("workflows definition has an issue")
            if not definition.get("menu_command"):
                definition["menu_command"] = False

        if type(name) == str:
            return {
                "plugin": dict([
                    [
                        name, {
                            "config": definition.get("config"), "ctx": definition.get("ctx"),
                            "plugins": definition.get("plugins"), "shared": definition.get("shared"),
                            "tasks": definition.get("tasks"), "workflows": definition.get("workflows")
                        }
                    ],
                    [
                        "menu_command", definition.get("menu_command")
                    ]
                ])
            }


class WorkflowBase(ClosureBase, ConcurencyBase, PluginBase, UtilsBase):
    """
    `WorkflowBase` to run the defined workflow. \n
    Use the Workflow Class to work with your class. This is intended to be the library logic file. \n

    ##### Instance Methods
    @`merge_tasks` \n
    @`reducer` \n
    @`run_task` \n

    """

    def __init__(self):
        """
        """
        super().__init__()
        # ConcurencyBase.__init__(self)
        # PluginsBase.__init__(self)
        self.shared = SharedBase.getInstance()
        self.getter, self.setter, self.deleter = self.class_closure(
            tasks={}, plugins={}, ctx={})

    def merge_tasks(self, tasks, inst, shared=None, clash_prefix=None):
        """
        """
        pass

    def reducer(self, result, task):
        """
        """
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
            if not hasattr(args, '__call__'):
                r_ = fn(self.getter("ctx", 1), result_, *args, **kwargs)
            else:
                if not hasattr(kwargs, '__call__'):
                    r_ = fn(self.getter("ctx", 1), result_, args(), **kwargs)
                else:
                    r_ = fn(self.getter("ctx", 1), result_, args(), kwargs())
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
        """
        """
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

        print("\nINSTANTIATING TASK NAMED: ", task.get("name"), "\n")
        tasks_to_run_in_task = [None, *before, fn_task, *after]

        import functools
        return functools.reduce(self.reducer, tasks_to_run_in_task)


class Workflow(WorkflowBase):
    """
    `Workflow` class to define a workflow

    ##### Instance Methods
    @`plugin_register` \n
    @`merge` \n
    @`create_workflow` \n
    @`get_all_tasks` \n
    @`start` \n

    """

    def __init__(self):
        super().__init__()

    def plugin_register(self, plugin_instance):
        """
        Register a defined plugin using `.plugin_register` \n
        { `plugin_instance` (`plugin` instance) } \n
        """
        pass

    def merge(self, inst, shared=False, clash_prefix=None):
        """
        Merge an Workflow with instance using `.merge` \n
        { `inst` (`plugin` instance), `shared` (bool), `clash_prefix` (str) } \n
        """
        pass

    def create_workflow(self, name, workflows, options):
        """
        Create an Workflow with definitions using `.create_workflow` \n
        { `name` (str), `workflows` (), `options` () }
        """
        pass

    def get_all_tasks(self, tasks, tsk=[]):
        """
        Get all tasks that you define from the workflow instance using `.get_all_tasks` \n
        { `tasks` (str) or (list) or (tuple), `tsk` (list) } \n
        """
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

    def start(self, tasks=["1"]):
        """
        Start the workflow tasks initantiation using `.start` \n
        `tasks`: type(str) or type(int) or type(list) or type(tuple) \n
        Tasks that need to be run \n
        Value Options: [ "1", 1, "shared:1", "shared:task", "task", ["shared:task", "task"], ("shared:task", "task") ] [Default: 1] \n
        """
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


def task(*work_args, **work_kwargs):
    """
    `task` Decorator to create a task \n
    `task` named kwargs: \n
    { `name` (str), `task_instance` (`Workflow` instance), `task_order` (int), `shared` (bool), `args` (list) or (tuple) or (function), `kwargs` (dict) or (function), `before` (tuple) or (list) or (dict), `after` (tuple) or (list) or (dict), `log` (bool) } \n
    ##### `task` NAMED KWARGS DEFINITION:
    `name`: type(str) \n
    `task_instance`: type(`Workflow` instance) \n
    `task_order`: type(int) \n
    [Default is int 1] \n
    `shared`: type(bool) \n
    Value Options [ True, False ] [Default is bool False] \n
    `args`: type(list) or type(tuple) or type(function) \n
    [Default is a empty list [] ] \n
    `kwargs`: type(dict) or type(function) \n
    [Default is a empty dict {}] \n
    `before` or `after` middleware task dict keys as a dict or list: \n
    Middleware object structure: { name, function, args, kwargs, options } [Default is empty list []] \n
    `log`: type(bool) \n
    Value Options [ True or False ].  [Default is bool False]
    """
    def get_decorator(function_):

        def add_tasks(*function_args, **function_kwargs):
            if not work_kwargs.get("name"):
                raise TypeError("Name Argument or task instance not provided")

            if type(work_kwargs.get("args")) != list or type(work_kwargs.get("args")) != tuple or not hasattr(work_kwargs.get("args"), '__call__'):
                work_kwargs["args"] = work_kwargs.get("args", [])
            if type(work_kwargs.get("kwargs")) != dict or not hasattr(work_kwargs.get("kwargs"), '__call__'):
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

            # args_normal = t.clean_args(
            #         function_, work_kwargs["args"], work_kwargs["kwargs"])
            if (True if (len(function_.__code__.co_varnames) == 4) else False) in [None, False]:
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
    "ClosureBase", "SharedBase", "UtilsBase", "ConcurencyBase",
    "TimerBase", "LogBase", "CommandsBase", "EventsBase", "QueuesBase", "SocketsBase",
    "HooksBase", "ActionsBase", "EPubSubBase", "IPubSubBase", "WebhooksBase",
    "SSHBase", "AuthenticationBase", "SQLORMBase", "PluginBase", "WorkflowBase",
    "Workflow", "task"
]
