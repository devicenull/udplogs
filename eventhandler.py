import logging

main_log = logging.getLogger("main_log")
event_log = logging.getLogger("event_log")

class EventHandler:
	def __init__(self):
		self.events = []

	def registerEvent(self,newevent):
		self.events.append(newevent)
		main_log.debug("Registered event %s" % newevent)

	def registerCallback(self,callback,events):
		pass

	def event(self,instr):
		instr = instr.strip()

		for cur in self.events:
			if cur.isMatch(instr):
				event_log.debug(cur(instr))

eventhandler = EventHandler()
