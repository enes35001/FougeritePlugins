# -*- coding: utf-8 -*-
__title__ = 'StackSizes'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class StackSizes:
    def On_ItemsLoaded(self, ItemsBlocks):
        ini = Plugin.GetIni("Settings")
        keys = ini.EnumSection("StackSizes")
        #Util.Log("-----------------------------")
        for key in keys:
            #Util.Log(key + "=" + str(ItemsBlocks.Find(key)._maxUses))
            ItemsBlocks.Find(key)._maxUses = int(ini.GetSetting("StackSizes", key))
            #Util.Log(key + "=" + str(ItemsBlocks.Find(key)._maxUses))
            #Util.Log("-----------------------------")
