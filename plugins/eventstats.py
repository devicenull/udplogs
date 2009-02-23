import logging
main_log = logging.getLogger("main_log")

from basestats import PlayerStats,WeaponStats,player_stats


def player_triggered(event,ip,port,timestamp):
	global player_stats
	if not player_stats[event.steamid].events.has_key(event.steamid):
		player_stats[event.steamid] = PlayerStats(event.steamid)

	if not player_stats[event.steamid].events.has_key(event.event):
		player_stats[event.steamid].events[event.event] = 0

	player_stats[event.steamid].events[event.event] += 1


from eventhandler import eventhandler
eventhandler.registerCallback(player_triggered,['player_triggered'])

