import logging

main_log = logging.getLogger("main_log")
event_log = logging.getLogger("event_log")

class EventHandler:
	def __init__(self):
		self.events = []

	def register(self,newevent):
		self.events.append(newevent)
		main_log.debug("Registered event %s" % newevent)

	def event(self,instr):
		instr = instr.strip()
		event_log.debug(instr)

		for cur in self.events:
			if cur.isMatch(instr):
				return cur(instr)
		return None

eventhandler = EventHandler()
