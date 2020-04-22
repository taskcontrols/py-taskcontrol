# # Project Workflow


from sys import path
path.append('./')


def workflow(*workflow_args, **workflow_kwargs):

    def get_decorator(function_):
        # print("get_decorator: Decorator init ", "workflow_args: ", workflow_args, "workflow_kwargs: ", workflow_kwargs)
        # print("get_decorator: ", function_)

        def order_tasks(*function_args, **function_kwargs):
            # print("Workflow order_tasks: Decorator init ", "function_args: ", function_args, "function_kwargs: ", function_kwargs)
            # print((function_, function_args, function_kwargs, workflow_args, workflow_kwargs))
            t = workflow_kwargs.get("task_instance")

            if not t:
                raise Exception("Task instance not provided")
            # Check before/after middlewares args and kwargs number and validity
            args_normal = t.clean_args(function_, function_args, function_kwargs)

            if not args_normal:
                raise Exception("Args and KwArgs do not match")

            t.set_task(
                function_, function_args, function_kwargs,
                workflow_args, workflow_kwargs
            )
            print("Workflow order_tasks - Task added: ", workflow_kwargs.get("name"))
        return order_tasks
    return get_decorator


__all__ = ["workflow"]

