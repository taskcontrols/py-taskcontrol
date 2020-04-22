import pytest


# decorator applied on a function and function invocation creates the task
# decorator creates tasks only on function invocation
# decorator creates instance tasks
# decorator creates shared tasks
class TestDecorator():
    pass


# decorator runs instance single tasks
# decorator runs instance multiple tasks
# decorator runs all instance tasks
class TestTaskRunner():
    pass


# decorator runs shared single task
# decorator runs shared multiple tasks
# decorator runs shared all tasks
class TestSharedTaskRunner():
    pass


# decorator runs a mix of instance and shared tasks
class TestAnyTaskRunner():
    pass


# middlewares can be invoked with arguments and keyword arguments
# middlewares can be invoked and returns (error or next value) after invocation
# middlewares can be invoked and returns (error or next value) after invocation
class TestMiddlewares():
    pass


# functions can be invoked with arguments and keyword arguments
# functions can be invoked and returns (error or next value) after invocation
# functions can be invoked and returns (error or next value) after invocation
class TestFunctions():
    pass


# middlewares can be invoked and can access results context of all previously invoked functions
class TestMiddlewareAccessContext():
    pass


# functions can be invoked and can access results context of all previously invoked functions
class TestFunctionsAccessContext():
    pass


# middlewares return results
class TestMiddlewaresResultReturns():
    pass


# functions return results
class TestFuctionsResultReturns():
    pass


# task runs return results and correct numbers
class TestTaskResultReturns():
    pass

