
from taskcontrol.lib.utils import ConcurencyBase


def runner(*args, **kwargs):
    print("Running pool function: Test", args, kwargs)
    return 2


if __name__ == "__main__":
    r = ConcurencyBase.process_pool(function=runner, args=("sync", "sync"), options={
        "join": True, "terminate": False, "lock": True, "needs_return": True
    })
    print("apply result run one ", r)

    r = ConcurencyBase.process_pool(function=runner, args=("sync",), options={
        "join": True, "terminate": False, "lock": True, "needs_return": True, "mode": "apply_async"
    })
    print("apply_async result run two ", r)

    r = ConcurencyBase.process_pool(function=runner, args=("sync",), options={
        "join": True, "terminate": False, "lock": True, "needs_return": True, "mode": "map"
    })
    print("map result run three ", r)

    r = ConcurencyBase.process_pool(function=runner, args=("sync",), options={
        "join": True, "terminate": False, "lock": True, "needs_return": True, "mode": "map_async"
    })
    print("map_async result run four ", r)


