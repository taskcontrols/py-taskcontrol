# taskcontrol


```python


# for git development repo
# from taskcontrol import Workflow, task

# for package
from taskcontrol import Workflow, task


# Instance of tasks and apis object
# Every instance will store it own list of tasks
#       with their before/after middlewares
sparrow = Workflow()


def nesttree(ctx, result, *args, **kwargs):
    print("Running my Middleware Function: nesttree - task items", args, kwargs)


@task(
    name="taskname",
    task_order=1,
    task_instance=sparrow,
    shared=False,
    args=[1, 2],
    kwargs={},
    before=[
        # before middleware order followed will be of the list sequence
        {
            "function": nesttree,
            "args": [11, 12],
            "kwargs": {"d": "Before Testing message Middleware "},

            # options { error : str,  error_next_value: Object, error_handler: function }
            #
            # error { str }: [next, error_handler, exit]
            # error_handler { function }
            # error_next_value { object }
            #
            # Usage:
            # "options": {"error": "next", "error_next_value": "value"}
            # "options": {"error": "exit"}
            # "options": {
            #    "error": "error_handler", error_handler: func, "error_next_value": "value"
            #    }

            "options": {"error": "next", "error_next_value": ""}
        }
    ],
    after=[
        # after middleware order followed will be of the list sequence
        {
            "function": nesttree,
            "args": [13, 14],
            "kwargs": {"d": "After Middleware Testing message"},
            "options": {
                "error": "error_handler",
                "error_next_value": "value",

                #
                # Default error_handler implementation used internally, if no
                #           error_handler is provided
                #
                # Implementation One:
                #   if error_next_value defined
                #       lambda err, value: (err, error_next_value)
                # Implementation Two:
                #   if error_next_value not defined
                #       lambda err, value: (err, None)
                #
                # Returning the two value tuple in error_handler implementation is compulsary
                #       err is the error that occurred
                #       error_next_value is error_next_value provided in options
                #

                "error_handler": lambda err, value: (err, None)
            }
        }
    ],
    log=False
)
def taskone(ctx, result, *args, **kwargs):
    print("Running my task function: taskone", args, kwargs)


# Invocation is needed to add the task with function arguments
# Invoke this where needed
# Example: Within some other function
# taskone(3, 4)


# Example two for decorator usage
@task(name="tasktwo",
          task_instance=t,
          task_order=2,
          shared=False,
          args=[1, 2],
          kwargs={},
          # Declare before/after as an list or an object (if single middleware function)
          before={
              "function": nesttree,
              "args": [21, 22],
              "kwargs": {"d": "Before Testing message"},
              "options": {"error": "next", "error_next_value": ""}
          },
          after=[],
          log=False
          )
def tasktwo(ctx, result, *args, **kwargs):
    print("Running my task function: tasktwo", args, kwargs)
    return args, kwargs


# Invoke this where needed
# Example: Within some other function


# TODO: Run all tasks
# Multiple Taskcontrol Tasks run
sparrow.start(tasks=["1"])
sparrow.start(tasks="1")


# TODO: Run all shared tasks
# Shared Taskcontrol Tasks run
sparrow.start(tasks=["shared:1"])
sparrow.start(tasks="shared:1")


# Multiple Taskcontrol Tasks run
run_1 = sparrow.start(tasks=["shared:taskname", "tasktwo"])
# print("sparrow.ctx ",sparrow.ctx)
print("run_1", run_1)


# TODO: Run Tasks run with mix of shared
# Multiple Taskcontrol Tasks run with mix of shared
sparrow.start(tasks=["taskname", "tasktwo", "shared:taskname"])


# Single Taskcontrol Tasks run
run_2 = sparrow.start(tasks="shared:taskname")
print("run_2", run_2)


# TODO: Run Tasks run with shared task
# Single Taskcontrol Tasks run for shared task
sparrow.start(tasks="shared:taskname")



```
