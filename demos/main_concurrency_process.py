
from taskcontrol.lib.utils import ConcurencyBase


def runner(*args, **kwargs):
    print("Test", args, kwargs)
    return True


if __name__ == "__main__":
    r = ConcurencyBase.process(target=runner, name="test", args=("sync",), options={
        "join": True, "terminate": False, "needs_return": True
    })
    print("result will show sync behaviour ", r)
    r = ConcurencyBase.process(target=runner, name="test", args=("async",), options={
        "join": False, "terminate": False, "needs_return": True
    })
    print("result will show async behaviour ", r)
