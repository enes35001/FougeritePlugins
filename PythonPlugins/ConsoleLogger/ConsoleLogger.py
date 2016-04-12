__title__ = 'ConsoleLogger'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByName("Fougerite")
import Fougerite

class ConsoleLogger:
    def On_Console(self, Player, ConsoleEvent):
        Util.Log("On_Console")
        command = ConsoleEvent.Class
        if ConsoleEvent.Function is not None:
            command = ConsoleEvent.Class + "." + ConsoleEvent.Function
        if ConsoleEvent.Args is not None:
            command = ConsoleEvent.Class + "." + ConsoleEvent.Function + " " + str.join(" ", ConsoleEvent.Args)
        if Player == None:
            Plugin.Log("Log", "Server Console has run: " + command)
        else:
            Plugin.Log("Log", Player.Name + "=" + Player.SteamID + " has run: " + command)      

