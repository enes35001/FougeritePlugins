__title__ = 'AdminLocations'
__author__ = 'Jakkee'
__version__ = '1.0.2'

import clr
clr.AddReferenceByPartialName("UnityEngine")
clr.AddReferenceByPartialName("Fougerite")
import UnityEngine
import Fougerite

class AdminLocations:
    def On_Command(self, Player, cmd, args):
        if cmd == "tploc":
            if Player.Admin:
                if len(args) == 0:
                    Player.Message("--------Usage--------")
                    Player.Message("/tploc [location]")
                    Player.Message("--Locations--")
                    Player.Message("smallrad")
		    Player.Message("bigrad")
		    Player.Message("factoryrad")
		    Player.Message("hangar")
		    Player.Message("oiltanks")
		    Player.Message("hackervalley")
		    Player.Message("frenchvalley")
		    Player.Message("event")
                elif len(args) == 1:
                    if args[0] == "smallrad":
                        Player.TeleportTo(6050, 381, -3620)
			Player.InventoryNotice("Small Rad Town")
		    elif args[0] == "bigrad":
                        Player.TeleportTo(5250, 371, -4850)
			Player.InventoryNotice("Big Rad Town")
                    elif args[0] == "factoryrad":
                        Player.TeleportTo(6300, 361, -4650)
			Player.InventoryNotice("Factory Rad")
                    elif args[0] == "hangar":
                        Player.TeleportTo(6600, 356, -4400)
			Player.InventoryNotice("Hangar")
                    elif args[0] == "oiltanks":
                        Player.TeleportTo(6690, 356, -3880)
			Player.InventoryNotice("Oil Tankers")
                    elif args[0] == "hackervalley":
                        Player.TeleportTo(5000, 461, -3000)
			Player.InventoryNotice("North Hacker Valley")
                    elif args[0] == "frenchvalley":
                        Player.TeleportTo(6056, 385, -4162)
			Player.InventoryNotice("French Valley")
                    elif args[0] == "event":
                        Player.TeleportTo(4668, 445, -3908)
			Player.InventoryNotice("Next Valley")
		    else:
                        Player.Message("unknown location")
                else:
                    Player.Message("usage: /tploc [location]")
            else:
                Player.Message("You are not allowed to use that command!")

    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
