__title__ = 'PortalGun'
__author__ = 'Jakkee'
__version__ = '1.0'
 
import clr
clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import UnityEngine
import Fougerite

 
class PortalGun:
#    def On_PluginInit(self):
#        if not Plugin.IniExists("Settings"):
#            Plugin.CreateIni("Settings")
#            ini = Plugin.GetIni("Settings")
#            ini.AddSetting("Settings", "Moderators can use", "true")
#            ini.Save()
#        DataStore.Flush("PortalGun")
#        ini = Plugin.GetIni("Settings")
#        DataStore.Add("PortalGun", "ModsCanUse", ini.GetSetting("Settings", "Moderators can use"))
#
    def On_Command(self, Player, cmd, args):
        if cmd == "p":
            if len(args) == 0:
                if Player.Admin:
                    target = len(UnityEngine.Physics.RaycastAll(Player.PlayerClient.controllable.character.eyesRay))
                    if target > 0:
                        Player.Message("Hit")
                        #UnityEngine.Debug.DrawRay(Player.PlayerClient.controllable.character.eyesRay)
                    else:
                        Player.Message("Get better aim fool!")
                else:
                    Player.Message("You are not allowed to use that command!")
            else:
                Player.Message("usage: /p")
        elif cmd == "gs":
            if Player.Admin:
                Player.Message(str(UnityEngine.Physics.gravity))
                UnityEngine.Physics.gravity = Util.CreateVector(float(0), float(0), float(0))
                Player.Message(str(UnityEngine.Physics.gravity))
        elif cmd == "gr":
            if Player.Admin:
                Player.Message(str(UnityEngine.Physics.gravity))
                UnityEngine.Physics.gravity = Util.CreateVector(float(0), float(-9.8), float(0))
                Player.Message(str(UnityEngine.Physics.gravity))
