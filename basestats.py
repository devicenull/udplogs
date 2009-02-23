from twisted.enterprise import adbapi

player_stats = {}

read_pool = adbapi.ConnectionPool("MySQLdb",db="playerstats",user="playerstats")
write_pool = read_pool

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

        def savePlayer(self):
                later = write_pool.runInteraction(self._writePlayerToDB)
                later.addErrback(self._DBError)

        def _writePlayerToDB(self,txn):
                txn.execute("""INSERT INTO players(player_id,lastconnect,kills,deaths,suicides) VALUES(SteamToInt(%s),%s,%s,%s,%s)
                                ON DUPLICATE KEY UPDATE lastconnect=%s, kills=kills+%s, deaths=deaths+%s, suicides=suicides+%s""",
                                (self.steamid,self.lastconnect,self.kills,self.deaths,self.suicides,self.lastconnect,self.kills,self.deaths,self.suicides))
                self.kills=0
                self.deaths=0
                self.suicides=0

		# Save any event info we have
		for cur in self.events.keys():
			txn.execute("""INSERT INTO players_events(player_id,event_id,triggercount) VALUES(SteamToInt(%s),%s,%s)
					ON DUPLICATE KEY UPDATE triggercount=triggercount+%s"""
					,(self.steamid,cur,self.events[cur],self.events[cur]))
			self.events[cur] = 0


                # Now save any weapons we have
                for cur in self.weapons.keys():
                        self.weapons[cur].saveWeapon(self)

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

        def saveWeapon(self,player):
                later = write_pool.runInteraction(self._writeWeaponToDB,player)
                later.addErrback(self._DBError)

        def _writeWeaponToDB(self,txn,player):
                txn.execute("""INSERT INTO player_weapons(player_id,weapon_name,kills,headshots,damage,tks) VALUES(SteamToInt(%s),%s,%s,%s,%s,%s)
                                ON DUPLICATE KEY UPDATE kills=kills+%s, headshots=headshots+%s, damage=damage+%s, tks=tks+%s""",
                                (player.steamid,self.name,self.kills,self.headshots,self.damage,self.tks,self.kills,self.headshots,self.damage,self.tks))
                self.kills=0
                self.damage=0
                self.tks=0
                self.headshots=0

        def _DBError(self,error):
                main_log.error(str(error))

