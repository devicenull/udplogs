import logging

main_log = logging.getLogger("main_log")

class FileInput:
	def __init__(self, eventHandler, filename):
		self.input = open(filename,"r")
		self.eventHandler = eventHandler
		main_log.debug("FileInput init, eventHandler=%s log source=%s" % (eventHandler,filename))

	# example line:
	# L 02/05/2009 - 01:04:11: "[SC-UBW] Yahn<1620><BOT><>" connected, address "none"
	# timestamp ends at char 25	
	def start(self):
		main_log.debug("FileInput starting!")
		for curLine in self.input:
			self.eventHandler.event(curLine[25:])

	def stop(self):
		main_log.debug("FileInput stopping!")
