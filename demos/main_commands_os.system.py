
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
    print("RUNNING RUN os_system to run into shell: \n")
    result_os_system = c.execute(command, mode="os_system", stdin_mode=True, options={ "args": cmd })
    print(result_os_system)

    # os_popen
    print("RUNNING RUN os_system - mkdir: \n")
    result_os_system = c.execute("mkdir", mode="os_system", stdin_mode=True, options={ "args": ["pythonscriptrun_ossystem"] })
    
    print(result_os_system)
