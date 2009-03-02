import logging
main_log = logging.getLogger("main_log")

from basestats import Stats


def player_triggered(event,ip,port,timestamp):
	player = Stats.getPlayer(event.steamid,ip,port)
	curevent = player.getEvent(event.event)
	
	curevent.trigger_count += 1

def player_joinedteam(event,ip,port,timestamp):
	player = Stats.getPlayer(event.steamid,ip,port)
	
	player.getTeam(event.newteam).join_count += 1

def server_map(event,ip,port,timestamp):
	curmap = Stats.getServerMap(ip,port)

	players = Stats.getPlayers(ip,port)
	for cur in players:
		players[cur].savePlayer(ip,port,curmap)

	Stats.setServerMap(ip,port,event.map)

from eventhandler import eventhandler
eventhandler.registerCallback(player_triggered,['player_triggered'])
eventhandler.registerCallback(player_joinedteam,['player_joinedteam'])
eventhandler.registerCallback(server_map,['server_map'])
