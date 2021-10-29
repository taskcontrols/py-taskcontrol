from taskcontrol.framework.utils import FileReaderBase

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
    # # Alternate ways - Readlines
    # # Adds all lines from filereaderdemo.log
    f = fr.file_open(logfile)
    l = fr.file_read(f, "readlines")
    print("lines", l)
    fr.file_close(l)
    fn = fr.file_open(writelogfile)
    s = fr.file_write(fn, l, "writelines")
    fr.file_close(fn)

    # # Alternate ways - Read
    # # Adds all lines from filereaderdemo.log
    f = fr.file_open(logfile)
    l = fr.file_read(f, "read")
    print("block", l)
    fr.file_close(l)
    fn = fr.file_open(writelogfile)
    s = fr.file_write(fn, l, "write")
    fr.file_close(fn)

    # # Alternate ways - Read with index
    # # Adds first 9 characters from filereaderdemo.log - "This isano"
    f = fr.file_open(logfile)
    l = fr.file_read(f, "read", 10)
    print("block", l)
    fr.file_close(l)
    fn = fr.file_open(writelogfile)
    s = fr.file_write(fn, l, "write")
    fr.file_close(fn)

    # # Alternate ways - Readline without index
    # # Adds first line from filereaderdemo.log - "This"
    f = fr.file_open(logfile)
    l = fr.file_read(f, "readline")
    print("block", l)
    fr.file_close(l)
    fn = fr.file_open(writelogfile)
    s = fr.file_write(fn, l, "writelines")
    fr.file_close(fn)

    # # Alternate ways - Readline without index
    # # Adds first line from filereaderdemo.log - "This"
    f = fr.file_open(logfile)
    l = fr.file_read(f, "readline")
    print("block", l)
    fr.file_close(l)
    fn = fr.file_open(writelogfile)
    s = fr.file_write(fn, l, "write")
    fr.file_close(fn)

    # # Alternate ways - Readline with index
    # # Adds first line from filereaderdemo.log - "This"
    f = fr.file_open(logfile)
    l = fr.file_read(f, "readline", 5)
    print("block", l)
    fr.file_close(l)
    fn = fr.file_open(writelogfile)
    s = fr.file_write(fn, l, "write")
    fr.file_close(fn)

    # # Alternate ways - file (returns array so needs to use writelines)
    # # Adds all lines from filereaderdemo.log
    f = fr.file_open(logfile)
    l = fr.file_read(f, "file")
    print("block", l)
    fr.file_close(l)
    fn = fr.file_open(writelogfile)
    s = fr.file_write(fn, l, "writelines")
    fr.file_close(fn)
