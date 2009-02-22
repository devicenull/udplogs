import logging

main_log = logging.getLogger("main_log")
event_log = logging.getLogger("event_log")

class EventHandler:
	def __init__(self):
		self.events = {}

	def registerEvent(self,newevent):
		eventname = newevent.__name__.split(".")[-1]
		self.events[eventname] = {"event":newevent,"callbacks":[]}
		main_log.debug("Registered event %s" % eventname)

	def registerCallback(self,callback,cb_events):
		for cur in cb_events:
			if self.events.has_key(cur):
				self.events[cur]['callbacks'].append(callback)
				main_log.debug("Registered callback %s for event %s" % (callback,cur))
			else:
				main_log.warning("Attempted to register callback %s for unknown event %s" % (callback,cur))

	def event(self,instr,ip="127.0.0.1",port=27015,timestamp="sometime"):
		instr = instr.strip().replace("\n","")

		found = 0
		for cur in self.events:
			if self.events[cur]['event'].isMatch(instr):
				theevent = self.events[cur]['event'](instr)
				event_log.debug(theevent)
				found = 1
				for cur_cb in self.events[cur]['callbacks']:
					cur_cb(theevent,ip,port,timestamp)

		if not found:
			event_log.info("Unknown event: *%s*" % instr)
eventhandler = EventHandler()
