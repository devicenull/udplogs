#!/usr/bin/python
import os, logging, logging.config

logging.config.fileConfig("logging.conf")
main_log = logging.getLogger("main_log")

main_log.info("udpLogs daemon starting up")

from input.file import FileInput
from eventhandler import EventHandler,eventhandler

config = {'basedir':'/home/devicenull/source/udpLogs'}

main_log.info("Loading events...")
eventcount = 0

for root, dirs, files in os.walk(os.path.join(config['basedir'],"events")):
	for cur in files:
		if cur[-3:] != ".py":
			continue
		curevent = cur[:-3]
		main_log.debug("Loading event %s" % curevent)
		__import__("events.%s" % curevent,globals())
		eventcount += 1

main_log.info("Loaded %i events!" % eventcount)

main_log.info("Loading plugins...")
plugincount = 0

for root, dirs, files in os.walk(os.path.join(config['basedir'],"plugins")):
	for cur in files:
		if cur[-3:] != ".py":
			continue
		curplugin = cur[:-3]
		main_log.debug("Loading plugin %s" % curplugin)
		__import__("plugins.%s" % curplugin,globals())
		plugincount += 1

main_log.info("Loaded %i plugins!" % plugincount)

fs = FileInput(eventhandler,"/home/devicenull/source/udpLogs/test.log")

fs.start()
