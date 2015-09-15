__title__ = 'CountryBlackList'
__author__ = 'Jakkee'
__version__ = '1.0.2'

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
        ini = Plugin.GetIni("Settings")
        if not ini.ContainsSetting("Settings", "LogErrors"):
            ini.AddSetting("Settings", "LogErrors", "true")
            ini.Save()
        DataStore.Add("CountryBlackList", "ShowAcceptedMessage", ini.GetBoolSetting("Settings", "ShowAcceptedMessage"))
        DataStore.Add("CountryBlackList", "ShowDeniedMessage", ini.GetBoolSetting("Settings", "ShowDeniedMessage"))
        DataStore.Add("CountryBlackList", "LogTimedOutConnection", ini.GetBoolSetting("Settings", "LogTimedOutConnection"))
        DataStore.Add("CountryBlackList", "LogErrors", ini.GetBoolSetting("Settings", "LogErrors"))
        DataStore.Add("CountryBlackList", "BlackListedCountries", ini.GetSetting("BlackList", "BlackListedCountries"))
        DataStore.Add("CountryBlackList", "JoinMessage", ini.GetSetting("Messages", "JoinMessage"))
        DataStore.Add("CountryBlackList", "DisconnectMessage", ini.GetSetting("Messages", "DisconnectMessage"))
        DataStore.Add("CountryBlackList", "OtherDisconnectMessage", ini.GetSetting("Messages", "OtherDisconnectMessage"))


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
        except Exception, e:
            if DataStore.Get("CountryBlackList", "LogErrors"):
                Plugin.Log("Error Log", str(e))
            return False

    def getcountry(self, Player):
        try:
            ip = Player.IP
            if ip == "127.0.0.1":
                ip = Util.GetStaticField("server", "ip")
            country = Web.GET("http://ipinfo.io/" + ip + "/country")
            return country
        except Exception, e:
            if DataStore.Get("CountryBlackList", "LogErrors"):
                Plugin.Log("Error Log", str(e))
            if DataStore.Get("CountryBlackList", "ShowDeniedMessage"):
                a = DataStore.Get("CountryBlackList", "JoinMessage")
                a = a.Replace("%player%", Player.Name)
                a = a.Replace("%country%", "unknown")
                Server.Broadcast(a)
            if DataStore.Get("CountryBlackList", "LogTimedOutConnection"):
                if not Plugin.IniExists("ConnectionLog"):
                    Plugin.CreateIni("ConnectionLog")
                    log = Plugin.GetIni("ConnectionLog")
                    log.Save()
                log = Plugin.GetIni("ConnectionLog")
                log.AddSetting("Timed out connections", Plugin.GetDate() + "|" + Plugin.GetTime() + " ", " SteamID: " + Player.SteamID + ". Name: " + Player.Name + ". IP: " + Player.IP)
                log.Save()

    def On_PlayerConnected(self, Player):
        try:
            bl = DataStore.Get("CountryBlackList", "BlackListedCountries")
            c = self.getcountry(Player)
            if self.find(bl, c):
                pdis = DataStore.Get("CountryBlackList", "DisconnectMessage")
                Player.Message(pdis + "[color red][[color cyan]" + c + "[color red]]")
                Player.Disconnect()
                if DataStore.Get("CountryBlackList", "ShowAcceptedMessage"):
                    a = DataStore.Get("CountryBlackList", "OtherDisconnectMessage")
                    a = a.Replace("%player%", Player.Name)
                    a = a.Replace("%country%", c)
                    Server.Broadcast(a)
            else:
                if DataStore.Get("CountryBlackList", "ShowAcceptedMessage"):
                    a = DataStore.Get("CountryBlackList", "JoinMessage")
                    a = a.Replace("%player%", Player.Name)
                    a = a.Replace("%country%", c)
                    Server.Broadcast(a)
        except Exception, e:
            if DataStore.Get("CountryBlackList", "LogErrors"):
                Plugin.Log("Error Log", str(e))
            pass
