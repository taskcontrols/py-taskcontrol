# Logger and timer Base

import time
from .sharedbase import ClosureBase, UtilsBase
from .interfaces import TimeBase


class Timer(TimeBase, ClosureBase, UtilsBase):

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
        t = self.getter("timers", options.get("name"))

        if len(t) == 1:
            timer = t[0].perf_counter()
        else:
            raise TypeError(
                "Wrong timer name provided. No such timer or multiple names matched")

        if not timer:
            raise ValueError("Did not find timer")
        if logger:
            logger.log(timer)
        return timer


if __name__ == "__main__":
    t = Timer({}, {})


__all__ = ["Timer"]
