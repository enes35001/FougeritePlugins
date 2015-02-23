__title__ = 'ReservedSlots'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class ReservedSlots:
    def On_PluginInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "Total reserved slots", "10")
            ini.AddSetting("Config", "Reserved slots for Moderators", "true")
            ini.AddSetting("Config", "Reserved slots for Admins", "true")
            ini.Save()
        DataStore.Flush("ReservedSlots")
        ini = Plugin.GetIni("Settings")
        DataStore.Add("ReservedSlots", "Max", int(ini.GetSetting("Config", "Total reserved slots")))
        DataStore.Add("ReservedSlots", "Mod", ini.GetSetting("Config", "Reserved slots for Moderators"))
        DataStore.Add("ReservedSlots", "Admin", ini.GetSetting("Config", "Reserved slots for Admins"))

    def isReserved(self, Player):
        try:
            user = self.getUserIni()
            if user.GetSetting("ReservedPlayers", Player.SteamID) is not None:
                return True
            elif DataStore.ContainsKey("Moderators", Player.SteamID):
                if DataStore.Get("ReservedSlots", "Mod") == "true":
                    return True
                else:
                    return False
            elif Player.Admin:
                if DataStore.Get("ReservedSlots", "Admin") == "true":
                    return True
                else:
                    return False
        except:
            pass

    def getUserIni(self):
        if not Plugin.IniExists("Users"):
            ini = Plugin.CreateIni("Users")
            ini.Save()
        return Plugin.GetIni("Users")

    def On_PlayerConnected(self, Player):
        try:
            if (len(Server.Players) + DataStore.Get("ReservedSlots", "Max")) >= Util.GetStaticField("server", "maxplayers"):
                if not self.isReserved(Player):
                    Player.Notice("Too Many Connected Players")
                    Util.Log("DENIED: " + Player.Name + " Reason: is not on the reserve list!")
                    Player.Disconnect()
                else:
                    Util.Log("ACCEPTED: " + Player.Name + " Reason: is on the reserve list!")
        except:
            pass

    def On_Command(self, Player, cmd, args):
        if cmd == "rsadd":
            if Player.Admin:
                if len(args) == 0:
                    Player.Message("Usage: /rsadd [name]")
                else:
                    user = self.CheckV(Player, args[0])
                    if user is not None:
                        ini = self.getUserIni()
                        ini.AddSetting("ReservedPlayers", user.SteamID, user.Name + " [" + Plugin.GetDate() + "|" + Plugin.GetTime() + "] Added by: " + Player.Name)
                        ini.Save()
                        Player.Message("Added " + user.Name + " to the reserved slot list!")
            else:
                Player.Message("You are not allowed to use this command!")
        elif cmd == "rsdel":
            if Player.Admin:
                if len(args) == 0:
                    Player.Message("Usage: /rsdel [name]")
                else:
                    user = self.CheckV(Player, args[0])
                    if user is not None:
                        ini = self.getUserIni()
                        ini.DeleteSetting("ReservedPlayers", user.SteamID)
                        ini.Save()
                        Player.Message("Removed " + user.Name + " from the reserved slot list!")
            else:
                Player.Message("You are not allowed to use this command!")

#DreTaX's amazing shit here...
    def GetPlayerName(self, namee):
        try:
            name = namee.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

#Also here...
    def CheckV(self, Player, args):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.join(" ", args))
            if p is not None:
                return p
            for pl in Server.Players:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            nargs = str(args).lower()
            p = self.GetPlayerName(nargs)
            if p is not None:
                return p
            for pl in Server.Players:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.Message("Couldn't find " + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.Message("Found " + str(count) + " players with similar name!")
            Player.Message("Use quotation marks if the name has a space in it.")
            return None