# taskcontrol

    Create named shared / isolated workflow task controls, and run them with respective before/after middlewares. taskcontrols also supports plugins, concurrency, and authentication  


# Features Details

* Create Named task controls (tasks) - instance and isolated
* Allows before / after middlewares for each task
* Access read-only contexts and results of middlewares/tasks
* Allows merging two instances of task controls with namespace clash handling
* Run instance, shared, and mix of tasks (individual or all groups)
* Allows working with Logging, Sockets, Events, Queues, Publisher-Subscriber Architectures, etc
* In-Development:
    * Allows support for / working with Concurrency
    * Allows working with Commands & Scripts (T), SSH (T), etc
    * Allows working with Scheduling (T), Files (T - normal, yaml, ini, and csv), etc
    * Allows working with ORMs/Databases (T), Authentication (T)
    * Allows working with best practices like Dependency Injection (T) within the library (including Tasks, Workflow)
    * Allows creating, registering, and using tasks/workflows as a plugin
    * Planned Integrations with Subversioning, Build Tools, Deployment
    * Planned Integrations with Data Transformation / Analytics Tooling
    * Planned Integrations with Testing, and Infrastructure Automation toolings
    * Monitoring Support
    * Provided in and Allows plugins support for Python, Javascript languages

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
from taskcontrol import workflow, Tasks


# Create an instance of the task you are creating
sparrow = Tasks()


# Middleware that we are running
# Use any middleware that runs with or withour returning results
# Demo uses common middleware for all. Please use you own middlewares
def nesttree(ctx, result, *args, **kwargs):
    print("Running my Middleware Function: nesttree - task items", args, kwargs)


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
def taskone(ctx, result, *args, **kwargs):
    print("Running my task function: taskone", args, kwargs)

sparrow.run(tasks="taskname")


```

