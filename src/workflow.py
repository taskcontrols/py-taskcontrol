# # Project Workflow
# Goal: Manage Workflow and related middlewares


def clean_args_kwargs(fn, wfargs, wfkwargs, fnca, fnckwa):
    # TODO: To be implemented
    # check if args and kwargs match to functions
    return {}


def run(task):
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

    # [print(t) for t in tasks["tasks"].items()]
    if tasks["tasks"][task]:
        print("Workflow found: ", task)
        print("The workflow object looks like this: ")
        print(tasks["tasks"][task])


tasks = {
    "tasks": {
        "taskname": {}
    },
    "run": run
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
            # clean_decorator = clean_args_kwargs(
            #     fn, wfargs, wfkwargs, fnca, fnckwa)

            # if not clean_decorator:
            #     raise Exception("Args and KwArgs do not match",
            #                     clean_decorator)

            global tasks

            # print("test 2")
            # print(tasks["tasks"][kwargs["name"]])

            if isinstance(tasks["tasks"][wfkwargs["name"]], dict):
                tasks["tasks"][wfkwargs["name"]] = {}

            tasks["tasks"][wfkwargs["name"]][wfkwargs["task_order"]] = {
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

            # print("test 3")
            # print(tasks["tasks"][kwargs["name"]][kwargs["task_order"]])

        return order_tasks
    return get_decorator
