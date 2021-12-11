from taskcontrol.lib import FileReaderBase

fr = FileReaderBase()

logfile = {
    "name": "logtest",
    "file": "./demos/logs/filereaderdemo.log",
    "mode": "r",
    "encoding": "UTF-8"
}

writelogfile = {
    "name": "filetest",
    "file": "./demos/logs/filereaderdemo_filename.log",
    "mode": "a",
    "encoding": "UTF-8"
}

if fr:
    fr.file_store(logfile)
    fr.file_store(writelogfile)

    # # Alternate ways - Readlines
    # # Adds all lines from filereaderdemo.log
    l = fr.file_read(logfile.get("name"), "readlines")
    print("lines 1: \n", l)
    s = fr.file_append(writelogfile.get("name"), l, "writelines")
