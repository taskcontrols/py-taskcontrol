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


# decorator runs instance single tasks
# decorator runs instance multiple tasks
# decorator runs all instance tasks

# IMPORTANT:
# Maintain the results of all tests even with change of flow
# These are functionality tests for running of decorator created tasks

class TestTaskRunner():

    def test_2_1_run_single_instance_task(self):
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

    def test_2_2_run_doesnot_single_instance_task(self):
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

    def test_2_3_run_multiple_instance_task(self):
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

    def test_2_4_doesnot_run_multiple_instance_task(self):
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

    def test_2_5_doesnot_run_single_instance_multiple_tasks(self):
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
                    assert j.get("result") == 205
                    assert (j.get("function") == "taskone" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname" 
        assert t.shared.getter("tasks", "tasktwo")[0].get("name") == "tasktwo"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert len(t.shared.getter("tasks", "tasktwo")) == 1
        assert type(t.shared.getter("tasks", "tasktwo")) == list

        t.shared.deleter("tasks", "tasktwo")

    def test_2_6_doesnot_run_single_instance_multiple_tasks(self):
        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)
            return 206

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
            return 206

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
                    assert j.get("result") == 206
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
                    assert j.get("result") == 206
                    assert (j.get("function") == "taskname" or j.get("function") == "tasktwo" or j.get(
                        "function") == "middleware")
                    assert j.get("name") == "taskname" or j.get("name") == "tasktwo"

        assert t.getter("tasks", "taskname")[0].get("name") == "taskname"
        assert type(t.getter("tasks", "taskname")[0].get("name")) == str
        assert t.shared.getter("tasks", "taskname") == []
        assert type(t.shared.getter("tasks", "taskname")) == list

    def test_2_7_doesnot_run_single_instance_multiple_tasks(self):
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
            print("Running my task function: taskone", a, b)
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
            print("Running my task function: taskone", a, b)
            return 207

        result = t.run(tasks="taskname")

        result = t.run(tasks="tasktwo")

        result = t.run(tasks="taskname")

        result = t.run(tasks=["shared:taskname", "shared:tasktwo"])

        t.shared.deleter("tasks", 'taskname')
        t.shared.deleter("tasks", 'tasktwo')

    def test_2_7_run_all_instance_task(self):
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
            print("Running my task function: taskone", a, b)
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
            print("Running my task function: taskone", a, b)
            return 207

        result = t.run(tasks="taskname")

        result = t.run(tasks="tasktwo")

        result = t.run(tasks="taskname")

        result = t.run(tasks=["taskname", "tasktwo"])

        result = t.run(tasks=1)

        result = t.run(tasks="1")

    def test_2_8_run_doesnot_all_instance_task(self):
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

        result = t.run(tasks="tasktwo")

        result = t.run(tasks="taskname")

        result = t.run(tasks=["taskname", "tasktwo"])

        result = t.run(tasks=["shared:taskname", "shared:tasktwo"])

        result = t.run(tasks=["tasknam", "shared:taskto"])

        result = t.run(tasks=["shared:1"])

        result = t.run(tasks="shared:1")


# decorator runs shared single task
# decorator runs shared multiple tasks
# decorator runs shared all tasks


# IMPORTANT:
# Maintain the results of all tests even with change of flow
# These are functionality tests for running of decorator created shared tasks

class TestSharedTaskRunner():

    def test_3_1_run_single_shared_tasks(self):
        pass

    def test_3_2_run_doesnot_single_shared_tasks(self):
        pass

    def test_3_3_run_single_shared_multiple_tasks(self):
        pass

    def test_3_4_doesnot_run_single_shared_multiple_tasks(self):
        pass

    def test_3_5_run_single_all_shared_tasks(self):
        pass

    def test_3_6_run_doesnot_single_all_shared_tasks(self):
        pass


# decorator runs a mix of instance and shared tasks


# IMPORTANT:
# Maintain the results of all tests even with change of flow
# These are functionality tests for running of decorator created tasks or shared tasks

class TestAnyTaskRunner():

    def test_4_1_any_type_task_shared_task(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=True
        )
        def taskone(ctx, result):
            print("Running my task function: taskone")
            return "taskname"

        result = t.run(tasks="shared:taskname")

    def test_4_2_any_type_task_shared_task_doesnot_run_throws_Error(self):
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

    def test_4_3_any_type_task_instance(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False
        )
        def taskname(ctx, result):
            print("Running my task function: taskname")
            return "taskname"

        result = t.run(tasks="taskname")

    def test_4_4_any_type_task_instance_doesnot_run_throws_Error(self):
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

    def test_4_5_any_type_task_shared_and_instance(self):
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

    def test_4_6_doesnot_any_type_task_shared_and_instance_throws_Error(self):
        with pytest.raises(Exception) as e:
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


# middlewares can be invoked with arguments and keyword arguments
# middlewares can be invoked and returns (error or next value) after invocation
# middlewares can be invoked and returns (error or next value) after invocation


# IMPORTANT:
# Maintain the results of all tests even with change of flow
# These are functionality tests for running of decorator created middlewares
# TODO: Write result asserts for all

class TestMiddlewares():

    def test_5_1_run_middlewares_before_middlewares(self):
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

    def test_5_2_run_middlewares_after_middlewares(self):
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

    def test_5_3_run_doesnot_middlewares_before_middleware(self):
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

    def test_5_4_run_doesnot_middlewares_after_middleware(self):
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

    def test_5_5_run_single_middleware_before_middleware(self):
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

    def test_5_6_run_single_middleware_after_middleware(self):
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

    def test_5_7_run_doesnot_single_middleware_before_middleware(self):
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

    def test_5_8_run_doesnot_single_middleware_after_middleware(self):
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

    def test_6_1_function_invocation_with_args(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_6_2_function_invocation_with_no_args_in_def(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[], kwargs={}
        )
        def taskone(ctx, result):
            print("Running my task function: taskone")

        result = t.run(tasks="taskname")

    def test_6_3_creates_task_without_args(self):
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

    def test_6_4_creates_task_with_kwargs(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[], kwargs={"a": 11, "b": 12}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_6_5_creates_task_without_kwargs(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[1, 2]
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_6_6_doesnot_create_task_without_args_without_kwargs(self):
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

    def test_6_7_function_invocation_returns_1_None(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_6_8_function_invocation_returns_2_None(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_6_9_function_invocation_returns_1_value(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a, b

        result = t.run(tasks="taskname")

    def test_6_10_function_invocation_returns_2_values(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return a+b

        result = t.run(tasks="taskname")

    def test_6_11_function_invocation_returns_3_value(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)
            return ctx, result, a, b, a*b

        result = t.run(tasks="taskname")

    def test_6_12_unction_doesnot_invoke_returns_throws_Error(self):
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

    def test_6_13_function_invocation_error_returns_completes_flow(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    # TODO: THIS TEST IS NOT COMPLETE FOR ITS ARGUMENTS

    def test_6_14_function_doesnot_invoke_error_returns_completes_flow_with_handler(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_6_15_functions_returns_results(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_6_16_functions_doesnot_return_results(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_6_17_functions_returns_right_results(self):
        t = Tasks()

        @workflow(
            name="taskname", task_instance=t,
            shared=False, args=[11, 12], kwargs={}
        )
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

    def test_6_18_functions_doesnot_return_right_results(self):
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
