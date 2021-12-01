

from ctests import cmd
from taskcontrol.lib import CommandsBase

c = CommandsBase()
# cmd = ["ssh", "-i", "./developers.pem", "user@192.168.0.1"]

# Comment following line out and change above cmd with your details or commands
if cmd:
    command = cmd.pop(0)

    # # Access the resulting process after the command execution
    result_run = c.execute(command, mode="subprocess_run", stdin_mode=True, options={
        "args": cmd, "input": "./testssh.sh", "capture_output": True})
    print(
        "RUNNING RESULT FOR subprocess_run:\n", result_run[0])
    print("Result stdout \n", result_run[0].stdout)
    print("Result stderr \n", result_run[0].stderr)
    print("Result Output \n", result_run[1])

    result_run = c.execute(command, mode="subprocess_run", stdin_mode=True, options={
        "args": cmd, "input": "bash testssh.sh", "capture_output": True})
    print(
        "RUNNING RESULT FOR subprocess_run:\n", result_run[0])
    print("Result stdout \n", result_run[0].stdout)
    print("Result stderr \n", result_run[0].stderr)
    print("Result Output \n", result_run[1])

    result_run = c.execute(command, mode="subprocess_run", stdin_mode=True, options={
        "args": cmd, "input": "rm -f testssh.txt", "capture_output": True})
    print(
        "RUNNING RESULT FOR subprocess_run:\n", result_run)
    # print("Result stdout \n", result_run)
    # print("Result stderr \n", result_run[0].stderr)
    # print("Result Output \n", result_run[1])

    result_run = c.execute(command, mode="subprocess_run", stdin_mode=True, options={
        "args": cmd, "input": "rm -f tests_popen"})
    print(
        "RUNNING RESULT FOR subprocess_run:\n", result_run[0])
    print("Result stdout \n", result_run[0].stdout)
    print("Result stderr \n", result_run[0].stderr)
    print("Result Output \n", result_run[1])

    result_run = c.execute(command, mode="subprocess_run", stdin_mode=True, options={
        "args": cmd, "input": "rm -f tests_passed_popen"})
    print(
        "RUNNING RESULT FOR subprocess_run:\n", result_run[0])
    print("Result stdout \n", result_run[0].stdout)
    print("Result stderr \n", result_run[0].stderr)
    print("Result Output \n", result_run[1])

    result_run = c.execute(command, mode="subprocess_run", stdin_mode=True, options={
        "args": cmd, "input": "rm -f tests"})
    print(
        "RUNNING RESULT FOR subprocess_run:\n", result_run[0])
    print("Result stdout \n", result_run[0].stdout)
    print("Result stderr \n", result_run[0].stderr)
    print("Result Output \n", result_run[1])

    result_run = c.execute(command, mode="subprocess_run", stdin_mode=True, options={
        "args": cmd, "input": "rm -f tests_passed"})
    print(
        "RUNNING RESULT FOR subprocess_run:\n", result_run[0])
    print("Result stdout \n", result_run[0].stdout)
    print("Result stderr \n", result_run[0].stderr)
    print("Result Output \n", result_run[1])

    # # Following has Error in implementation
    # # TODO: Following does not send input from the PIPE - .communicate and stdin.write does not work
    # # # # - Following does not capture the Output from the PIPE
    # # # # - Have to use input instead of std_input to send and get the stdin and stdout
    # # # #
    result_run = c.execute(command, mode="subprocess_run", stdin_mode=True, options={
        "args": cmd, "stdin_input": "./testssh.sh"})
    print(
        "RUNNING RESULT FOR subprocess_run:\n", result_run[0])
    print("Result stdout \n", result_run[0].stdout)
    print("Result stderr \n", result_run[0].stderr)
    print("Result Output \n", result_run[1])
