from taskcontrol import task, Taskflow

sparrow = Taskflow()

@task(
    name="taskname",
    task_instance=sparrow
)
def taskone(ctx, result, *args, **kwargs):
    print("Running my task function: taskone", args, kwargs)
    return args, kwargs

result = sparrow.run()
print(result)
