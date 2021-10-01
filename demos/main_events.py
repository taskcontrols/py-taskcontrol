
# Actions and Listeners
# (Publisher Subscriber using Action like functions)
from taskcontrol.actions import Events


print("\nActions:\nDemonstrating Action and Action Listeners")
event = Events()


def run(data):
    print("Run Action Handler ->", data)


c = event.event_register({"name": "new", "event": run})
if c:
    event.listener_register(
        {"name": "run", "event_name": "new", "listener": run})
    event.on("new", "runner", lambda data: print(
        "Second Listener running -> ", data))
    event.start("new")
    print("'new' event state is", event.get_state("new"))
    event.set_state("new", False)
    print("'new' event state is", event.get_state("new"))
    event.set_state("new", True)
    print("'new' event state is", event.get_state("new"))
    event.send({"event_name": "new", "message": "Testing message"})
    event.emit("new", "Testing message")
    event.listener_register({"event_name": "new", "name": "run"})
    event.stop("new")
    event.event_unregister("new")
