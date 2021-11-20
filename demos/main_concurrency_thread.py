
from taskcontrol.lib.utils import ConcurencyBase


def runner(*args, **kwargs):
    print("Test", args, kwargs)
    return True


# if __name__ == "__main__":
r = ConcurencyBase.thread(target=runner, name="test", args=(1, 2), options={
    "join": True, "needs_return": True
})
print("result", r)
