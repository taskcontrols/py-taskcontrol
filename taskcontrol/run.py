
import argparse
import sys
import copy
from taskcontrol.lib import UtilsBase


class CLI(UtilsBase):
    def __init__(self, **kwargs):
        super().__init__("taskcontrolcli", {}, **kwargs)
        self.create({"name": "a", "action": lambda x: print(x)})

    def run(self, arg, config_object):
        print("Args from the command line: ", arg)
        print("Config_Object from the command line: ", config_object)


def run():
    print("CLI MENU [TODO]: \n")
    c = CLI()
    cmd_config = {
        "name": "parser",
        "add_subparsers": {
            "title": "CHOICES",
            "dest": "CHOICES",
            "add_parser": {
                "a": {
                    "help": "Run a Taskcontrol Agent (Client-Server Arch). Alternatively, use option `agent`",
                    "aliases": ["agent"],
                    "add_argument": {"--ipaddress": {"alias": "-ip", "nargs": "*"}, "--port": {}}
                },
                "s": {
                    "help": "Run a Taskcontrol Server (Client-Server Arch). Alternatively, use option `server`",
                    "aliases": ["server"],
                    "add_argument": {"--ipaddress": {"alias": "-ip", "nargs": "*"}, "--port": {}}
                },
                "w": {
                    "help": "Run a Taskcontrol Webhook Server (Webhooks Arch). Alternatively, use option `webhook`",
                    "aliases": ["webhook"],
                    "add_argument": {"--ipaddress": {"alias": "-ip", "nargs": "*"}, "--port": {}}
                },
                "pb": {
                    "help": "Run a Taskcontrol PubSub Server (Publisher-Server-Subscriber Arch). Alternatively, use option `pubsub`",
                    "aliases": ["pubsub"],
                    "add_argument": {
                        "--publisher": {"alias": "-p", "nargs": "*"},
                        "--subscriber": {"alias": "-s", "nargs": "*"},
                        "--server": {"alias": "-srv", "nargs": "*"}
                    }
                },
                "sh": {
                    "help": "Run Commands, or Commands file, or bash, or powershell file. Alternatively, use option `shell`",
                    "aliases": ["shell"],
                    "add_argument": {
                        "--options": {"alias": "-p", "nargs": "*"}
                    }
                },
                "ssh": {
                    "help": "Run Commands, or Commands file, or bash, or powershell file using SSH",
                    "add_argument": {
                        "--bashfile": {"alias": "-bf", "nargs": "*"},
                        "--commands": {"alias": "-cmds", "nargs": "*"},
                        "--serversfile": {"alias": "-sf", "nargs": "*"}
                    },
                    "add_subparsers": {
                        "title": "server",
                        "dest": "server",
                        "add_parser": {
                                "srv": {
                                    "add_argument": {
                                        # # # [-B bind_interface] [-b bind_address] [-c cipher_spec] [-D [bind_address:]port]
                                        # # # [-E log_file] [-e escape_char] [-F configfile] [-I pkcs11]
                                        # # # [-i identity_file] [-J [user@]host[:port]] [-L address]
                                        # # # [-l login_name] [-m mac_spec] [-O ctl_cmd] [-o option] [-p port]
                                        # # # [-Q query_option] [-R address] [-S ctl_path] [-W host:port]
                                        # # # [-w local_tun[:remote_tun]] destination [command]
                                        "-B": {"nargs": "*"},
                                        "-b": {"nargs": "*"},
                                        "-c": {"nargs": "*"},
                                        "-D": {"nargs": "*"},
                                        "-E": {"nargs": "*"},
                                        "-e": {"nargs": "*"},
                                        "-F": {"nargs": "*"},
                                        "-I": {"nargs": "*"},
                                        "-i": {"nargs": "*"},
                                        "-J": {"nargs": "*"},
                                        "-L": {"nargs": "*"},
                                        "-l": {"nargs": "*"},
                                        "-m": {"nargs": "*"},
                                        "-O": {"nargs": "*"},
                                        "-o": {"nargs": "*"},
                                        "-p": {"nargs": "*"},
                                        "-Q": {"nargs": "*"},
                                        "-R": {"nargs": "*"},
                                        "-S": {"nargs": "*"},
                                        "-W": {"nargs": "*"},
                                        "-p": {"nargs": "*"},
                                        "-Q": {"nargs": "*"},
                                        "-R": {"nargs": "*"},
                                        "-S": {"nargs": "*"},
                                        "-W": {"nargs": "*"},
                                        "-w": {"nargs": "*"},
                                        "destination": {"nargs": "*"}
                                    }
                                }
                        }
                    }
                },
                "p": {
                    "help": "Run the Plugin creation tasks. Alternatively, use option `plugin`",
                    "aliases": ["plugin"],
                    "add_argument": {
                        "--create": {"alias": "-c", "nargs": "*"},
                        "--register": {"alias": "-r", "nargs": "*"},
                        "--install": {"alias": "-i", "nargs": "*"}
                    }
                }
            }
        }
    }

    plugin_config = {
        "add_parser": {
            "ep": {
                "help": "Run the Plugin creation tasks. Alternatively, use option `someexternalcommand`",
                "aliases": ["someexternalcommand"],
                "add_argument": {
                    "--some": {"alias": "-c", "nargs": "*"},
                    "--external": {"alias": "-r", "nargs": "*"},
                    "--command": {"alias": "-i", "nargs": "*"}
                }
            }
        }
    }

    for i in plugin_config.get("add_parser"):
        cmd_config.get("add_subparsers").get("add_parser").update(
            dict([[i, plugin_config.get("add_parser").get(i)]])
        )

    def generate_parse_object(subparser, parser, config_object={}):
        if subparser:
            title = subparser.get("title")
            dest = subparser.get("dest")
            add_parser = subparser.get("add_parser")

            config_object["add_subparsers"] = {}
            config_object["add_subparsers"][title] = parser.add_subparsers(
                title=title, dest=dest)
            config_object["add_subparsers"]["parsers"] = {}

            for pkey in add_parser:
                add_parser_help = add_parser.get(pkey).get("help", "")
                aliases = add_parser.get(pkey).get("aliases", [])
                add_argument = add_parser.get(pkey).get("add_argument", {})
                add_subparsers = add_parser.get(pkey).get("add_subparsers", {})

                config_object["add_subparsers"]["parsers"][pkey] = {}
                config_object["add_subparsers"]["parsers"][pkey]["parser"] = config_object["add_subparsers"][title].add_parser(
                    name=pkey,
                    aliases=aliases,
                    help=add_parser_help
                )
                config_object["add_subparsers"]["parsers"][pkey]["add_argument"] = {}
                for akey in add_argument:
                    nargs = add_argument.get(
                        akey, {"nargs": "*"}).get("nargs")
                    alias = add_argument.get(akey).get("alias")
                    if alias:
                        config_object["add_subparsers"]["parsers"][pkey]["add_argument"][akey] = config_object["add_subparsers"]["parsers"][pkey]["parser"].add_argument(
                            akey,
                            alias,
                            nargs=nargs
                        )
                    else:
                        config_object["add_subparsers"]["parsers"][pkey]["add_argument"][akey] = config_object["add_subparsers"]["parsers"][pkey]["parser"].add_argument(
                            akey,
                            nargs=nargs
                        )
                config_object["add_subparsers"]["parsers"][pkey]["add_subparsers"] = {
                }
                config_object["add_subparsers"]["parsers"][pkey]["parser"] = argparse.ArgumentParser(
                )
                config_object["add_subparsers"]["parsers"][pkey]["add_subparsers"] = generate_parse_object(
                    add_subparsers, config_object["add_subparsers"]["parsers"][pkey]["parser"], config_object["add_subparsers"]["parsers"][pkey]["add_subparsers"])
        return config_object

    parser = argparse.ArgumentParser()
    name = cmd_config.get("name")
    subparser = cmd_config.get("add_subparsers")
    result = generate_parse_object(subparser, parser)

    cargs = parser.parse_args()
    c.run(cargs, result)
