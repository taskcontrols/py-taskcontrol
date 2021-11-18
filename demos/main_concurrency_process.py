
from taskcontrol.lib.utils import ConcurencyBase


def runner():
    print("Test")
    return True


if __name__ == "__main__":
    r = ConcurencyBase.process(target=runner, name="test", options={
        "join": True, "terminate": True, "needs_return": True
    })
    print("result", r)
