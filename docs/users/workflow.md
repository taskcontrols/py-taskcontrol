# taskcontrol


## task decorator arguments
* Usage:
    ```python
    @task(
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
    def function: <function> (ctx, result, *args, **kwargs):
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
