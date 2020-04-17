# # Project Workflow
# Goal: Manage Workflow and related middlewares
# TODO: Moving to clas based decorator seems more beneficial

def tasks():

    tasks = {
        "taskname": {}
    }

    def run_middleware(fn, error_obj, *args, **kwargs):
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

    def clean_args(fn, wf_args, wf_kwargs, fn_a, fn_kwa):
        tpl = fn.__code__.co_varnames
        k_fn_kwa = fn_kwa.keys()
        l_tpl, l_fn_a, l_k_fn_kwa = (len(tpl), len(fn_a), len(k_fn_kwa))
        if (l_tpl == l_fn_a + l_k_fn_kwa):
            for k in k_fn_kwa:
                if not tpl.index(k) >= l_fn_a:
                    return False
            return True
        return False

    def get_task(task=None):
        if not isinstance(task, None) and isinstance(task, str):
            return tasks[task]
        return tasks

    def set_task(fn, fn_a, fn_kwa, wf_args, wf_kwargs):

        if isinstance(tasks[wf_kwargs["name"]], dict):
            tasks[wf_kwargs["name"]] = {}

        tasks[wf_kwargs["name"]][wf_kwargs["task_order"]] = {
            "name": wf_kwargs["name"],
            "wf_args": wf_args, "wf_kwargs": wf_kwargs,
            "fn_a": fn_a, "fn_kwa": fn_kwa,
            "before": wf_kwargs["before"],
            "after": wf_kwargs["after"],
            "function": fn
        }
        # print("set_task: Task added", kwargs["name"])
        # print("set_task: ", tasks[kwargs["name"]][kwargs["task_order"]])

    def run_task(task):
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

    def run(task):
        if isinstance(task, str):
            run_task(task)
        elif isinstance(task, list):
            [run_task(t) for t in task.items()]
        else:
            print("No workflow or task available to run")

    def setter():
        return {
            "get_task": get_task, "set_task": set_task,
            "run_task": run_task,
            "clean_args": clean_args,
            "run_middleware": run_middleware
        }

    return {
        "run": run,
        "setter": setter
    }


def workflow(*wf_args, **wf_kwargs):

    def get_decorator(fn):
        # print("get_decorator: Decorator init ", "wf_args: ", wf_args, "wf_kwargs: ", wf_kwargs)
        # print("get_decorator: ", fn)

        # check before middlewares args and kwargs number and validity
        # check after middlewares args and kwargs number and validity

        def order_tasks(*fn_a, **fn_kwa):
            # print("order_tasks: Decorator init ", "fn_a: ", fn_a, "fn_kwa: ", fn_kwa)
            global tasks
            t = tasks()["setter"]()
            args_normal = t["clean_args"](fn, wf_args, wf_kwargs, fn_a, fn_kwa)
            if not args_normal:
                raise Exception("Args and KwArgs do not match")

            t["set_task"](fn, fn_a, fn_kwa, wf_args, wf_kwargs)

            print("order_tasks - Task added: ", wf_kwargs["name"])
            # print("order_tasks: ", t["tasks"][wf_kwargs["name"]][wf_kwargs["task_order"]])

        return order_tasks
    return get_decorator
