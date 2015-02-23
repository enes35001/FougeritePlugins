__title__ = 'XHTServer'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class XHTServer:
    def On_ServerInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "MaxPlayers", "500")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        Util.SetStaticField("server", "maxplayers", int(ini.GetSetting("Config", "MaxPlayers")))

    def On_PlayerConnected(self, Player):
        Player.SendCommand("deathscreen.reason " + '"' + "              WELCOME TO XHTs DEV SERVER!                         We test plugins on here first!                                    Developed by Jakkee. (Also you have not died)" + '"')
        Player.SendCommand("deathscreen.show")

    def On_Command(self, Player, cmd, args):
        if cmd == "spawn":
            if len(args) == 0:
                if Player.Admin:
                    try:
                        #World.Spawn(":player_soldier", Player.X, Player.Y - 1.6, Player.Z)
                        #World.Spawn("C130", Player.X, Player.Y + 100, Player.Z)
                        World.Spawn("OilTankRusty2", Player.X, Player.Y + 6, Player.Z)
                    except:
                        Player.Message("failed to spawn")
#http://forum.rustoxide.com/threads/placing-foundation-crates-npc-in-game-world.745/page-2
#http://webcache.googleusercontent.com/search?q=cache:7cDKWx7K-qQJ:gomagma.org/community/index.php%3Fthreads/spawning-objects-npcs.57/page-3+&cd=1&hl=en&ct=clnk&gl=au

