# -*- coding: utf-8 -*-
__title__ = 'StackSizes'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class StackSizes:
    def On_ItemsLoaded(self, ItemsBlocks):
        """if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Items", "Metal Ore", "250")
            ini.AddSetting("Items", "Sulfur Ore", "250")
            ini.AddSetting("Items", "Leather", "250")
            ini.AddSetting("Items", "Cloth", "250")
            ini.AddSetting("Items", "Animal Fat", "250")
            ini.AddSetting("Items", "Low Grade Fuel", "250")
            ini.AddSetting("Items", "Workbench", "1")
            ini.AddSetting("Items", "Stone Hatchet", "1")
            ini.AddSetting("Items", "Furnace", "1")
            ini.AddSetting("Items", "Torch", "250")
            ini.AddSetting("Items", "Low Quality Metal", "250")
            ini.AddSetting("Items", "Metal Door", "5")
            ini.AddSetting("Items", "Large Wood Storage", "5")
            ini.AddSetting("Items", "Small Stash", "5")
            ini.AddSetting("Items", "Gunpowder", "250")
            ini.AddSetting("Items", "Sulfur", "250")
            ini.AddSetting("Items", "Wood Planks", "250")
            ini.AddSetting("Items", "Paper", "250")
            ini.AddSetting("Items", "Explosives", "250")
            ini.AddSetting("Items", "Bandage", "5")
            ini.AddSetting("Items", "Large Medkit", "5")
            ini.AddSetting("Items", "Small Medkit", "5")
            ini.AddSetting("Items", "Arrow", "10")
            ini.AddSetting("Items", "Handmade Shell", "250")
            ini.AddSetting("Items", "Shotgun Shells", "250")
            ini.AddSetting("Items", "556 Ammo", "250")
            ini.AddSetting("Items", "9mm Ammo", "250")
            ini.AddSetting("Items", "Explosive Charge", "5")
            ini.AddSetting("Items", "F1 Grenade", "10")
            ini.AddSetting("Items", "Flare", "10")
            ini.AddSetting("Items", "Research Kit 1", "1")
            ini.AddSetting("Items", "Cooked Chicken Breast", "250")
            ini.AddSetting("Items", "Anti-Radiation Pills", "250")
            ini.AddSetting("Items", "Wood", "250")
            ini.AddSetting("Items", "Wood Pillar", "250")
            ini.AddSetting("Items", "Wood Foundation", "250")
            ini.AddSetting("Items", "Wood Wall", "250")
            ini.AddSetting("Items", "Wood Doorway", "250")
            ini.AddSetting("Items", "Wood Window", "250")
            ini.AddSetting("Items", "Wood Stairs", "250")
            ini.AddSetting("Items", "Wood Ramp", "250")
            ini.AddSetting("Items", "Wood Ceiling", "250")
            ini.AddSetting("Items", "Metal Pillar", "250")
            ini.AddSetting("Items", "Metal Foundation", "250")
            ini.AddSetting("Items", "Metal Fragments", "250")
            ini.AddSetting("Items", "Metal Wall", "250")
            ini.AddSetting("Items", "Metal Doorway", "250")
            ini.AddSetting("Items", "Metal Window", "250")
            ini.AddSetting("Items", "Metal Stairs", "250")
            ini.AddSetting("Items", "Metal Ramp", "250")
            ini.AddSetting("Items", "Metal Ceiling", "250")
            ini.AddSetting("Items", "Metal Window Bars", "5")
            ini.Save()
        ini = Plugin.GetIni("Settings")
        keys = ini.EnumSection("Items")
        for key in keys:
            ItemsBlocks.Find(key)._maxUses = int(ini.GetSetting("Items", key))"""
        for block in ItemsBlocks:
            if not Plugin.IniExists("Log"):
                Plugin.CreateIni("Log")
                ini = Plugin.GetIni("Log")
                ini.Save()
            ini = Plugin.GetIni("Log")
            ini.AddSetting("Items", str(block), str(block._maxUses))
            ini.Save()
