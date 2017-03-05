__title__ = 'TempMute'
__author__ = 'Jakkee'
__version__ = '1.1.1'

import clr
clr.AddReferenceByName("Fougerite")
import Fougerite, System, sys, re
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")
try:
    import datetime
except ImportError:
    raise ImportError("Missing Extra Libs folder! {DateTime module}")
rustpp = Server.GetRustPPAPI()

class TempMute:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        try:
            count = 0
            for id in DataStore.Keys("TempMute"):
                tick = int(DataStore.Get("TempMute", id).split(",")[0])
                mutetime = int(DataStore.Get("TempMute", id).split(",")[1])
                calc = System.Environment.TickCount - tick
                if calc >= mutetime:
                    rustpp.UnMute(long(id))
                    DataStore.Remove("TempMute", Player.SteamID)
                    count += 1
                else:
                    Data = Plugin.CreateDict()
                    Data["TargetSteamID"] = id
                    Plugin.CreateParallelTimer("UnMute", mutetime - calc, Data).Start()
                    rustpp.Mute(long(id), "Re-Add (ID: " + str(id) + ")")
                continue
            Fougerite.Logger.LogDebug("TempMute: UnMuted " + str(count) + " players")
        except:
            pass

    def On_Command(self, Player, cmd, args):
        if cmd == "tempmute":
            if Player.Moderator or Player.Admin:
                if len(args) >= 2:
                    targetargs = re.findall(r'"([^"]*)"', str.join(" ", args))
                    target = self.CheckV(Player, targetargs)
                    if target is not None:
                        count = 0
                        for s in re.findall(r'\b\d+\b', str.join(" ", args)):
                            s = str.join("", s)
                        mutetime = self.CheckString(s)
                        if mutetime is not None:
                            if not rustpp.IsMuted(long(target.SteamID)):
                                Data = Plugin.CreateDict()
                                Data["TargetSteamID"] = Player.SteamID
                                rustpp.Mute(long(target.SteamID), target.Name)
                                Plugin.CreateParallelTimer("UnMute", mutetime * 1000, Data).Start()
                                DataStore.Add("TempMute", target.SteamID, str(System.Environment.TickCount) + ", " + str(mutetime * 1000))
                                Fougerite.Logger.LogDebug(target.Name + " has been muted by " + Player.Name)
                                mutetime = str(datetime.timedelta(seconds=mutetime))
                                target.MessageFrom("TempMute", "You have been muted for " + mutetime + "seconds!")
                                Server.BroadcastFrom("TempMute", target.Name + "[/color] has been muted for " + mutetime + "seconds, By " + Player.Name)
                            else:
                                Player.MessageFrom("TempMute", target.Name + "[/color] has already been muted!")
                        else:
                            Player.MessageFrom("TempMute", 'Could not find a time to mute for')
                            Player.MessageFrom("TempMute", 'Usage: /tempmute "Player Name" <Seconds>')
                    else:
                        Player.MessageFrom("TempMute", 'Could not find '+ str.join(" ", targetargs))
                        Player.MessageFrom("TempMute", 'Usage: /tempmute "Player Name" <Seconds>')
                        return
                else:
                    Player.MessageFrom("TempMute", 'Usage: /tempmute "Player Name" <Seconds>')
                    Player.MessageFrom("TempMute", 'Example: /tempmute "' + Player.Name + '[/color]" 500')
            else:
                Player.messageFrom("TempMute", "You are not allowed to use this command!")
        elif cmd == "unmute":
            if Player.Moderator or Player.Admin:
                target = self.CheckV(Player, targetargs)
                if target is not None:
                    if DataStore.ContainsSetting("TempMute", target.SteamID):
                        DataStore.Remove("TempMute", Player.SteamID)

    def On_Chat(self, Player, ChatMessage):
        if rustpp.IsMuted(long(Player.SteamID)):
            tick = int(DataStore.Get("TempMute", Player.SteamID).split(",")[0])
            mutetime = int(DataStore.Get("TempMute", Player.SteamID).split(",")[1])
            calc = System.Environment.TickCount - tick
            if calc >= mutetime:
                DataStore.Remove("TempMute", Player.SteamID)
                for timer in Plugin.GetParallelTimer("UnMute"):
                    data = timer.Args
                    if data["TargetSteamID"] == Player.SteamID:
                        timer.Kill()
                        break
                rustpp.UnMute(long(Player.SteamID))
                Fougerite.Logger.LogDebug(Player.Name + " has been unmuted!")
                Player.MessageFrom("TempMute", "You have been unmuted!")
                return True
            else:
                Player.MessageFrom("TempMute", "Time remaining: " + str(datetime.timedelta(seconds= (mutetime-calc) / 1000)))
        else:
            if DataStore.ContainsKey("TempMute", Player.SteamID):
                DataStore.Remove("TempMute", Player.SteamID)
                for timer in Plugin.GetParallelTimer("UnMute"):
                    data = timer.Args
                    if data["TargetSteamID"] == Player.SteamID:
                        timer.Kill()
                        break

    def CheckString(self, arg):
        try:
            number = int(float(str(arg)))
            return number
        except:
            return None

    def UnMuteCallback(self, timer):
        timer.Kill()
        Data = timer.Args
        PlayerID = Data["TargetSteamID"]
        DataStore.Remove("TempMute", PlayerID)
        if rustpp.IsMuted(long(PlayerID)):
            rustpp.UnMute(long(PlayerID))
            try:
                Player = Fougerite.Player.FindBySteamID(PlayerID)
                Fougerite.Logger.LogDebug(Player.Name + " has been unmuted!")
                Player.MessageFrom("TempMute", "You have been unmuted!")
            except:
                pass

    #Method provided by Spoock. Converted to Python by DreTaX
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
            for pl in Server.ActivePlayers:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            return None
        elif count == 1 and p is not None:
            return p
        else:
            #Player.MessageFrom("TempMute", "Found " + str(count) + " players with similar a name. Use a more correct name!")
            return None
    #GetPlayerName provided by DreTaX

    def GetPlayerName(self, name):
        try:
            name = name.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

