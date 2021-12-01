# taskcontrol

    Create named shared / isolated Workflow task controls, and run them with respective before/after middlewares. taskcontrols also supports plugins, concurrency, and authentication  


# Minimal Usage Demo

* Import `Workflow` and `task` object from `lib` module in taskcontrol package
* Create a Task instance using the `Workflow` class
* Create a task definition using `@task` decorator
    - Usage: 
        - `@task(name, task_order, task_instance, args, kwargs, before, after, shared, log)`
        - `def function(...){...}`
    - `name`, `task_instance` keys definitions are compulsary
* Run the task when needed using `.start(tasks=['taskname'])` invocation


## Demo Code

```python


# for package
from taskcontrol import Workflow, task

# Create an instance of the task you are creating
sparrow = Workflow()

# task decorator
@task(
    # Task name
    name="migrate",
    # Task instance
    task_instance=sparrow
)
# Main function for the task
def taskone(ctx, result, *args, **kwargs):
    print("Running my task function: migrate", args, kwargs)

# Run single task
sparrow.start(tasks="migrate")
# sparrow.start(tasks=["taskname"])

# Run all tasks
sparrow.start()
# sparrow.start(tasks=["1"])


```

