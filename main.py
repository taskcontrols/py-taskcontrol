import shutil

def executable(command):
        return shutil.which(command)
print(executable("python"))