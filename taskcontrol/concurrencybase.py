# Actions and Hooks Base
# TODO: Create structure


class ConcurencyBase():

    # asynchronous, needs_join
    def mthread_run(self, function, options):
        from threading import Thread
        result = None
        worker = Thread(target=function, daemon=True, args=(
            *options.get("args"), result), kwargs={**options.get("kwargs")})
        worker.setDaemon(True)
        worker.start()
        if options.get("needs_join"):
            worker.join()
        return worker, result

    # asynchronous, needs_join
    def mprocess_run(self, function, options):
        from multiprocessing import Process, Array
        # Apply Array for share with multiple treads
        # check need here. Create a common one outside by user
        worker = Process(target=function, args=(
            *options.get("args"),), kwargs={**options.get("kwargs")})
        worker.start()
        if options.get("needs_join"):
            result = worker.join()
        return worker, result

