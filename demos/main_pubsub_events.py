from taskcontrol.actions import EPubSub


def run(data):
    print("Running Pubsub")


def publisher(data):
    print("Running publisher", data)


def subscriber(data):
    print("Running subscriber", data)


config = {"name": "new", "handler": run, "queue": None, "maxsize": 10,
          "queue_type": "queue", "processing_flag": False,  "batch_interval": 5, "events": {}}
name = config.get("name")

pb = EPubSub()
p = pb.pubsub_create(config)

if p:
    print("Event register", pb.register_event(
        name, {"name": "testevent", "event": run}))
    print("Publish register", pb.register_publisher(
        name, {"name": "pubone", "event_name": "testevent", "publisher": publisher}))
    print("Subscribers register", pb.register_subscriber(
        name, {"name": "subone", "event_name": "testevent", "subscriber": subscriber}))
    print("Subscribers register", pb.register_subscriber(
        name, {"name": "subtwo", "event_name": "testevent", "subscriber": subscriber}))
    print("Event sending", pb.send({"event_name": "testevent",
                                    "message": "Testing event testevent"}))
    print("Publisher unregister", pb.unregister_publisher(
        name, {"name": "pubone", "event_name": "testevent"}))
    print("Subscriber unregister", pb.unregister_subscriber(
        name, {"name": "subone", "event_name": "testevent"}))
    print("Subscriber unregister", pb.unregister_subscriber(
        name, {"name": "subtwo", "event_name": "testevent"}))
    print("Pubsub Object ", pb.fetch(name))
    print("Pubsub Object Deleted ", pb.pubsub_delete(name))
    print("Pubsub Object ", pb.fetch(name))
