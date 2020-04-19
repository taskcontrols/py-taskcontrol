# workflow
    Create named workflows and run tasks with respective before and after middlewares

Workflow is a python library to create tasks in and based on named workflows. It allows middlewares before and after each task. workflow can run single or multiple tasks at a task invocation.

It provides a simple decorator that takes the name, task, before, after arguments to set up the named workflow.

# Installation

##### Command:

    pip3 install taskcontrol

##### Package Link:
    
    https://github.com/ganeshkbhat/taskcontrol
    https://pypi.org/project/taskcontrol/

# Features

* Create tasks
* Named workflow tasks
* Single or multiple tasks
* Workflow decorator with simple options to setup workflow
* Allows middlewares before each task (data fetch, auth, etc)
* Allows middlewares after each task (data save, logging, logout, cleanup, etc)


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

# Multiple Workflow Tasks run
t.run(tasks=["taskname", "tasktwo"])

# Single Workflow Tasks run
# t.run(tasks="taskname")


```

##### Note:

Though it may support Python version 2.x. However, it has not been tested in 2.x. The Syntax and Features of the library supports Python version 2.x. Use at your own risk.
<!-- 
# Wiki
 -->


# Todo

<!-- * Add Tests -->
* Add plugin system


# License


The MIT License (MIT) - See [LICENSE](./LICENSE) for further details


Copyright © 2020 - till library works:
    Ganesh B <ganeshsurfs@gmail.com>


