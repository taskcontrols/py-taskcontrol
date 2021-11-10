from taskcontrol.lib.utils import EPubSubBase


def run(data):
    print("Running Pubsub ", data)


def publisher(data):
    print("Running publisher ", data)


def subscriber(data):
    print("Running subscriber ", data)


config = {"name": "new", "handler": run, "queue": None, "maxsize": 10,
          "queue_type": "queue", "processing_flag": False,  "batch_interval": 5, "events": {}}
name = config.get("name")

pb = EPubSubBase()
p = pb.pubsub_create(config)

if p:
    print("Event registered ", pb.register_event(name, {"name": "testevent", "event": run}))
    print("Event listened ", pb.listen(name, "testevent"))
    print("Publisher registered ", pb.register_publisher(name, {"name": "pubone", "event_name": "testevent", "publisher": publisher}))
    print("Subscribers registered ", pb.register_subscriber(name, {"name": "subone", "event_name": "testevent", "subscriber": subscriber}))
    print("Subscribers registered ", pb.register_subscriber(name, {"name": "subtwo", "event_name": "testevent", "subscriber": subscriber}))
    print("Event sending ", pb.send({"event_name": "testevent", "queue_name": "new", "message": "Testing event testevent", "publisher": "pubone"}))
    print("Publisher unregistered ", pb.unregister_publisher(name, {"name": "pubone", "event_name": "testevent"}))
    print("Subscriber unregistered ", pb.unregister_subscriber(name, {"name": "subone", "event_name": "testevent"}))
    print("Subscriber unregistered ", pb.unregister_subscriber(name, {"name": "subtwo", "event_name": "testevent"}))
    print("Pubsub Object PRINT FROM SCRIPT: ", pb.fetch(name))
    print("Event unlistened ", pb.stop(name, "testevent"))
    print("Pubsub Object Deleted ", pb.pubsub_delete(name))
    print("Pubsub Object (Should return Error for handling) ", pb.fetch(name))
