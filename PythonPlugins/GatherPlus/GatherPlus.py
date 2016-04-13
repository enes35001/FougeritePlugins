__title__ = 'GatherPlus'
__author__ = 'Jakkee'
__version__ = '4.2.3'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

PluginSettings = {}


class GatherPlus:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("GatherRate", "Wood", "2")
            ini.AddSetting("GatherRate", "Sulfur Ore", "2")
            ini.AddSetting("GatherRate", "Metal Ore", "2")
            ini.AddSetting("GatherRate", "Stones", "2")
            ini.AddSetting("GatherRate", "Leather", "2")
            ini.AddSetting("GatherRate", "Cloth", "2")
            ini.AddSetting("GatherRate", "RawChickenBreast", "2")
            ini.AddSetting("GatherRate", "AnimalFat", "2")
            ini.AddSetting("GatherRate", "Blood", "2")
            ini.AddSetting("TotalResources", "MutantBear", "5")
            ini.AddSetting("TotalResources", "MutantWolf", "3")
            ini.AddSetting("TotalResources", "Bear", "5")
            ini.AddSetting("TotalResources", "Wolf", "3")
            ini.AddSetting("TotalResources", "Chicken", "2")
            ini.AddSetting("TotalResources", "Rabbit", "2")
            ini.AddSetting("TotalResources", "Boar", "4")
            ini.AddSetting("TotalResources", "Stag", "5")
            ini.AddSetting("TotalResources", "WoodPile", "100")
            ini.AddSetting("TotalResources", "SulfurOre", "100")
            ini.AddSetting("TotalResources", "MetalOre", "100")
            ini.AddSetting("TotalResources", "StoneOre", "100")
            ini.Save()
        PluginSettings.clear()
        ini = Plugin.GetIni("Settings")
        for key in ini.EnumSection("GatherRate"):
            number = self.check(ini.GetSetting("GatherRate", key))
            if number is not None:
                PluginSettings[key] = number
                continue
            else:
                Util.Log("GatherPlus: ERROR setting GatherRate for: " + key + ". Setting is not a number!")
                continue
        for key in ini.EnumSection("TotalResources"):
            number = self.check(ini.GetSetting("TotalResources", key))
            if number is not None:
                PluginSettings[key] = number
                continue
            else:
                Util.Log("GatherPlus: ERROR setting TotalResource for: " + key + ". Setting is not a number!")
                continue

    def check(self, no):
        try:
            no = int(no)
            no += 1
            no -= 1
            return no
        except:
            return None

    def On_Command(self, Player, cmd, args):
        if cmd == "woodrate":
            if Player.Admin:
                if len(args) == 1:
                    name = self.check(args[0])
                    if name is not None:
                        ini = Plugin.GetIni("Settings")
                        ini.AddSetting("Config", "Wood", str(name))
                        ini.Save()
                        PluginSettings["Wood"] = int(name)
                        Player.Message(str(name) + " is the new gather rate for Wood!")
                    else:
                        Player.Message("usage: /woodrate [Number]")
                else:
                    Player.Message("usage: /woodrate [Number]")
            else:
                Player.MessageFrom("GatherPlus", "You're not allowed to use this command!")
        elif cmd == "sulfurrate":
            if Player.Admin:
                if len(args) == 1:
                    name = self.check(args[0])
                    if name is not None:
                        ini = Plugin.GetIni("Settings")
                        ini.AddSetting("Config", "Sulfur Ore", str(name))
                        ini.Save()
                        PluginSettings["Sulfur"] = int(name)
                        Player.Message(str(name) + " is the new gather rate for Sulfur Ore!")
                    else:
                        Player.Message("usage: /sulfurrate [Number]")
                else:
                    Player.Message("usage: /sulfurrate [Number]")
            else:
                Player.MessageFrom("GatherPlus", "You're not allowed to use this command!")
        elif cmd == "metalrate":
            if Player.Admin:
                if len(args) == 1:
                    name = self.check(args[0])
                    if name is not None:
                        ini = Plugin.GetIni("Settings")
                        ini.AddSetting("Config", "Metal Ore", str(name))
                        ini.Save()
                        PluginSettings["Metal Ore"] = int(name)
                        Player.Message(str(name) + " is the new gather rate for Metal Ore!")
                    else:
                        Player.Message("usage: /metalrate [Number]")
                else:
                    Player.Message("usage: /metalrate [Number]")
            else:
                Player.MessageFrom("GatherPlus", "You're not allowed to use this command!")
        elif cmd == "stonesrate":
            if Player.Admin:
                if len(args) == 1:
                    name = self.check(args[0])
                    if name is not None:
                        ini = Plugin.GetIni("Settings")
                        ini.AddSetting("Config", "Stones", str(name))
                        ini.Save()
                        PluginSettings["Stones"] = int(name)
                        Player.Message(str(name) + " is the new gather rate for Stones!")
                    else:
                        Player.Message("usage: /stonesrate [Number]")
                else:
                    Player.Message("usage: /stonesrate [Number]")
            else:
                Player.MessageFrom("GatherPlus", "You're not allowed to use this command!")
        elif cmd == "leatherrate":
            if Player.Admin:
                if len(args) == 1:
                    name = self.check(args[0])
                    if name is not None:
                        ini = Plugin.GetIni("Settings")
                        ini.AddSetting("Config", "Leather", str(name))
                        ini.Save()
                        PluginSettings["Leather"] = int(name)
                        Player.Message(str(name) + " is the new gather rate for Leather!")
                    else:
                        Player.Message("usage: /leatherrate [Number]")
                else:
                    Player.Message("usage: /leatherrate [Number]")
            else:
                Player.MessageFrom("GatherPlus", "You're not allowed to use this command!")
        elif cmd == "clothrate":
            if Player.Admin:
                if len(args) == 1:
                    name = self.check(args[0])
                    if name is not None:
                        ini = Plugin.GetIni("Settings")
                        ini.AddSetting("Config", "Cloth", str(name))
                        ini.Save()
                        PluginSettings["Cloth"] = int(name)
                        Player.Message(str(name) + " is the new gather rate for Cloth!")
                    else:
                        Player.Message("usage: /clothrate [Number]")
                else:
                    Player.Message("usage: /clothrate [Number]")
            else:
                Player.MessageFrom("GatherPlus", "You're not allowed to use this command!")
        elif cmd == "chickenrate":
            if Player.Admin:
                if len(args) == 1:
                    name = self.check(args[0])
                    if name is not None:
                        ini = Plugin.GetIni("Settings")
                        ini.AddSetting("Config", "RawChickenBreast", str(name))
                        ini.Save()
                        PluginSettings["RawChickenBreast"] = int(name)
                        Player.Message(str(name) + " is the new gather rate for Raw Chicken Breast!")
                    else:
                        Player.Message("usage: /chickenrate [Number]")
                else:
                    Player.Message("usage: /chickenrate [Number]")
            else:
                Player.MessageFrom("GatherPlus", "You're not allowed to use this command!")
        elif cmd == "fatrate":
            if Player.Admin:
                if len(args) == 1:
                    name = self.check(args[0])
                    if name is not None:
                        ini = Plugin.GetIni("Settings")
                        ini.AddSetting("Config", "AnimalFat", str(name))
                        ini.Save()
                        PluginSettings["AnimalFat"] = int(name)
                        Player.Message(str(name) + " is the new gather rate for Animal Fat!")
                    else:
                        Player.Message("usage: /fatrate [Number]")
                else:
                    Player.Message("usage: /fatrate [Number]")
            else:
                Player.MessageFrom("GatherPlus", "You're not allowed to use this command!")
        elif cmd == "bloodrate":
            if Player.Admin:
                if len(args) == 1:
                    name = self.check(args[0])
                    if name is not None:
                        ini = Plugin.GetIni("Settings")
                        ini.AddSetting("Config", "Blood", str(name))
                        ini.Save()
                        PluginSettings["Blood"] = int(name)
                        Player.Message(str(name) + " is the new gather rate for Blood Bags!")
                    else:
                        Player.Message("usage: /bloodrate [Number]")
                else:
                    Player.Message("usage: /bloodrate [Number]")
            else:
                Player.MessageFrom("GatherPlus", "You're not allowed to use this command!")
        elif cmd == "gatherhelp":
            if Player.Admin:
                Player.Message("/woodrate [Number]")
                Player.Message("/sulfurrate [Number]")
                Player.Message("/metalrate [Number]")
                Player.Message("/stonesrate [Number]")
                Player.Message("/leatherrate [Number]")
                Player.Message("/clothrate [Number]")
                Player.Message("/chickenrate [Number]")
                Player.Message("/bloodrate [Number]")
                Player.Message("/fatrate [Number]")
            else:
                Player.MessageFrom("GatherPlus", "You're not allowed to use this command!")

    def ResourceSpawn(self, ResourceTarget):
        #Plugin.Log("startingTotals", str(ResourceTarget) + " = " + str(ResourceTarget.startingTotal))
        try:
            if str(ResourceTarget) == "MutantBear(Clone) (ResourceTarget)":
                ResourceTarget.startingTotal = PluginSettings["MutantBear"]
            elif str(ResourceTarget) == "MutantWolf(Clone) (ResourceTarget)":
                ResourceTarget.startingTotal = PluginSettings["MutantWolf"]
            elif str(ResourceTarget) == "Chicken_A(Clone) (ResourceTarget)":
                ResourceTarget.startingTotal = PluginSettings["Chicken"]
            elif str(ResourceTarget) == "Rabbit_A(Clone) (ResourceTarget)":
                ResourceTarget.startingTotal = PluginSettings["Rabbit"]
            elif str(ResourceTarget) == "Boar_A(Clone) (ResourceTarget)":
                ResourceTarget.startingTotal = PluginSettings["Boar"]
            elif str(ResourceTarget) == "Stag_A(Clone) (ResourceTarget)":
                ResourceTarget.startingTotal = PluginSettings["Stag"]
            elif str(ResourceTarget) == "Wolf(Clone) (ResourceTarget)":
                ResourceTarget.startingTotal = PluginSettings["Wolf"]
            elif str(ResourceTarget) == "Bear(Clone) (ResourceTarget)":
                ResourceTarget.startingTotal = PluginSettings["Bear"]
            elif str(ResourceTarget) == "WoodPile(Clone) (ResourceTarget)":
                ResourceTarget.startingTotal = PluginSettings["WoodPile"]
            elif str(ResourceTarget) == "Ore1(Clone) (ResourceTarget)":
                ResourceTarget.startingTotal = PluginSettings["SulfurOre"]
            elif str(ResourceTarget) == "Ore2(Clone) (ResourceTarget)":
                ResourceTarget.startingTotal = PluginSettings["MetalOre"]
            elif str(ResourceTarget) == "Ore3(Clone) (ResourceTarget)":
                ResourceTarget.startingTotal = PluginSettings["StoneOre"]
            else:
                Util.Log("GatherPlus: Unknown ResourceTarget [" + str(ResourceTarget) + "]")
                Util.Log("GatherPlus: Ignore this message if you have spawned in " + str(ResourceTarget) + " yourself!")
        except Exception, e:
            Plugin.Log("ErrorLog", str(e))

    def On_PlayerGathering(self, Player, GatherEvent):
        if GatherEvent.Item == "Wood":
            if Player.Inventory.FreeSlots > 0:
                rate = PluginSettings["Wood"]
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Sulfur Ore":
            if Player.Inventory.FreeSlots > 0:
                rate = PluginSettings["Sulfur Ore"]
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Metal Ore":
            if Player.Inventory.FreeSlots > 0:
                rate = PluginSettings["Metal Ore"]
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Stones":
            if Player.Inventory.FreeSlots > 0:
                rate = PluginSettings["Stones"]
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Leather":
            if Player.Inventory.FreeSlots > 0:
                rate = PluginSettings["Leather"]
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Cloth":
            if Player.Inventory.FreeSlots > 0:
                rate = PluginSettings["Cloth"]
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Raw Chicken Breast":
            if Player.Inventory.FreeSlots > 0:
                rate = PluginSettings["RawChickenBreast"]
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Animal Fat":
            if Player.Inventory.FreeSlots > 0:
                rate = PluginSettings["AnimalFat"]
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Blood":
            if Player.Inventory.FreeSlots > 0:
                rate = PluginSettings["Blood"]
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
