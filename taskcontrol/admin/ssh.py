
from taskcontrol.lib import CommandsBase

def sshshell(command):
    c = CommandsBase()
    cmd = command.pop(0)
    result = c.execute(cmd, mode="os_system", stdin_mode=True, options={ "args": command })
    return result


def ssh(command, ssh_commands):
    c = CommandsBase()
    cmd = command.pop(0)

    if (len(ssh_commands) - 2) != "echo '\nENTERING SSH WINDOW: \n'":
        ssh_commands.insert(0, "echo '\nENTERING SSH WINDOW: \n'")
    if (len(ssh_commands) - 2) != "echo 'EXITING SSH WINDOW: \n'":
        ssh_commands.append("echo 'EXITING SSH WINDOW: \n'")
    if (len(ssh_commands) - 1) != "exit 0":
        ssh_commands.append("exit 0")
    
    result_popen = c.execute(cmd, mode="subprocess_popen", stdin_mode=True, options={ "args": command, "stdin_input": " && ".join(ssh_commands) })
    return result_popen

