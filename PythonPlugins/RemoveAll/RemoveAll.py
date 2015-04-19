__title__ = 'RemoveAll'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class RemoveAll:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        DataStore.Flush("Removeall")

    def On_Command(self, Player, cmd, args):
        if cmd == "removeall":
            if Player.Admin or self.isMod(Player.SteamID):
                if len(args) == 0:
                    if DataStore.Get("Removeall", Player.SteamID) is not None:
                        DataStore.Remove("Removeall", Player.SteamID)
                        Player.Notice("RemoveAll is deactivated!")
                    else:
                        DataStore.Add("Removeall", Player.SteamID, "Standard")
                        Player.Notice("RemoveAll is activated!")
                elif len(args) == 1:
                    if args[0] == "refund":
                        if DataStore.Get("Removeall", Player.SteamID) == "Standard":
                            DataStore.Remove("Removeall", Player.SteamID)
                            DataStore.Add("Removeall", Player.SteamID, "Refund")
                            Player.Notice("RemoveAll changed to Refund mode")
                        elif DataStore.Get("Removeall", Player.SteamID) == "Refund":
                            DataStore.Remove("Removeall", Player.SteamID)
                            Player.Notice("RemoveAll is deactivated!")
                        else:
                            DataStore.Add("Removeall", Player.SteamID, "Refund")
                            Player.Notice("RemoveAll is activated!")
                    else:
                        Player.Message("usage: /removeall")
                else:
                    Player.Message("usage: /removeall")
            else:
                Player.message("You are not allowed to use that command!")

    def On_EntityHurt(self, HurtEvent):
        try:
            type = DataStore.Get("Removeall", HurtEvent.Attacker.SteamID)
            if type is not None:
                if type == "Standard":
                    for x in HurtEvent.Entity.GetLinkedStructs():
                        x.Destroy()
                if type == "Refund":
                    for x in HurtEvent.Entity.GetLinkedStructs():
                        x.Destroy()
                        HurtEvent.Attacker.Inventory.AddItem(x.Name)
                HurtEvent.Attacker.Message("Structure removed!")
        except e:
            HurtEvent.Attacker.Message("FAILED: Check console for errors")
            Util.Log("---------------------------------")
            Util.Log("Removeall Error")
            Util.Log(e)
            Util.Log("---------------------------------")

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        else:
            return False



