# TODO: Reorder tasks
import pytest

from taskcontrol.workflow import workflow, Tasks


# decorator applied on a function and function invocation creates the task
# decorator creates tasks only on function invocation
# decorator creates instance tasks
# decorator creates shared tasks

# IMPORTANT:
# Maintain the results of all tests even with change of flow
# These are functionality tests for usage of decorator
# TODO: Write result asserts for some

# [   {
#     'result': [
#         {'result': (11, 12, 'one more'), 'function': 'nesttree', 'name': 'taskname'},
#     ]
#     }
# ]

class TestDecorator():

    def test_1_0_creates_task_with_bare_minimals(self):
        t = Tasks()

        @workflow(
            name="taskname",
            task_instance=t,
            args=[1, 2], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return ("one", )

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == tuple
                    assert j.get("result") == ("one", )
                    assert j.get("function") == "taskone"
                    assert j.get("name") == "taskname"

    def test_1_1_creates_task_before_as_list(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 1, 2

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            args=[1, 2], kwargs={},
            before=[{
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                    "options": {"error": "next", "error_next_value": ""}
                    }])
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a, b

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == tuple
                    assert j.get("result") == (1, 2)
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

    def test_1_2_creates_task_before_as_dict(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 1, 2

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            args=[1, 2], kwargs={},
            before={
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            })
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a, b

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == tuple
                    assert j.get("result") == (1, 2)
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

    def test_1_3_creates_task_after_as_list(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 1, 2

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            args=[1, 2], kwargs={},
            after=[{
                "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, value)}
            }])
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a, b

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == tuple
                    assert j.get("result") == (1, 2)
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

    def test_1_4_creates_task_after_as_dict(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 1, 2

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
            before=[{
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }],
            after={
                "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, value)}
            })
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a, b

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == tuple
                    assert j.get("result") == (1, 2)
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

    def test_1_5_creates_task_after_and_before_as_dict(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 1, 2

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            args=[1, 2], kwargs={},
            before={
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            },
            after={
                "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, value)}
            })
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a, b

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == tuple
                    assert j.get("result") == (1, 2)
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

    def test_1_6_creates_task_after_and_before_as_list(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 1, 2

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            args=[1, 2], kwargs={},
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
            return a, b

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == tuple
                    assert j.get("result") == (1, 2)
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

    def test_1_7_creates_task_with_before_list_with_right_args(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 1, 2

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
            before=[{
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }])
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a, b

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == tuple
                    assert j.get("result") == (1, 2)
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

    def test_1_8_creates_task_with_after_list_with_right_args(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 1, 2

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            args=[1, 2], kwargs={},
            after=[{
                "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, value)}
            }])
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a, b

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == tuple
                    assert j.get("result") == (1, 2)
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

    def test_1_9_doesnot_creates_task_with_before_list_with_wrong_args_throws_Exception(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items",
                      k, c, d, kwargs)

            @workflow(
                name="taskname", task_order=1, task_instance=t,
                shared=False, args=[1, 2], kwargs={}, log=False,
                before=[{
                    "function": middleware, "args": [11], "kwargs": {"d": "Before Testing message Middleware "},
                    "options": {"error": "next", "error_next_value": ""}
                }],
                after=[{
                    "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                    "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, value)}
                }])
            def taskone(ctx, result, a, b):
                print("Running my task function: taskone", a, b)

            result = t.run(tasks="taskname")

        assert e.type is Exception

    def test_1_10_doesnot_creates_task_with_after_list_with_wrong_args_throws_TypeError(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items",
                      k, c, d, kwargs)

            @workflow(
                name="taskname", task_order=1, task_instance=t,
                shared=False, args=[1, 2], kwargs={}, log=False,
                before=[{
                    "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                    "options": {"error": "next", "error_next_value": ""}
                }],
                after=[{
                    "function": middleware, "args": [13], "kwargs": {"d": "After Middleware Testing message"},
                    "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, value)}
                }])
            def taskone(ctx, result, a, b):
                print("Running my task function: taskone", a, b)

            result = t.run(tasks="taskname")

        assert e.type is Exception

    def test_1_11_doesnot_creates_task_with__before_and_after_list_with_wrong_args_throws_TypeError(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items",
                      k, c, d, kwargs)

            @workflow(
                name="taskname", task_order=1, task_instance=t,
                shared=False, args=[1, 2], kwargs={}, log=False,
                before=[{
                    "function": middleware, "args": [12], "kwargs": {"d": "Before Testing message Middleware "},
                    "options": {"error": "next", "error_next_value": ""}
                }],
                after=[{
                    "function": middleware, "args": [13], "kwargs": {"d": "After Middleware Testing message"},
                    "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, value)}
                }])
            def taskone(ctx, result, a, b):
                print("Running my task function: taskone", a, b)

            result = t.run(tasks="taskname")

        assert e.type is Exception

    def test_1_12_doesnot_creates_task_with_wrong_print_args_for_task_function_throws_TypeError(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items",
                      k, c, d, kwargs)
                return 1, 2

            @workflow(
                name="taskname", task_order=1, task_instance=t,
                shared=False, args=[1, 2], kwargs={}, log=False,
                before=[{
                    "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                    "options": {"error": "next", "error_next_value": ""}
                }],
                after=[{
                    "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                    "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, value)}
                }])
            def taskone(ctx, result, a, b):
                print("Running my task function: taskone", a, c)
                return a, b

            result = t.run(tasks="taskname")

        assert e.type is Exception

    def test_1_13_doesnot_creates_task_with_wrong_def_of_args_for_task_function_throws_TypeError(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items",
                      k, c, d, kwargs)
                return 1, 2

            @workflow(
                name="taskname", task_order=1, task_instance=t,
                shared=False, args=[1, 2], kwargs={}, log=False,
                before=[{
                    "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                    "options": {"error": "next", "error_next_value": ""}
                }],
                after=[{
                    "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                    "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, value)}
                }])
            def taskone(ctx, result, a):
                print("Running my task function: taskone", a)
                return 1, 2

            result = t.run(tasks="taskname")

        assert e.type is Exception

    def test_1_14_creates_instance_task(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 114

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
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
            return 114

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 114
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

    def test_1_15_doesnot_create_instance_task(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 115

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
            return 115

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks="shared:taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 115
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert type(t.getter("tasks", "taskname")) == list
        assert t.get_all_tasks("taskname", []) == []
        assert len(t.get_all_tasks("taskname", [])) == 0
        assert t.get_all_tasks("shared:taskname", []) != []

        t.shared.deleter("tasks", 'taskname')

    def test_1_16_creates_shared_task(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 116

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
            return 116

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks="shared:taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 116
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert type(t.getter("tasks", "taskname")) == list
        assert t.get_all_tasks("taskname", []) == []
        assert len(t.get_all_tasks("taskname", [])) == 0
        assert t.get_all_tasks("shared:taskname", []) != []

        t.shared.deleter("tasks", 'taskname')

    def test_1_17_doesnot_create_shared_task(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items", k, c, d, kwargs)
                return 117

            @workflow(
                name="taskname", task_order=1, task_instance=t,
                shared=False, args=[1], kwargs={}, log=False,
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
                return 117

            result = t.run(tasks="taskname")
        
        assert e.type is Exception

    def test_1_18_doesnot_create_shared_task(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items", k, c, d, kwargs)
                return 118

            @workflow(
                name="taskname", task_order=1, task_instance=t,
                shared=False, args=[1], kwargs={}, log=False,
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
                return 118

            result = t.run(tasks="shared:tasktwo")
        
        assert e.type is Exception

    def test_1_19_doesnot_create_shared_task(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items", k, c, d, kwargs)
                return 119

            @workflow(
                name="taskname", task_order=1, task_instance=t,
                shared=False, args=[1], kwargs={}, log=False,
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
                return 119

            result = t.run(tasks="taskname")

        assert e.type is Exception

    def test_1_20_doesnot_create_shared_task(self):
        
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 120

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
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
            return 120

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 120
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert type(t.getter("tasks", "taskname")) == list
        assert t.get_all_tasks("taskname", []) != []
        assert len(t.get_all_tasks("taskname", [])) == 1
        assert len(t.get_all_tasks("shared:taskname", [])) == 0
        assert type(t.get_all_tasks("shared:taskname", [])) == list
        assert t.get_all_tasks("shared:taskname", []) == []

    def test_1_21_does_not_create_task_without_name_throws_TypeError(self):
        with pytest.raises(TypeError) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items",
                      k, c, d, kwargs)
                return 121

            @workflow(
                task_order=1, task_instance=t,
                shared=False, args=[1, 2], kwargs={}, log=False,
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
                return 121

            result = t.run(tasks="taskname")

        assert e.type is TypeError

    def test_1_22_does_not_create_task_without_task_instance_throws_TypeError(self):
        with pytest.raises(TypeError) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items",
                      k, c, d, kwargs)
                return 122

            @workflow(
                name="taskname", task_order=1,
                shared=False, args=[1, 2], kwargs={}, log=False,
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
                return 122

            result = t.run(tasks="taskname")

        assert e.type is TypeError

    def test_1_23_creates_task_without_taskorder(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items",
                  k, c, d, kwargs)
            return 123

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
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
            return 123

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 123
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

    def test_1_24_creates_task_without_before(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 124

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
            after=[{
                "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, value)}
            }])
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 124

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 124
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

    def test_1_25_creates_task_without_after(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 125

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
            before=[{
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }])
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 125

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 125
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

    def test_1_26_creates_task_without_log(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 126

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
            }])
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 126

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 126
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list



## decorator error scenarios of instance tasks


# IMPORTANT:
# Maintain the results of all tests even with change of flow
# These are functionality tests for running of decorator created tasks or shared tasks

class TestInstanceErrorScenarios():
    def test_2_1_throws_error_without_name(self):
        pass
    def test_2_2_throws_error_without_instance(self):
        pass
    def test_2_3_runs_doesnot_throw_error_without_shared(self):
        pass
    def test_2_4_runs_default_shared_is_False(self):
        pass
    def test_2_5_runs_doesnot_throw_error_without_order(self):
        pass
    def test_2_6_runs_default_order_is_FIFO(self):
        pass
    def test_2_7_runs_doesnot_throw_error_without_before(self):
        pass
    def test_2_8_runs_default_before_empty_list(self):
        pass
    def test_2_9_runs_doesnot_throw_error_without_after(self):
        pass
    def test_2_10_runs_default_after_empty_list(self):
        pass
    def test_2_11_runs_doesnot_throw_error_without_log(self):
        pass
    def test_2_12_runs_default_log_is_false(self):
        pass
    def test_2_13_runs_wrong_taskname_and_returns_no_result(self):
        pass
    


## decorator error scenarios of shared tasks

# IMPORTANT:
# Maintain the results of all tests even with change of flow
# These are functionality tests for running of decorator created tasks or shared tasks

class TestSharedErrorScenarios():
    def test_3_1_runs_doesnot_throw_error_without_shared(self):
        pass
    def test_3_2_runs_default_shared_is_False(self):
        pass
    def test_3_3_runs_wrong_shared_taskname_and_returns_no_result(self):
        pass


# decorator runs instance single tasks
# decorator runs instance multiple tasks
# decorator runs all instance tasks

# IMPORTANT:
# Maintain the results of all tests even with change of flow
# These are functionality tests for running of decorator created tasks

class TestTaskRunner():

    def test_4_1_run_single_instance_task(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 201

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
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 201

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 201
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

    def test_4_2_run_doesnot_single_instance_task(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 202

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 202

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert type(t.shared.getter("tasks", "taskname")) == list
        assert len(t.shared.getter("tasks", "taskname")) == 1

        t.shared.deleter("tasks", 'taskname')

    def test_4_3_run_multiple_instance_task(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 203

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
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 203

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 203
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list


        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 203

        result = t.run(tasks="tasktwo")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 203
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        @workflow(
            name="taskthree", task_order=1, task_instance=t,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskthree", a, b)
            return 203

        result = t.run(tasks=["taskthree"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 203
                    assert (j.get("function") == "taskthree" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree"

        assert t.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskthree") == []
        assert type(t.getter("tasks", "shared:taskthree")) == list

        result = t.run(tasks=["tasktwo", "taskname", "taskthree"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 3

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 203
                    assert (j.get("function") == "taskone" or j.get("function") == "tasktwo" or j.get("function") == "taskthree" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskname" or j.get("name") == "taskthree"

        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

    def test_4_4_doesnot_run_multiple_instance_task(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 204

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
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 204

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 204
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        t = Tasks()

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
            print("Running my task function: tasktwo", a, b)
            return 204

        result = t.run(tasks="shared:tasktwo")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 204
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo") == []
        assert type(t.getter("tasks", "tasktwo")) == list

        result = t.run(tasks=["taskname", "shared:tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 204
                    assert (j.get("function") == "taskone" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo"

        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert len(t.shared.getter("tasks", "tasktwo")) == 1
        assert type(t.shared.getter("tasks", "tasktwo")) == list

        t.shared.deleter("tasks", "tasktwo")

    def test_4_5_run_single_instance_multiple_tasks(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 205

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
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 205

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 205
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

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
            print("Running my task function: tasktwo", a, b)
            return 205

        result = t.run(tasks="shared:tasktwo")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 205
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo") == []
        assert type(t.getter("tasks", "tasktwo")) == list

        result = t.run(tasks=["taskname", "shared:tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 205
                    assert (j.get("function") == "taskone" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname" 
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert len(t.shared.getter("tasks", "tasktwo")) == 1
        assert type(t.shared.getter("tasks", "tasktwo")) == list

        t.shared.deleter("tasks", "tasktwo")

    def test_4_6_doesnot_run_single_instance_multiple_tasks(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 206

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
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 206

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 206
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

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
            print("Running my task function: tasktwo", a, b)
            return 206

        result = t.run(tasks="shared:tasktwo")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 206
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo") == []
        assert type(t.getter("tasks", "tasktwo")) == list

        result = t.run(tasks=["taskname", "shared:tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 206
                    assert (j.get("function") == "taskone" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname" 
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert len(t.shared.getter("tasks", "tasktwo")) == 1
        assert type(t.shared.getter("tasks", "tasktwo")) == list

        result = t.run(tasks=["taskname", "tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 206
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname" 
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert len(t.shared.getter("tasks", "tasktwo")) == 1
        assert type(t.shared.getter("tasks", "tasktwo")) == list

        t.shared.deleter("tasks", "tasktwo")

    def test_4_7_doesnot_run_single_instance_multiple_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 207

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
            print("Running my task function: taskname", a, b)
            return 207

        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 207

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 207
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks="tasktwo")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 207
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        result = t.run(tasks=["taskname", "shared:tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        # Running two tasks, but result is one
        assert len(result) != 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 207
                    assert (j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskname") == []
        assert type(t.shared.getter("tasks", "taskname")) == list

    def test_4_8_run_all_instance_task(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 208

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
            return 208

        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 208

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 208
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks="tasktwo")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 208
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        result = t.run(tasks=["taskname"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 208
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["taskname", "tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 208
                    assert (j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        result = t.run(tasks=1)

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 208
                    assert (j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        result = t.run(tasks="1")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 208
                    assert (j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        result = t.run(tasks=["1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 208
                    assert (j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

    def test_3_9_run_doesnot_all_instance_task(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 209

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
            return 209

        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 209

        result = t.run(tasks="tasktwo")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 209
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 209
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["taskname", "tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 209
                    assert (j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        result = t.run(tasks=["shared:taskname", "shared:tasktwo"])

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks=["tasknam", "shared:taskto"])

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks=["shared:1"])

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks="shared:1")

        assert type(result) == list
        assert len(result) == 0


## decorator runs shared single task
## decorator runs shared multiple tasks
## decorator runs shared all tasks


# IMPORTANT:
# Maintain the results of all tests even with change of flow
# These are functionality tests for running of decorator created shared tasks

class TestSharedTaskRunner():

    def test_5_1_run_single_shared_from_single_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 301

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 301
        
        result = t.run(tasks="shared:taskname")
        
        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 301
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["shared:taskname"])
        
        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 301
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        t.shared.deleter("tasks", 'taskname')

    def test_5_2_doesnot_run_single_shared_from_instance_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 302

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
            print("Running my task function: taskname", a, b)
            return 302

        result = t.run(tasks="shared:tasknam")

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks="shared:taskname")

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

    def test_5_3_doesnot_run_single_shared_from_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 303

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 303

        result = t.run(tasks="shared:tasknam")

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["shared:tasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        t.shared.deleter("tasks", 'taskname')

    def test_5_4_doesnot_run_single_instance_task_from_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 304

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 304

        result = t.run(tasks="tasknam")

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks=["tasknam"])

        assert type(result) == list
        assert len(result) == 0

        t.shared.deleter("tasks", 'taskname')

    def test_5_5_doesnot_run_single_instance_task_from_instance_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 305

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
            print("Running my task function: taskname", a, b)
            return 305

        result = t.run(tasks="tasknam")

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks=["tasknam"])

        assert type(result) == list
        assert len(result) == 0

    def test_5_6_doesnot_run_single_shared_task_from_multiple_instance_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 306

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
            print("Running my task function: taskname", a, b)
            return 306

        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 306

        result = t.run(tasks="shared:sharedtaskname")

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["shared:sharedtaskname"])

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks="shared:sharedtaskname")

        assert type(result) == list
        assert len(result) == 0

        assert s.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks=["shared:sharedtaskname"])

        assert type(result) == list
        assert len(result) == 0

        assert s.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

    def test_5_7_doesnot_run_single_instance_task_from_multiple_instance_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 307

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
            print("Running my task function: taskname", a, b)
            return 307
        
        s = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=s,
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
            print("Running my task function: taskname", a, b)
            return 307

        result = t.run(tasks="tasknam")

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["tasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks="tasknam")

        assert type(result) == list
        assert len(result) == 0

        assert s.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.getter("tasks", "taskname")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks=["tasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert s.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.getter("tasks", "taskname")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

    def test_5_8_doesnot_run_single_shared_task_from_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 308

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 308
        
        @workflow(
            name="taskthree", task_order=1, task_instance=t,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskthree", a, b)
            return 308

        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
            print("Running my task function: tasktwo", a, b)
            return 308

        result = t.run(tasks="shared:sharedtaskname")

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["shared:sharedtaskname"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks="shared:sharedtaskname")

        assert type(result) == list
        assert len(result) == 0

        assert s.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks=["shared:sharedtaskname"])

        assert type(result) == list
        assert len(result) == 0

        assert s.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')
        t.shared.deleter("tasks", 'tasktwo')

    def test_5_9_doesnot_run_single_instance_task_from_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 309

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 309
        
        @workflow(
            name="taskthree", task_order=1, task_instance=t,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskthree", a, b)
            return 309

        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
            print("Running my task function: tasktwo", a, b)
            return 309

        result = t.run(tasks="sharedtaskname")

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["sharedtaskname"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks="sharedtaskname")

        assert type(result) == list
        assert len(result) == 0

        assert s.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert s.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(s.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert s.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks=["sharedtaskname"])

        assert type(result) == list
        assert len(result) == 0

        assert s.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert s.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(s.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert s.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')
        t.shared.deleter("tasks", 'tasktwo')

    def test_5_10_doesnot_run_single_shared_from_mixed_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 310

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
            print("Running my task function: taskname", a, b)
            return 310

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
            print("Running my task function: tasktwo", a, b)
            return 310

        result = t.run(tasks="shared:sharedtaskname")

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["shared:sharedtasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

        t.shared.deleter("tasks", 'tasktwo')

    def test_5_11_doesnot_run_single_instance_task_from_mixed_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 311

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
            print("Running my task function: taskname", a, b)
            return 311

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
            print("Running my task function: tasktwo", a, b)
            return 311

        result = t.run(tasks="sharedtaskname")

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["sharedtasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

        t.shared.deleter("tasks", 'tasktwo')

    def test_5_12_run_single_shared_from_instance_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 312

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
            print("Running my task function: taskname", a, b)
            return 312

        result = t.run(tasks="shared:tasknam")

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks="shared:sharedtaskname")

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

        result = t.run(tasks=["shared:tasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["shared:sharedtaskname"])

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

    def test_5_13_run_single_shared_from_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 313

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 313
        
        result = t.run(tasks="shared:taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 313
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

        result = t.run(tasks=["shared:taskname"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 313
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

        t.shared.deleter("tasks", 'taskname')

    def test_5_14_run_single_instance_task_from_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 314

        t = Tasks()

        @workflow(
            name="sharedtaskname", task_order=1, task_instance=t,
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
        def sharedtaskname(ctx, result, a, b):
            print("Running my task function: sharedtaskname", a, b)
            return 314

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "sharedtaskname")[0].get("name") == "sharedtaskname"
        assert type(t.shared.getter("tasks", "sharedtaskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list
        assert t.getter("tasks", "taskname") == []
        assert type(t.getter("tasks", "taskname")) == list

        result = t.run(tasks=["taskname"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "sharedtaskname")[0].get("name") == "sharedtaskname"
        assert type(t.shared.getter("tasks", "sharedtaskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "taskname")) == list
        assert t.getter("tasks", "taskname") == []
        assert type(t.getter("tasks", "taskname")) == list

        t.shared.deleter("tasks", 'sharedtaskname')

    def test_5_15_run_single_instance_task_from_instance_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 315

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
            print("Running my task function: taskname", a, b)
            return 315

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 315
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        result = t.run(tasks=["taskname"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 315
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        result = t.run(tasks="tasknam")

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks=["tasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

    def test_5_16_run_single_shared_from_mixed_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 316

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
            print("Running my task function: taskname", a, b)
            return 316

        @workflow(
            name="sharedtaskname", task_order=1, task_instance=t,
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
        def sharedtaskname(ctx, result, a, b):
            print("Running my task function: sharedtaskname", a, b)
            return 316

        result = t.run(tasks="shared:sharedtaskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 316
                    assert (j.get("function") == "sharedtaskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "sharedtaskname"

        assert t.shared.getter("tasks", "sharedtaskname")[0].get("name") == "sharedtaskname"
        assert type(t.shared.getter("tasks", "sharedtaskname")[0].get("name")) == str
        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

        result = t.run(tasks=["shared:sharedtaskname"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 316
                    assert (j.get("function") == "sharedtaskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "sharedtaskname"

        assert t.shared.getter("tasks", "sharedtaskname")[0].get("name") == "sharedtaskname"
        assert type(t.shared.getter("tasks", "sharedtaskname")[0].get("name")) == str
        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

        result = t.run(tasks="shared:sharedtasknam")

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "sharedtaskname")[0].get("name") == "sharedtaskname"
        assert type(t.shared.getter("tasks", "sharedtaskname")[0].get("name")) == str
        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

        result = t.run(tasks=["shared:sharedtasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "sharedtaskname")[0].get("name") == "sharedtaskname"
        assert type(t.shared.getter("tasks", "sharedtaskname")[0].get("name")) == str
        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

        t.shared.deleter("tasks", 'sharedtaskname')

    def test_5_17_run_single_instance_task_from_mixed_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 317

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
            print("Running my task function: taskname", a, b)
            return 317

        @workflow(
            name="sharedtaskname", task_order=1, task_instance=t,
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
        def sharedtaskname(ctx, result, a, b):
            print("Running my task function: sharedtaskname", a, b)
            return 317

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 317
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.shared.getter("tasks", "sharedtaskname")[0].get("name") == "sharedtaskname"
        assert type(t.shared.getter("tasks", "sharedtaskname")[0].get("name")) == str
        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

        result = t.run(tasks=["taskname"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 317
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.shared.getter("tasks", "sharedtaskname")[0].get("name") == "sharedtaskname"
        assert type(t.shared.getter("tasks", "sharedtaskname")[0].get("name")) == str
        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

        result = t.run(tasks="tasknam")

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "sharedtaskname")[0].get("name") == "sharedtaskname"
        assert type(t.shared.getter("tasks", "sharedtaskname")[0].get("name")) == str
        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

        result = t.run(tasks=["tasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "sharedtaskname")[0].get("name") == "sharedtaskname"
        assert type(t.shared.getter("tasks", "sharedtaskname")[0].get("name")) == str
        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:sharedtaskname") == []
        assert type(t.getter("tasks", "shared:sharedtaskname")) == list

        t.shared.deleter("tasks", 'sharedtaskname')

    def test_5_18_run_single_shared_task_from_multiple_instance_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 318

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
            print("Running my task function: taskname", a, b)
            return 318

        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 318

        result = t.run(tasks="shared:sharedtasknam")

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks=["shared:sharedtasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks="shared:sharedtasknam")

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["shared:sharedtasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert s.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

    def test_5_19_run_single_instance_task_from_multiple_instance_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 319

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
            print("Running my task function: taskname", a, b)
            return 319

        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 319

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 319
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        result = t.run(tasks=["taskname"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 319
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        result = t.run(tasks="tasknam")

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks=["tasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks="tasktwo")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 319
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        result = s.run(tasks=["tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 319
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        result = s.run(tasks="tasknam")

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["tasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert s.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

    def test_5_20_run_single_shared_task_from_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 320

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 320

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
            print("Running my task function: tasktwo", a, b)
            return 320

        result = t.run(tasks="shared:taskname")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 320
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["shared:taskname"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 320
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks="shared:tasktwo")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 320
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["shared:tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 320
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks="shared:sharedtaskname")

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["shared:sharedtaskname"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'tasktwo')

    def test_5_21_run_single_instance_task_from_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 321

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 321

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
            print("Running my task function: tasktwo", a, b)
            return 321

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["taskname"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'tasktwo')

    def test_5_22_doesnot_run_multiple_shared_from_multiple_instance_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 322

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
            print("Running my task function: taskname", a, b)
            return 322
        
        s = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=s,
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
            print("Running my task function: taskname", a, b)
            return 322

        result = t.run(tasks=["shared:taskname", "shared:tasktwo"])

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks=["shared:taskname", "shared:tasktwo"])

        assert type(result) == list
        assert len(result) == 0

        assert s.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.getter("tasks", "taskname")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

    def test_5_23_doesnot_run_multiple_shared_from_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 323

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 323
        
        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
            print("Running my task function: tasktwo", a, b)
            return 323

        result = t.run(tasks=["shared:tasknam", "shared:tasktw"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = t.run(tasks=["shared:tasktw"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks=["shared:tasknam", "shared:tasktw"])

        assert type(result) == list
        assert len(result) == 0

        assert s.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert s.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "shared:tasktwo") == []
        assert type(s.getter("tasks", "shared:tasktwo")) == list
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks=["shared:tasktw"])

        assert type(result) == list
        assert len(result) == 0

        assert s.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert s.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "shared:tasktwo") == []
        assert type(s.getter("tasks", "shared:tasktwo")) == list
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'tasktwo')

    def test_5_24_doesnot_run_multiple_instance_from_multiple_instance_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 324

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
            print("Running my task function: taskname", a, b)
            return 324

        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 324

        result = t.run(tasks=["tasknam", "tasktw"])

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks=["tasknam", "tasktw"])

        assert type(result) == list
        assert len(result) == 0

        assert s.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "shared:tasktwo") == []
        assert type(s.getter("tasks", "shared:tasktwo")) == list

    def test_5_25_doesnot_run_multiple_instance_from_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 325

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 325

        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
            print("Running my task function: tasktwo", a, b)
            return 325

        result = t.run(tasks=["tasknam", "tasktw"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        result = s.run(tasks=["tasknam", "tasktw"])

        assert type(result) == list
        assert len(result) == 0

        assert s.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert s.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "shared:tasktwo") == []
        assert type(s.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'tasktwo')

    def test_5_26_doesnot_run_multiple_shared_from_mixed_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 326

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 326
        
        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 326

        result = t.run(tasks=["shared:tasknam", "shared:tasktw"])

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["shared:tasknam", "shared:tasktw"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert s.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list
        assert s.getter("tasks", "shared:tasktwo") == []
        assert type(s.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')

    def test_5_27_doesnot_run_multiple_instance_from_mixed_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 327

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 327
        
        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 327

        result = t.run(tasks=["tasknam", "tasktw"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert s.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        result = s.run(tasks=["tasknam", "tasktw"])

        assert type(result) == list
        assert len(result) == 0

        assert s.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert s.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list
        assert s.getter("tasks", "shared:tasktwo") == []
        assert type(s.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')

    def test_5_28_doesnot_run_multiple_instance_from_multiple_instance_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 328

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 328
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 328

        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
            print("Running my task function: tasktwo", a, b)
            return 328

        result = t.run(tasks=["tasktw", "taskname"])

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["tasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert s.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert s.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.shared.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list
        assert s.getter("tasks", "shared:tasktwo") == []
        assert type(s.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'tasktwo')

    def test_5_29_doesnot_run_multiple_shared_from_multiple_instance_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 329

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 329
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 329
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskthree", a, b)
            return 329

        result = t.run(tasks=["shared:tasktwo", "shared:tasknam"])

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks=["shared:tasknam"])

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["shared:tasktwo", "shared:tasknam"])

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["shared:tasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert s.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert s.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(s.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list
        assert s.getter("tasks", "shared:tasktwo") == []
        assert type(s.getter("tasks", "shared:tasktwo")) == list
        assert s.getter("tasks", "shared:taskthree") == []
        assert type(s.getter("tasks", "shared:taskthree")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')

    def test_5_30_run_multiple_shared_from_multiple_instance_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 330

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
            print("Running my task function: taskname", a, b)
            return 330
        
        @workflow(
            name="taskfour", task_order=1, task_instance=t,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskfour", a, b)
            return 330
        
        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 330
        
        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskthree", a, b)
            return 330

        result = t.run(tasks=["shared:taskname", "shared:taskthree", "shared:taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 330
                    assert (j.get("function") == "taskname" or j.get("function") == "taskthree" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "taskthree" or j.get("name") == "taskfour"

        result = t.run(tasks=["shared:taskthree", "shared:taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 330
                    assert (j.get("function") == "taskname" or j.get("function") == "taskthree" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "taskthree" or j.get("name") == "taskfour"

        result = t.run(tasks=["shared:taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 330
                    assert (j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour"

        result = t.run(tasks=["shared:taskthre"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(t.shared.getter("tasks", "taskfour")[0].get("name")) == str

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert s.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        t.shared.deleter("tasks", 'taskfour')
        t.shared.deleter("tasks", 'taskthree')

    def test_5_31_run_multiple_shared_from_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 331

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
            print("Running my task function: taskname", a, b)
            return 331
        
        @workflow(
            name="taskfour", task_order=1, task_instance=t,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskfour", a, b)
            return 331
        
        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 331
        
        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskthree", a, b)
            return 331

        result = t.run(tasks=["shared:taskname", "shared:taskthree", "shared:taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 331
                    assert (j.get("function") == "taskname" or j.get("function") == "taskthree" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "taskthree" or j.get("name") == "taskfour"

        result = t.run(tasks=["shared:taskthree", "shared:taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 331
                    assert (j.get("function") == "taskthree" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree" or j.get("name") == "taskfour"

        result = t.run(tasks=["shared:taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 331
                    assert (j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour"

        result = t.run(tasks=["shared:taskthre"])

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert s.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(t.shared.getter("tasks", "taskfour")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        t.shared.deleter("tasks", 'taskfour')
        t.shared.deleter("tasks", 'taskthree')

    def test_5_32_run_multiple_instance_from_multiple_instance_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 332

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
            print("Running my task function: taskname", a, b)
            return 332
        
        s = Tasks()

        @workflow(
            name="tasktwo", task_order=1, task_instance=s,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 332

        result = t.run(tasks=["taskname", "tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 332
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        result = t.run(tasks=["taskname"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 332
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        result = t.run(tasks=["tasknam"])

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["taskname", "tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 332
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        result = s.run(tasks=["tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 332
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        result = s.run(tasks=["tasktw"])

        assert type(result) == list
        assert len(result) == 0

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert s.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(s.getter("tasks", "tasktwo")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list
        assert s.getter("tasks", "shared:tasktwo") == []
        assert type(s.getter("tasks", "shared:tasktwo")) == list

    def test_5_33_run_multiple_instance_from_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 333

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 333
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 333
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskthree", a, b)
            return 333
        
        @workflow(
            name="taskfour", task_order=1, task_instance=s,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskfour", a, b)
            return 333

        result = t.run(tasks=["tasktwo", "taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 333
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        result = t.run(tasks=["tasknam"])

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["tasktwo", "taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 333
                    assert (j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour"

        result = s.run(tasks=["tasknam"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str
        assert t.getter("tasks", "shared:taskname") == []
        assert type(t.getter("tasks", "shared:taskname")) == list

        assert s.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(s.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert s.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(s.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskname") == []
        assert type(s.getter("tasks", "shared:taskname")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')

    def test_5_34_run_multiple_shared_from_mixed_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 334

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 334
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 334
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskthree", a, b)
            return 334
        
        @workflow(
            name="taskfour", task_order=1, task_instance=s,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskfour", a, b)
            return 334

        result = t.run(tasks=["shared:taskthree", "shared:taskname"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 334
                    assert (j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree" or j.get("name") == "taskname"

        result = t.run(tasks=["shared:taskname"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 334
                    assert (j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname"

        result = t.run(tasks=["shared:taskthree"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 334
                    assert (j.get("function") == "taskthree" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree"

        result = t.run(tasks=["shared:tasktw", "shared:taskfou"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskfour") == []
        assert type(s.getter("tasks", "shared:taskfour")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')

    def test_5_35_run_multiple_instance_from_mixed_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 335

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 335
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 335
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskthree", a, b)
            return 335
        
        @workflow(
            name="taskfour", task_order=1, task_instance=s,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskfour", a, b)
            return 335

        result = t.run(tasks=["tasktwo", "taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 335
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"

        result = t.run(tasks=["tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 335
                    assert (j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo"

        result = s.run(tasks=["taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 335
                    assert (j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour"

        result = t.run(tasks=["tasktw", "taskfou"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str

        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str

        assert s.getter("tasks", "shared:taskfour") == []
        assert type(s.getter("tasks", "shared:taskfour")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')

    def test_5_36_run_multiple_instance_from_multiple_instance_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 336

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 336
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 336
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskthree", a, b)
            return 336
        
        @workflow(
            name="taskfour", task_order=1, task_instance=s,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskfour", a, b)
            return 336

        result = t.run(tasks=["tasktwo", "taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 336
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"

        result = s.run(tasks=["tasktwo", "taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 336
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"

        result = s.run(tasks=["tasktw", "taskfou"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskfour") == []
        assert type(s.getter("tasks", "shared:taskfour")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')

    def test_5_37_run_multiple_shared_from_multiple_instance_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 337

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 337
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 337
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskthree", a, b)
            return 337
        
        @workflow(
            name="taskfour", task_order=1, task_instance=s,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskfour", a, b)
            return 337

        result = t.run(tasks=["shared:taskthree", "tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 337
                    assert (j.get("function") == "taskthree" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree" or j.get("name") == "tasktwo"
        
        result = t.run(tasks=["shared:taskname", "tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 337
                    assert (j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo"

        result = t.run(tasks=["shared:taskname", "taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 337
                    assert (j.get("function") == "taskname" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "taskfour"

        result = s.run(tasks=["shared:taskname", "shared:taskthree"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 337
                    assert (j.get("function") == "taskname" or j.get("function") == "taskthree" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "taskthree"

        result = s.run(tasks=["shared:tasktw", "shared:taskfou"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskfour") == []
        assert type(s.getter("tasks", "shared:taskfour")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')

    def test_5_38_doesnot_run_all_from_multiple_instance_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 338

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 338
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 338
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskthree", a, b)
            return 338
        
        @workflow(
            name="taskfour", task_order=1, task_instance=s,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskfour", a, b)
            return 338

        # result = t.run(tasks=[1, "shared:1"])
        result = t.run(tasks=[1])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 338
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "tasktwo" or j.get("name") == "taskname"
        
        result = t.run(tasks=["1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 338
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "tasktwo" or j.get("name") == "taskname"
        
        result = t.run(tasks=["shared:1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 338
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "tasktwo" or j.get("name") == "taskname"
        
        result = t.run(tasks=1)

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 338
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "tasktwo" or j.get("name") == "taskname"
        
        result = t.run(tasks="1")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 338
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "tasktwo" or j.get("name") == "taskname"
        
        result = t.run(tasks="shared:1")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 338
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "tasktwo" or j.get("name") == "taskname"
        
        result = s.run(tasks=[1])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 338
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "tasktwo" or j.get("name") == "taskname"
        
        result = s.run(tasks=["1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 338
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "tasktwo" or j.get("name") == "taskname"
        
        result = s.run(tasks=["shared:1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 338
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "tasktwo" or j.get("name") == "taskname"
        
        result = s.run(tasks=1)

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 338
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "tasktwo" or j.get("name") == "taskname"
        
        result = s.run(tasks="1")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 338
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "tasktwo" or j.get("name") == "taskname"
        
        result = s.run(tasks="shared:1")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 338
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "tasktwo" or j.get("name") == "taskname"
        
        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskfour") == []
        assert type(s.getter("tasks", "shared:taskfour")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')
    
    def test_5_39_run_all_from_multiple_instance_multiple_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 339

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 339
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 339
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 339
        
        @workflow(
            name="taskfour", task_order=1, task_instance=s,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 339

        result = t.run(tasks=[1, "shared:1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 3

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 339
                    assert (j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree" or j.get("name") == "taskname" or j.get("name") == "tasktwo"
        
        result = t.run(tasks=["1", "shared:1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 3

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 339
                    assert (j.get("function") == "taskthree" or j.get("function") == "tasktwo" or j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree" or j.get("name") == "taskname" or j.get("name") == "tasktwo"

        result = s.run(tasks=[1, "shared:1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 3

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 339
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskname" or j.get("function") == "taskthree" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "taskname"
        
        result = s.run(tasks=["1", "shared:1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 3

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 339
                    assert (j.get("function") == "taskfour" or j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskfour" or j.get("name") == "taskthree" or j.get("name") == "taskname"
        
        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskfour") == []
        assert type(s.getter("tasks", "shared:taskfour")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')

    def test_5_40_run_all_shared_from_all_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 340

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 340
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 340
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 340
        
        @workflow(
            name="taskfour", task_order=1, task_instance=s,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 340
        
        result = t.run(tasks=["shared:1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 340
                    assert (j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree" or j.get("name") == "taskname"
        
        result = t.run(tasks="shared:1")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 340
                    assert (j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree" or j.get("name") == "taskname"
        
        result = s.run(tasks=["shared:1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 340
                    assert (j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree" or j.get("name") == "taskname"
        
        result = s.run(tasks="shared:1")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 340
                    assert (j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree" or j.get("name") == "taskname"
        
        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskfour") == []
        assert type(s.getter("tasks", "shared:taskfour")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')

    def test_5_41_run_all_instance_from_all_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 341

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 341
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 341
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 341
        
        @workflow(
            name="taskfour", task_order=1, task_instance=s,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 341
        
        result = t.run(tasks=1)

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 341
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"
        
        result = t.run(tasks="1")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 341
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"
        
        result = t.run(tasks=[1])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 341
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"
        
        result = t.run(tasks=["1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 341
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"

        result = s.run(tasks=1)

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 341
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"
        
        result = s.run(tasks="1")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 341
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"
        
        result = s.run(tasks=[1])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 341
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"
        
        result = s.run(tasks=["1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 341
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"
        
        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskfour") == []
        assert type(s.getter("tasks", "shared:taskfour")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')

    def test_5_42_run_multiple_mixed_from_mixed_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 342

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 342
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 342
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 342
        
        @workflow(
            name="taskfour", task_order=1, task_instance=s,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 342

        result = t.run(tasks=["shared:taskthree", "tasktwo"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 342
                    assert (j.get("function") == "taskthree" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree" or j.get("name") == "tasktwo"

        result = t.run(tasks=["shared:taskname", "tasktwo", "shared:taskthree"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 3

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 342
                    assert (j.get("function") == "taskname" or j.get("function") == "taskthree" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo" or j.get("name") == "taskthree"

        result = s.run(tasks=["shared:taskname", "taskfour"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 342
                    assert (j.get("function") == "taskname" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "taskfour"
        
        result = s.run(tasks=["shared:taskname", "taskfour", "shared:taskthree"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 3

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 342
                    assert (j.get("function") == "taskname" or j.get("function") == "taskthree" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "taskfour" or j.get("name") == "taskthree"

        result = t.run(tasks=["shared:tasktw", "shared:taskfou"])

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["shared:tasktw", "shared:taskfou"])

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks=["tasktw", "shared:taskfou"])

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["shared:tasktw", "taskfou"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskfour") == []
        assert type(s.getter("tasks", "shared:taskfour")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')
    
    def test_5_43_doesnot_run_all_shared_from_all_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 343

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 343
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 343
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 343
        
        @workflow(
            name="taskfour", task_order=1, task_instance=s,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 343
        
        result = t.run(tasks=1)

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 343
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"
        
        result = t.run(tasks="1")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 343
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"
        
        result = t.run(tasks=["1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 343
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"

        result = s.run(tasks=1)

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 343
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"
        
        result = s.run(tasks="1")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 343
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"
        
        result = s.run(tasks=["1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 1

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 343
                    assert (j.get("function") == "tasktwo" or j.get("function") == "taskfour" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "tasktwo" or j.get("name") == "taskfour"
        
        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskfour") == []
        assert type(s.getter("tasks", "shared:taskfour")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')

    def test_5_44_doesnot_run_all_instance_from_all_shared_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 344

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskname", a, b)
            return 344
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: tasktwo", a, b)
            return 344
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskthree", a, b)
            return 344
        
        @workflow(
            name="taskfour", task_order=1, task_instance=s,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskfour", a, b)
            return 344
        
        result = t.run(tasks="shared:1")

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 344
                    assert (j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree" or j.get("name") == "taskname"
        
        result = s.run(tasks=["shared:1"])

        assert type(result) == list
        assert len(result) > 0
        assert len(result) == 2

        for r in result:
            assert type(r) == dict
            assert len(r) == 1
            for i in r.keys():
                assert type(i) == str
                assert type(r[i]) == list
                for j in r[i]:
                    assert type(j.get("result")) == int
                    assert j.get("result") == 344
                    assert (j.get("function") == "taskthree" or j.get("function") == "taskname" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskthree" or j.get("name") == "taskname"

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskfour") == []
        assert type(s.getter("tasks", "shared:taskfour")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')

    def test_5_45_doesnot_run_multiple_mixed_from_mixed_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 345

        t = Tasks()

        @workflow(
            name="taskname", task_order=1, task_instance=t,
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
        def taskname(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 345
        
        @workflow(
            name="tasktwo", task_order=1, task_instance=t,
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
        def tasktwo(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 345
        
        s = Tasks()

        @workflow(
            name="taskthree", task_order=1, task_instance=s,
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
        def taskthree(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 345
        
        @workflow(
            name="taskfour", task_order=1, task_instance=s,
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
        def taskfour(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return 345

        result = t.run(tasks=["shared:taskthre", "taskfour"])

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks=["shared:tasknam", "taskfour", "shared:tasthree"])

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["shared:tasknme", "tasktwo"])

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["shared:tasknam", "tasktwo", "shared:taskthre"])

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks=["shared:taskthre", "tastwo"])

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks=["shared:tasknam", "tastwo", "shared:taskhree"])

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["shared:tasknae", "taskfor"])

        assert type(result) == list
        assert len(result) == 0
        
        result = s.run(tasks=["shared:tasknam", "taskfou", "shared:taskthre"])

        assert type(result) == list
        assert len(result) == 0

        result = t.run(tasks=["shared:tasktw", "shared:taskfou"])

        assert type(result) == list
        assert len(result) == 0

        result = s.run(tasks=["shared:tasktw", "shared:taskfou"])

        assert type(result) == list
        assert len(result) == 0

        assert t.shared.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.shared.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskthree")[0].get("name") == "taskthree"
        assert type(t.shared.getter("tasks", "taskthree")[0].get("name")) == str
        assert t.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "tasktwo")[0].get("name")) == str
        assert s.getter("tasks", "taskfour")[0].get("name") == "taskfour"
        assert type(s.getter("tasks", "taskfour")[0].get("name")) == str
        assert s.getter("tasks", "shared:taskfour") == []
        assert type(s.getter("tasks", "shared:taskfour")) == list
        assert t.getter("tasks", "shared:tasktwo") == []
        assert type(t.getter("tasks", "shared:tasktwo")) == list

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'taskthree')


## decorator runs a mix of instance and shared tasks


# IMPORTANT:
# Maintain the results of all tests even with change of flow
# These are functionality tests for running of decorator created tasks or shared tasks

class TestAnyTaskRunner():

    def test_6_1_any_type_task_shared_task(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=True
        )
        def taskone(ctx, result):
            print("Running my task function: taskone")
            return "taskname"

        result = t.run(tasks="shared:taskname")

    def test_6_2_any_type_task_shared_task_doesnot_run_throws_Error(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            @workflow(
                name="taskname",
                shared=False
            )
            def taskone(ctx, result):
                print("Running my task function: taskone")
                return "taskname"

            result = t.run(tasks="shared:taskname")

    def test_6_3_any_type_task_instance(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False
        )
        def taskname(ctx, result):
            print("Running my task function: taskname")
            return "taskname"

        result = t.run(tasks="taskname")

    def test_6_4_any_type_task_instance_doesnot_run_throws_Error(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            @workflow(
                name="taskname",
                shared=False
            )
            def taskname(ctx, result):
                print("Running my task function: taskname")
                return "taskname"

            result = t.run(tasks="taskname")

    def test_6_5_any_type_task_shared_and_instance(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False
        )
        def taskname(ctx, result):
            print("Running my task function: taskname")
            return "taskname"

        @workflow(
            name="taskone", task_instance=t,
            shared=True
        )
        def taskone(ctx, result):
            print("Running my task function: taskone")
            return "taskone"

        result = t.run(tasks=["taskname", "shared:taskone"])

    def test_6_6_doesnot_run_any_type_task_shared_and_instance(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False
        )
        def taskname(ctx, result):
            print("Running my task function: taskname")
            return "taskname"

        @workflow(
            name="taskone", task_instance=t,
            shared=True
        )
        def taskone(ctx, result):
            print("Running my task function: taskone")
            return "taskone"

        result = t.run(tasks=["taskname", "shared:taskone"])

        assert type(result) == list
        assert len(result) == 2



## middlewares can be invoked with arguments and keyword arguments
## middlewares can be invoked and returns (error or next value) after invocation
## middlewares can be invoked and returns (error or next value) after invocation


# IMPORTANT:
# Maintain the results of all tests even with change of flow
# These are functionality tests for running of decorator created middlewares
# TODO: Write result asserts for all

class TestMiddlewares():

    def test_7_1_run_middlewares_before_middlewares(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_instance=t,
            shared=False,
            before=[{
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }])
        def taskone(ctx, result):
            print("Running my task function: taskone")

        result = t.run(tasks="taskname")

    def test_7_2_run_middlewares_after_middlewares(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_instance=t,
            shared=False,
            after=[{
                "function": middleware,
                "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }])
        def taskname(ctx, result):
            print("Running my task function: taskname")

        result = t.run(tasks="taskname")

    def test_7_3_run_doesnot_middlewares_before_middleware(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items",
                      k, c, d, kwargs)

            @workflow(
                name="taskname", task_instance=t,
                shared=False,
                before=[{
                    "function": middleware,
                    "options": {"error": "next", "error_next_value": ""}
                }])
            def taskone(ctx, result):
                print("Running my task function: taskone")

            result = t.run(tasks="taskname")

        assert e.type == TypeError

    def test_7_4_run_doesnot_middlewares_after_middleware(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items",
                      k, c, d, kwargs)

            @workflow(
                name="taskname", task_instance=t,
                shared=False,
                after=[{
                    "function": middleware,
                    "options": {"error": "next", "error_next_value": ""}
                }])
            def taskone(ctx, result):
                print("Running my task function: taskone")

            result = t.run(tasks="taskname")

        assert e.type == TypeError

    def test_7_5_run_single_middleware_before_middleware(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_instance=t,
            shared=False,
            before=[{
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }])
        def taskone(ctx, result):
            pass

        result = t.run(tasks="taskname")

    def test_7_6_run_single_middleware_after_middleware(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_instance=t,
            shared=False,
            after=[{
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }])
        def taskone(ctx, result):
            pass

        result = t.run(tasks="taskname")

    def test_7_7_run_doesnot_single_middleware_before_middleware(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items",
                      k, c, d, kwargs)

            @workflow(
                name="taskname", task_instance=t,
                shared=False,
                before=[{
                    "function": middleware,
                    "options": {"error": "next", "error_next_value": ""}
                }])
            def taskone(ctx, result):
                pass

            result = t.run(tasks="taskname")

    def test_7_8_run_doesnot_single_middleware_after_middleware(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items",
                      k, c, d, kwargs)

            @workflow(
                name="taskname", task_instance=t,
                shared=False,
                after=[{
                    "function": middleware,
                    "options": {"error": "next", "error_next_value": ""}
                }])
            def taskone(ctx, result):
                pass

            result = t.run(tasks="taskname")


# functions can be invoked with arguments and keyword arguments
# functions can be invoked and returns (error or next value) after invocation
# functions can be invoked and returns (error or next value) after invocation


# IMPORTANT:
# Maintain the results of all tests even with change of flow
# These are functionality tests for creating of decorator created tasks
# TODO: Write result asserts for all

class TestFunctions():

    def test_8_1_function_invocation_with_args(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_8_2_function_invocation_with_no_args_in_def(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[], kwargs={}
        )
        def taskone(ctx, result):
            print("Running my task function: taskone")

        result = t.run(tasks="taskname")

    def test_8_3_creates_task_without_args(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            @workflow(
                name="taskname", task_instance=t,
                shared=False, kwargs={}
            )
            def taskone(ctx, result, a, b):
                print("Running my task function: taskone", a, b)

            result = t.run(tasks="taskname")

        assert e.type is Exception

    def test_8_4_creates_task_with_kwargs(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[], kwargs={"a": 11, "b": 12}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_8_5_creates_task_without_kwargs(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[1, 2]
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_8_6_doesnot_create_task_without_args_without_kwargs(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            @workflow(
                name="taskname", task_instance=t,
                shared=False
            )
            def taskone(ctx, result, a, b):
                print("Running my task function: taskone", a, b)

            result = t.run(tasks="taskname")

        assert e.type == Exception

    def test_8_7_function_invocation_returns_1_None(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_8_8_function_invocation_returns_2_None(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_8_9_function_invocation_returns_1_value(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a, b

        result = t.run(tasks="taskname")

    def test_8_10_function_invocation_returns_2_values(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a+b

        result = t.run(tasks="taskname")

    def test_8_11_function_invocation_returns_3_value(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return ctx, result, a, b, a*b

        result = t.run(tasks="taskname")

    def test_8_12_unction_doesnot_invoke_returns_throws_Error(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result):
            print("Running my task function: taskone")
            return ctx, result

        result = t.run(tasks="taskname")

    # TODO: THIS TEST IS NOT COMPLETE FOR ITS ARGUMENTS

    def test_8_13_function_invocation_error_returns_completes_flow(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    # TODO: THIS TEST IS NOT COMPLETE FOR ITS ARGUMENTS

    def test_8_14_function_doesnot_invoke_error_returns_completes_flow_with_handler(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_8_15_functions_returns_results(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_8_16_functions_doesnot_return_results(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_8_17_functions_returns_right_results(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_8_18_functions_doesnot_return_right_results(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")


# middlewares return results

class TestBeforeMiddlewaresResultReturns():

    def test_7_1_middlewares_doesnot_return_results(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items",
                  k, c, d, kwargs)

        @workflow(
            name="taskname", task_instance=t,
            before=[{
                    "function": middleware, "args": [11, 12, 13], "kwargs":{},
                    "options": {"error": "next", "error_next_value": ""}
                    }],
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_7_2_middlewares_invocation_returns_1_None(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items",
                  k, c, d, kwargs)

        @workflow(
            name="taskname", task_instance=t,
            before=[{
                    "function": middleware, "args": [11, 12, 13], "kwargs":{},
                    "options": {"error": "next", "error_next_value": ""}
                    }],
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_7_3_middlewares_invocation_returns_2_None(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items",
                  k, c, d, kwargs)
            return None

        @workflow(
            name="taskname", task_instance=t,
            before=[{
                    "function": middleware, "args": [11, 12, 13], "kwargs":{},
                    "options": {"error": "next", "error_next_value": ""}
                    }],
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_7_4_middlewares_invocation_returns_1_values(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items",
                  k, c, d, kwargs)
            return k, c, d

        @workflow(
            name="taskname", task_instance=t,
            before=[{
                    "function": middleware, "args": [11, 12, 13], "kwargs":{},
                    "options": {"error": "next", "error_next_value": ""}
                    }],
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_7_5_middlewares_invocation_returns_2_values(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items",
                  k, c, d, kwargs)
            return k

        @workflow(
            name="taskname", task_instance=t,
            before=[{
                    "function": middleware, "args": [11, 12, 13], "kwargs":{},
                    "options": {"error": "next", "error_next_value": ""}
                    }],
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_7_6_middlewares_invocation_returns_3_values(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items",
                  k, c, d, kwargs)
            return k, c

        @workflow(
            name="taskname", task_instance=t,
            before=[{
                    "function": middleware, "args": [11, 12, 13], "kwargs":{},
                    "options": {"error": "next", "error_next_value": ""}
                    }],
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_7_7_middlewares_doesnot_invoke_returns_throws_Error(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items",
                  k, c, d, kwargs)
            return a, c

        @workflow(
            name="taskname", task_instance=t,
            before=[{
                    "function": middleware,
                    "options": {"error": "next", "error_next_value": ""}
                    }],
            shared=False
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_7_8_middlewares_invocation_error_returns_completes_flow(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items",
                  k, c, d, kwargs)
            return k, c, d

        @workflow(
            name="taskname", task_instance=t,
            before=[{
                    "function": middleware,
                    "options": {"error": "next", "error_next_value": "some value"}
                    }],
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_7_9_middlewares_doesnot_invoke_error_returns_completes_flow_with_handler(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items",
                  k, c, d, kwargs)
            return k, c, d

        @workflow(
            name="taskname", task_instance=t,
            before=[{
                    "function": middleware, "args": [11, 12, 13], "kwargs":{},
                    "options": {"error": "next", "error_handler": lambda x, y: (y, x), "error_next_value": ""}
                    }],
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

# middlewares return results


class TestAfterMiddlewaresResultReturns():

    def test_8_1_middlewares_doesnot_return_results(self):
        pass

    def test_8_2_middlewares_invocation_returns_1_None(self):
        pass

    def test_8_3_middlewares_invocation_returns_2_None(self):
        pass

    def test_8_4_middlewares_invocation_returns_1_values(self):
        pass

    def test_8_5_middlewares_invocation_returns_2_values(self):
        pass

    def test_8_6_middlewares_invocation_returns_3_values(self):
        pass

    def test_8_7_middlewares_doesnot_invoke_returns_throws_Error(self):
        pass

    def test_8_8_middlewares_invocation_error_returns_completes_flow(self):
        pass

    def test_8_9_middlewares_doesnot_invoke_error_returns_completes_flow_with_handler(self):
        pass


# task runs return results and correct numbers

class TestTaskResultReturns():

    def test_9_1_task_returns_results(self):
        pass

    def test_9_2_task_returns_right_results(self):
        pass

    def test_9_3_task_doesnot_return_right_results(self):
        pass

    def test_9_3_task_doesnot_return_wrong_results(self):
        pass

    def test_9_4_task_return_wrong_results(self):
        pass

    def test_9_5_task_returns_incorrect_numbers(self):
        pass

    def test_9_6_task_returns_correct_numbers(self):
        pass

    def test_9_7_task_doesnot_return_incorrect_numbers(self):
        pass

    def test_9_8_task_doesnot_return_correct_numbers(self):
        pass


# middlewares can be invoked and can access results context of all previously invoked functions

class TestMiddlewareAccessContext():

    def test_10_1_middlewares_can_access_context(self):
        pass

    def test_10_2_middlewares_doesnot_access_context(self):
        pass


# functions can be invoked and can access results context of all previously invoked functions

class TestFunctionsAccessContext():

    def test_11_1_functions_can_access_context(self):
        pass

    def test_11_2_functions_doesnot_access_context(self):
        pass


class TestMiddlewareBeforeForAsyncAwait:

    def test_12_1_Middleware_before_for_asyncAwait(self):
        pass

    def test_12_2_Middleware_after_for_asyncAwait(self):
        pass

    def test_12_3_Middleware_function_for_asyncAwait(self):
        pass


class TestMiddlewareBeforeForMultiThreads:

    def test_13_1_Middleware_before_for_multiThreads_without_Join(self):
        pass

    def test_13_2_Middleware_before_for_multiThreads_with_Join(self):
        pass

    def test_13_3_Middleware_after_for_multiThreads_without_Join(self):
        pass

    def test_13_4_Middleware_after_for_multiThreads_with_Join(self):
        pass

    def test_13_5_Middleware_function_for_multiThreads_without_Join(self):
        pass

    def test_13_6_Middleware_function_for_multiThreads_with_Join(self):
        pass


class TestMiddlewareBeforeForMultiProcessing:

    def test_14_1_Middleware_before_for_multiProcessing_without_Join(self):
        pass

    def test_14_2_Middleware_before_for_multiProcessing_with_Join(self):
        pass

    def test_14_3_Middleware_after_for_multiProcessing_without_Join(self):
        pass

    def test_14_4_Middleware_after_for_multiProcessing_with_Join(self):
        pass

    def test_14_5_Middleware_function_for_multiProcess_without_Join(self):
        pass

    def test_14_6_Middleware_function_for_multiProcess_with_Join(self):
        pass
