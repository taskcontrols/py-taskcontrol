# Actions and Hooks Base


class ConcurencyBase():

    # consider adding concurrency futures
    def futures_run(self):
        pass

    # consider adding asyncio lib
    def asyncio_run(self):
        pass

    # asynchronous, needs_join
    def mthread_run(self, function, options):
        # # args, kwargs, needs_join, share_value
        # Consider adding thread alive, and other method options access to functions
        from threading import Thread
        result = None
        if type(options) == dict:
            share_value = options.get("share_value")
        worker = Thread(
            target=function,
            daemon=True,
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
        # options structure
        # args, kwargs, needs_join

        # Consider adding process alive, and other method options access to functions
        from multiprocessing import Process
        result = None

        # # Check need here. Create a common one outside by user
        # # Consider if you want to handle this
        # sv = options.get("share_value")
        # sa = options.get("share_array")
        # sq = options.get("share_queue")
        # spi = options.get("share_pipe")
        # sl = options.get("share_lock")
        # srl = options.get("share_rlock")
        # sm = options.get("share_manager")
        # spl = options.get("share_pool")
        # sc = options.get("share_connection")
        # se = options.get("share_event")
        # ss = options.get("share_semaphore")
        # ssb = options.get("share_bounded_semaphore")

        worker = Process(
            target=function,
            args=(*options.get("args"), ),
            kwargs={**options.get("kwargs")}
        )
        worker.start()
        if options.get("needs_join"):
            result = worker.join()
        return {"worker": worker, "result": result}
