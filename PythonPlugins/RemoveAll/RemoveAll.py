__title__ = 'RemoveAll'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class RemoveAll:
    def On_Command(self, Player, cmd, args):
        if cmd == "remove":
            if Player.Admin:
                if len(args) == 0:
                    if DataStore.Get(Player.SteamID, "RemoveAll") == "true":
                        DataStore.Remove(Player.SteamID, "RemoveAll")
                        Player.Notice("RemoveAll is deactivated!")
                    else:
                        DataStore.Add(Player.SteamID, "RemoveAll", "true")
                        Player.Notice("RemoveAll is activated!")
                else:
                    Player.Message("usage: /remove")
            else:
                Player.message("You are not allowed to use that command!")

    def On_EntityHurt(self, Player, HurtEvent):
        if DataStore.Get(Player.SteamID, "RemoveAll") == "true":
            for x in HurtEvent.Entity.GetLinkedStructs():
                x.Destroy()
                #HurtEvent.Entity.Destroy()
            Player.Message("Structure removed!")



