__title__ = 'WastelandRestrictor'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class WastelandRestrictor:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "DisplayMessage", "true")
            ini.Save()
        DataStore.Flush("WasteLand")
        ini = Plugin.GetIni("Settings")
        DataStore.Add("WasteLand", "Message", ini.GetSetting("Settings", "DisplayMessage"))

    def On_EntityDeployed(self, Player, Entity):
        if Entity.X < 3000 or Entity.Z > 1300:
            Entity.Destroy()
            if DataStore.Get("WasteLand", "Message") == "true":
                Player.Message("You can not build this far out!")