__title__ = 'RockBaseFinder'
__author__ = 'Jakkee'
__version__ = '1.0'
 
import clr
clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import UnityEngine
import Fougerite

 
class RockBaseFinder:
    def On_EntityDeployed(self, Player, Entity):
        if Player.Admin:
            origin = Util.CreateVector(Entity.X, Entity.Y + 1, Entity.Z)
            direction = Util.CreateVector(float(0), float(1), float(0))
            hit = UnityEngine.Physics.Raycast(origin, direction)
            if hit:
                Player.Message(str(hit))
                #Player.Message("Hit")
            else:
                Player.Message("Nothing above")

    def On_Command(self, Player, cmd, args):
        if cmd == "down":
            if Player.Admin:
                #DiSt = int(DataStore.Get("RockBaseFinder", "Distance"))
                Player.TeleportTo(Player.X, Player.Y - 2, Player.Z)
                Player.Message("Teleported 2m below!")
            else:
                Player.Message("You are not allowed to use that command!")
"""    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "Distance", "2")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        DataStore.Add("RockBaseFinder", "Distance", ini.GetSetting("Config", "Distance"))"""
