from taskcontrol.framework.utils import LogBase
import logging

log = LogBase()


if log:
    
    lg = log.logger_create({
        "name": "logtest",
        "handlers": {"handler": {"type": "file", "format": "%(levelname)s - %(asctime)s - %(name)s - %(message)s", "path": "./demos/logs/", "file": "filename.log"}, "level": logging.INFO}
    })
    if lg:
        l = log.log({
            "name": "logtest",
            "level": "info",
            "message": "This is a test"
        })
        if not l:
            print("Error in logging")
        d = log.logger_delete("logtest")
        if d:
            print("Log deleted")
        else:
            print("Unable to delete")
