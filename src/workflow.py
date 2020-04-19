# # Project Workflow
# Goal: Manage Workflow and related middlewares
# TODO: Make unusable WorkflowBase methods private
# TODO: Add Simple scalable plugin system


class WorkflowBase():

    tasks = {
        "taskname": {}
    }

    plugins = {
        "pluginname": {
            "taskname": {}
        }
    }


    def __run_middleware(self, fn, error_obj, log, *args, **kwargs):
        try:
            if log:
                print("Workflow running middleware function: ", fn.__name__)
            return True, fn(*args, **kwargs)
        except Exception as e:
            if log:
                print("Running error for middleware")

            if not hasattr(error_obj, "error"):
                error_obj["error"] = "exit"

            ero = error_obj.get("error")
            erno = error_obj.get("error_next_value")

            if ero == "next":
                return 'next', (e, erno)
            elif ero == "error_handler":
                if not hasattr(error_obj, "error_handler"):
                    return "error_handler", (e, erno)
                return 'error_handler', error_obj.get("error_handler")(e, erno)
            elif ero == "exit":
                raise Exception("error_obj['error'] exit: Error during middleware: ",
                                fn.__name__, str(e))
            else:
                raise Exception(
                    "Error during middleware: flow[options[error]] value error")


    def __get_md_args(self, f, action, log):
        
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


    def __setup_run_middleware(self, task, md_action, log):

        #       Iterate through before/after for each task
        #           trigger before functions with next
        #           if there is an error, then based on option:
        #               trigger error_handler
        #               trigger next
        #               trigger exit

        actions = task.get("wf_kwargs").get(md_action)
        log  = task.get("wf_kwargs").get("log")

        if actions and isinstance(actions, list):
            for action in actions:
                fn = action.get("function")
                err_obj, a, kwa = self.__get_md_args(fn, action, log)
                self.__run_middleware(fn, err_obj, log, *a, **kwa)
        elif actions and isinstance(actions, dict):
            err_obj, a, kwa = self.__get_md_args(
                actions.get("function"), actions, log)
            self.__run_middleware(actions.get("function"),
                                 err_obj, log, *a, **kwa)


    def clean_args(self, fn, wf_args, wf_kwargs, fn_a, fn_kwa):
        
        tpl = fn.__code__.co_varnames
        k_fn_kwa = fn_kwa.keys()
        l_tpl, l_fn_a, l_k_fn_kwa = len(tpl), len(fn_a), len(k_fn_kwa)

        if (l_tpl == l_fn_a + l_k_fn_kwa):
            for k in k_fn_kwa:
                if not tpl.index(k) >= l_fn_a:
                    return False
            return True
        return False


    def get_tasks(self, task=None):
        
        if task and isinstance(task, str):
            return self.tasks.get(task)
        return self.tasks


    def set_task(self, fn, fn_a, fn_kwa, wf_args, wf_kwargs):

        wfname = wf_kwargs.get("name")
        # print("tasks.keys() ", tasks.keys())

        print("Workflow task name to add: ", wfname)

        if wfname not in self.tasks.keys():
            self.tasks[wfname] = {}

        if not isinstance(self.tasks[wfname], dict):
            self.tasks.update({wfname: {}})

        self.tasks[wfname].update({
            "task_order": wf_kwargs["task_order"],
            "wf_args": wf_args, "wf_kwargs": wf_kwargs,
            "fn_a": fn_a, "fn_kwa": fn_kwa,
            "before": wf_kwargs["before"],
            "after": wf_kwargs["after"],
            "function": fn
        })

        print("Workflow set_task: Adding Task: ", wfname)
        # print("Workflow set_task: ", tasks[kwargs["name"]][kwargs["task_order"]])


    def run_task(self, task):

        tsk = self.get_tasks(task)
        log = tsk.get("log")

        if log:
            print("Workflow task found: ", tsk.get("name"))
            # print("The workflow object looks like this: ", tsk)

        if tsk:
            # TODO: Put in try except block for clean errors

            #       Iterate through before for each task
            if log:
                print("Workflow before middlewares for task now running: ",
                      task.get("name"))
            self.__setup_run_middleware(tsk, "before", log)

            #       Invoke task
            if log:
                print("Workflow task run: ", task.get("name"))
            tsk.get("function")(*tsk.get("fn_a"), **tsk.get("fn_kwa"))

            #       Iterate through after for each task
            if log:
                print("Workflow after middlewares for task now running: ",
                      task.get("name"))
            self.__setup_run_middleware(tsk, "after", log)


    def merge_instance(self, inst, clash_prefix):
        pass


class Tasks(WorkflowBase):


    def add_plugin(self, plugin_inst):
        pass


    def merge(self, inst, clash_prefix):
        self.merge_instance(inst, clash_prefix)


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
            "run_task": self.run_task,
            "clean_args": self.clean_args
        }


def workflow(*wf_args, **wf_kwargs):


    def get_decorator(fn):
        # print("get_decorator: Decorator init ", "wf_args: ", wf_args, "wf_kwargs: ", wf_kwargs)
        # print("get_decorator: ", fn) 
        
        def order_tasks(*fn_a, **fn_kwa):
            # print("Workflow order_tasks: Decorator init ", "fn_a: ", fn_a, "fn_kwa: ", fn_kwa)

            t = wf_kwargs.get("task_instance")
            if not t:
                raise Exception("Task instance not provided")

            # Check before/after middlewares args and kwargs number and validity
            args_normal = t.clean_args(fn, wf_args, wf_kwargs, fn_a, fn_kwa)

            if not args_normal:
                raise Exception("Args and KwArgs do not match")

            # print((fn, fn_a, fn_kwa, wf_args, wf_kwargs))
            t.set_task(fn, fn_a, fn_kwa, wf_args, wf_kwargs)

            print("Workflow order_tasks - Task added: ", wf_kwargs.get("name"))

        return order_tasks
    return get_decorator


__all__ = ["Tasks", "workflow"]

