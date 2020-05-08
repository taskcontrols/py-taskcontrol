from taskcontrol.workflow import workflow, Tasks



t = Tasks()

def middleware(ctx, result, k, c, d, **kwargs):
    print("Running my Middleware Function: test - task items", k, c, d, kwargs)
    return 16

@workflow(
    name="taskname", task_order=1, task_instance=t,
    shared=True, args=[1, 2], kwargs={}, log=False,
    before=[{
        "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
        "options": {"error": "next", "error_next_value": ""}
    }],
    after=[{
        "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
        "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, value)}
    }])
def taskone(ctx, result, a, b):
    print("Running my task function: taskone", a, b)
    return 16

result = t.run(tasks="shared:taskname")
print(result)

