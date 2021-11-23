from taskcontrol import workflow, Tasks

sparrow = Tasks()

@workflow(
    name="taskname",
    task_instance=sparrow
)
def taskone(ctx, result, *args, **kwargs):
    print("Running my task function: taskone", args, kwargs)

sparrow.run()
