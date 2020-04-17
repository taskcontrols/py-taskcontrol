from src.workflow import workflow, tasks


def test(k):
    print(k)


@workflow(
    name="taskname", task_order=1,
    before=[
        {
            # before middleware order followed will be of the list sequence
            "functions": [test],
            "flow": {
                "test": {
                    "args": [], "kwargs": {"k": "Testing message"},
                    # error { str }: [next, exit], error_handler { function }
                    "options": {"error": "next", "error_next_value": ""}
                }
            }
        }
    ],
    after=[
        {
            # after middleware order followed will be of the list sequence
            "functions": [test],
            "flow": {
                "test": {
                    "args": [], "kwargs": {"k": "Testing message"},
                    # error { str }: [next, exit], error_handler { function }
                    # "options": {"error": "exit"}
                    "options": {"error": "error_handler", "error_next_value": "", "error_handler": ""}
                }
            }
        }
    ]
)
def taskone(a, b):
    print(a, b)


taskone(3, 4)


tasks()["run"](task="taskname")
