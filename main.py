from src.workflow import workflow, tasks


def move(msg):
    print(msg)


def test(msg):
    move(msg)


@workflow(
    name="taskname", task_order=1,
    before=[
        {
            # order followed will be of the list sequence
            "functions": [test],
            "flow": {
                "test": {
                    "args": [], "kwargs": {"msg": "Testing message"},
                    # error: next, exit, error_handler
                    "options": {"error": "next", "error_next_value": ""}
                }
            }
        }
    ],
    after=[
        {
            "functions": [test],
            "flow": {
                "test": {
                    "args": [], "kwargs": {"msg": "Testing message"},
                    # error: next, exit, error_handler
                    "options": {"error": "error_handler", "error_next_value": "", "error_handler": ""}
                }
            }
        }
    ]
)
def taskone(a, b):
    print(a, b)
taskone(3, 4)


tasks["run"](task="taskname")
