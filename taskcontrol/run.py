
import argparse
from taskcontrol.lib import UtilsBase


class CLI(UtilsBase):
    def __init__(self, **kwargs):
        super().__init__("taskcontrolcli", {}, **kwargs)
        self.create({"name": "a", "action": lambda x: print(x)})

    def run(self, commands):
        # cmd_list = commands.strip(" ").split(",")
        # r = {}
        # for cmd in cmd_list:
        #     r[cmd] = self.fetch(str(cmd))  # ["action"]()
        #     print(r[cmd])
        #     print("Menu Option ", str(cmd), "has been processed. \n")
        pass


def run():
    print("[TODO] CLI MENU: \n")
    c = CLI()

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--user', '-u', help='username')
    # parent_parser.add_argument('--debug', default=False, required=False,
    #                            action='store_true', dest="debug", help='debug flag')

    main_parser = argparse.ArgumentParser()
    service_subparsers = main_parser.add_subparsers(dest="service_command")

    ssh = service_subparsers.add_parser("--ssh", help="""
        SSH Automate: Run the bash shell script to different ssh servers. 
        --ssh -servers -commands -script
    """, parents=[parent_parser])

    sshshell = service_subparsers.add_parser("--sshshell", help="""
        SSH Shell: Open the ssh shell of the host:port. 
        --sshshell **_all_ssh_options**
    """, parents=[parent_parser])

    clientagent = service_subparsers.add_parser("--client-agent", help="""
        Client-Agent Architecture: Agent. Run the Client-Server Client Agent in the host:port. 
        --client-agent host port
    """, parents=[parent_parser])

    clientserver = service_subparsers.add_parser("--client-server", help="""
        Client-Agent Architecture: Server. Run the Client-Server Server Host in the host:port. 
        --client-server host port
    """, parents=[parent_parser])

    pubsub_publisher = service_subparsers.add_parser("--publisher", help="""
        Publish-Subscribe Architecture: Publisher. Run the Client-Server Server Host in the host:port. 
        --publisher host port
    """, parents=[parent_parser])

    pubsub_subscriber = service_subparsers.add_parser("--subscriber", help="""
        Publish-Subscribe Architecture: Subscriber. Run the Client-Server Server Host in the host:port. 
        --subscriber host port
    """, parents=[parent_parser])

    pubsub_server = service_subparsers.add_parser("--pubsub-server", help="""
        Publish-Subscribe Architecture: Server. Run the Client-Server Server Host in the host:port. 
        --pubsub-server host port
    """, parents=[parent_parser])

    webhookserver = service_subparsers.add_parser("--client-server", help="""
        WebHooks Server: Run the Client-Server Server Host in the host:port. 
        --client-server host port
    """, parents=[parent_parser])

    plugins = service_subparsers.add_parser("--plugin", help="""
        Plugins: Create a plugin. 
        --plugin config
    """, parents=[parent_parser])

    commands = service_subparsers.add_parser("--command", help="""
        Commands: Run commands in the shell once or iterated. 
        --command
    """, parents=[parent_parser])

    # action_subparser = service_parser.add_subparsers(title="action",
    #                     dest="action_command")
    # action_parser = action_subparser.add_parser("second", help="second",
    #                     parents=[parent_parser])

    args = main_parser.parse_args()
    c.run(args)
