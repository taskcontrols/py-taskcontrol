
# Actions and Listeners
# (Publisher Subscriber using Action like functions)
from taskcontrol.actions import Action


print("\nActions:\nDemonstrating Action and Action Listeners")
action = Action()

def run(data):
    print("Run Action Handler", data)

action.register_event({"name": "new", "event": run})
action.register_listener({"name": "new", "action": "run", "listener": run})
action.listen({"name": "new"})
action.message({"name": "new", "message": "Testing message"})
action.stop_listening({"name": "new"})
action.unregister_listener({"name": "new", "action": "run"})
action.unregister_event({"name": "new"})
