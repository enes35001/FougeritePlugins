__title__ = 'CountryBlackList'
__author__ = 'Jakkee'
__version__ = '1.0.1'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class CountryBlackList:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "ShowAcceptedMessage", "true")
            ini.AddSetting("Settings", "ShowDeniedMessage", "true")
            ini.AddSetting("Settings", "LogTimedOutConnection", "true")
            ini.AddSetting("BlackList", "BlackListedCountries", "RU, KR")
            ini.AddSetting("Messages", "JoinMessage", "[color cyan]%player%[/color] has connected from: [color cyan]%country%[/color]")
            ini.AddSetting("Messages", "DisconnectMessage", "Your country is on the servers blacklist")
            ini.AddSetting("Messages", "OtherDisconnectMessage", "[color cyan]%player%[/color] is trying to connect from: [color cyan]%country%[/color] but is black listed")
            ini.Save()

    def find(self, b, c):
        try:
            #Throws an error if website timed out (Because c has no string)
            b = b.Replace(" ", "")
            b = b.split(',')
            c = c[:-1]
            for a in b:
                if c == a:
                    return True
            return False
        except:
            return False

    def getcountry(self, Player):
        try:
            country = Web.GET("http://ipinfo.io/" + Player.IP + "/country")
            return country
        except:
            ini = Plugin.GetIni("Settings")
            if ini.GetSetting("Settings", "ShowDeniedMessage") == "true":
                a = ini.GetSetting("Messages", "JoinMessage")
                a = a.Replace("%player%", Player.Name)
                a = a.Replace("%country%", "unknown")
                Server.Broadcast(a)
            if ini.GetSetting("Settings", "LogTimedOutConnection") == "true":
                if not Plugin.IniExists("ConnectionLog"):
                    Plugin.CreateIni("ConnectionLog")
                    log = Plugin.GetIni("ConnectionLog")
                    log.Save()
                log = Plugin.GetIni("ConnectionLog")
                log.AddSetting("Timed out connections", Plugin.GetDate() + "|" + Plugin.GetTime() + " ", " SteamID: " + Player.SteamID + ". Name: " + Player.Name + ". IP: " + Player.IP)
                log.Save()
            pass

    def On_PlayerConnected(self, Player):
        try:
            ini = Plugin.GetIni("Settings")
            bl = ini.GetSetting("BlackList", "BlackListedCountries")
            c = self.getcountry(Player)
            if self.find(bl, c):
                pdis = ini.GetSetting("Messages", "DisconnectMessage")
                Player.Message(pdis + "[color red][[color cyan]" + c + "[color red]]")
                Player.Disconnect()
                if ini.GetSetting("Settings", "ShowAcceptedMessage") == "true":
                    a = ini.GetSetting("Messages", "OtherDisconnectMessage")
                    a = a.Replace("%player%", Player.Name)
                    a = a.Replace("%country%", c)
                    Server.Broadcast(a)
            else:
                if ini.GetSetting("Settings", "ShowAcceptedMessage") == "true":
                    a = ini.GetSetting("Messages", "JoinMessage")
                    a = a.Replace("%player%", Player.Name)
                    a = a.Replace("%country%", c)
                    Server.Broadcast(a)
        except:
            pass