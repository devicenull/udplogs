import logging

main_log = logging.getLogger("main_log")

from twisted.enterprise import adbapi

read_pool = adbapi.ConnectionPool("MySQLdb",db="playerstats",user="playerstats")
write_pool = read_pool

class Stats:
	servers = {}
	
	@staticmethod
	def getPlayer(steamid,server_ip,server_port):
		srvkey = "%s:%i" % (server_ip,server_port)
		if not Stats.servers.has_key(srvkey):
			Stats.servers[srvkey] = {}

		if not Stats.servers[srvkey].has_key(steamid):
			Stats.servers[srvkey][steamid] = PlayerStats(steamid)

		return Stats.servers[srvkey][steamid]

class PlayerStats:
        steamid = ""
        names = []
        ip = "unknown"
        kills = 0
        deaths = 0
        steamid = 0
        lastconnect = 0
        suicides = 0

        weapons = {}
	events = {}


        def __init__(self,steamid):
                self.steamid = steamid
                if self.steamid == "BOT":
                        self.steamid="STEAM_0:1:1199"

        def checkName(self,newname):
                found = 0
                for cur in self.names:
                        if newname.lower() == cur.lower():
                                found = 1
                if not found:
                        self.names.append(newname)


	def getWeapon(self,wpnname):
		if not self.weapons.has_key(wpnname):
			self.weapons[wpnname] = WeaponStats(wpnname)

		return self.weapons[wpnname]

	def getEvent(self,eventname):
		if not self.events.has_key(eventname):
			self.events[eventname] = EventStats(eventname)

		return self.events[eventname]

        def savePlayer(self,server_ip,server_port):
                later = write_pool.runInteraction(self._writePlayerToDB,(server_ip,server_port))
                later.addErrback(self._DBError)

        def _writePlayerToDB(self,txn,(server_ip,server_port)):
		txn.execute("""INSERT INTO servers(server_ip,server_port) VALUES(%s,%s)
				ON DUPLICATE KEY UPDATE server_ip=server_ip""",(server_ip,server_port))

                txn.execute("""SELECT server_id FROM servers WHERE server_ip=%s AND server_port=%s""",(server_ip,server_port))
		server_id = txn.fetchone()[0]

		txn.execute("""INSERT INTO players(server_id,player_id,lastconnect,kills,deaths,suicides) VALUES(%s,SteamToInt(%s),%s,%s,%s,%s)
                                ON DUPLICATE KEY UPDATE lastconnect=%s, kills=kills+%s, deaths=deaths+%s, suicides=suicides+%s""",
                                (server_id,self.steamid,self.lastconnect,self.kills,self.deaths,self.suicides,self.lastconnect,self.kills,self.deaths,self.suicides))
                self.kills=0
                self.deaths=0
                self.suicides=0

		# Save any event info we have
		for cur in self.events.keys():
			self.events[cur].saveEvent(self,server_id)

                # Now save any weapons we have
                for cur in self.weapons.keys():
                        self.weapons[cur].saveWeapon(self,server_id)

        def _DBError(self,error):
                main_log.error(str(error))

class WeaponStats:
        name = "unknown"
        kills = 0
        headshots = 0
        damage = 0
        tks = 0

        def __init__(self,weapon):
                self.name = weapon

        def saveWeapon(self,player,server_id):
                later = write_pool.runInteraction(self._writeWeaponToDB,player,server_id)
                later.addErrback(self._DBError)

        def _writeWeaponToDB(self,txn,player,server_id):
                txn.execute("""INSERT INTO player_weapons(server_id,player_id,weapon_name,kills,headshots,damage,tks) VALUES(%s,SteamToInt(%s),%s,%s,%s,%s,%s)
                                ON DUPLICATE KEY UPDATE kills=kills+%s, headshots=headshots+%s, damage=damage+%s, tks=tks+%s""",
                                (server_id,player.steamid,self.name,self.kills,self.headshots,self.damage,self.tks,self.kills,self.headshots,self.damage,self.tks))
                self.kills=0
                self.damage=0
                self.tks=0
                self.headshots=0

        def _DBError(self,error):
                main_log.error(str(error))


class EventStats:
	name = "unknown"
	trigger_count = 0
	last_trigger = 0

	def __init__(self,event):
		self.name = event

	def trigger(self):
		self.trigger_count += 1
		self.last_trigger = time.time()

	def saveEvent(self,player,server_id):
		later = write_pool.runINteraction(self._writeEventToDB,player,server_id)
		later.addErrback(self._DBError)

	def _writeEventToDB(self,txn,player,server_id):
		txn.execute("""INSERT INTO player_events(server_id,player_id,event_name,triggercount) VALUES(%s,SteamToInt(%s),%s,%s)
				ON DUPLICATE KEY triggercount=triggercount+%s"""
				,(server_id,player.steamid,self.name,self.trigger_count))
		self.trigger_count = 0
