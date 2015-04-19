__title__ = 'Notice'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class Notice:
    def On_PlayerConnected(self, Player):
        Util.Log("Blahh")
        #Player.SendCommand("deathscreen.reason " + '"' + "              WELCOME TO XHTs DEV SERVER!                         We test plugins on here first!                                    Developed by Jakkee. (Also you're not dead)" + '"')
        #Player.SendCommand("deathscreen.show")
