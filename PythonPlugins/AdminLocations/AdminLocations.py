__title__ = 'AdminLocations'
__author__ = 'Jakkee'
__version__ = '1.1'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
TeleportLocations = {}


class AdminLocations:
    def On_PluginInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Example", "Location Name", "Location X, Y, Z")
            ini.AddSetting("Locations", "Small Rad", "6050, 381, -3620")
            ini.AddSetting("Locations", "Big Rad", "5250, 371, -4850")
            ini.AddSetting("Locations", "Factory Rad", "6300, 361, -4650")
            ini.AddSetting("Locations", "Hanger", "6600, 356, -4400")
            ini.AddSetting("Locations", "Oil Tankers", "6690, 356, -3880")
            ini.AddSetting("Locations", "North Hacker Valley", "5000, 461, -3000")
            ini.AddSetting("Locations", "French Valley", "6056, 385, -4162")
            ini.AddSetting("Locations", "North Next Valley", "4668, 445, -3908")
            ini.Save()
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        TeleportLocations.clear()
        ini = Plugin.GetIni("Settings")
        for key in ini.EnumSection("Locations"):
            TeleportLocations[key] = ini.GetSetting("Locations", key)
            
    def On_Command(self, Player, cmd, args):
        if cmd == "tploc":
            if Player.Admin:
                if len(args) == 0:
                    count = 1
                    for loc in TeleportLocations.keys():
                        Player.Message(str(count) + ") " + loc)
                        count += 1
                elif len(args) == 1:
                    name = None
                    try:
                        need = int(args[0])
                    except:
                        Player.Message("usage: /tploc [Number]")
                    count = 1
                    for loc in TeleportLocations.keys():
                        if not count == need:
                            count += 1
                            continue
                        else:
                            name = loc
                            break
                    if name is not None:
                        cords = TeleportLocations[name].replace(" ", "").split(",")
                        Player.TeleportTo(float(cords[0]), float(cords[1]), float(cords[2]), False)
                        Player.InventoryNotice(name)
                    else:
                        Player.Message("Can not find that location!")
                else:
                    Player.Message("usage: /tploc [Number]")
            else:
                Player.Message("You are not allowed to use that command!")
