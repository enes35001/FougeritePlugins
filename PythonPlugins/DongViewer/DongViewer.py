__title__ = 'DongViewer'
__author__ = 'Jakkee'
__version__ = '1.1.4'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite

class DongViewer:
    def On_PlayerConnected(self, Player):
        Player.SendCommand("censor.nudity False")

    def On_Command(self, Player, cmd, args):
        if cmd == "dongs":
            if len(args) == 0:
                Player.MessageFrom("DongViewer", "Usage: /dongs [on/off]")
            elif len(args) == 1:
                if args[0] == "on":
                    Player.SendCommand("censor.nudity False")
                    Player.MessageFrom("DongViewer", "You can now see dongs")
                elif args[0] == "off":
                    Player.SendCommand("censor.nudity True")
                    Player.MessageFrom("DongViewer", "You can no longer see dongs")
                else:
                    Player.MessageFrom("DongViewer", "Usage: /dongs [on/off]")
            elif len(args) > 1:
                Player.MessageFrom("DongViewer", "Usage: /dongs [on/off]")
