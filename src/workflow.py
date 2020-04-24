# # Project Workflow


from sys import path
path.append('./')

from .bases import WorkflowBase

class Tasks(WorkflowBase):

    def add_plugin(self, plugin_inst):
        pass

    def merge(self, inst, shared=False, clash_prefix=None):
        if shared == True:
            self.shared_tasks.tasks = self.merge_tasks(
                self.shared_tasks.tasks, inst, shared, clash_prefix
            )
        elif shared == False:
            self.tasks = self.merge_tasks(
                self.tasks, inst, shared, clash_prefix
            )

    def run(self, tasks):
        # print("Workflow task list provided being instantiated: ", str(tasks))
        # add this to context (shared/local check design)
        result = []

        if isinstance(tasks, str):
            # Iterate task through single task
            result.append(self.run_task(tasks))
        elif isinstance(tasks, list):
            # Iterate task through tasks
            # reduce is a better and easier way. Compare looping ways
            [result.append(self.run_task(task_)) for task_ in tasks]
        else:
            print("No workflow or task available to run")
        return result


def workflow(*workflow_args, **workflow_kwargs):
    # print("get_decorator: Decorator init ", "workflow_args: ", workflow_args, "workflow_kwargs: ", workflow_kwargs)
    def get_decorator(function_):
        # print("get_decorator: ", function_)
        def order_tasks(*function_args, **function_kwargs):
            # print("Workflow order_tasks: Decorator init ", "function_args: ", function_args, "function_kwargs: ", function_kwargs)
            # print((function_, function_args, function_kwargs, workflow_args, workflow_kwargs))
            t = workflow_kwargs.get("task_instance")
            if not t:
                raise Exception("Task instance not provided")
            args_normal = t.clean_args(
                function_, function_args, function_kwargs)
            if not args_normal:
                raise Exception("Args and KwArgs do not match")
            t.set_task(
                function_, function_args, function_kwargs,
                workflow_args, workflow_kwargs
            )
            print("Workflow order_tasks - Task added: ",
                  workflow_kwargs.get("name"))
        return order_tasks
    return get_decorator


__all__ = ["Tasks", "workflow"]
