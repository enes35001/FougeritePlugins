__title__ = 'SystemName'
__author__ = 'Jakkee'
__version__ = '2.1.5'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class SystemName:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("SystemName", "Servername", "Fougerite")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        Server.server_message_name = ini.GetSetting("SystemName", "Servername")

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def On_Command(self, Player, cmd, args):
        if cmd == "servername":
            if Player.Admin:
                if len(args) == 0:
                    Player.MessageFrom("SystemName", "Usage: /servername [Servername]")
                elif len(args) > 0:
                    name = self.argsToText(args)
                    ini = Plugin.GetIni("Settings")
                    ini.DeleteSetting("SystemName", "Servername")
                    ini.AddSetting("SystemName", "Servername", name)
                    ini.Save()
                    Server.server_message_name = name
                    Player.MessageFrom(name, " is the new system name!")
            else:
                Player.Message("You are not allowed to use that command")
