__title__ = 'AntiSuicide'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class AntiSuicide:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not DataStore.ContainsKey("AntiSuicide", "Enabled"):
            DataStore.Add("AntiSuicide", "Enabled", False)

    def On_Command(self, Player, cmd, args):
        if cmd == "suicide":
            if Player.Admin or Player.Moderator:
                if len(args) == 1:
                    if args[0] == "on":
                        if DataStore.Get("AntiSuicide", "Enabled"):
                            Player.MessageFrom("AntiSuicide", "is already enabled!")
                        else:
                            DataStore.Add("AntiSuicide", "Enabled", True)
                            Player.MessageFrom("AntiSuicide", "is now enabled!")
                    elif args[0] == "off":
                        if DataStore.Get("AntiSuicide", "Enabled"):
                            DataStore.Add("AntiSuicide", "Enabled", False)
                            Player.MessageFrom("AntiSuicide", "is now disabled!")
                        else:
                            Player.MessageFrom("AntiSuicide", "is already disabled!")                         
                    else:
                        Player.MessageFrom("AntiSuicide", "Usage: /suicide <on/off>")
                else:
                    Player.MessageFrom("AntiSuicide", "Usage: /suicide <on/off>")
            else:
                Player.Message("You are not allowed to use that command!")

    def On_ClientConsole(self, Player, cmd, args):
        Server.Broadcast(Player.Name + " ran: " + cmd)
        if cmd == "suicide":
            if not Player.Admin:
                if not Player.Moderator:
                    if DataStore.Get("AntiSuicide", "Enabled"):
                        Player.MessageFrom("AntiSuicide", "Suicide is blocked!")
                        return False
            return True
