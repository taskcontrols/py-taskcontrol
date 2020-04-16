# # Project Workflow
# Goal: Manage Workflow and related middlewares


def tasks():

    tasks = {
        "taskname": {}
    }

    def next(obj):
        pass

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

    def clean_args(fn, wfargs, wfkwargs, fna, fnkwa):
        # TODO: To be implemented
        # check if args and kwargs match to functions
        return {}

    def set_task(fn, fna, fnkwa, wfargs, wfkwargs):

        if isinstance(tasks[wfkwargs["name"]], dict):
            tasks[wfkwargs["name"]] = {}

        tasks[wfkwargs["name"]][wfkwargs["task_order"]] = {
            "wf_args": wfargs,
            "wf_kwargs": wfkwargs,
            "fn_a": fna,
            "fn_kwa": fnkwa,
            "function": fn,
            "before": wfkwargs["before"],
            "after": wfkwargs["after"],
            "name": wfkwargs["name"]
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

    def setter():
        return {
            "tasks": tasks,
            "clean_args": clean_args,
            "run_middleware": run_middleware,
            "set_task": set_task
        }

    return {
        "run": run,
        "setter": setter
    }


def workflow(*wfargs, **wfkwargs):

    def get_decorator(fn):
        # print("get_decorator: Decorator init ", "wf_args: ", wfargs, "wf_kwargs: ", wfkwargs)
        # print("get_decorator: ", fn)

        # check before middlewares args and kwargs number and validity
        # check after middlewares args and kwargs number and validity

        def order_tasks(*fna, **fnkwa):

            global tasks
            t = tasks()["setter"]()

            # TODO: To be implemented
            # clean_decorator = t.clean_args( fn, wfargs, wfkwargs, fna, fnkwa )

            # if not clean_decorator:
            #     raise Exception("Args and KwArgs do not match", clean_decorator)

            t["set_task"](fn, fna, fnkwa, wfargs, wfkwargs)

            print("order_tasks - Task added: ", wfkwargs["name"])
            # print("order_tasks: ", t["tasks"][wfkwargs["name"]][wfkwargs["task_order"]])

        return order_tasks
    return get_decorator
