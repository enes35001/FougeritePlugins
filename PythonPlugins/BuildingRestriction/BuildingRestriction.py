__title__ = 'BuildingRestriction'
__author__ = 'Jakkee'
__version__ = '1.0.1'

import clr
clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import UnityEngine
import Fougerite


class BuildingRestriction:
    def On_PluginInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "Max Height", "5")
            ini.AddSetting("Config", "Max Foundations", "9")
            ini.AddSetting("Config", "Moderators bypass limits?", "false")
            ini.AddSetting("Config", "Admins bypass limits?", "false")
            ini.Save()
        DataStore.Flush("BuildingRestriction")
        ini = Plugin.GetIni("Settings")
        DataStore.Add("BuildingRestriction", "Max Height", int(ini.GetSetting("Config", "Max Height")) * 4)
        DataStore.Add("BuildingRestriction", "Max Foundations", int(ini.GetSetting("Config", "Max Foundations")))
        DataStore.Add("BuildingRestriction", "ModBypass", ini.GetSetting("Config", "Moderators bypass limits?"))
        DataStore.Add("BuildingRestriction", "AdminBypass", ini.GetSetting("Config", "Admins bypass limits?"))

    def isMod(self, id):
        try:
            if DataStore.ContainsKey("Moderators", id):
                if DataStore.Get("BuildingRestriction", "ModBypass") == "true":
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def isAdmin(self, p):
        try:
            if p.Admin:
                if DataStore.Get("BuildingRestriction", "AdminBypass") == "true":
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def On_EntityDeployed(self, Player, Entity):
        if Entity.Name == "WoodPillar" or "MetalPillar":
            """if self.isAdmin(Player):
                return
            elif self.isMod(Player.SteamID):
                return
            else:"""
            height = round(int(DataStore.Get("BuildingRestriction", "Max Height")), 0)
            for pillar in Entity.GetLinkedStructs():
                if pillar.Name != "WoodPillar" or "MetalPillar":
                    continue
                if height < Entity.Y - pillar.Y:
                    Server.Broadcast("Callback")
                    try:
                        Player.Inventory.AddItem(Entity.Name, 1)
                        Player.InventoryNotice("1 x " + Entity.Name)
                        Entity.Destroy()
                        Player.Message("Max build height reached for this base [ " + str(DataStore.Get("BuildingRestriction", "Max Height") / 4) + " units tall ]")
                    except:
                        pass
                    break
        elif Entity.Name == "WoodFoundation" or "MetalFoundation":
            """if self.isAdmin(Player):
                return
            elif self.isMod(Player.SteamID):
                return
            else:"""
            count = 0
            total = int(DataStore.Get("BuildingRestriction", "Max Foundations"))
            for foundation in Entity.GetLinkedStructs():
                if foundation.Name != "WoodFoundation" or "MetalFoundation":
                    continue
                count += 1
                if count == total:
                    Server.Broadcast("Callback")
                    try:
                        Player.Inventory.AddItem(Entity.Name, 1)
                        Player.InventoryNotice("1 x " + Entity.Name)
                        Entity.Destroy()
                        Player.Message("Max foundations reached for this base [ " + str(DataStore.Get("BuildingRestriction", "Max Foundations")) + " Foundations ]")
                    except:
                        pass
                    break
