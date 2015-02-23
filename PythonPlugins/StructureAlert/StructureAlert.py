__title__ = 'StructureAlert'
__author__ = 'Jakkee'
__version__ = '1.0'
 
import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
 
 
class StructureAlert:
    def On_PluginInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "IgnoreDeployables", "true")
            ini.Save()
        DataStore.Flush("StructureAlert")
        ini = Plugin.GetIni("Settings")
        DataStore.Add("StructureAlert", "Ignore", ini.GetSetting("Settings", "IgnoreDeployables"))
 
    def On_Command(self, Player, cmd, args):
        if cmd == "alert":
            if len(args) == 0:
                if DataStore.Get("StructureAlert", Player.SteamID) == "true":
                    DataStore.Remove("StructureAlert", Player.SteamID)
                    Player.Message("You will no longer get alerts when your structures get damaged")
                else:
                    DataStore.Add("StructureAlert", Player.SteamID, "true")
                    Player.Message("You will now get an alert when someone damages your structure")
            else:
                Player.Message("usage: /alert")

    def On_EntityHurt(self, HurtEvent):
        try:
            if not HurtEvent.IsDecay:
                Server.Broadcast("Entity Name: [" + HurtEvent.Entity.Name + "]")
                Server.Broadcast("Weapon Name: [" + HurtEvent.WeaponName + "]")
                if HurtEvent.WeaponName == "Explosive Charge" or "F1 Grenade":
                    Creator = self.GetPlayerName(HurtEvent.Entity.Creator)
                    Attacker = self.GetPlayerName(HurtEvent.Attacker)
                    if HurtEvent.Entity.Name == "Barricade_Fence_Deployable" or "CampFire" or "WoodBox" or "Workbench" or "Furnace" or "LargeWoodSpikeWall" or "WoodSpikeWall":
                        if DataStore.Get("StructureAlert", "Ignore") == "true":
                            return
                        elif DataStore.Get("StructureAlert", Creator.SteamID) == "true":
                            Creator.Notice("Your base is under attack by: " + Attacker.Name + "!")
                        else:
                            return
                    elif DataStore.Get("StructureAlert", Creator.SteamID) == "true":
                        Creator.Notice("Your base is under attack by: " + Attacker.Name + "!")
                    else:
                        return
        except:
            pass

#DreTaX's Methods below
    def GetPlayerName(self, name):
        try:
            name = name.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

    def GetIt(self, Entity):
        try:
            if Entity.IsDeployableObject():
                return Entity.Object.ownerID
            if Entity.IsStructure():
                return Entity.Object._master.ownerID
        except:
            return None
