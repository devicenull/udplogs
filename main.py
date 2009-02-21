#!/usr/bin/python
import os, logging, logging.config

logging.config.fileConfig("logging.conf")
main_log = logging.getLogger("main_log")

main_log.info("udpLogs daemon starting up")

from input.file import FileInput
from eventhandler import EventHandler,eventhandler

print globals()

for root, dirs, files in os.walk("/home/devicenull/source/udpLogs/events"):
	for cur in files:
		if cur[-3:] == ".py":
			curevent = cur[:-3]
			main_log.debug("Loading event %s" % curevent)
			__import__("events.%s" % curevent,globals())


fs = FileInput(eventhandler,"/home/devicenull/source/udpLogs/test.log")

fs.start()
