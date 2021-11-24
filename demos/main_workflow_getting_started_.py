from taskcontrol import task, Workflow

sparrow = Workflow()

@task(
    name="taskname",
    task_instance=sparrow
)
def taskone(ctx, result, *args, **kwargs):
    print("Running my task function: taskone", args, kwargs)
    return args, kwargs

result = sparrow.start()
print(result)
