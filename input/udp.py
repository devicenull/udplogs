import logging

main_log = logging.getLogger("main_log")

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class UDPInput(DatagramProtocol):
	def __init__(self, eventHandler, port):
		self.eventHandler = eventHandler
		reactor.listenUDP(port,self)

	def start(self):
		reactor.run()

	def datagramReceived(self, data, (host, port)):
		if data[0:5] != "\xFF\xFF\xFF\xFFR":
			# not a udp log message
			return
		data = data[5:]
		timestamp = data[2:23]
		self.eventHandler.event(data[25:].strip(),host,port,timestamp)
		
