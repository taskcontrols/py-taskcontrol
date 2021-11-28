
from taskcontrol.lib import CommandsBase

c = CommandsBase()
cmd = ["ssh", "-i", "./developers.pem", "user@192.168.0.1"]
command = cmd.pop(0)


# # Access the resulting process after the command execution
# # Will have STDOUT or STDERR

result_popen = c.execute(command, mode="subprocess_popen", stdin_mode=True, options={"args": cmd, "stdin_input": "touch tests"})
print("RUNNING RESULT FOR POPEN [Popen Object - key:'stdout' type(_io.TextIOWrapper)]:\n")
for l in result_popen.__dict__.get("_stdout_buff"):
    for i in l.split("\n"):
        print(i)

result_run = c.execute(command, mode="subprocess_run", stdin_mode=True, options={"args": cmd, "stdin_input": "touch tests"})
print("RUNNING RESULT FOR RUN [CompletedProcess Object - key:'stdout' type(str)]:\n")
print(result_run.__dict__.get("stdout"))

# # TODO: Locks up in Windows(x64)
# # result = c.execute(command, mode="subprocess_call", stdin_mode=True, options={"args": cmd, "stdin_input": "touch tests"})
# # print("RUNNING RESULT FOR CALL:\n")

# os_popen
result_run = c.execute("mkdir nwdir", mode="os_open", stdin_mode=True, options={ "args": "" })
print("RUNNING RESULT FOR RUN os_open: \n")
print(result_run)
