# Concurrency Base


from threading import Thread
from multiprocessing import Process, Array, Value

# TODO: Refactor getters and setters and make code simpler

class ConcurencyBase():

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
            share_value = options.get("share_value")
        daemon = options.get("daemon")
        if type(daemon) != bool:
            daemon = True

        worker = Thread(
            target=function,
            daemon=daemon,
            args=(*options.get("args"), ),
            kwargs={"result": result, **options.get("kwargs")}
        )
        worker.setDaemon(True)
        worker.start()

        if options.get("needs_join"):
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
            share_value = options.get("share_value")
            if share_value:
                value = share_value
            share_array = options.get("share_array")
            if share_array and type(share_array) == dict:
                arrays = Array(share_array.get("type"),
                               share_array.get("value"))
            if share_array and type(share_array) == list:
                arrays = []
                for s in share_array:
                    arrays.push(Array(s.get("type"), s.get("value")))

        daemon = options.get("daemon")
        if type(daemon) != bool:
            daemon = True

        worker = Process(
            target=function,
            args=(*options.get("args"), ),
            kwargs={**options.get("kwargs")}
        )
        worker.daemon = daemon
        worker.start()

        if options.get("needs_join"):
            result = worker.join()
            return {"result": result}

        terminate = options.get("terminate")
        if type(terminate) != bool and terminate == True:
            worker.terminate()
            return {"result": result}

        return {"worker": worker, "result": result}

    def run_concurrently(self, function, options):
        mode = options.get("mode")
        if mode:
            if mode == "process":
                return self.mprocess_run(function, options)
            if mode == "thread":
                return self.mthread_run(function, options)
            if mode == "async":
                pass
        return None
