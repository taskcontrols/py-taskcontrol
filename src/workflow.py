# # Project Workflow
# Goal: Manage Workflow and related middlewares
# TODO: Change all object attribute fetches to .get(attr) method

tasks = {
    "taskname": {}
}


class WorkflowBase():

    def run_middleware(self, fn, error_obj, log, *args, **kwargs):
        try:
            if log:
                print("Workflow run middleware function: ", fn.__name__)
            return True, fn(*args, **kwargs)
        except Exception as e:
            if log:
                print("Running error for middleware")
            
            if not hasattr(error_obj, "error"):
                error_obj["error"] = "next"
            
            ero = error_obj.get("error")
            erno = error_obj.get("error_next_value")

            if ero == "next":
                return 'next', (e, erno)
            elif ero == "error_handler":
                if not hasattr(error_obj, "error_handler"):
                    if hasattr(error_obj, "error_next_value"):
                        return "error_handler", (e, erno)
                    return "error_handler", (e, None)
                return 'error_handler', error_obj.get("error_handler")(e, erno)
            elif ero == "exit":
                raise Exception("error_obj['error'] exit: Error during middleware: ",
                                fn.__name__, str(e))
            else:
                raise Exception(
                    "Error during middleware: flow[options[error]] value error")

    def setup_run_middleware(self, task, md_action, log):
        
        def get_md_args(f, action, log):
                    f_dt = action.get("flow").get(f.__name__)

                    if f_dt and isinstance(f_dt, dict):
                        a, kwa, err_obj = [], {}, {}
                        if "args" in f_dt and isinstance(f_dt.get("args"), list):
                            a = f_dt.get("args")
                        if "kwargs" in f_dt and isinstance(f_dt.get("kwargs"), dict):
                            kwa = f_dt.get("kwargs")
                        if "options" in f_dt and isinstance(f_dt.get("options"), dict):
                            err_obj = f_dt.get("options")
                    return err_obj, log, a, kwa

        #       Iterate through before/after for each task
        #           trigger before functions with next
        #           if there is an error, then based on option:
        #               trigger error_handler
        #               trigger next
        #               trigger exit

        actions = task.get("wf_kwargs").get(md_action)
        if actions and isinstance(actions, list):
            for action in actions:
                
                fns_list = action.get("functions")
                
                if fns_list and isinstance(fns_list, list):
                    for f in fns_list:
                        err_obj, log, a, kwa = get_md_args(f, action, log)
                        self.run_middleware(f, err_obj, log, *a, **kwa)
                elif fns_list and hasattr(fns_list, callable):
                    err_obj, log, a, kwa = get_md_args(fns_list, action, log)
                    self.run_middleware(fns_list, err_obj, log, *a, **kwa)
                else:
                    pass

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
        global tasks
        if task and isinstance(task, str):
            return tasks.get(task)
        return tasks

    def set_task(self, fn, fn_a, fn_kwa, wf_args, wf_kwargs):
        global tasks

        wfname = wf_kwargs.get("name")
        # print("tasks.keys() ", tasks.keys())
        print("Workflow task name to add: ", wfname)

        if wfname not in tasks.keys():
            tasks[wfname] = {}

        if not isinstance(tasks[wfname], dict):
            tasks.update({wfname: {}})

        tasks[wfname].update({
            "task_order": wf_kwargs["task_order"],
            "wf_args": wf_args, "wf_kwargs": wf_kwargs,
            "fn_a": fn_a, "fn_kwa": fn_kwa,
            "before": wf_kwargs["before"],
            "after": wf_kwargs["after"],
            "function": fn
        })

        print("Workflow set_task: Task added: ", wfname)
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
                print("Workflow before middlewares for task now running: ", task.get("name"))
            self.setup_run_middleware(tsk, "before", log)

            #       Invoke task
            if log:
                print("Workflow task run: ", task.get("name"))
            tsk.get("function")(*tsk.get("fn_a"), **tsk.get("fn_kwa"))

            #       Iterate through after for each task
            if log:
                print("Workflow after middlewares for task now running: ", task.get("name"))
            self.setup_run_middleware(tsk, "after", log)


class Task(WorkflowBase):
    def run(self, task):
        if isinstance(task, str):
            # Iterate task through single task
            print("Workflow task provided instantiated.")
            self.run_task(task)
        elif isinstance(task, list):
            # Iterate task through tasks
            print("Workflow task list provided instantiated.")
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

            print("order_tasks - Task added: ", wf_kwargs.get("name"))

        return order_tasks
    return get_decorator


__all__ = ["Task", "workflow"]
