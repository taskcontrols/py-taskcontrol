# Logger and timer Base

import time
from .sharedbase import ClosureBase
from .interfaces import TimeBase
# TODO: Refactor getters and setters and make code simpler


class Timer(TimeBase, ClosureBase):

    def __init__(self, options, timers={}):
        super()

        if not options and type(options) != dict:
            raise TypeError("Options not provided")

        self.getter, self.setter, self.deleter = self.class_closure(
            timers=timers)

    def time(self, options):

        # options object expected
        # {"name":"name", "logger": "", "format": ""}

        logger = options.get("logger")
        timer = self.getter("timers", options.get("name"))

        if len(timer) == 1:
            t = timer[0].perf_counter()
        else:
            raise TypeError(
                "Wrong timer name provided. No such timer or multiple names matched")

        if not t:
            raise ValueError("Did not find timer")
        if logger:
            logger.log(t)

        return t


if __name__ == "__main__":
    t = Timer({}, {})


__all__ = ["Timer"]
