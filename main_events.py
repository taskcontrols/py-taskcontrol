
# Actions and Listeners
# (Publisher Subscriber using Action like functions)
from taskcontrol.actions import Events


print("\nActions:\nDemonstrating Action and Action Listeners")
event = Events()

def run(data):
    print("Run Action Handler", data)

event.register_event({"name": "new", "event": run})
event.register_listener({"event_name": "new", "name": "run", "listener": run})
event.listen({"name": "new"})
event.message({"event_name": "new", "message": "Testing message"})
event.stop_listening({"event_name": "new"})
event.unregister_listener({"event_name": "new", "action": "run"})
event.unregister_event({"name": "new"})
