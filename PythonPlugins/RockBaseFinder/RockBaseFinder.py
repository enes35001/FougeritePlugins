__title__ = 'RockBaseFinder'
__author__ = 'Jakkee'
__version__ = '1.0.1'

import clr
clr.AddReferenceByPartialName("UnityEngine")
clr.AddReferenceByPartialName("Fougerite")
import UnityEngine
import Fougerite

class RockBaseFinder:
    def On_Command(self, Player, cmd, args):
        if cmd == "down":
            if Player.Admin:
                DiSt = int(DataStore.Get("RockBaseFinder", "Distance"))
                YY = (Player.Y)
                NewY = (YY - DiSt)
                Player.TeleportTo(Player.X, NewY, Player.Z)
                Player.Message("Teleported " + (str(DiSt)) +"m below!")
            else:
                Player.Message("You are not allowed to use that command!")

    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "Distance", "2")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        DataStore.Add("RockBaseFinder", "Distance", ini.GetSetting("Config", "Distance"))
