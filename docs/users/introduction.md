# taskcontrol

#### Workflow Automation Library with support for Concurrent or Event based processes or activities in Local/Network Automation Tasks, including CI/CD activities.


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


from taskcontrol import Workflow, task

sparrow = Workflow()

@task(
    name="migrate",
    task_instance=sparrow
)
def taskone(ctx, result, *args, **kwargs):
    print("Running my task function: migrate", args, kwargs)

# Run one tasks
sparrow.start(tasks="migrate")
# sparrow.start(tasks=["migrate"])

# Run all tasks
sparrow.start()
# sparrow.start(tasks=["1"])


```

