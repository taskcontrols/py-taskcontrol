
from taskcontrol.lib import UtilsBase

class CLI(UtilsBase):
    def __init__(self, **kwargs):
        super().__init__("taskcontrolcli", {}, **kwargs)

def run():
    c = CLI()
    print("[TODO] CLI Menu Working as Expected: \n")

