import logging
main_log = logging.getLogger("main_log")

from basestats import Stats


def player_triggered(event,ip,port,timestamp):
	player = Stats.getPlayer(event.steamid,ip,port)
	curevent = player.getEvent(event.event)
	
	curevent.trigger_count += 1

from eventhandler import eventhandler
eventhandler.registerCallback(player_triggered,['player_triggered'])

