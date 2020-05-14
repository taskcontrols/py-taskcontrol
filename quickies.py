from taskcontrol.workflow import workflow, Tasks


def middleware(ctx, result, k, c, d, **kwargs):
    print("Running my Middleware Function: test - task items", k, c, d, kwargs)
    return 26


t = Tasks()


@workflow(
    name="taskname", task_order=1, task_instance=t,
    shared=False, args=[1, 2], kwargs={},
    before=[{
        "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
        "options": {"error": "next", "error_next_value": ""}
    }],
    after=[{
        "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
        "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, value)}
    }],
    log=False
)
def taskname(ctx, result, a, b):
    print("Running my task function: taskone", a, b)
    return 26


@workflow(
    name="tasktwo", task_order=1, task_instance=t,
    shared=True, args=[1, 2], kwargs={},
    before=[{
        "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
        "options": {"error": "next", "error_next_value": ""}
    }],
    after=[{
        "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
        "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, value)}
    }],
    log=False
)
def tasktwo(ctx, result, a, b):
    print("Running my task function: taskone", a, b)
    return 26


result = t.run(tasks=["taskname", "tasktwo"])
print(result)
t.shared.delete_shared_tasks("shared:tasktwo")
print(t.shared.get_shared_tasks(1))
