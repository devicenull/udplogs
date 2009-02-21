
import logging
main_log = logging.getLogger("main_log")

player_count = 0
def player_connect(event,ip,port,timestamp):
	global player_count
	player_count += 1
	main_log.debug("%i players have connected so far" % player_count)

from eventhandler import eventhandler
eventhandler.registerCallback(player_connect,['player_connect'])
