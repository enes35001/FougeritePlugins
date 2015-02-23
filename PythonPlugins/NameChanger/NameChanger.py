__title__ = 'NameChanger'
__author__ = 'Jakkee'
__version__ = '1.0.1'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class NameChanger:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def On_Command(self, Player, cmd, args):
        if cmd == "rename":
            if Player.Admin:
                if len(args) == 0:
                    Player.Message("Usage: /rename [Name]")
                elif not len(args) <= 15:
                    name = self.argsToText(args)
                    Player.Name = name
                    Player.Notice(name + " is your new name!")
                else:
                    Player.Message("Usage: /rename [Name]")
                    Player.Message("Please use less than 15 characters")
            else:
                Player.Message("You are not allowed to use that command")
