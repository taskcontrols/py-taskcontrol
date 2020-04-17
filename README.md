# workflow
    Create named workflows and run tasks with before and after middlewares

Workflow is a python library to create tasks in and based on named workflows. It allows middlewares before and after each task. workflow can run single or multiple tasks at a task invocation.

It provides a simple decorator that takes the name, task, before, after arguments to set up the named workflow.

# Installation

##### Command:

    pip3 install workflow-name-TBD

##### Package Link:
    

# Features
# Feature Details
# Technical Specifications

##### Requirements:

* Python 3.x
* Any OS supporting Python 3.x

##### Package Dependencies:

* None

##### Quick Demo:

```javascript

// from src.workflow import workflow, tasks
from workflow-name-TBD import workflow, tasks


def test(k):
    print(k)


@workflow(
    name="taskname", task_order=1,
    before=[
        {
            # before middleware order followed will be of the list sequence
            "functions": [test],
            "flow": {
                "test": {
                    "args": [], "kwargs": {"k": "Testing message"},
                    
                    # options: { error : <str>,  error_next_value: <Object>, error_handler: <function> }
                    # 
                    # error { <str> }: [next, error_handler, exit]
                    # error_handler { <function> }
                    # error_next_value { <Object> }
                    # 
                    # Usage:
                    # "options": {"error": "next", "error_next_value": "value"}
                    # "options": {"error": "exit"}
                    # "options": {
                    #    "error": "error_handler", error_handler: func, "error_next_value": "value"
                    #    }

                    "options": {"error": "next", "error_next_value": ""}
                }
            }
        }
    ],
    after=[
        {
            # after middleware order followed will be of the list sequence
            "functions": [test],
            "flow": {
                "test": {
                    "args": [], "kwargs": {"k": "Testing message"},
                    "options": {
                            "error": "error_handler",
                            "error_next_value": "value",
                            "error_handler": lambda err, value: value
                        }
                }
            }
        }
    ]
)
def taskone(a, b):
    print(a, b)


# Invocation is needed to add the task with function arguments
# Invoke this where needed
# Example: Within some other function
taskone(3, 4)


# Invoke this where needed
# Example: Within some other function
# tasks()["run"](task=["taskname", "tasktwo"])
tasks()["run"](task="taskname")

```

##### Note:

Though it may support Python version 2.x. However, it has not been tested in 2.x. The Syntax and Features of the library supports Python version 2.x. Use at your own risk.

# Wiki
# Todo
# References
# License
