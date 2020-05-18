# Concurrency Base


from threading import Thread
from multiprocessing import Process


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
            kwargs={**options.get("kwargs")}
        )
        worker.setDaemon(True)
        worker.start()
        if options.get("needs_join"):
            worker.join()
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

        # sv = options.get("share_value")

        worker = Process(
            target=function,
            args=(*options.get("args"), ),
            kwargs={**options.get("kwargs")}
        )
        worker.start()
        if options.get("needs_join"):
            result = worker.join()
        return {"worker": worker, "result": result}

