__title__ = 'StackSizes'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class StackSizes:
    def On_ItemsLoaded(self, ItemsBlocks):
        Util.Log("----------------------------")
        Util.Log("plugin started...")
        item = ItemsBlocks.Find("556 Ammo")
        Util.Log("Found: " + str(item))
        Util.Log("MaxUses: " + str(item._maxUses))
        Util.Log("----------------------------")

    def On_PlugInit(self):
        """Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Items", "Arrow", "10")
            ini.AddSetting("Items", "556 Ammo", "")
            ini.AddSetting("Items", "9mm Ammo", "")
            ini.AddSetting("Items", "Shotgun Shells", "")
            ini.AddSetting("Items", "Wood", "")
            ini.AddSetting("Items", "Sulfur Ore", "")
            ini.AddSetting("Items", "Stones", "")
            ini.AddSetting("Items", "Animal Fat", "")
            ini.AddSetting("Items", "Metal Ore", "")
            ini.AddSetting("Items", "Blood Bags", "")
            ini.AddSetting("Items", "Cloth", "")
            ini.AddSetting("Items", "Paper", "")
            ini.AddSetting("Items", "Small Stash", "")
            ini.AddSetting("Items", "Large Medkit", "")
            ini.AddSetting("Items", "Small Medkit", "")
            ini.AddSetting("Items", "", "")
            ini.AddSetting("Items", "", "")
            ini.AddSetting("Items", "", "")
            ini.AddSetting("Items", "", "")
            ini.AddSetting("Items", "", "")
            ini.AddSetting("Items", "", "")
            ini.AddSetting("Items", "", "")
            ini.AddSetting("Items", "", "")
            ini.AddSetting("Items", "", "")
            ini.AddSetting("Items", "", "")
            ini.AddSetting("Items", "", "")
            ini.AddSetting("Items", "", "")
            ini.AddSetting("Items", "", "")
            ini.Save()"""

                
            
