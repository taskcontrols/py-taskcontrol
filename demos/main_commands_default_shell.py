
from taskcontrol.lib import CommandsBase

c = CommandsBase()
# cmd = ["ssh", "-i", "./developers.pem", "user@192.168.0.1"]

# Comment following line out and change above cmd with your details or commands
from ctests import cmd
if cmd:
    command = cmd.pop(0)

    # # Access the resulting process after the command execution
    # # Will have STDOUT or STDERR
    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
                        "args": cmd, "stdin_input": "./testssh.sh"})
    print("RUNNING shell through subprocess_popen:\n")
    print(result_popen[0].__dict__.get("_stdout_buff")[0])

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
                        "args": cmd, "stdin_input": "./testssh_rm.sh"})
    print("RUNNING shell through subprocess_popen:\n")
    print(result_popen[0].__dict__.get("_stdout_buff")[0])

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
                        "args": cmd, "stdin_input": "./testssh_all.sh"})
    print("RUNNING shell through subprocess_popen:\n")
    print(result_popen[0].__dict__.get("_stdout_buff")[0])

    #### RUNNING RESULT FOR BASH.SH USING BASH

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
                        "args": cmd, "stdin_input": "bash ./testssh.sh"})
    print("RUNNING shell through subprocess_popen:\n")
    print(result_popen[0].__dict__.get("_stdout_buff")[0])

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
                        "args": cmd, "stdin_input": "bash ./testssh_rm.sh"})
    print("RUNNING shell through subprocess_popen:\n")
    print(result_popen[0].__dict__.get("_stdout_buff")[0])

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
                        "args": cmd, "stdin_input": "bash ./testssh_all.sh"})
    print("RUNNING shell through subprocess_popen:\n")
    print(result_popen[0].__dict__.get("_stdout_buff")[0])

    #### RUNNING RESULT FOR BASH.SH USING RBASH

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
                        "args": cmd, "stdin_input": "rbash ./testssh.sh"})
    print("RUNNING shell through subprocess_popen:\n")
    print(result_popen[0].__dict__.get("_stdout_buff")[0])

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
                        "args": cmd, "stdin_input": "rbash ./testssh_rm.sh"})
    print("RUNNING shell through subprocess_popen:\n")
    print(result_popen[0].__dict__.get("_stdout_buff")[0])

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
                        "args": cmd, "stdin_input": "rbash ./testssh_all.sh"})
    print("RUNNING shell through subprocess_popen:\n")
    print(result_popen[0].__dict__.get("_stdout_buff")[0])

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
                        "args": cmd, "stdin_input": "rbash ./testssh.sh"})
    print("RUNNING shell through subprocess_popen:\n")
    print(result_popen[0].__dict__.get("_stdout_buff")[0])

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
                        "args": cmd, "stdin_input": "rbash ./testssh_bash.sh"})
    print("RUNNING shell through subprocess_popen:\n")
    print(result_popen[0].__dict__.get("_stdout_buff")[0])

    result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={
                        "args": cmd, "stdin_input": "echo '\n\nECHO_SSH_RAN_WELL'"})
    print("RUNNING shell through subprocess_popen:\n")
    print(result_popen[0].__dict__.get("_stdout_buff")[0])

