# # Project Workflow
# Goal: Manage Workflow and related middlewares
# TODO: Change all object attribute fetches to .get(attr) method

tasks = {
    "taskname": {}
}


class Task():

    def run_middleware(self, fn, error_obj={}, *args, **kwargs):
        try:
            if args and kwargs:
                return True, fn(args, kwargs)
            elif args and not kwargs:
                return True, fn(args)
            elif not args and kwargs:
                return True, fn(kwargs)
            else:
                return True, fn()
        except Exception as e:
            if not hasattr(error_obj, "error"):
                error_obj["error"] = "next"

            if error_obj["error"] == "next":
                return 'next', (e, error_obj["error_next_value"])
            elif error_obj["error"] == "error_handler":
                if not hasattr(error_obj, "error_handler"):
                    if hasattr(error_obj, "error_next_value"):
                        return "error_handler", (e, error_obj["error_next_value"])
                    return "error_handler", (e, None)
                return 'error_handler', error_obj["error_handler"](e, error_obj["error_next_value"])
            elif error_obj["error"] == "exit":
                raise Exception("error_obj['error'] exit: Error during middleware: ",
                                fn.__name__, str(e))
            else:
                raise Exception(
                    "Error during middleware: flow[options[error]] value error")

    def setup_run_middleware(self, tsk, md_action):
        #       Iterate through before/after for each task
        #           trigger before functions with next
        #           if there is an error, then based on option:
        #               trigger error_handler
        #               trigger next
        #               trigger exit

        if tsk["wf_kwargs"][md_action] and isinstance(tsk["wf_kwargs"][md_action], list):

            for bf in tsk["wf_kwargs"][md_action]:
                if bf["functions"] and isinstance(bf["functions"], list):
                    for f in bf["functions"]:
                        if bf["flow"][f.__name__] and isinstance(bf["flow"][f.__name__], dict):
                            f_dt = bf["flow"][f.__name__]
                            a = []
                            kwa = {}
                            err_obj = {}
                            if "args" in f_dt and isinstance(f_dt["args"], list):
                                a = f_dt["args"]
                            if "kwargs" in f_dt and isinstance(f_dt["kwargs"], dict):
                                kwa = f_dt["kwargs"]
                            if "options" in f_dt and isinstance(f_dt["options"], dict):
                                err_obj = f_dt["options"]

                            self.run_middleware(f, err_obj, a, kwa)

                elif bf["functions"] and hasattr(bf["functions"], callable):
                    if bf["flow"][f.__name__] and isinstance(bf["flow"][f.__name__], dict):
                        f_dt = bf["flow"][f.__name__]
                        a = []
                        kwa = {}
                        err_obj = {}
                        if "args" in f_dt and isinstance(f_dt["args"], list):
                            a = bf["flow"][f.__name__]["args"]
                        if "kwargs" in f_dt and isinstance(f_dt["kwargs"], dict):
                            kwa = bf["flow"][f.__name__]["args"]
                        if "options" in f_dt and isinstance(f_dt["options"], dict):
                            err_obj = f_dt["options"]

                        self.run_middleware(f, err_obj, a, kwa)
                else:
                    pass

    def clean_args(self, fn, wf_args, wf_kwargs, fn_a, fn_kwa):
        tpl = fn.__code__.co_varnames
        k_fn_kwa = fn_kwa.keys()
        l_tpl, l_fn_a, l_k_fn_kwa = (len(tpl), len(fn_a), len(k_fn_kwa))
        if (l_tpl == l_fn_a + l_k_fn_kwa):
            for k in k_fn_kwa:
                if not tpl.index(k) >= l_fn_a:
                    return False
            return True
        return False

    def get_tasks(self, task=None):
        global tasks
        if task and isinstance(task, str):
            return tasks.get(task)
        return tasks

    def set_task(self, fn, fn_a, fn_kwa, wf_args, wf_kwargs):
        global tasks
        # print("tasks.keys() ", tasks.keys())
        print("task name to add: ", wf_kwargs["name"])

        if wf_kwargs["name"] not in tasks.keys():
            tasks[wf_kwargs["name"]] = {}

        if not isinstance(tasks[wf_kwargs["name"]], dict):
            tasks.update({wf_kwargs["name"]: {}})

        tasks[wf_kwargs["name"]].update({
            "task_order": wf_kwargs["task_order"],
            "wf_args": wf_args, "wf_kwargs": wf_kwargs,
            "fn_a": fn_a, "fn_kwa": fn_kwa,
            "before": wf_kwargs["before"],
            "after": wf_kwargs["after"],
            "function": fn
        })

        print("set_task: Task added", wf_kwargs["name"])
        # print("set_task: ", tasks[kwargs["name"]][kwargs["task_order"]])

    def run_task(self, task):
        global tasks

        tsk = self.get_tasks(task)

        if tsk:
            # print("Workflow found: ", task)
            # print("The workflow object looks like this: ", tsk)

            # Put in try except block for clean errors

            #       Iterate through before for each task
            self.setup_run_middleware(tsk, "before")
            #       Invoke task
            tsk["function"](tsk["fn_a"], tsk["fn_kwa"])
            #       Iterate through after for each task
            self.setup_run_middleware(tsk, "after")

    def run(self, task):
        if isinstance(task, str):
            # Iterate task through single task
            self.run_task(task)
        elif isinstance(task, list):
            # Iterate task through tasks
            [self.run_task(t) for t in task]
        else:
            print("No workflow or task available to run")

    def setter(self):
        return {
            "get_tasks": self.get_tasks,
            "set_task": self.set_task,
            "run_task": self.run_task,
            "clean_args": self.clean_args,
            "run_middleware": self.run_middleware
        }


def workflow(*wf_args, **wf_kwargs):

    def get_decorator(fn):
        # print("get_decorator: Decorator init ", "wf_args: ", wf_args, "wf_kwargs: ", wf_kwargs)
        # print("get_decorator: ", fn)

        # check before middlewares args and kwargs number and validity
        # check after middlewares args and kwargs number and validity

        def order_tasks(*fn_a, **fn_kwa):
            # print("order_tasks: Decorator init ", "fn_a: ", fn_a, "fn_kwa: ", fn_kwa)
            global Task
            global tasks
            t = Task()
            args_normal = t.clean_args(fn, wf_args, wf_kwargs, fn_a, fn_kwa)
            if not args_normal:
                raise Exception("Args and KwArgs do not match")

            # print((fn, fn_a, fn_kwa, wf_args, wf_kwargs))
            t.set_task(fn, fn_a, fn_kwa, wf_args, wf_kwargs)

            print("order_tasks - Task added: ", wf_kwargs["name"])

        return order_tasks
    return get_decorator


__all__ = ["Task", "workflow"]
