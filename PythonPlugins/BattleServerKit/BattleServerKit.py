__title__ = 'BattleServerKit'
__author__ = 'Jakkee'
__version__ = '1.1.5'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class BattleServerKit:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("LoadOut"):
            Plugin.CreateIni("LoadOut")
            ini = Plugin.GetIni("LoadOut")
            ini.AddSetting("Armour", "Helmet", "Kevlar Helmet")
            ini.AddSetting("Armour", "Vest", "Leather Vest")
            ini.AddSetting("Armour", "Pants", "Leather Pants")
            ini.AddSetting("Armour", "Boots", "Kevlar Boots")
            ini.AddSetting("HotBar", "Item0", "P250")
            ini.AddSetting("HotBar", "Qty0", "8")
            ini.AddSetting("HotBar", "Item1", "MP5A4")
            ini.AddSetting("HotBar", "Qty1", "30")
            ini.AddSetting("HotBar", "Item2", "Large Medkit")
            ini.AddSetting("HotBar", "Qty2", "5")
            ini.AddSetting("HotBar", "Item3", "Large Medkit")
            ini.AddSetting("HotBar", "Qty3", "5")
            ini.AddSetting("HotBar", "Item4", "Small Rations")
            ini.AddSetting("HotBar", "Qty4", "10")
            ini.AddSetting("HotBar", "Item5", "Hatchet")
            ini.AddSetting("HotBar", "Qty5", "1")
            ini.AddSetting("Inventory", "Item0", "Holo sight")
            ini.AddSetting("Inventory", "Qty0", "1")
            ini.AddSetting("Inventory", "Item1", "9mm Ammo")
            ini.AddSetting("Inventory", "Qty1", "400")
            ini.AddSetting("Inventory", "Item2", "Laser Sight")
            ini.AddSetting("Inventory", "Qty2", "1")
            ini.AddSetting("Inventory", "Item3", "Wood Planks")
            ini.AddSetting("Inventory", "Qty3", "40")
            ini.AddSetting("Inventory", "Item4", "Cooked Chicken Breast")
            ini.AddSetting("Inventory", "Qty4", "25")
            ini.Save()
        DataStore.Flush("LoadOut")
        ini = Plugin.GetIni("LoadOut")
        #ARMOUR
        count = 0
        Akey = ini.EnumSection("Armour")
        for x in Akey:
            if not ini.GetSetting("Armour", x) == "":
                DataStore.Add("LoadOut", "A" + str(count), ini.GetSetting("Armour", x))
                count += 1
            else:
                count += 1
                continue
        #HOTBAR
        count = 0
        qty = 0
        Akey = ini.EnumSection("HotBar")
        for x in Akey:
            if "Item" in x:
                if not ini.GetSetting("HotBar", x) == "":
                    DataStore.Add("LoadOut", "HI" + str(count), ini.GetSetting("HotBar", x))
                    count += 1
                else:
                    count += 1
                    continue
            else:
                if not ini.GetSetting("HotBar", x) == "":
                    DataStore.Add("LoadOut", "HQ" + str(count), ini.GetSetting("HotBar", x))
                    count += 1
                else:
                    count += 1
                    continue
        #INVENTORY
        count = 0
        qty = 0
        Akey = ini.EnumSection("Inventory")
        for x in Akey:
            if "Item" in x:
                if not ini.GetSetting("Inventory", x) == "":
                    DataStore.Add("LoadOut", "II" + str(count), ini.GetSetting("Inventory", x))
                    count += 1
                else:
                    count += 1
                    continue
            else:
                if not ini.GetSetting("Inventory", x) == "":
                    DataStore.Add("LoadOut", "IQ" + str(count), ini.GetSetting("Inventory", x))
                    count += 1
                else:
                    count += 1
                    continue

    def On_PlayerSpawned(self, Player, SpawnEvent):
        Player.Inventory.RemoveItem("Rock", 1)
        Player.Inventory.RemoveItem("Bandage", 3)
        Player.Inventory.RemoveItem("Torch", 250)
        if Player.Inventory.FreeSlots == 36:
            #ARMOUR
            count = 0
            slot = 36
            for x in DataStore.Keys("LoadOut"):
                if x == "A" + str(count):
                    Player.Inventory.AddItemTo(DataStore.Get("LoadOut", "A" + str(count)), slot, 1)
                    count += 1
                    slot =+ 1
                else:
                    count += 1
                    slot += 1
                    continue
            #HOTBAR
            count = 0
            slot = 30
            for x in DataStore.Keys("LoadOut"):
                if x == "HI" + str(count):
                    if not DataStore.Get("LoadOut", "HQ" + str(count)) == "":
                        Player.Inventory.AddItemTo(DataStore.Get("LoadOut", "HI" + str(count)), slot, int(DataStore.Get("LoadOut", "HQ" + str(count))))
                        count += 1
                        slot += 1
                    else:
                        count += 1
                        slot += 1
                        continue
                else:
                    count += 1
                    slot += 1
                    continue
            #INVENTORY
            count = 0
            for x in DataStore.Keys("LoadOut"):
                if x == "II" + str(count):
                    if not DataStore.Get("LoadOut", "IQ" + str(count)) == "":
                        Player.Inventory.AddItemTo(DataStore.Get("LoadOut", "II" + str(count)), int(DataStore.Get("LoadOut", "IQ" + str(count))))
                        count += 1
                    else:
                        count += 1
                        continue
                else:
                    count += 1
                    continue
            Player.Notice("Here is your respawn kit!")
        else:
            return
