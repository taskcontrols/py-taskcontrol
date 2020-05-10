# taskcontrol

    Create named shared / isolated workflow task controls, and run them with respective before/after middlewares. taskcontrols also supports plugins, concurrency, and authentication  


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

sparrow.run(tasks="taskname")


```

