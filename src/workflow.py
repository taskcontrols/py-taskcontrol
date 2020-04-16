# # Project Workflow
# Goal: Manage Workflow and related middlewares


def clean_args(fn, wfargs, wfkwargs, fnca, fnckwa):
    # TODO: To be implemented
    # check if args and kwargs match to functions
    return {}


def tasks():

    tasks = {
        "taskname": {}
    }

    def set_task(fn, fnca, fnckwa, wfargs, wfkwargs):

        if isinstance(tasks[wfkwargs["name"]], dict):
            tasks[wfkwargs["name"]] = {}

        tasks[wfkwargs["name"]][wfkwargs["task_order"]] = {
            "wf_args": wfargs,
            "wf_kwargs": wfkwargs,
            "fnca": fnca,
            "fnckwa": fnckwa,
            "function": fn,
            "function_name": fn.__name__,
            "before": wfkwargs["before"],
            "after": wfkwargs["after"],
            "name": wfkwargs["name"]
        }

    def run(task):

        # [print(t) for t in tasks.items()]
        if tasks[task]:
            print("Workflow found: ", task)
            print("The workflow object looks like this: ")
            print(tasks[task])
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

    return {
        "run": run,
        "set_task": set_task
    }


def workflow(*wfargs, **wfkwargs):

    def get_decorator(fn):
        # print("test 1")
        # print("args ", args)
        # print("kwargs ", kwargs)
        # print(fn)

        # check before middlewares args and kwargs number and validity
        # check after middlewares args and kwargs number and validity

        def order_tasks(*fnca, **fnckwa):
            # TODO: To be implemented
            # clean_decorator = clean_args(
            #     fn, wfargs, wfkwargs, fnca, fnckwa)

            # if not clean_decorator:
            #     raise Exception("Args and KwArgs do not match",
            #                     clean_decorator)

            global tasks
            t = tasks()
            t["set_task"](fn, fnca, fnckwa, wfargs, wfkwargs)

            # print("test 3")
            # print(tasks[kwargs["name"]][kwargs["task_order"]])

        return order_tasks
    return get_decorator
