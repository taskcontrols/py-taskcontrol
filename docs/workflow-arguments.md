# taskcontrol

# Workflow decorator argument usage


#### name
* `name` key takes a string for the name of task instance
* `<str>` type
* Usage:
    ```python

    from taskcontrol.workflow import workflow, Tasks

    sparrow = Tasks()
    @workflow( name="taskname", task_instance=sparrow )
    def taskone(ctx, result, a, b):
        print("Running my task function: taskone", a, b)
        return a,b

    ```


#### task_instance
* `task_instance` key takes instance of the Tasks object imported
* Task instance which is used for creating tasks
* Tasks are isolated to this task instance
* `<object>` instance type
* Usage:
    ```python

    from taskcontrol.workflow import workflow, Tasks

    sparrow = Tasks()
    @workflow( name="taskname", task_instance=sparrow )
    def taskone(ctx, result, a, b):
        print("Running my task function: taskone", a, b)
        return a,b

    ```


#### log
* `log` key takes a boolean to allow logging or not
* Whether logging should be allowed or not (Not functional yet)
* `<boolean>` type
* Usage:
    ```python

    from taskcontrol.workflow import workflow, Tasks

    sparrow = Tasks()
    @workflow( name="taskname", task_instance=sparrow, log=False )
    def taskone(ctx, result, a, b):
        print("Running my task function: taskone", a, b)
        return a,b

    ```


#### after
* `after` key takes definitions of a list of dict / dict definitions
* after middleware order followed will be of the list sequence
* `<list>` type or `<dict>` type
* Usage:
    - Using as an single dictionary definition

        ```python

        from taskcontrol.workflow import workflow, Tasks

        sparrow = Tasks()

        def nesttree(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: nesttree - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_instance=sparrow,
            after = {
                "function": nesttree,
                "args": [11, 12],
                "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a,b

        ```

    - Using as a list definition

        ```python

        from taskcontrol.workflow import workflow, Tasks

        def nesttree(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: nesttree - task items", k, c, d, kwargs)

        sparrow = Tasks()

        @workflow(
            name="taskname", task_instance=sparrow,
            after = [{
                "function": nesttree,
                "args": [11, 12],
                "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }]
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a,b

        ```


#### before
* `before` key takes definitions of a list of dict / dict
* before middleware order followed will be of the list sequence
* `<list>` type or `<dict>` type
* Usage:
    - Using as an dictionary

        ```python

        from taskcontrol.workflow import workflow, Tasks

        sparrow = Tasks()

        def nesttree(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: nesttree - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_instance=sparrow,
            before = {
                "function": nesttree,
                "args": [11, 12],
                "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a,b

        ```

    - Using as a list

        ```python

        from taskcontrol.workflow import workflow, Tasks

        sparrow = Tasks()
        
        def nesttree(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: nesttree - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_instance=sparrow,
            before = [{
                "function": nesttree,
                "args": [11, 12],
                "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }]
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a,b

        ```


#### args
* `args` key takes a list of definitions
* Arguments that should be provided to the task function the decorator is applied on
* `<list>` type
* Usage:
    ```python

    from taskcontrol.workflow import workflow, Tasks

    sparrow = Tasks()
    @workflow( name="taskname", task_instance=sparrow, args=[11, 12] )
    def taskone(ctx, result, a, b):
        print("Running my task function: taskone", a, b)
        return a,b

    ```


#### kwargs
* `kwargs` key takes a list of definitions
* Keyword arguments for the function the decorator is applied on
* `<dict>` type
* Usage:
    ```python

    from taskcontrol.workflow import workflow, Tasks

    sparrow = Tasks()
    @workflow( name="taskname", task_instance=sparrow, kwargs={"a":11, "b":12} )
    def taskone(ctx, result, a, b):
        print("Running my task function: taskone", a, b)
        return a,b

    ```


#### shared
* `shared` key takes a boolean whether to create a shared task or not
* Whether the Task is a shared task or instance isolated task
* Shared Task is sharable and accessable across the app
* `<boolean>` type
* Usage:
    ```python

    from taskcontrol.workflow import workflow, Tasks

    sparrow = Tasks()
    @workflow( name="taskname", task_instance=sparrow, shared=True )
    def taskone(ctx, result, a, b):
        print("Running my task function: taskone", a, b)
        return a,b

    ```


#### task_order
* `task_order` key takes an ordering number / integer
* Order of the task function when all tasks are run (Not functional yet)
* `<int>` type
* Usage:
    ```python

    from taskcontrol.workflow import workflow, Tasks

    sparrow = Tasks()
    @workflow( name="taskname", task_instance=sparrow, task_order=1 )
    def taskone(ctx, result, a, b):
        print("Running my task function: taskone", a, b)
        return a,b

    ```


## Entire Usage:


```python


from taskcontrol.workflow import workflow, Tasks

sparrow = Tasks()
def nesttree(ctx, result, k, c, d, **kwargs):
    print("Running my Middleware Function: nesttree - task items", k, c, d, kwargs)

@workflow(
    name="taskname",
    task_order=1,
    task_instance=sparrow,
    shared=False,
    args=[1, 2],
    kwargs={},
    before=[
        {
            "function": nesttree,
            "args": [11, 12],
            "kwargs": {"d": "Before Testing message Middleware "},
            "options": {"error": "next", "error_next_value": ""}
        }
    ],
    after={
            "function": nesttree,
            "args": [11, 12],
            "kwargs": {"d": "Before Testing message Middleware "},
            "options": {"error": "next", "error_next_value": ""}
        },
    log=False
)
def taskone(ctx, result, a, b):
    print("Running my task function: taskone", a, b)


```
