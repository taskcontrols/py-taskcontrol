<p align="center">
  <img width="40%" height="30%" src="https://github.com/taskcontrols/py-taskcontrol/blob/master/docs/images/logo.jpg">
</p>

# taskcontrol  (py-taskcontrol)


##### Workflow Automation Library with support for Concurrent or Event based processes or activities in Local/Network Automation Tasks, including CI/CD activities.


* `taskcontrol (py-taskcontrol)` is a python library to create tasks in and based on named taskflow controls. It allows middlewares before and after each task with support for concurrent processing. taskcontrol can run single or multiple tasks during task invocation/runs.
* It provides a simple decorator called `task` that takes arguments to set up the named taskflow controls. It also provides methods to create a plugin and allow working with tasks as a module and/or pre-created ordered task list. Taskcontrol allows for scaling of plugin development with various utilities like authentication, logging, concurrency, sockets, events, publisher-subscriber architectures, webhooks, client-server http api servers etc.


[Actively Developed, Funding Invited]


# Features

* Create Named task controls (tasks) - instance and isolated
* Allows before / after middlewares for each task
* Access read-only contexts and results of middlewares/tasks
* Allows merging two instances of task controls with namespace clash handling
* Run instance, shared, and mix of tasks (individual or all groups)
* Allows working with Logging, Sockets, Events, Queues etc
* Allows working with Publisher-Subscriber Architectures, Client-Agent Architectures, Webhooks
* In-Development:
    * Allows support for / working with Concurrency
    * Allows working with Commands & Scripts (T), SSH (T), etc
    * Allows working with Scheduling (T), Files (T - normal, yaml, ini, and csv), etc
    * Allows working with ORMs/Databases (T), Authentication (T)
    * Allows creating, registering, and using tasks / workflows as a plugin
    * Planned Integrations with Subversioning, Build Tools, Deployment
    * Planned Integrations with Data Transformation / Analytics Tooling
    * Planned Integrations with Testing, and Infrastructure Automation toolings
    * Monitoring Support
    * Allows working with best practices like Dependency Injection (T) within the library (including Tasks, Workflow)
    * Hooks support after dependency-injection package integration
    * Provided in and Allows plugins support for Python, Javascript languages


# Installation


##### Command:

* Python

        pip3 install taskcontrol


##### Version:

    In Development Version: 1.3.0b1 (functional - production ready with plugin and concurrency support, with demos)
    Current Version: 1.3.0b0 (functional - production ready with most planned features with MVP, with demos)
    Previous Version: 1.2.5 (functional - production ready with most planned features with MVP, with demos)
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

* Python 3.x and above (any OS)


##### Package Dependencies:

* dependency-injector (planned todo)


##### Quick Demo:

[General demo example - main_workflow.py](https://github.com/taskcontrols/py-taskcontrol/blob/master/demos/main_workflow.py)


```python


from taskcontrol import Workflow, task

sparrow = Workflow()

@task(
    name="migrate",
    task_instance=sparrow
)
def fly(ctx, result, *args, **kwargs):
    print("Running my task function: fly", args, kwargs)
    return args, kwargs

result = sparrow.start()
print(result)


```


##### Note:

Though it may support Python version 2.x. However, it has not been tested in 2.x. The Syntax and Features of the library supports Python version 2.x. Use at your own risk.


# Wiki

* [Getting started](https://github.com/taskcontrols/py-taskcontrol/blob/master/docs/users/getting-started.md)
    
    Describes in short the usage of the package

* [taskcontrols wiki](https://github.com/taskcontrols/py-taskcontrol/wiki)
    
    Documentation for taskcontrols


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

* Check the [.todo](https://github.com/taskcontrols/py-taskcontrol/blob/master/.todo) file
<!-- 
* e2e and Unit Tests - Add Tests (Structure of package created - to be cleaned after writing tests)
* Allow creating and registering a set of task controls as a plugin
* Allow working with commands (Todo), ssh (Todo), Files (Todo - normal, yaml, ini, json, and csv), Scheduling (Todo), Dependency Injection (Todo), ORMs/Databases (Todo), Authentication (Todo)
* [C?] Consider Workflow/Tasks tracking system and Dashboard with its own progress and logging
* [C?] Consider compatibility to Chef/CircleCI/Github/Other Automation tools, atleast as externally added plugins

-->

# Status

* In Active Development (taskcontrol version 1.3.0 and Common Integrations and Activities as Plugins)

# Support

[Paypal.me/taskcontrols](https://paypal.me/taskcontrols)

[Be a Patreon](https://www.patreon.com/taskcontrols)


# License

The MIT License (MIT) - See [LICENSE](https://github.com/taskcontrols/py-taskcontrol/blob/master/LICENSE) for further details


Copyright © 2020 - till library works

taskcontrols@gmail.com


