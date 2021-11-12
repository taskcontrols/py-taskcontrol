from taskcontrol import FileReaderBase

fr = FileReaderBase()

logfile = {
    "name": "logtest",
    "file": "./demos/logs/filereaderdemo.log",
    "mode": "r"
}

writelogfile = {
    "name": "filetest",
    "file": "./demos/logs/filereaderdemo_filename.log",
    "mode": "a"
}

if fr:
    pass

