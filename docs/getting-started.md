# taskcontrol
    Create named shared / isolated workflow task controls, and run them with respective before/after middlewares


# Features Details

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

# Demo Usage

* Import workflow and Tasks object from workflow module in taskcontrol package
* Create a Task instance
* Create a workflow definition using `@workflow` decorator
    - Usage: 
        - `@workflow(name, task_order, task_instance, args, kwargs, before, after, shared, log)`
        - `def function(...){...}`
    - `name`, `task_instance` keys definitions are compulsary
    - `args`, `kwargs`, optional for function arguments - throws `TypeError` if wrong args provided
    - `before` and `after` keys are optional and provides before and after middlewares for a specific task
    - `shared` key is optional and defaults to `False`
    - `log` key is optional and default to `False`
* Run the task when needed using `.run(tasks=['taskname'])` invocation


## workflow decorator arguments
* Usage:
    ```python
    @workflow(
        name = <str>,
        task_order = <int>,
        task_instance = <object_instance>,
        shared = <boolean>,
        args = <list>,
        kwargs = <dict>,
        before = <list[<dict>]> or <dict> [
            {
                "function": <function>,
                "args": <list[<object>]>,
                "kwargs": <dict>,
                "options": <dict> {"error": <str>, "error_next_value": <object> or <any>}
            }
        ],
        after = <list[<dict>]> or <dict>  [ {
                "function": <function>,
                "args": <list>,
                "kwargs": <dict>,
                "options": { "error":<str>, "error_next_value":<object> or <any>, "error_handler":<function>}
            }
        ],
        log = <boolean>
    )
    def function: <function> (ctx, result, args, ..., kwargs):
        <code_here>
    ```


#### name
* `name` key takes a string for the name of task instance
* `<str>` type
* [more]()


#### log
* `log` key takes a boolean to allow logging or not
* Whether logging should be allowed or not (Not functional yet)
* `<boolean>` type
* [more]()


#### after
* `after` key takes definitions of a list of dict / dict definitions
* after middleware order followed will be of the list sequence
* `<list>` type or `<dict>` type
* [more]()


#### before
* `before` key takes definitions of a list of dict / dict
* before middleware order followed will be of the list sequence
* `<list>` type or `<dict>` type
* [more]()


#### args
* `args` key takes a list of definitions
* Arguments that should be provided to the task function the decorator is applied on
* `<list>` type
* [more]()


#### kwargs
* `kwargs` key takes a list of definitions
* Keyword arguments for the function the decorator is applied on
* `<dict>` type
* [more]()


#### shared
* `shared` key takes a boolean whether to create a shared task or not
* Whether the Task is a shared task or instance isolated task
* Shared Task is sharable and accessable across the app
* `<boolean>` type
* [more]()


#### task_instance
* `task_instance` key takes instance of the Tasks object imported
* Task instance which is used for creating tasks
* Tasks are isolated to this task instance
* `<object>` instance type
* [more]()


#### task_order
* `task_order` key takes an ordering number / integer
* Order of the task function when all tasks are run (Not functional yet)
* `<int>` type
* [more]()


## Demo Usage


```python


# for package
from taskcontrol.workflow import workflow, Tasks


# Create an instance of the task you are creating
sparrow = Tasks()


# Middleware that we are running
# Use any middleware that runs with or withour returning results
# Demo uses common middleware for all. Please use you own middlewares
def nesttree(ctx, result, k, c, d, **kwargs):
    print("Running my Middleware Function: nesttree - task items", k, c, d, kwargs)


# workflow decorator
@workflow(
    
    # Task name
    name="taskname",
    
    # Order of the task function when all tasks are run (Not functional yet)
    task_order=1,
    
    # Task instance whic is used for creating tasks
    # Tasks are isolated to this task instance
    task_instance=sparrow,

    # Whether the Task is a shared task or instance isolated task
    # Shared Task is sharable and accessable across the app
    shared=False,

    # Arguments that should be provided to the task function the decorator is applied on
    args=[1, 2],

    # Keyword arguments for the function the decorator is applied on
    kwargs={},

    # before middleware order followed will be of the list sequence
    before=[
        {
            "function": nesttree,
            "args": [11, 12],
            "kwargs": {"d": "Before Testing message Middleware "},
            "options": {"error": "next", "error_next_value": ""}
        }
    ],

    # after middleware order followed will be of the list sequence
    after=[
        {
            "function": nesttree,
            "args": [13, 14],
            "kwargs": {"d": "After Middleware Testing message"},
            "options": {
                "error": "error_handler",
                "error_next_value": "value",
                "error_handler": lambda err, value: (err, None)
            }
        }
    ],

    # Whether logging should be allowed or not (Not functional yet)
    log=False
)
# Main function for the task
def taskone(ctx, result, a, b):
    print("Running my task function: taskone", a, b)


```

