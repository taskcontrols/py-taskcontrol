# taskcontrol
    Create named shared / isolated workflow task controls, and run them with respective before/after middlewares

taskcontrol is a python library to create tasks in and based on named workflow controls. It allows middlewares before and after each task. taskcontrol can run single or multiple tasks at a task run invocation.

It provides a simple decorator called `workflow` that takes the name, task_instance, task_order, shared, before, after arguments to set up the named workflow controls.

It also provides methods to create a plugin and work with tasks as a module and/or pre-created ordered task list.


# Installation

##### Command:

    pip3 install taskcontrol

##### Package Link:
    
    https://github.com/ganeshkbhat/taskcontrol
    https://pypi.org/project/taskcontrol/

# Features

* Create Named task controls (tasks) using a Workflow decorator with simple options to setup workflow
* Allows middlewares before each task (data fetch, auth, etc)
* Allows middlewares after each task (data save, logging, logout, cleanup, etc)
* Allows context (currently read-only) for each set of tasks run accessible by any function
* Allows accessing returns/results of runs by each task or their middlewares
* Allows creating isolated instance tasks or common/shared tasks based on shared keyword argument
* Allows creating and merging two instances of task controls with namespace clash handling
* Allows running single or multiple isolated, shared, or mixed tasks for each set of tasks run
<!-- * In-Development: Allows creating, registering, and using a set of task controls as a plugin -->
<!-- * In-Development: Allows  -->

<!-- # Feature Details -->

# Technical Specifications

##### Requirements:

* Python 3.x
* Any OS supporting Python 3.x

##### Package Dependencies:

* None

##### Quick Demo:

```python


# for git development repo
# from src.workflow import workflow, Tasks

# for package
from taskcontrol import workflow, Tasks


# Instance of tasks and apis object
# Every instance will store it own list of tasks
#       with their before/after middlewares
t = Tasks()


def test(ctx, result, k, c, d, **kwargs):
    print("Running my Middleware Function: test - task items", k, c, d, kwargs)


@workflow(
    name="taskname",
    task_order=1,
    task_instance=t,
    shared=False,
    args=[1, 2],
    kwargs={},
    before=[
        # before middleware order followed will be of the list sequence
        {
            "function": test,
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
            "function": test,
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
def taskone(ctx, result, a, b):
    print("Running my task function: taskone", a, b)


# Invocation is needed to add the task with function arguments
# Invoke this where needed
# Example: Within some other function
# taskone(3, 4)


# Example two for decorator usage
@workflow(name="tasktwo",
          task_instance=t,
          task_order=2,
          shared=False,
          args=[1, 2],
          kwargs={},
          # Declare before/after as an list or an object (if single middleware function)
          before={
              "function": test,
              "args": [21, 22],
              "kwargs": {"d": "Before Testing message"},
              "options": {"error": "next", "error_next_value": ""}
          },
          after=[],
          log=False
          )
def tasktwo(ctx, result, a, b):
    print("Running my task function: tasktwo", a, b)
    return a, b


# tasktwo(5, 6)


# Invoke this where needed
# Example: Within some other function


# TODO: Run all tasks
# Multiple Workflow Tasks run
t.run(tasks=["1"])
t.run(tasks="1")


# TODO: Run all shared tasks
# Shared Workflow Tasks run
t.run(tasks=["shared:1"])
t.run(tasks="shared:1")


# Multiple Workflow Tasks run
run_1 = t.run(tasks=["shared:taskname", "tasktwo"])
# print("t.ctx ",t.ctx)
print("run_1", run_1)


# TODO: Run Tasks run with mix of shared
# Multiple Workflow Tasks run with mix of shared
t.run(tasks=["taskname", "tasktwo", "shared:taskname"])


# Single Workflow Tasks run
run_2 = t.run(tasks="shared:taskname")
print("run_2", run_2)


# TODO: Run Tasks run with shared task
# Single Workflow Tasks run for shared task
t.run(tasks="shared:taskname")



```

##### Note:

Though it may support Python version 2.x. However, it has not been tested in 2.x. The Syntax and Features of the library supports Python version 2.x. Use at your own risk.

    Minor argument order change from 1.1.0 version
    ctx, and result is compulsary argument which are magically provided

<!-- 
# Wiki
 -->


##### Crazy Hint:
You can also create a simple workflow without taskcontrol using a simple list or nested list and loop through them using a for/while loop and invoke them during looping

```python


# Loop the lists below and invoke the functions 
lst = ["f1", "f2", "f3"]
nest_lst = [["f1", "f2"], "f3", "f4", ["f5"]]


# Use a reducer if you want to send args to next function like below
def test(a,b):
    print(a,b)
    return {"a":a, "b":b}
def tester(a,b):
    print(a,b)
    return None

kwargs_for_first_function_the_its_returns_or_other_value_for_next_func = {"a":"a", "b":"b"}
ls = [kwargs_for_first_function_the_its_returns_or_other_value_for_next_func, test, tester]
import functools 
def red(kwargs_for_first_then_func, p):
    i = p(kwargs.get("a"), kwargs.get("b"))
    return i
functools.reduce(red, ls)


```

# Todo

* e2e and Unit Tests: Add Tests
* In-Development: Allows creating and registering a set of task controls as a plugin


# License


The MIT License (MIT) - See [LICENSE](./LICENSE) for further details


Copyright © 2020 - till library works:
    Ganesh B <ganeshsurfs@gmail.com>

