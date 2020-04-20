# taskcontrol
    Create named workflow task controls and run the tasks with respective before and after middlewares

taskcontrol is a python library to create tasks in and based on named workflow controls. It allows middlewares before and after each task. taskcontrol can run single or multiple tasks at a task run invocation.

It provides a simple decorator called `workflow` that takes the name, task_instance, task_order, task_global, before, after arguments to set up the named workflow control.

# Installation

##### Command:

    pip3 install taskcontrol

##### Package Link:
    
    https://github.com/ganeshkbhat/taskcontrol
    https://pypi.org/project/taskcontrol/

# Features

* Create task controls (tasks)
* Named workflow tasks
* Single or multiple tasks
* Workflow decorator with simple options to setup workflow
* Allows middlewares before each task (data fetch, auth, etc)
* Allows middlewares after each task (data save, logging, logout, cleanup, etc)
* Allows merging to instances of task controls
* In-Development: Allows creating shared/common task controls
* In-Development: Allows creating and registering a set of task controls as a plugin
* In-Development: Allows adding a plugin to your task controls


# Feature Details
# Technical Specifications

##### Requirements:

* Python 3.x
* Any OS supporting Python 3.x

##### Package Dependencies:

* None

##### Quick Demo:

```javascript


# for git development repo
# from src.workflow import workflow, Tasks


# for package
from taskcontrol import workflow, Tasks


# Instance of tasks object
# Every instance will store it own list of tasks 
#       with their before/after middlewares
t = Task()


def test(k, c, d):
    print("Running my Middleware Function: test - task items", k, c, d)


@workflow(
    name="taskname",
    task_order=1,
    task_instance = t,
    shared=True,
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
            "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
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
    log=True
)
def taskone(a, b):
    print("Running my task function: taskone", a, b)


# Invocation is needed to add the task with function arguments
# Invoke this where needed
# Example: Within some other function
taskone(3, 4)


# Example two for decorator usage
@workflow(name="tasktwo",
        task_instance = t,
        task_order=2,
        task_global=False,
          # Declare before/after as an list or an object (if single middleware function)
          before={
              "function": test,
              "args": [21, 22],
              "kwargs": {"d": "Before Testing message"},
              "options": {"error": "next", "error_next_value": ""}
          },
          after=[]
          )
def tasktwo(a, b):
    print("Running my task function: tasktwo", a, b)

tasktwo(5, 6)


# Invoke this where needed
# Example: Within some other function


# TODO: Run all tasks
# Multiple Workflow Tasks run
# t.run(tasks=["all"])


# TODO: Run all shared tasks
# Shared Workflow Tasks run
# t.run(tasks=["shared:all"])


# Multiple Workflow Tasks run
t.run(tasks=["taskname", "tasktwo"])


# TODO: Run Tasks run with mix of shared
# Multiple Workflow Tasks run with mix of shared
# t.run(tasks=["taskname", "tasktwo", "shared:taskname"])


# Single Workflow Tasks run
# t.run(tasks="taskname")


# TODO: Run Tasks run with shared task
# Single Workflow Tasks run for shared task
# t.run(tasks="shared:taskname")


```

##### Note:

Though it may support Python version 2.x. However, it has not been tested in 2.x. The Syntax and Features of the library supports Python version 2.x. Use at your own risk.
<!-- 
# Wiki
 -->


# Todo

<!-- * Add Tests -->

* In-Development: Allows merging two instances of task controls
* In-Development: Allows creating shared/common task controls
* In-Development: Allows creating and registering a set of task controls as a plugin
* In-Development: Allows adding a plugin to your task controls


# License


The MIT License (MIT) - See [LICENSE](./LICENSE) for further details


Copyright © 2020 - till library works:
    Ganesh B <ganeshsurfs@gmail.com>


