__title__ = 'TestPlugin'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import UnityEngine
import Fougerite
import System


class TestPlugin:
    def On_PluginInit(self):
        Server.Broadcast("Plugins reloaded!")

    def On_Command(self, Player, cmd, args):
        if cmd == "c":
            if Player.Admin:
                System.BanList.Add(Player.SteamID, Player.Name, "Test")
                Player.Message("Added SteamID: " + Player.SteamID + " to the bans list!")
            else:
                Player.Message("You are not allowed to use that command!")
        elif cmd == "log":
            if Player.Admin:
                array = UnityEngine.Resources.FindObjectsOfTypeAll(UnityEngine.GameObject)
                count = 0
                Player.Message("Logging...")
                for ent in array:
                    Plugin.Log("ListOfEntitys", str(ent.name))
                    count += 1
                Player.Message("Found: " + str(count) + " entitys!")
                
            
