# Actions and Hooks Base


class ConcurencyBase():

    # asynchronous, needs_join
    def mthread_run(self, function, options):
        # Consider adding thread alive, and other method options access to functions
        from threading import Thread
        result = None
        if type(options) == dict:
            share_data = options.get("share_data")
        worker = Thread(
            target=function,
            daemon=True,
            args=(*options.get("args"), ),
            kwargs={**options.get("kwargs"),
                    "share_data": share_data, "result": result}
        )
        worker.setDaemon(True)
        worker.start()
        if options.get("needs_join"):
            worker.join()
        return worker, result

    # asynchronous, needs_join
    def mprocess_run(self, function, options):
        # Consider adding process alive, and other method options access to functions
        from multiprocessing import Process, Array, Value
        result = None
        sa = options.get("share_array")
        sv = options.get("share_data")
        # check need here. Create a common one outside by user
        worker = Process(
            target=function,
            args=(*options.get("args"), ),
            kwargs={**options.get("kwargs"),
                    "share_array": sa, "share_value": sv}
        )
        worker.start()
        if options.get("needs_join"):
            result = worker.join()
        return worker, result
