
# Actions and Listeners
# (Publisher Subscriber using Action like functions)
from taskcontrol.actions import Events


print("\nActions:\nDemonstrating Action and Action Listeners")
event = Events()

def run(data):
    print("Run Action Handler", data)

