import logging

main_log = logging.getLogger("main_log")
event_log = logging.getLogger("event_log")

class EventHandler:
	def event(self,instr):
		instr = instr.strip()
		event_log.debug(instr)
