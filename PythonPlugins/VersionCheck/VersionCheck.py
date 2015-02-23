__title__ = 'VersionCheck'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class VersionCheck:
    """def On_PluginInit(self):
        self.versioncheck("http://fougerite.com/resources/98/")

    def versioncheck(self, website):
        Util.Log("Checking: " + website + " ...")
        if not Plugin.IniExists("Log"):
            Plugin.CreateIni("Log")
            log = Plugin.GetIni("Log")
            log.Save()
        s = Web.GET(website)
        #version = FindVersion in s (Line 1300ish)
        #if self.__version__ < version:
            #for Player in Server.Players:
                #if not Player.Admin
                    #Continue
                 #else:
                   #Player.Message(self.__title__ + " has new update, Downloading version: " + version)
               #file = System.Net.WebRequestMethods.File.DownloadFile(http://fougerite.com/lol/lol.py
               #for Player in Server.Players:
                   #if not Player.Admin
                       #Continue
                   #else:
                       #Player.Message(self.__title__ + " Downloaded! Reload to take effect!")
        log = Plugin.GetIni("Log")
        log.AddSetting("Log", Plugin.GetDate() + "|" + Plugin.GetTime(), "Website Response: " + s)
        log.Save()
        Util.Log("Saved log file")"""
