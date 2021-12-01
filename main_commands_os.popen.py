
from taskcontrol.lib import CommandsBase

c = CommandsBase()
# cmd = ["ssh", "-i", "./developers.pem", "user@192.168.0.1"]

# Comment following line out and change above cmd with your details or commands
from ctests import cmd
if cmd:
    command = cmd.pop(0)


    # # Access the resulting process after the command execution
    # # Will have STDOUT or STDERR

    # os_popen
    result_run = c.execute("mkdir nwdir", mode="os_popen", stdin_mode=True, options={ "args": "" })
    print("RUNNING RESULT FOR RUN os_open: \n")
    print(result_run)
