# # Project Workflow
# Goal: Manage Workflow and related middlewares


def tasks():

    tasks = {
        "taskname": {}
    }

    def clean_args(fn, wfargs, wfkwargs, fnca, fnckwa):
        # TODO: To be implemented
        # check if args and kwargs match to functions
        return {}

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
        # print("set_task: test 3")
        # print("set_task: ", tasks[kwargs["name"]][kwargs["task_order"]])

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
        "clean_args": clean_args,
        "set_task": set_task
    }


def workflow(*wfargs, **wfkwargs):

    def get_decorator(fn):
        # print("get_decorator: test 1")
        # print("get_decorator: args ", args)
        # print("get_decorator: kwargs ", kwargs)
        # print("get_decorator: ", fn)

        # check before middlewares args and kwargs number and validity
        # check after middlewares args and kwargs number and validity

        def order_tasks(*fnca, **fnckwa):

            global tasks
            t = tasks()

            # TODO: To be implemented
            # clean_decorator = t.clean_args( fn, wfargs, wfkwargs, fnca, fnckwa )

            # if not clean_decorator:
            #     raise Exception("Args and KwArgs do not match", clean_decorator)

            t["set_task"](fn, fnca, fnckwa, wfargs, wfkwargs)

            # print("order_tasks: test 3")
            # print("order_tasks: ", tasks[kwargs["name"]][kwargs["task_order"]])

        return order_tasks
    return get_decorator
