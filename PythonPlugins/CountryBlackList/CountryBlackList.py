__title__ = 'CountryBlackList'
__author__ = 'Jakkee'
__version__ = '2.0.1'

try:
    import clr
    clr.AddReferenceByPartialName("Fougerite", "GeoIP")
    import Fougerite
    import GeoIP
    from GeoIP import GeoIP as RealGeoIP  
except:
    raise ImportError("Failed to reference the GeoIP.dll, Download from: http://fougerite.com/resources/geoip.135/")

geo = RealGeoIP.Instance
PluginSettings = {}


class CountryBlackList:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "ShowAcceptedMessage", "true")
            ini.AddSetting("Settings", "ShowDeniedMessage", "true")
            ini.AddSetting("Settings", "LogTimedOutConnection", "true")
            ini.AddSetting("Settings", "EnableWhitelist", "true")
            ini.AddSetting("BlackList", "BlackListedCountries", "TK, JO")
            ini.AddSetting("Messages", "JoinMessage", "%PLAYER% has connected from: %COUNTRY%")
            ini.AddSetting("Messages", "PlayerDisconnectMessage", "Your country is on the servers blacklist")
            ini.AddSetting("Messages", "ServerDisconnectMessage", "%PLAYER% is trying to connect from: %COUNTRY% but is black listed")
            ini.AddSetting("Messages", "UnknownLocation", "A hidden location")
            ini.Save()
        if not Plugin.IniExists("WhiteList"):
            Plugin.CreateIni("WhiteList")
            ini = Plugin.GetIni("WhiteList")
            ini.AddSetting("SteamID", "IP Address", "Players Name")
            ini.AddSetting("76561198135558142", "127.0.0.1", "Xiled Jakkee")
            ini.Save()
        PluginSettings.clear()
        ini = Plugin.GetIni("Settings")
        PluginSettings["SAM"] = ini.GetBoolSetting("Settings", "ShowAcceptedMessage")
        PluginSettings["SDM"] = ini.GetBoolSetting("Settings", "ShowDeniedMessage")
        PluginSettings["LTOC"] = ini.GetBoolSetting("Settings", "LogTimedOutConnection")
        PluginSettings["EW"] = ini.GetBoolSetting("Settings", "EnableWhitelist")
        PluginSettings["BL"] = ini.GetSetting("BlackList", "BlackListedCountries")
        PluginSettings["JM"] = ini.GetSetting("Messages", "JoinMessage")
        PluginSettings["PDM"] = ini.GetSetting("Messages", "PlayerDisconnectMessage")
        PluginSettings["DM"] = ini.GetSetting("Messages", "ServerDisconnectMessage")
        PluginSettings["UL"] = ini.GetSetting("Messages", "UnknownLocation")

    def find(self, blacklist, CountryCode):
        try:
            blacklist = blacklist.Replace(" ", "")
            blacklist = blacklist.split(',')
            for configlist in blacklist:
                if CountryCode == configlist:
                    return True
                else:
                    continue
            return False
        except:
            return False

    def OnWhiteList(self, Player):
        if Player.Admin or Player.Moderator:
            return True
        else:
            if Plugin.IniExists("WhiteList"):
                ini = Plugin.GetIni("WhiteList")
                for id in ini.Sections:
                    if ini.ContainsSetting(id, Player.IP):
                        return True
                    if id == Player.SteamID:
                        return True
            return False

    def On_Command(self, Player, cmd, args):
        if cmd == "wlist":
            if Player.Admin or Player.Moderator:
                if len(args) == 0:
                    Player.MessageFrom("CountryBlackList", "Usage: /wlist <User Name>")
                    Player.MessageFrom("CountryBlackList", "Adds a user to the whitelist")
                else:
                    target = self.CheckV(Player, args)
                    if target is not None:
                        if not Plugin.IniExists("WhiteList"):
                            Plugin.CreateIni("WhiteList")
                        ini = Plugin.GetIni("WhiteList")
                        ini.AddSetting(target.SteamID, target.IP, target.Name)
                        ini.Save()
            else:
                Player.MessageFrom("CountryBlackList", "You are not allowed to use this command!")

    def On_PlayerConnected(self, Player):
        try:                    
            IPData = geo.GetDataOfIP(Player.IP)
            if IPData is None:
                if PluginSettings["SAM"]:
                    msg = PluginSettings["JM"]
                    msg = msg.Replace("%PLAYER%", Player.Name)
                    msg = msg.Replace("%COUNTRY%", PluginSettings["UL"])
                    Server.Broadcast(msg)
                if PluginSettings["LTOC"]:
                    Plugin.Log("Unknown Location", Player.SteamID + "=" + "Player.Name" + " [" + Player.IP + "]")
                return
            countrycode = IPData.CountryShort
            blacklist = PluginSettings["BL"]
            if self.find(blacklist, countrycode):
                if PluginSettings["EW"]:
                    if OnWhiteList(Player.SteamID, Player.IP):
                        if PluginSettings["SAM"]:
                            msg = PluginSettings["JM"]
                            msg = msg.Replace("%PLAYER%", Player.Name)
                            msg = msg.Replace("%COUNTRY%", IPData.Country)
                            Server.Broadcast(msg)
                        return
                playerdisconnectMSG = PluginSettings["PDM"]
                if PluginSettings["SDM"]:
                    msg = PluginSettings["DM"]
                    msg = msg.Replace("%PLAYER%", Player.Name)
                    msg = msg.Replace("%COUNTRY%", IPData.Country)
                    Server.Broadcast(msg)
                Player.Message(playerdisconnectMSG + " [" + countrycode + "]")
                Player.Disconnect()
            else:
                if PluginSettings["SAM"]:
                    msg = PluginSettings["JM"]
                    msg = msg.Replace("%PLAYER%", Player.Name)
                    msg = msg.Replace("%COUNTRY%", IPData.Country)
                    Server.Broadcast(msg)
        except:
            if PluginSettings["SAM"]:
                msg = PluginSettings["JM"]
                msg = msg.Replace("%PLAYER%", Player.Name)
                msg = msg.Replace("%COUNTRY%", PluginSettings["UL"])
                Server.Broadcast(msg)
            if PluginSettings["LTOC"]:
                Plugin.Log("Unknown Location", Player.SteamID + "=" + "Player.Name" + " [" + Player.IP + "]")

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
            Player.Message("Couldn't find " + str.join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.Message("Found " + str(count) + " players with similar name!")
            Player.Message("Use quotation marks if the name has a space in it.")

