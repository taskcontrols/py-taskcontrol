from src.workflow import workflow, Task


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
                        # 
                        # Default error_handler implementation used internally, if no 
                        #           error_handler is provided
                        # 
                        # Implementation One:
                        #   if error_next_value defined
                        #       lambda err, value: (err, error_next_value)
                        # Implementation Two:
                        #   if error_next_value not defined
                        #       lambda err, value: (err, None)
                        # 
                        # Returning the two value tuple in error_handler implementation is compulsary
                        #       err is the error that occurred
                        #       error_next_value is error_next_value provided in options
                        # 
                        "error_handler": lambda err, value: (err, None)
                    }
                }
            }
        }
    ]
)
def taskone(a, b):
    print("Running my task: taskone", a, b)


# Invocation is needed to add the task with function arguments
# Invoke this where needed
# Example: Within some other function
taskone(3, 4)


@workflow(name="tasktwo", task_order=2, before=[], after=[])
def tasktwo(a, b):
    print("Running my task: tasktwo", a, b)


tasktwo(5, 6)

# Invoke this where needed
# Example: Within some other function
Task().run(task=["taskname", "tasktwo"])
# Task().run(task="taskname")
