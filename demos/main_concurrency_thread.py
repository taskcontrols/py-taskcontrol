
from taskcontrol.lib.utils import ConcurencyBase


def runner():
    print("Test")
    return True


# if __name__ == "__main__":
r = ConcurencyBase.thread(target=runner, name="test", options={
    "join": True, "needs_return": True
})
print("result", r)
