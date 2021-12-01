
from ctests import cmd
from taskcontrol.lib import CommandsBase

c = CommandsBase()
# cmd = ["ssh", "-i", "./developers.pem", "user@192.168.0.1"]

# Comment following line out and change above cmd with your details or commands
if cmd:
    command = cmd.pop(0)

    # # Access the resulting process after the command execution
    # # Will have STDOUT or STDERR

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
        "args": cmd, "input": "touch tests"})
    print(
        "RUNNING RESULT FOR subprocess_popen:\n", result_popen[0])
    print("Result stdout \n", result_popen[0].stdout)
    print("Result stderr \n", result_popen[0].stderr)
    print("Result Output \n", result_popen[1])

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
        "args": cmd, "stdin_input": "rm -f tests"})
    print(
        "RUNNING RESULT FOR POPEN [Popen Object - key:'stdout' type(_io.TextIOWrapper)]:\n")

    for l in result_popen[0].__dict__.get("_stdout_buff"):
        for i in l.split("\n"):
            print(i)

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
        "args": cmd, "stdin_input": "touch tests_passed"})
    print(
        "RUNNING RESULT FOR POPEN [Popen Object - key:'stdout' type(_io.TextIOWrapper)]:\n")

    for l in result_popen[0].__dict__.get("_stdout_buff"):
        for i in l.split("\n"):
            print(i)
