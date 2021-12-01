
from taskcontrol.lib import CommandsBase

c = CommandsBase()
# cmd = ["ssh", "-i", "./developers.pem", "user@192.168.0.1"]

# Comment following line out and change above cmd with your details or commands
from ctests import cmd
if cmd:
    command = cmd.pop(0)

    # # Access the resulting process after the command execution
    # # Will have STDOUT or STDERR

    # # TODO: Locks up in Windows(x64)
    result = c.execute(command, mode="subprocess_call", stdin_mode=True, options={"args": cmd, "stdin_input": "touch tests"})
    print("RUNNING RESULT FOR CALL:\n", result)

    result = c.execute("./testsh.sh", mode="subprocess_call", stdin_mode=False)
    print("RUNNING RESULT FOR CALL BASH:\n", result)

    result = c.execute(command, mode="subprocess_call", stdin_mode=True, options={"args": cmd, "stdin_input": "touch tests"})
    print("RUNNING RESULT FOR CALL:\n", result)

