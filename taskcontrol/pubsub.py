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


class LoggerBase():

    def create(self):
        pass

    def log(self, level, message):
        pass

    def remove(self):
        pass


# Inherit shared and logging
class ActionsBase():

    # list of registered actions/events
    actions = []
    # list of actions/events listeners
    action_listeners = []

    def action_state(self):
        pass

    def register_event(self):
        pass

    def register_listener(self):
        pass

    def unregister_listener(self):
        pass

    def message(self):
        pass

    def listen(self):
        pass


# Inherit shared and logging
class HooksBase():

    # list of registered web hooks
    hooks = []

    def hook_state(self):
        pass

    def service_run(self):
        pass

    def service_stop(self):
        pass

    def register_hook(self):
        pass

    def register_receiver(self):
        pass

    def send(self):
        pass

    def receive(self):
        pass

