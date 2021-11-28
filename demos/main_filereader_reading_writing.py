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
    s = fr.file_write(writelogfile.get("name"), l, "writelines")

    # # Alternate ways - Read
    # # Adds all lines from filereaderdemo.log
    l = fr.file_read(logfile.get("name"), "read")
    print("block 2: \n", l)
    s = fr.file_write(writelogfile.get("name"), l, "write")

    # # Alternate ways - Read with index
    # # Adds first 9 characters from filereaderdemo.log - "This isano"
    l = fr.file_read(logfile.get("name"), "read", 10)
    print("block 3: \n", l)
    s = fr.file_write(writelogfile.get("name"), l, "write")

    # # Alternate ways - Readline without index
    # # Adds first line from filereaderdemo.log - "This"
    l = fr.file_read(logfile.get("name"), "readline")
    print("block 4: \n", l)
    s = fr.file_write(writelogfile.get("name"), l, "writelines")

    # # Alternate ways - Readline without index
    # # Adds first line from filereaderdemo.log - "This"
    l = fr.file_read(logfile.get("name"), "readline")
    print("block 5: \n", l)
    s = fr.file_write(writelogfile.get("name"), l, "write")

    # # Alternate ways - Readline with index
    # # Adds first line from filereaderdemo.log - "This"
    l = fr.file_read(logfile.get("name"), "readline", 5)
    print("block 6: \n", l)
    s = fr.file_write(writelogfile.get("name"), l, "write")

    # # Alternate ways - file (returns array so needs to use writelines)
    # # Adds all lines from filereaderdemo.log
    l = fr.file_read(logfile.get("name"), "file")
    print("block 7: \n", l)
    s = fr.file_write(writelogfile.get("name"), l, "writelines")
