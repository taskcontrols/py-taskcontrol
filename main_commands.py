
from taskcontrol.lib import CommandsBase

c = CommandsBase()
# cmd = ["ssh", "-i", "./developers.pem", "user@192.168.0.1"]
cmd = ["ssh", "-i", "C:/Users/gb/Documents/220921-070721/developers.pem", "admin@ec2-3-109-0-135.ap-south-1.compute.amazonaws.com"]
command = cmd.pop(0)


# # Access the resulting process after the command execution
# # Will have STDOUT or STDERR

result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={"args": cmd, "stdin_input": "touch tests"})
print("RUNNING RESULT FOR POPEN:\n")
for l in result_popen.__dict__.get("_stdout_buff"):
    for i in l.split("\n"):
        print(i)

result_run = c.execute(command, mode="subprocess_run", stdin_mode=True, options={"args": cmd, "stdin_input": "touch tests"})
print("RUNNING RESULT FOR RUN:\n")
print(result_run.__dict__.get("stdout"))

# TODO: Locks up in Windows(x64)
# result = c.execute(command, mode="subprocess_call", stdin_mode=True, options={"args": cmd, "stdin_input": "touch tests"})
# print("RUNNING RESULT FOR CALL:\n")

# TODO: os_popen

