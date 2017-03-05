__title__ = 'BuildingRestriction'
__author__ = 'Jakkee'
__version__ = '1.0.3'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
PluginSettings = {}


class BuildingRestriction:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "Max WoodHeight", "5")
            ini.AddSetting("Config", "Max WoodFoundations", "9")
            ini.AddSetting("Config", "Max MetalHeight", "5")
            ini.AddSetting("Config", "Max MetalFoundations", "12")
            ini.AddSetting("Config", "Moderators bypass limits?", "false")
            ini.AddSetting("Config", "Admins bypass limits?", "false")
            ini.Save()
        PluginSettings.clear()
        ini = Plugin.GetIni("Settings")
        PluginSettings["Max WoodHeight"] = int(ini.GetSetting("Config", "Max WoodHeight")) * 4
        PluginSettings["Max WoodFoundations"] = int(ini.GetSetting("Config", "Max WoodFoundations"))
        PluginSettings["Max MetalHeight"] = int(ini.GetSetting("Config", "Max MetalHeight")) * 4
        PluginSettings["Max MetalFoundations"] = int(ini.GetSetting("Config", "Max MetalFoundations"))
        PluginSettings["ModBypass"] = ini.GetBoolSetting("Config", "Moderators bypass limits?")
        PluginSettings["AdminBypass"] = ini.GetBoolSetting("Config", "Admins bypass limits?")

    def isMod(self, ActualPlacer):
        try:
            if DataStore.ContainsKey("Moderators", ActualPlacer.SteamID) or ActualPlacer.Moderator:
                if PluginSettings["ModBypass"]:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def isAdmin(self, ActualPlacer):
        try:
            if ActualPlacer.Admin:
                if PluginSettings["AdminBypass"]:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def On_EntityDeployed(self, Player, Entity, ActualPlacer):
        if Entity.Name == "WoodPillar":
            if self.isAdmin(ActualPlacer):
                return
            elif self.isMod(ActualPlacer):
                return
            else:
                height = round(PluginSettings["Max WoodHeight"], 0)
                for ent in Entity.GetLinkedStructs():
                    if ent.Name == "WoodFoundation":
                        if height < Entity.Y - ent.Y:
                            try:
                                ActualPlacer.Inventory.AddItem("Wood Pillar", 1)
                                ActualPlacer.InventoryNotice("1 x " + Entity.Name)
                                Entity.Destroy()
                                ActualPlacer.Message("Max build height reached for this base [ " + str(PluginSettings["Max WoodHeight"] / 4) + " units tall ]")
                            except:
                                break
                            break
                        else:
                            continue
        elif Entity.Name == "MetalPillar":
            if self.isAdmin(ActualPlacer):
                return
            elif self.isMod(ActualPlacer):
                return
            else:
                height = round(PluginSettings["Max MetalHeight"], 0)
                for ent in Entity.GetLinkedStructs():
                    if ent.Name == "MetalFoundation":
                        if height < Entity.Y - ent.Y:
                            try:
                                ActualPlacer.Inventory.AddItem("Metal Pillar", 1)
                                ActualPlacer.InventoryNotice("1 x " + Entity.Name)
                                Entity.Destroy()
                                ActualPlacer.Message("Max build height reached for this base [ " + str(PluginSettings["Max MetalHeight"] / 4) + " units tall ]")
                            except:
                                break
                            break
                        else:
                            continue
        elif Entity.Name == "WoodFoundation":
            if self.isAdmin(ActualPlacer):
                return
            elif self.isMod(ActualPlacer):
                return
            else:
                count = 0
                total = PluginSettings["Max WoodFoundations"]
                for ent in Entity.GetLinkedStructs():
                    if ent.Name == "WoodFoundation":
                        count += 1
                        if count == total:
                            try:
                                ActualPlacer.Inventory.AddItem("Wood Foundation", 1)
                                ActualPlacer.InventoryNotice("1 x " + Entity.Name)
                                Entity.Destroy()
                                ActualPlacer.Message("Max foundations reached for this base [ " + str(PluginSettings["Max WoodFoundations"]) + " Foundations ]")
                            except:
                                break
                            break
                    else:
                        continue
        elif Entity.Name == "MetalFoundation":
            if self.isAdmin(ActualPlacer):
                return
            elif self.isMod(ActualPlacer):
                return
            else:
                count = 0
                total = PluginSettings["Max MetalFoundations"]
                for ent in Entity.GetLinkedStructs():
                    if ent.Name == "MetalFoundation":
                        count += 1
                        if count == total:
                            try:
                                ActualPlacer.Inventory.AddItem("Metal Foundation", 1)
                                ActualPlacer.InventoryNotice("1 x " + Entity.Name)
                                Entity.Destroy()
                                ActualPlacer.Message("Max foundations reached for this base [ " + str(PluginSettings["Max MetalFoundations"]) + " Foundations ]")
                            except:
                                break
                            break
                    else:
                        continue
