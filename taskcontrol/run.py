
from taskcontrol.lib import UtilsBase

class CLI(UtilsBase):
    def __init__(self, **kwargs):
        super().__init__("taskcontrolcli", {}, **kwargs)

def run():
    c = CLI()
    print("[TODO] CLI MENU: \n")
    print("""
    You can choose to start or run the following: \n
    (Type options index seperated using commas)

    1. Client-Agent Architecture: Server
    2. Client-Agent Architecture: Client
    3. Publish-Subscribe Architecture: Server
    4. Publish-Subscribe Architecture: Publisher
    5. Publish-Subscribe Architecture: Subscriber
    6. WebHooks Server
    7. TBD (More to come including Plugins, SSH, Commands, etc)

    """)

