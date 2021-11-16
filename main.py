
import threading
from threading import Thread


result = 0


class RThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, daemon=False, Verbose=None):
        Thread.__init__(self, group=group, target=target,
                        name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args, timeout=-1)
        return self._return


def function_():
    global result
    result += 10
    return True


def thread_task(lock, function_):
    lock.acquire()
    res = function_()
    lock.release()
    return res


def main_task():
    lock = threading.Lock()
    t1 = threading.Thread(
        name='threading',
        target=thread_task,
        args=(lock, function_)
    )
    t1.start()
    t1.join()
    return t1


def main_rtask():
    lock = threading.Lock()
    t1 = RThread(
        target=thread_task,
        name='threadingreturns',
        args=(lock, function_),
        daemon=True
    )
    t1.start()
    t1.join()
    return t1


if __name__ == "__main__":
    print(main_task(), result)
    print(main_rtask(), result)
