__title__ = 'NpcLoot'
__author__ = 'Jakkee'
__version__ = '1.0.4'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class NpcLoot:
    def On_NPCKilled(self, DamageEvent):
        if DamageEvent.Victim.Name == "Wolf":
            if DataStore.Get("NpcLoot", "Wolf") == "true":
                World.Spawn(";drop_lootsack_zombie", DamageEvent.Victim.X - 1.5, World.GetGround(DamageEvent.Victim.X - 1.5, DamageEvent.Victim.Z), DamageEvent.Victim.Z)
            else:
                return
        elif DamageEvent.Victim.Name == "Bear":
            if DataStore.Get("NpcLoot", "Bear") == "true":
                World.Spawn(";drop_lootsack_zombie", DamageEvent.Victim.X - 1.5, World.GetGround(DamageEvent.Victim.X - 1.5, DamageEvent.Victim.Z), DamageEvent.Victim.Z)
            else:
                return
        elif DamageEvent.Victim.Name == "Stag_A":
            if DataStore.Get("NpcLoot", "Stag") == "true":
                World.Spawn(";drop_lootsack_zombie", DamageEvent.Victim.X - 1, World.GetGround(DamageEvent.Victim.X - 1, DamageEvent.Victim.Z), DamageEvent.Victim.Z)
            else:
                return
        elif DamageEvent.Victim.Name == "Boar_A":
            if DataStore.Get("NpcLoot", "Boar") == "true":
                World.Spawn(";drop_lootsack_zombie", DamageEvent.Victim.X - 1, World.GetGround(DamageEvent.Victim.X - 1, DamageEvent.Victim.Z), DamageEvent.Victim.Z)
            else:
                return
        elif DamageEvent.Victim.Name == "Chicken_A":
            if DataStore.Get("NpcLoot", "Chicken") == "true":
                World.Spawn(";drop_lootsack_zombie", DamageEvent.Victim.X - 0.8, World.GetGround(DamageEvent.Victim.X - 0.8, DamageEvent.Victim.Z), DamageEvent.Victim.Z)
            else:
                return
        elif DamageEvent.Victim.Name == "Rabbit_A":
            if DataStore.Get("NpcLoot", "Rabbit") == "true":
                World.Spawn(";drop_lootsack_zombie", DamageEvent.Victim.X - 0.8, World.GetGround(DamageEvent.Victim.X - 0.8, DamageEvent.Victim.Z), DamageEvent.Victim.Z)
            else:
                return
        else:
            return

    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("DropsLoot", "Bear", "true")
            ini.AddSetting("DropsLoot", "Wolf", "true")
            ini.AddSetting("DropsLoot", "Chicken", "false")
            ini.AddSetting("DropsLoot", "Rabbit", "false")
            ini.AddSetting("DropsLoot", "Stag(Deer)", "false")
            ini.AddSetting("DropsLoot", "Boar(Pig)", "false")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        DataStore.Flush("NpcLoot")
        DataStore.Add("NpcLoot", "Bear", ini.GetSetting("DropsLoot", "Bear"))
        DataStore.Add("NpcLoot", "Wolf", ini.GetSetting("DropsLoot", "Wolf"))
        DataStore.Add("NpcLoot", "Chicken", ini.GetSetting("DropsLoot", "Chicken"))
        DataStore.Add("NpcLoot", "Rabbit", ini.GetSetting("DropsLoot", "Rabbit"))
        DataStore.Add("NpcLoot", "Stag", ini.GetSetting("DropsLoot", "Stag(Deer)"))
        DataStore.Add("NpcLoot", "Boar", ini.GetSetting("DropsLoot", "Boar(Pig)"))
