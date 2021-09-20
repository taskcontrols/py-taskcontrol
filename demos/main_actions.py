
# Actions and Listeners
# (Publisher Subscriber using Events like functions)
from taskcontrol.actions import Actions


print("\nActions/Events:\nDemonstrating Event and Event Listeners")
action = Actions()

def run(data):
    print("Run Event Handler", data)

action.register_event({"name": "new", "event": run})
action.register_listener({"name": "new", "action": "run", "listener": run})
action.listen({"name": "new"})
action.message({"name": "new", "message": "Testing message"})
action.stop_listening({"name": "new"})
action.unregister_listener({"name": "new", "action": "run"})
action.unregister_event({"name": "new"})

