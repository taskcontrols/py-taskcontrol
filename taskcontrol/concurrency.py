# Concurrency Base


from threading import Thread, Lock
from multiprocessing import Process, Array, Value, Manager
from .sharedbase import UtilsBase


class ConcurencyBase(UtilsBase):

    # consider adding concurrency futures
    def futures_run(self):
        pass

    # consider adding asyncio lib
    def asyncio_run(self):
        pass

    # asynchronous, needs_join
    def mthread_run(self, function, options):
        """
        Description of mthread_run

        Args:
            self (undefined):
            function (undefined):
            options (undefined):

        """

        # options structure
        # # args, kwargs, needs_join, share_value

        # Test this instance of MThreading for lock and other params

        result = None

        if type(options) == dict:
            # # Keeping following to be user responsibility
            # # Check addition later
            # share_value = options.get("share_value")
            pass

        daemon = options.get("daemon")
        if type(daemon) != bool:
            daemon = True

        args = options.get("args")
        if not args:
            args = []

        kwargs = options.get("kwargs")
        if not kwargs:
            kwargs = {}

        need_lock = options.get("lock")
        if need_lock:
            lock = Lock()

        if lock:
            args = (lock, *args)
        else:
            arg = (*args,)

        worker = Thread(
            target=function,
            args=arg,
            kwargs={"result": result, **kwargs}
        )
        worker.setDaemon(daemon)
        worker.start()

        if options.get("needs_join") or options.get("needs_join") == None:
            worker.join()
            return {"result": result}

        return {"worker": worker, "result": result}

    # asynchronous, needs_join
    def mprocess_run(self, function, options):
        """
        Description of mprocess_run

        Args:
            self (undefined):
            function (undefined):
            options (undefined):

        """

        # options structure
        # args, kwargs, needs_join

        # Test this instance of MProcessing for lock and other params

        result = None

        # # Check need here. Create a common one outside by user
        # # Consider if you want to handle this (Negative currently)

        # # share_value, share_array, share_queue, share_pipe, share_lock, share_rlock,
        # # share_manager, share_pool, share_connection, share_event,
        # # share_semaphore, share_bounded_semaphore

        if type(options) == dict:
            # # Keeping following to be user responsibility
            # # Check addition later
            # share_value = options.get("share_value")
            # share_array = options.get("share_array")

            args = options.get("args")
            if not args:
                args = []

            kwargs = options.get("kwargs")
            if not kwargs:
                kwargs = {}

        daemon = options.get("daemon")
        if type(daemon) != bool:
            daemon = True

        worker = Process(
            target=function,
            args=(*args,),
            kwargs={**kwargs}
        )
        worker.daemon = daemon
        worker.start()

        if options.get("needs_join") or options.get("needs_join") == None:
            result = worker.join()
            return {"result": result}

        terminate = options.get("terminate")
        if type(terminate) != bool or terminate == True:
            worker.terminate()
            return {"result": result}

        return {"worker": worker, "result": result}

    # asynchronous, needs_join
    def mprocess_pool_run(self, function, options):
        pass

    def run_concurrently(self, function, options):
        mode = options.get("mode")
        if mode:
            if mode == "process":
                return self.mprocess_run(function, options)
            if mode == "process_pool":
                return self.mprocess_pool_run(function, options)
            if mode == "thread":
                return self.mthread_run(function, options)
            if mode == "async":
                pass
            if mode == "futures":
                pass
        return None


if __name__ == "__main__":
    concurrency = ConcurencyBase()


__all__ = ["ConcurencyBase"]
