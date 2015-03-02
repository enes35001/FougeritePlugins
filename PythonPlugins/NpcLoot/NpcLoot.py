__title__ = 'NpcLoot'
__author__ = 'Jakkee'
__version__ = '1.0.3'

import clr
clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("System")
import System
import Fougerite
import re


class NpcLoot:

    version = None

    def On_NPCKilled(self, DamageEvent):
        if self.version < 108:
            #Old Version
            if DamageEvent.Victim.Name == "Stag_A":
                if DataStore.Get("NpcLoot", "Stag") == "true":
                    coords = str(DamageEvent.Victim.Character.transform.position).replace(',', ':')
                    coords = self.Stringify(coords)
                    coords = self.Parse(str(coords))
                    coords = self.ReplaceToDot(coords[0])
                    World.Spawn(";drop_lootsack_zombie", float(coords[0]) - 1, World.GetGround(float(coords[0]) - 1, float(coords[2])), float(coords[2]))
                else:
                    return
            elif DamageEvent.Victim.Name == "Bear":
                if DataStore.Get("NpcLoot", "Bear") == "true":
                    coords = str(DamageEvent.Victim.Character.transform.position).replace(',', ':')
                    coords = self.Stringify(coords)
                    coords = self.Parse(str(coords))
                    coords = self.ReplaceToDot(coords[0])
                    World.Spawn(";drop_lootsack_zombie", float(coords[0]) - 1.5, World.GetGround(float(coords[0]) - 1, float(coords[2])), float(coords[2]))
                else:
                    return
            elif DamageEvent.Victim.Name == "Boar_A":
                if DataStore.Get("NpcLoot", "Boar") == "true":
                    coords = str(DamageEvent.Victim.Character.transform.position).replace(',', ':')
                    coords = self.Stringify(coords)
                    coords = self.Parse(str(coords))
                    coords = self.ReplaceToDot(coords[0])
                    World.Spawn(";drop_lootsack_zombie", float(coords[0]) - 1, World.GetGround(float(coords[0]) - 1, float(coords[2])), float(coords[2]))
                else:
                    return
            elif DamageEvent.Victim.Name == "Wolf":
                if DataStore.Get("NpcLoot", "Wolf") == "true":
                    coords = str(DamageEvent.Victim.Character.transform.position).replace(',', ':')
                    coords = self.Stringify(coords)
                    coords = self.Parse(str(coords))
                    coords = self.ReplaceToDot(coords[0])
                    World.Spawn(";drop_lootsack_zombie", float(coords[0]) - 1.5, World.GetGround(float(coords[0]) - 1, float(coords[2])), float(coords[2]))
                else:
                    return
            elif DamageEvent.Victim.Name == "Chicken_A":
                if DataStore.Get("NpcLoot", "Chicken") == "true":
                    coords = str(DamageEvent.Victim.Character.transform.position).replace(',', ':')
                    coords = self.Stringify(coords)
                    coords = self.Parse(str(coords))
                    coords = self.ReplaceToDot(coords[0])
                    World.Spawn(";drop_lootsack_zombie", float(coords[0]) - 0.8, World.GetGround(float(coords[0]) - 1, float(coords[2])), float(coords[2]))
                else:
                    return
            elif DamageEvent.Victim.Name == "Rabbit_A":
                if DataStore.Get("NpcLoot", "Rabbit") == "true":
                    coords = str(DamageEvent.Victim.Character.transform.position).replace(',', ':')
                    coords = self.Stringify(coords)
                    coords = self.Parse(str(coords))
                    coords = self.ReplaceToDot(coords[0])
                    World.Spawn(";drop_lootsack_zombie", float(coords[0]) - 0.8, World.GetGround(float(coords[0]) - 1, float(coords[2])), float(coords[2]))
                else:
                    return
            else:
                return
        else:
            #New version
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
        #Removes everything apart from numbers
        v = re.sub("[^0-9]", "", Fougerite.Bootstrap.Version)
        try:    
            self.version = int(v)
        except:
            self.version = int("100")

#these below are 100% not stolen from DreTaX... Or are they?
    def Stringify(self, loc):
        s = re.sub("[[\]\'\ ]", '', str(loc))
        return str(s)

    def Parse(self, String):
        return String.split(',')

    def ReplaceToDot(self, String):
        str = re.sub('[(\)]', '', String)
        return str.split(':')
