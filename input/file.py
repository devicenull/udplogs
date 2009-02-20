import logging

main_log = logging.getLogger("main_log")

class FileInput:
	def __init__(self, eventHandler, filename):
		self.input = open(filename,"r")
		self.eventHandler = eventHandler
		main_log.debug("FileInput init, eventHandler=%s log source=%s" % (eventHandler,filename))
	
	def start(self):
		main_log.debug("FileInput starting!")
		for curLine in self.input:
			self.eventHandler.event(curLine)

	def stop(self):
		main_log.debug("FileInput stopping!")
