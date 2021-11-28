
from taskcontrol.lib import UtilsBase


class CLI(UtilsBase):
    def __init__(self, **kwargs):
        super().__init__("taskcontrolcli", {}, **kwargs)
        self.create({ "name": "a", "action": lambda x: print(x) })

    def run(self, commands):
        cmd_list = commands.strip(" ").split(",")
        r = {}
        for cmd in cmd_list:
            r[cmd] = self.fetch(str(cmd))  # ["action"]()
            print(r[cmd])
            print("Menu Option ", str(cmd), "has been processed. \n")


def run():
    print("[TODO] CLI MENU: \n")
    print("""
    You can choose to start or run the following: \n
    (Type options index seperated using commas) \n

    a. Client-Agent Architecture: Server \n
    b. Client-Agent Architecture: Client \n
    c. Publish-Subscribe Architecture: Server \n
    d. Publish-Subscribe Architecture: Publisher \n
    e. Publish-Subscribe Architecture: Subscriber \n
    f. WebHooks Server \n
    g. TBD (More to come including Plugins, SSH, Commands, etc) \n
    \n
    \n
    """)
    i = input("Provide Option(s) seperated by commas: \n")
    c = CLI()
    c.run(i)
