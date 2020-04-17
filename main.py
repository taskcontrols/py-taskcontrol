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
                    
                    # options { error : str,  error_next_value: Object, error_handler: function }
                    # 
                    # error { str }: [next, error_handler, exit]
                    # error_handler { function }
                    # error_next_value { object }
                    #
                    # Usage:
                    # "options": {"error": "next", "error_next_value": "value"}
                    # "options": {"error": "exit"}
                    # "options": { 
                    #    "error": "error_handler", error_handler: func, "error_next_value": "value"
                    #    }

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
                    "options": {
                            "error": "error_handler",
                            "error_next_value": "value",
                            "error_handler": lambda err, value: value
                        }
                }
            }
        }
    ]
)
def taskone(a, b):
    print(a, b)

# Invocation is needed to add the task with function arguments
# Invoke this where needed
# Example: Within some other function
taskone(3, 4)

# Invoke this where needed
# Example: Within some other function
# tasks()["run"](task=["taskname", "tasktwo"])
tasks()["run"](task="taskname")
