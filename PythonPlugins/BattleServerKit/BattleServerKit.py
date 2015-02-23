__title__ = 'BattleServerKit'
__author__ = 'Jakkee'
__version__ = '1.1.4'

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
        if ini.GetSetting("Armour", "Helmet") is not None:
            DataStore.Add("LoadOut", "AH", ini.GetSetting("Armour", "Helmet"))
        if ini.GetSetting("Armour", "Vest") is not None:
            DataStore.Add("LoadOut", "AV", ini.GetSetting("Armour", "Vest"))
        if ini.GetSetting("Armour", "Pants") is not None:
            DataStore.Add("LoadOut", "AP", ini.GetSetting("Armour", "Pants"))
        if ini.GetSetting("Armour", "Boots") is not None:
            DataStore.Add("LoadOut", "AB", ini.GetSetting("Armour", "Boots"))
        if ini.GetSetting("HotBar", "Item0") is not None:
            DataStore.Add("LoadOut", "HI0", ini.GetSetting("HotBar", "Item0"))
        if ini.GetSetting("HotBar", "Qty0") is not None:
            DataStore.Add("LoadOut", "HQ0", ini.GetSetting("HotBar", "Qty0"))
        if ini.GetSetting("HotBar", "Item1") is not None:
            DataStore.Add("LoadOut", "HI1", ini.GetSetting("HotBar", "Item1"))
        if ini.GetSetting("HotBar", "Qty1") is not None:
            DataStore.Add("LoadOut", "HQ1", ini.GetSetting("HotBar", "Qty1"))
        if ini.GetSetting("HotBar", "Item2") is not None:
            DataStore.Add("LoadOut", "HI2", ini.GetSetting("HotBar", "Item2"))
        if ini.GetSetting("HotBar", "Qty2") is not None:
            DataStore.Add("LoadOut", "HQ2", ini.GetSetting("HotBar", "Qty2"))
        if ini.GetSetting("HotBar", "Item3") is not None:
            DataStore.Add("LoadOut", "HI3", ini.GetSetting("HotBar", "Item3"))
        if ini.GetSetting("HotBar", "Qty3") is not None:
            DataStore.Add("LoadOut", "HQ3", ini.GetSetting("HotBar", "Qty3"))
        if ini.GetSetting("HotBar", "Item4") is not None:
            DataStore.Add("LoadOut", "HI4", ini.GetSetting("HotBar", "Item4"))
        if ini.GetSetting("HotBar", "Qty4") is not None:
            DataStore.Add("LoadOut", "HQ4", ini.GetSetting("HotBar", "Qty4"))
        if ini.GetSetting("HotBar", "Item5") is not None:
            DataStore.Add("LoadOut", "HI5", ini.GetSetting("HotBar", "Item5"))
        if ini.GetSetting("HotBar", "Qty5") is not None:
            DataStore.Add("LoadOut", "HQ5", ini.GetSetting("HotBar", "Qty5"))
        if ini.GetSetting("Inventory", "Item0") is not None:
            DataStore.Add("LoadOut", "II0", ini.GetSetting("Inventory", "Item0"))
        if ini.GetSetting("Inventory", "Qty0") is not None:
            DataStore.Add("LoadOut", "IQ0", ini.GetSetting("Inventory", "Qty0"))
        if ini.GetSetting("Inventory", "Item1") is not None:
            DataStore.Add("LoadOut", "II1", ini.GetSetting("Inventory", "Item1"))
        if ini.GetSetting("Inventory", "Qty1") is not None:
            DataStore.Add("LoadOut", "IQ1", ini.GetSetting("Inventory", "Qty1"))
        if ini.GetSetting("Inventory", "Item2") is not None:
            DataStore.Add("LoadOut", "II2", ini.GetSetting("Inventory", "Item2"))
        if ini.GetSetting("Inventory", "Qty2") is not None:
            DataStore.Add("LoadOut", "IQ2", ini.GetSetting("Inventory", "Qty2"))
        if ini.GetSetting("Inventory", "Item3") is not None:
            DataStore.Add("LoadOut", "II3", ini.GetSetting("Inventory", "Item3"))
        if ini.GetSetting("Inventory", "Qty3") is not None:
            DataStore.Add("LoadOut", "IQ3", ini.GetSetting("Inventory", "Qty3"))
        if ini.GetSetting("Inventory", "Item4") is not None:
            DataStore.Add("LoadOut", "II4", ini.GetSetting("Inventory", "Item4"))
        if ini.GetSetting("Inventory", "Qty4") is not None:
            DataStore.Add("LoadOut", "IQ4", ini.GetSetting("Inventory", "Qty4"))
        if ini.GetSetting("Inventory", "Item5") is not None:
            DataStore.Add("LoadOut", "II5", ini.GetSetting("Inventory", "Item5"))
        if ini.GetSetting("Inventory", "Qty5") is not None:
            DataStore.Add("LoadOut", "IQ5", ini.GetSetting("Inventory", "Qty5"))
        if ini.GetSetting("Inventory", "Item6") is not None:
            DataStore.Add("LoadOut", "II6", ini.GetSetting("Inventory", "Item6"))
        if ini.GetSetting("Inventory", "Qty6") is not None:
            DataStore.Add("LoadOut", "IQ6", ini.GetSetting("Inventory", "Qty6"))
        if ini.GetSetting("Inventory", "Item7") is not None:
            DataStore.Add("LoadOut", "II7", ini.GetSetting("Inventory", "Item7"))
        if ini.GetSetting("Inventory", "Qty7") is not None:
            DataStore.Add("LoadOut", "IQ7", ini.GetSetting("Inventory", "Qty7"))
        if ini.GetSetting("Inventory", "Item8") is not None:
            DataStore.Add("LoadOut", "II8", ini.GetSetting("Inventory", "Item8"))
        if ini.GetSetting("Inventory", "Qty8") is not None:
            DataStore.Add("LoadOut", "IQ8", ini.GetSetting("Inventory", "Qty8"))
        if ini.GetSetting("Inventory", "Item9") is not None:
            DataStore.Add("LoadOut", "II9", ini.GetSetting("Inventory", "Item9"))
        if ini.GetSetting("Inventory", "Qty9") is not None:
            DataStore.Add("LoadOut", "IQ9", ini.GetSetting("Inventory", "Qty9"))
        if ini.GetSetting("Inventory", "Item10") is not None:
            DataStore.Add("LoadOut", "II10", ini.GetSetting("Inventory", "Item10"))
        if ini.GetSetting("Inventory", "Qty10") is not None:
            DataStore.Add("LoadOut", "IQ10", ini.GetSetting("Inventory", "Qty10"))

    def On_PlayerSpawned(self, Player, SpawnEvent):
        Player.Inventory.RemoveItem("Rock", 1)
        Player.Inventory.RemoveItem("Bandage", 3)
        Player.Inventory.RemoveItem("Torch", 250)
        if Player.Inventory.FreeSlots == 36:
            if DataStore.Get("LoadOut", "AH") is not None:
                Player.Inventory.AddItemTo(DataStore.Get("LoadOut", "AH"), 36, 1)
            if DataStore.Get("LoadOut", "AV") is not None:
                Player.Inventory.AddItemTo(DataStore.Get("LoadOut", "AV"), 37, 1)
            if DataStore.Get("LoadOut", "AP") is not None:
                Player.Inventory.AddItemTo(DataStore.Get("LoadOut", "AP"), 38, 1)
            if DataStore.Get("LoadOut", "AB") is not None:
                Player.Inventory.AddItemTo(DataStore.Get("LoadOut", "AB"), 39, 1)
            if DataStore.Get("LoadOut", "HI0") and DataStore.Get("LoadOut", "HQ0") is not None:
                Player.Inventory.AddItemTo(DataStore.Get("LoadOut", "HI0"), 30, int(DataStore.Get("LoadOut", "HQ0")))
            if DataStore.Get("LoadOut", "HI1") and DataStore.Get("LoadOut", "HQ1") is not None:
                Player.Inventory.AddItemTo(DataStore.Get("LoadOut", "HI1"), 31, int(DataStore.Get("LoadOut", "HQ1")))
            if DataStore.Get("LoadOut", "HI2") and DataStore.Get("LoadOut", "HQ2") is not None:
                Player.Inventory.AddItemTo(DataStore.Get("LoadOut", "HI2"), 32, int(DataStore.Get("LoadOut", "HQ2")))
            if DataStore.Get("LoadOut", "HI3") and DataStore.Get("LoadOut", "HQ3") is not None:
                Player.Inventory.AddItemTo(DataStore.Get("LoadOut", "HI3"), 33, int(DataStore.Get("LoadOut", "HQ3")))
            if DataStore.Get("LoadOut", "HI4") and DataStore.Get("LoadOut", "HQ4") is not None:
                Player.Inventory.AddItemTo(DataStore.Get("LoadOut", "HI4"), 34, int(DataStore.Get("LoadOut", "HQ4")))
            if DataStore.Get("LoadOut", "HI5") and DataStore.Get("LoadOut", "HQ5") is not None:
                Player.Inventory.AddItemTo(DataStore.Get("LoadOut", "HI5"), 35, int(DataStore.Get("LoadOut", "HQ5")))
            if DataStore.Get("LoadOut", "II0") and DataStore.Get("LoadOut", "IQ0") is not None:
                Player.Inventory.AddItem(DataStore.Get("LoadOut", "II0"), int(DataStore.Get("LoadOut", "IQ0")))
            if DataStore.Get("LoadOut", "II1") and DataStore.Get("LoadOut", "IQ1") is not None:
                Player.Inventory.AddItem(DataStore.Get("LoadOut", "II1"), int(DataStore.Get("LoadOut", "IQ1")))
            if DataStore.Get("LoadOut", "II2") and DataStore.Get("LoadOut", "IQ2") is not None:
                Player.Inventory.AddItem(DataStore.Get("LoadOut", "II2"), int(DataStore.Get("LoadOut", "IQ2")))
            if DataStore.Get("LoadOut", "II3") and DataStore.Get("LoadOut", "IQ3") is not None:
                Player.Inventory.AddItem(DataStore.Get("LoadOut", "II3"), int(DataStore.Get("LoadOut", "IQ3")))
            if DataStore.Get("LoadOut", "II4") and DataStore.Get("LoadOut", "IQ4") is not None:
                Player.Inventory.AddItem(DataStore.Get("LoadOut", "II4"), int(DataStore.Get("LoadOut", "IQ4")))
            if DataStore.Get("LoadOut", "II5") and DataStore.Get("LoadOut", "IQ5") is not None:
                Player.Inventory.AddItem(DataStore.Get("LoadOut", "II5"), int(DataStore.Get("LoadOut", "IQ5")))
            if DataStore.Get("LoadOut", "II6") and DataStore.Get("LoadOut", "IQ6") is not None:
                Player.Inventory.AddItem(DataStore.Get("LoadOut", "II6"), int(DataStore.Get("LoadOut", "IQ6")))
            if DataStore.Get("LoadOut", "II7") and DataStore.Get("LoadOut", "IQ7") is not None:
                Player.Inventory.AddItem(DataStore.Get("LoadOut", "II7"), int(DataStore.Get("LoadOut", "IQ7")))
            if DataStore.Get("LoadOut", "II8") and DataStore.Get("LoadOut", "IQ8") is not None:
                Player.Inventory.AddItem(DataStore.Get("LoadOut", "II8"), int(DataStore.Get("LoadOut", "IQ8")))
            if DataStore.Get("LoadOut", "II9") and DataStore.Get("LoadOut", "IQ9") is not None:
                Player.Inventory.AddItem(DataStore.Get("LoadOut", "II9"), int(DataStore.Get("LoadOut", "IQ9")))
            if DataStore.Get("LoadOut", "II10") and DataStore.Get("LoadOut", "IQ10") is not None:
                Player.Inventory.AddItem(DataStore.Get("LoadOut", "II10"), int(DataStore.Get("LoadOut", "IQ10")))
            Player.Notice("Here is your respawn kit!")
        else:
            return
