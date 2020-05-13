<p align="center">
  <img width="40%" height="30%" src="https://github.com/taskcontrols/py-taskcontrol/blob/master/docs/images/logo.jpg">
</p>

# taskcontrol  (py-taskcontrol)
    Create named shared / isolated workflow task controls, and run them with respective before/after middlewares


taskcontrol (py-taskcontrol) is a python library to create tasks in and based on named workflow controls. It allows middlewares before and after each task. taskcontrol can run single or multiple tasks at a task run invocation.

It provides a simple decorator called `workflow` that takes the name, task_instance, task_order, shared, before, after arguments to set up the named workflow controls.

It also provides methods to create a plugin and work with tasks as a module and/or pre-created ordered task list.


# Features

* Create Named task controls (tasks) - instance and isolated
* Allows middlewares before / after each task (data fetch, auth, data save, logging, logout, cleanup, etc)
* Access read-only contexts and results of middlewares/tasks
* Allows Merging two instances of task controls with namespace clash handling
* Run instance, shared, and mix of tasks (individual or all groups)
* In-Development: Allows creating, registering, and using task controls as a plugin


# Installation


##### Command:

* Python

        pip3 install taskcontrol


##### Version:

    In Development Version: 1.2.6 (functional - production ready with plugin and concurrency support, fully tested)
    Current Version: 1.2.5 (functional - production ready with most planned features with MVP, partly tested)
    Previous Version: 1.1.2 (functional - production ready minor issues)
    Previous Version: 1.1.0/1.1.1 (functional - not production ready - minor bug. Please upgrade to v1.1.2)



[Releases](https://github.com/taskcontrols/py-taskcontrol/blob/master/docs/users/releases.md) Lists in short the releases of the package


##### Package Link:
    
    https://github.com/taskcontrols/py-taskcontrol
    https://pypi.org/project/taskcontrol
    
##### Website:
    
    https://taskcontrols.github.io/


# Technical Specifications


##### Requirements:

* Python 3.x and above
* Any OS supporting Python 3.x and above


##### Package Dependencies:

* None


##### Quick Demo:

[demo example - main.py](https://github.com/taskcontrols/py-taskcontrol/blob/master/main.py)


```python



from taskcontrol.workflow import workflow, Tasks

sparrow = Tasks()

def middleware_trees(ctx, result, k, c, d, **kwargs):
    print("Running my Middleware Function: middleware_trees - task items", k, c, d, kwargs)


@workflow(
    name="taskname",
    task_order=1,
    task_instance=sparrow,
    shared=False,
    args=[1, 2],
    kwargs={},
    before=[
        {
            "function": middleware_trees,
            "args": [11, 12],
            "kwargs": {"d": "Before Testing message Middleware "},
            "options": {"error": "next", "error_next_value": ""}
        }
    ],
    after=[
        {
            "function": middleware_trees,
            "args": [13, 14],
            "kwargs": {"d": "After Middleware Testing message"},
            "options": {
                "error": "error_handler",
                "error_next_value": "value",
                "error_handler": lambda err, value: (err, None)
            }
        }
    ],
    log=False
)
def taskone(ctx, result, a, b):
    print("Running my task function: taskone", a, b)


# Run single task
sparrow.run(tasks="taskname")


# Run all tasks
sparrow.run(tasks=["1"])
# sparrow.run(tasks=["taskname", ..., "anothertask"])



```


##### Note:

Though it may support Python version 2.x. However, it has not been tested in 2.x. The Syntax and Features of the library supports Python version 2.x. Use at your own risk.



# Wiki

* [Getting started](https://github.com/taskcontrols/py-taskcontrol/blob/master/docs/users/getting-started.md)
    
    Describes in short the usage of the package

* [taskcontrol `workflow` decorator](https://github.com/taskcontrols/py-taskcontrol/blob/master/docs/users/workflow.md)
    
    Describes how to use the taskcontrol workflow decorator in detail

* [taskcontrol `workflow` decorator argument details](https://github.com/taskcontrols/py-taskcontrol/blob/master/docs/users/workflow-arguments.md)
    
    Describes in detail the arguments of workflow decorator

* [taskcontrol `workflow` before / after argument for middleware declaration](https://github.com/taskcontrols/py-taskcontrol/blob/master/docs/users/workflow-middlewares.md)
    
    Describes creating, defining, and running middlewares

* [taskcontrol `workflow` instance and shared tasks argument](https://github.com/taskcontrols/py-taskcontrol/blob/master/docs/users/workflow-instance-shared-tasks.md)
    
    Describes creating a instance (isolated task) and an shared task (available to all instances)


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

# [Todo](https://github.com/taskcontrols/py-taskcontrol/blob/master/.todo)


* e2e and Unit Tests - Add Tests (Structure of package created - to be cleaned after writing tests)
* Allow creating and registering a set of task controls as a plugin
* Add logging system


# Status

* In Active Development (taskcontrol version 1.2.6)


# Support

[Paypal.me/taskcontrols](https://paypal.me/taskcontrols)

[Be a Patreon](https://www.patreon.com/taskcontrols)


# License

The MIT License (MIT) - See [LICENSE](https://github.com/taskcontrols/py-taskcontrol/blob/master/LICENSE) for further details


Copyright © 2020 - till library works

taskcontrols@gmail.com


