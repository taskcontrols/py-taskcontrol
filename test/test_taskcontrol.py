import pytest

from src.workflow import workflow, Tasks


# decorator applied on a function and function invocation creates the task
# decorator creates tasks only on function invocation
# decorator creates instance tasks
# decorator creates shared tasks


class TestDecorator():

    def test_creates_task_before_as_list(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
            before=[{
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                    "options": {"error": "next", "error_next_value": ""}
                    }],
            after=[{
                "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, None)}
            }])
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")
        print(result)

        assert type(result) == list
        assert not hasattr(result, "result")
        assert len(result) > 0
        assert type(result[0]) == dict

        for i in result:
            assert type(i) == dict
            assert len(i) == 1
            assert len(i.keys()) == 1

            for j in i:
                assert type(j) == str
                assert len(i[j]) == 3
                assert type(i[j]) == list

    def test_creates_task_before_as_dict(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
            before={
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            },
            after=[{
                "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, None)}
            }])
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert not hasattr(result, "result")
        assert len(result) > 0
        assert type(result[0]) == dict

        for i in result:
            assert type(i) == dict
            assert len(i) == 1
            assert len(i.keys()) == 1

            for j in i:
                assert type(j) == str
                assert len(i[j]) == 3
                assert type(i[j]) == list
    
    def test_creates_task_after_as_list(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
            before=[{
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }],
            after=[{
                "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, None)}
            }])
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert not hasattr(result, "result")
        assert len(result) > 0
        assert type(result[0]) == dict

        for i in result:
            assert type(i) == dict
            assert len(i) == 1
            assert len(i.keys()) == 1

            for j in i:
                assert type(j) == str
                assert len(i[j]) == 3
                assert type(i[j]) == list

    def test_creates_task_after_as_dict(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
            before=[{
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }],
            after={
                "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, None)}
            })
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert not hasattr(result, "result")
        assert len(result) > 0
        assert type(result[0]) == dict

        for i in result:
            assert type(i) == dict
            assert len(i) == 1
            assert len(i.keys()) == 1

            for j in i:
                assert type(j) == str
                assert len(i[j]) == 3
                assert type(i[j]) == list

    def test_creates_task_after_and_before_as_dict(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
            before={
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            },
            after={
                "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, None)}
            })
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert not hasattr(result, "result")
        assert len(result) > 0
        assert type(result[0]) == dict

        for i in result:
            assert type(i) == dict
            assert len(i) == 1
            assert len(i.keys()) == 1

            for j in i:
                assert type(j) == str
                assert len(i[j]) == 3
                assert type(i[j]) == list

    def test_creates_task_after_and_before_as_list(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
            before=[{
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }],
            after=[{
                "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, None)}
            }])
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert not hasattr(result, "result")
        assert len(result) > 0
        assert type(result[0]) == dict

        for i in result:
            assert type(i) == dict
            assert len(i) == 1
            assert len(i.keys()) == 1

            for j in i:
                assert type(j) == str
                assert len(i[j]) == 3
                assert type(i[j]) == list

    def test_creates_task_with_before_list_with_right_args(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
            before=[{
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }],
            after=[{
                "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, None)}
            }])
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert not hasattr(result, "result")
        assert len(result) > 0
        assert type(result[0]) == dict

        for i in result:
            assert type(i) == dict
            assert len(i) == 1
            assert len(i.keys()) == 1

            for j in i:
                assert type(j) == str
                assert len(i[j]) == 3
                assert type(i[j]) == list

    def test_creates_task_with_after_list_with_right_args(self):
        t = Tasks()

        def middleware(ctx, result, k, c, d, **kwargs):
            print("Running my Middleware Function: test - task items", k, c, d, kwargs)

        @workflow(
            name="taskname", task_order=1, task_instance=t,
            shared=False, args=[1, 2], kwargs={}, log=False,
            before=[{
                "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                "options": {"error": "next", "error_next_value": ""}
            }],
            after=[{
                "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, None)}
            }])
        def taskone(ctx, result, a, b):
            print("Running my task function: taskone", a, b)

        result = t.run(tasks="taskname")

        assert type(result) == list
        assert not hasattr(result, "result")
        assert len(result) > 0
        assert type(result[0]) == dict

        for i in result:
            assert type(i) == dict
            assert len(i) == 1
            assert len(i.keys()) == 1

            for j in i:
                assert type(j) == str
                assert len(i[j]) == 3
                assert type(i[j]) == list

    def test_doesnot_creates_task_with_before_list_with_wrong_args_throws_TypeError(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items", k, c, d, kwargs)

            @workflow(
                name="taskname", task_order=1, task_instance=t,
                shared=False, args=[1, 2], kwargs={}, log=False,
                before=[{
                    "function": middleware, "args": [11], "kwargs": {"d": "Before Testing message Middleware "},
                    "options": {"error": "next", "error_next_value": ""}
                }],
                after=[{
                    "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                    "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, None)}
                }])
            def taskone(ctx, result, a, b):
                print("Running my task function: taskone", a, b)

            result = t.run(tasks="taskname")

        assert e.type is Exception

    def test_doesnot_creates_task_with_after_list_with_wrong_args_throws_TypeError(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items", k, c, d, kwargs)

            @workflow(
                name="taskname", task_order=1, task_instance=t,
                shared=False, args=[1, 2], kwargs={}, log=False,
                before=[{
                    "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                    "options": {"error": "next", "error_next_value": ""}
                }],
                after=[{
                    "function": middleware, "args": [13], "kwargs": {"d": "After Middleware Testing message"},
                    "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, None)}
                }])
            def taskone(ctx, result, a, b):
                print("Running my task function: taskone", a, b)

            result = t.run(tasks="taskname")

        assert e.type is Exception

    def test_doesnot_creates_task_with__before_and_after_list_with_wrong_args_throws_TypeError(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items", k, c, d, kwargs)

            @workflow(
                name="taskname", task_order=1, task_instance=t,
                shared=False, args=[1, 2], kwargs={}, log=False,
                before=[{
                    "function": middleware, "args": [12], "kwargs": {"d": "Before Testing message Middleware "},
                    "options": {"error": "next", "error_next_value": ""}
                }],
                after=[{
                    "function": middleware, "args": [13], "kwargs": {"d": "After Middleware Testing message"},
                    "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, None)}
                }])
            def taskone(ctx, result, a, b):
                print("Running my task function: taskone", a, b)

            result = t.run(tasks="taskname")

        assert e.type is Exception

    def test_doesnot_creates_task_with_wrong_print_args_for_task_function_throws_TypeError(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items", k, c, d, kwargs)

            @workflow(
                name="taskname", task_order=1, task_instance=t,
                shared=False, args=[1, 2], kwargs={}, log=False,
                before=[{
                    "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                    "options": {"error": "next", "error_next_value": ""}
                }],
                after=[{
                    "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                    "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, None)}
                }])
            def taskone(ctx, result, a, b):
                print("Running my task function: taskone", a, c)

            result = t.run(tasks="taskname")

        assert e.type is TypeError

    def test_doesnot_creates_task_with_wrong_def_of_args_for_task_function_throws_TypeError(self):
        with pytest.raises(Exception) as e:
            t = Tasks()

            def middleware(ctx, result, k, c, d, **kwargs):
                print("Running my Middleware Function: test - task items", k, c, d, kwargs)

            @workflow(
                name="taskname", task_order=1, task_instance=t,
                shared=False, args=[1, 2], kwargs={}, log=False,
                before=[{
                    "function": middleware, "args": [11, 12], "kwargs": {"d": "Before Testing message Middleware "},
                    "options": {"error": "next", "error_next_value": ""}
                }],
                after=[{
                    "function": middleware, "args": [13, 14], "kwargs": {"d": "After Middleware Testing message"},
                    "options": {"error": "error_handler", "error_next_value": "value", "error_handler": lambda err, value: (err, None)}
                }])
            def taskone(ctx, result, a):
                print("Running my task function: taskone", a)

            result = t.run(tasks="taskname")

        assert e.type is TypeError

    def test_creates_instance_task(self):
        pass

    def test_doesnot_create_instance_task(self):
        pass

    def test_create_shared_task(self):
        pass

    def test_doesnot_create_shared_task(self):
        pass


# decorator runs instance single tasks
# decorator runs instance multiple tasks
# decorator runs all instance tasks
class TestTaskRunner():

    def test_run_single_instance_task(self):
        pass

    def test_run_doesnot_single_instance_task(self):
        pass

    def test_run_multiple_instance_task(self):
        pass

    def test_run_doesnot_multiple_instance_task(self):
        pass

    def test_run_all_instance_task(self):
        pass

    def test_run_doesnot_all_instance_task(self):
        pass


# decorator runs shared single task
# decorator runs shared multiple tasks
# decorator runs shared all tasks
class TestSharedTaskRunner():

    def test_run_single_shared_tasks(self):
        pass

    def test_run_doesnot_single_shared_tasks(self):
        pass

    def test_run_single_multiple_tasks(self):
        pass

    def test_run_doesnot_single_multiple_tasks(self):
        pass

    def test_run_single_all_shared_tasks(self):
        pass

    def test_run_doesnot_single_all_shared_tasks(self):
        pass


# decorator runs a mix of instance and shared tasks
class TestAnyTaskRunner():

    def test_any_type_task(self):
        pass

    def test_doesnot_any_type_task(self):
        pass


# middlewares can be invoked with arguments and keyword arguments
# middlewares can be invoked and returns (error or next value) after invocation
# middlewares can be invoked and returns (error or next value) after invocation
class TestMiddlewares():

    def test_run_middlewares(self):
        pass

    def test_run_doesnot_middlewares(self):
        pass

    def test_run_single_middleware(self):
        pass

    def test_run_doesnot_single_middleware(self):
        pass


# functions can be invoked with arguments and keyword arguments
# functions can be invoked and returns (error or next value) after invocation
# functions can be invoked and returns (error or next value) after invocation
class TestFunctions():
    def test_function_invocation_with_arguments(self):
        pass

    def test_function_doesnot_invoke_with_arguments(self):
        pass

    def test_function_invocation_returns(self):
        pass

    def test_function_doesnot_invoke_returns(self):
        pass

    def test_function_invocation_error_returns(self):
        pass

    def test_function_doesnot_invoke_error_returns(self):
        pass


# middlewares can be invoked and can access results context of all previously invoked functions
class TestMiddlewareAccessContext():
    def test_middlewares_can_access_context(self):
        pass

    def test_middlewares_doesnot_access_context(self):
        pass


# functions can be invoked and can access results context of all previously invoked functions
class TestFunctionsAccessContext():
    def test_functions_can_access_context(self):
        pass

    def test_functions_doesnot_access_context(self):
        pass


# middlewares return results
class TestMiddlewaresResultReturns():
    def test_middlewares_returns_results(self):
        pass

    def test_middlewares_doesnot_return_results(self):
        pass


# functions return results
class TestFuctionsResultReturns():

    def test_functions_returns_results(self):
        pass

    def test_functions_doesnot_return_results(self):
        pass

    def test_functions_returns_right_results(self):
        pass

    def test_functions_doesnot_return_right_results(self):
        pass


# task runs return results and correct numbers
class TestTaskResultReturns():

    def test_task_returns_results(self):
        pass

    def test_task_returns_right_results(self):
        pass

    def test_task_doesnot_return_right_results(self):
        pass

    def test_task_doesnot_return_wrong_results(self):
        pass

    def test_task_return_wrong_results(self):
        pass

    def test_task_returns_incorrect_numbers(self):
        pass

    def test_task_returns_correct_numbers(self):
        pass

    def test_task_doesnot_return_incorrect_numbers(self):
        pass

    def test_task_doesnot_return_correct_numbers(self):
        pass
