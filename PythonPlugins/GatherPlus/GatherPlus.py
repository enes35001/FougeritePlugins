__title__ = 'GatherPlus'
__author__ = 'Jakkee'
__version__ = '4.1.6'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class GatherPlus:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "Wood", "2")
            ini.AddSetting("Config", "Sulfur Ore", "2")
            ini.AddSetting("Config", "Metal Ore", "2")
            ini.AddSetting("Config", "Stones", "2")
            ini.AddSetting("Config", "Leather", "2")
            ini.AddSetting("Config", "Cloth", "2")
            ini.AddSetting("Config", "RawChickenBreast", "2")
            ini.AddSetting("Config", "AnimalFat", "2")
            ini.AddSetting("Config", "Blood", "2")
            ini.Save()
        DataStore.Flush("GatherRate")
        ini = Plugin.GetIni("Settings")
        DataStore.Add("GatherRate", "Wood", int(ini.GetSetting("Config", "Wood")))
        DataStore.Add("GatherRate", "Sulfur", int(ini.GetSetting("Config", "Sulfur Ore")))
        DataStore.Add("GatherRate", "Metal", int(ini.GetSetting("Config", "Metal Ore")))
        DataStore.Add("GatherRate", "Stones", int(ini.GetSetting("Config", "Stones")))
        DataStore.Add("GatherRate", "Leather", int(ini.GetSetting("Config", "Leather")))
        DataStore.Add("GatherRate", "Cloth", int(ini.GetSetting("Config", "Cloth")))
        DataStore.Add("GatherRate", "Chicken", int(ini.GetSetting("Config", "RawChickenBreast")))
        DataStore.Add("GatherRate", "Fat", int(ini.GetSetting("Config", "AnimalFat")))
        DataStore.Add("GatherRate", "Blood", int(ini.GetSetting("Config", "Blood")))

    def check(self, arg):
        try:
            i = int(arg)
            return i
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
                        DataStore.Remove("GatherRate", "Wood")
                        DataStore.Add("GatherRate", "Wood", int(ini.GetSetting("Config", "Wood")))
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
                        DataStore.Remove("GatherRate", "Sulfur")
                        DataStore.Add("GatherRate", "Sulfur", int(ini.GetSetting("Config", "Sulfur Ore")))
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
                        DataStore.Remove("GatherRate", "Metal")
                        DataStore.Add("GatherRate", "Metal", int(ini.GetSetting("Config", "Metal Ore")))
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
                        DataStore.Remove("GatherRate", "Stones")
                        DataStore.Add("GatherRate", "Stones", int(ini.GetSetting("Config", "Stones")))
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
                        DataStore.Remove("GatherRate", "Leather")
                        DataStore.Add("GatherRate", "Leather", int(ini.GetSetting("Config", "Leather")))
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
                        DataStore.Remove("GatherRate", "Cloth")
                        DataStore.Add("GatherRate", "Cloth", int(ini.GetSetting("Config", "Cloth")))
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
                        DataStore.Remove("GatherRate", "Chicken")
                        DataStore.Add("GatherRate", "Chicken", int(ini.GetSetting("Config", "RawChickenBreast")))
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
                        DataStore.Remove("GatherRate", "Fat")
                        DataStore.Add("GatherRate", "Fat", int(ini.GetSetting("Config", "AnimalFat")))
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
                        DataStore.Remove("GatherRate", "Blood")
                        DataStore.Add("GatherRate", "Blood", int(ini.GetSetting("Config", "Blood")))
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

    def On_PlayerGathering(self, Player, GatherEvent):
        if GatherEvent.Item == "Wood":
            if Player.Inventory.FreeSlots > 0:
                rate = DataStore.Get("GatherRate", "Wood")
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Sulfur Ore":
            if Player.Inventory.FreeSlots > 0:
                rate = DataStore.Get("GatherRate", "Sulfur")
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Metal Ore":
            if Player.Inventory.FreeSlots > 0:
                rate = DataStore.Get("GatherRate", "Metal")
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Stones":
            if Player.Inventory.FreeSlots > 0:
                rate = DataStore.Get("GatherRate", "Stones")
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Leather":
            if Player.Inventory.FreeSlots > 0:
                rate = DataStore.Get("GatherRate", "Leather")
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Cloth":
            if Player.Inventory.FreeSlots > 0:
                rate = DataStore.Get("GatherRate", "Cloth")
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Raw Chicken Breast":
            if Player.Inventory.FreeSlots > 0:
                rate = DataStore.Get("GatherRate", "Chicken")
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Animal Fat":
            if Player.Inventory.FreeSlots > 0:
                rate = DataStore.Get("GatherRate", "Fat")
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
        elif GatherEvent.Item == "Blood":
            if Player.Inventory.FreeSlots > 0:
                rate = DataStore.Get("GatherRate", "Blood")
                gathered = GatherEvent.Quantity * (rate-1)
                Player.Inventory.AddItem(GatherEvent.Item, gathered)
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif Player.Inventory.FreeSlots == 0:
                GatherEvent.Quantity = 0
                Player.Notice("Inventory full, can't gather")
