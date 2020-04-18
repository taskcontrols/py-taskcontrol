# # Project Workflow
# Goal: Manage Workflow and related middlewares

tasks = {
    "taskname": {}
}


class Task():

    def run_middleware(self, fn, error_obj, *args, **kwargs):
        try:
            return True, fn(args, kwargs)
        except Exception as e:
            if error_obj["error"] == "next":
                return 'next', error_obj["error_next_value"]
            elif error_obj["error"] == "error_handler":
                return 'error_handler', error_obj["error_handler"](e, error_obj["error_next_value"])
            elif error_obj["error"] == "exit":
                raise Exception("exit: Error during middleware: ",
                                fn.__name__, str(e))

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

    def get_task(self, task=None):
        global tasks
        if not isinstance(task, None) and isinstance(task, str):
            return tasks[task]
        return tasks

    def set_task(self, fn, fn_a, fn_kwa, wf_args, wf_kwargs):
        global tasks
        print("tasks.keys()", tasks.keys(), wf_kwargs["name"])
        
        if wf_kwargs["name"] not in tasks.keys():
            tasks[wf_kwargs["name"]] = {}

        if not isinstance(tasks[wf_kwargs["name"]], dict):
            tasks.update({wf_kwargs["name"]: {}})

        tasks[wf_kwargs["name"]].update({
            wf_kwargs["task_order"]: {
                "name": wf_kwargs["name"],
                "wf_args": wf_args, "wf_kwargs": wf_kwargs,
                "fn_a": fn_a, "fn_kwa": fn_kwa,
                "before": wf_kwargs["before"],
                "after": wf_kwargs["after"],
                "function": fn
            }
        })

        # print("set_task: Task added", kwargs["name"])
        # print("set_task: ", tasks[kwargs["name"]][kwargs["task_order"]])

    def run_task(self, task):
        global tasks
        if tasks[task]:
            print("Workflow found: ", task)
            print("The workflow object looks like this: ", tasks[task])

            # Put in try except block for clean errors

            # TODO: To be implemented

            # Iterate task through tasks

            #       Iterate through before for each task
            #           trigger before functions with next
            #           else if error based on option:
            #               trigger error_handler
            #               trigger next
            #               trigger exit

            #       Trigger task

            #       Iterate through after for each task
            #           trigger after functions with next
            #           else if error based on option:
            #               trigger error_handler
            #               trigger next
            #               trigger exit

    def run(self, task):
        if isinstance(task, str):
            self.run_task(task)
        elif isinstance(task, list):
            [self.run_task(t) for t in task]
        else:
            print("No workflow or task available to run")

    def setter(self):
        return {
            "get_task": self.get_task,
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
            t= Task()
            args_normal= t.clean_args(fn, wf_args, wf_kwargs, fn_a, fn_kwa)
            if not args_normal:
                raise Exception("Args and KwArgs do not match")
            
            # print((fn, fn_a, fn_kwa, wf_args, wf_kwargs))
            t.set_task(fn, fn_a, fn_kwa, wf_args, wf_kwargs)

            print("order_tasks - Task added: ", wf_kwargs["name"])
            # print("order_tasks: ", tasks[wf_kwargs["name"]][wf_kwargs["task_order"]])

        return order_tasks
    return get_decorator


__all__= ["Task", "workflow"]

