#!/usr/bin/python
import logging, logging.config

logging.config.fileConfig("logging.conf")
main_log = logging.getLogger("main_log")

main_log.info("udpLogs daemon starting up")

from input.file import FileInput
from eventhandler import EventHandler

eh = EventHandler()
fs = FileInput(eh,"/home/devicenull/source/udpLogs/test.log")

fs.start()
