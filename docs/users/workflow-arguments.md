# taskcontrol


# Task decorator argument usage

All Decorator arguments that can be used are are below. The only compulsory arguments are `name` and `task_instance`. `args`, `kwargs` key used for the function args and keyword args are not compulsory but the function will throw errors if there is a number of arguments mismatch.


#### name
* `name` key takes a string for the name of task instance
* `<str>` type
* Usage:
    ```python

    from taskcontrol import Workflow, task

    sparrow = Workflow()
    @task( name="taskname", task_instance=sparrow )
    def taskone(ctx, result, *args, **kwargs):
        print("Running my task function: taskone", args, kwargs)
        return args, kwargs

    ```


#### task_instance
* `task_instance` key takes instance of the Tasks object imported
* Task instance which is used for creating tasks
* Tasks are isolated to this task instance
* `<object>` instance type
* Usage:
    ```python

    from taskcontrol import Workflow, task

    sparrow = Workflow()
    @task( name="taskname", task_instance=sparrow )
    def taskone(ctx, result, *args, **kwargs):
        print("Running my task function: taskone", args, kwargs)
        return args, kwargs

    ```


#### log
* `log` key takes a boolean to allow logging or not
* Whether logging should be allowed or not (Not functional yet)
* `<boolean>` type
* Usage:
    ```python

    from taskcontrol import Workflow, task

    sparrow = Workflow()
    @task( name="taskname", task_instance=sparrow, log=False )
    def taskone(ctx, result, *args, **kwargs):
        print("Running my task function: taskone", args, kwargs)
        return args, kwargs

    ```


#### after
* `after` key takes definitions of a list of dict / dict definitions
* after middleware order followed will be of the list sequence
* `<list>` type or `<dict>` type
* Usage:
    - Using as an single dictionary definition

        ```python

        from taskcontrol import Workflow, task

        sparrow = Workflow()

        def nesttree(ctx, result, *args, **kwargs):
            print("Running my Middleware Function: nesttree - task items", args, kwargs)

        @task(
            name="taskname", task_instance=sparrow,
            after = {
                "function": nesttree,
                "args": [11, 12],
                "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }
        )
        def taskone(ctx, result, *args, **kwargs):
            print("Running my task function: taskone", args, kwargs)
            return args, kwargs

        ```

    - Using as a list definition

        ```python

        from taskcontrol import Workflow, task

        def nesttree(ctx, result, *args, **kwargs):
            print("Running my Middleware Function: nesttree - task items", args, kwargs)

        sparrow = Workflow()

        @task(
            name="taskname", task_instance=sparrow,
            after = [{
                "function": nesttree,
                "args": [11, 12],
                "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }]
        )
        def taskone(ctx, result, *args, **kwargs):
            print("Running my task function: taskone", args, kwargs)
            return args, kwargs

        ```


#### before
* `before` key takes definitions of a list of dict / dict
* before middleware order followed will be of the list sequence
* `<list>` type or `<dict>` type
* Usage:
    - Using as an dictionary

        ```python

        from taskcontrol import Workflow, task

        sparrow = Workflow()

        def nesttree(ctx, result, *args, **kwargs):
            print("Running my Middleware Function: nesttree - task items", args, kwargs)

        @task(
            name="taskname", task_instance=sparrow,
            before = {
                "function": nesttree,
                "args": [11, 12],
                "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }
        )
        def taskone(ctx, result, *args, **kwargs):
            print("Running my task function: taskone", args, kwargs)
            return args, kwargs

        ```

    - Using as a list

        ```python

        from taskcontrol import Workflow, task

        sparrow = Workflow()
        
        def nesttree(ctx, result, *args, **kwargs):
            print("Running my Middleware Function: nesttree - task items", args, kwargs)

        @task(
            name="taskname", task_instance=sparrow,
            before = [{
                "function": nesttree,
                "args": [11, 12],
                "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }]
        )
        def taskone(ctx, result, *args, **kwargs):
            print("Running my task function: taskone", args, kwargs)
            return args, kwargs

        ```


#### args
* `args` key takes a list of definitions
* Arguments that should be provided to the task function the decorator is applied on
* `<list>` type
* Usage:
    ```python

    from taskcontrol import Workflow, task

    sparrow = Workflow()
    @task( name="taskname", task_instance=sparrow, args=[11, 12] )
    def taskone(ctx, result, *args, **kwargs):
        print("Running my task function: taskone", args, kwargs)
        return args, kwargs

    ```


#### kwargs
* `kwargs` key takes a list of definitions
* Keyword arguments for the function the decorator is applied on
* `<dict>` type
* Usage:
    ```python

    from taskcontrol import Workflow, task

    sparrow = Workflow()
    @task( name="taskname", task_instance=sparrow, kwargs={"a":11, "b":12} )
    def taskone(ctx, result, *args, **kwargs):
        print("Running my task function: taskone", args, kwargs)
        return args, kwargs

    ```


#### shared
* `shared` key takes a boolean whether to create a shared task or not
* Whether the Task is a shared task or instance isolated task
* Shared Task is sharable and accessable across the app
* `<boolean>` type
* Usage:
    ```python

    from taskcontrol import Workflow, task

    sparrow = Workflow()
    @task( name="taskname", task_instance=sparrow, shared=True )
    def taskone(ctx, result, *args, **kwargs):
        print("Running my task function: taskone", args, kwargs)
        return args, kwargs

    ```


#### task_order
* `task_order` key takes an ordering number / integer
* Order of the task function when all tasks are run (Not functional yet)
* `<int>` type
* Usage:
    ```python

    from taskcontrol import Workflow, task

    sparrow = Workflow()
    @task( name="taskname", task_instance=sparrow, task_order=1 )
    def taskone(ctx, result, *args, **kwargs):
        print("Running my task function: taskone", args, kwargs)
        return args, kwargs

    ```


## Entire Usage:


```python


from taskcontrol import Workflow, task

sparrow = Workflow()
def nesttree(ctx, result, *args, **kwargs):
    print("Running my Middleware Function: nesttree - task items", args, kwargs)

@task(
    name="taskname",  # task name 
    task_order=1,  # task order when to run when all runs are used 
    task_instance=sparrow,  # instance of Task 
    shared=False,  # boolean whether a shared task 
    args=[1, 2],  # list of args 
    kwargs={},  # dict of kwargs 
    before=[  # before middleware definition
        {
            "function": nesttree,  # middleware function definition
            "args": [11, 12],  # list of args 
            "kwargs": {"d": "Before Testing message Middleware "},  # dict of kwargs 
            "options": {"error": "next", "error_next_value": ""}  # dict options
        }
    ],
    after={  # after middleware definition
            "function": nesttree,  # list of args 
            "args": [11, 12],  # list of args 
            "kwargs": {"d": "Before Testing message Middleware "},  # dict of kwargs
            "options": {"error": "next", "error_next_value": ""}  # dict options
        },
    log=False  # log enabled or not
)
def taskone(ctx, result, *args, **kwargs):
    print("Running my task function: taskone", args, kwargs)
    return args, kwargs


```

