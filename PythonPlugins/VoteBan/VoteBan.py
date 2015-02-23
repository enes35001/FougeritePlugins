__title__ = 'VoteBan'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class VoteBan:

#Storing these here so if the player disconnects it doesn't matter
    target = None
    targetname = None
    targetid = None
    targetip = None

    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "Moderators bannable", "false")
            ini.AddSetting("Config", "Admins bannable", "false")
            ini.Save()
        if self.target is not None:
            Server.Broadcast("--------------------------- [color green]VoteBan[/color] ---------------------------")
            Server.Broadcast("Server has reloaded and cancelled voting to ban [color red]" + self.targetname + "[/color]")
            Server.Broadcast("Please do not question or complain to the server staff")
            Server.Broadcast("--------------------------------------------------------------------")
            self.removetarget()
        DataStore.Flush("VoteBanY")
        DataStore.Flush("VoteBanN")
        DataStore.Flush("RIGGED")
        self.killtimer("VoteBanTimer")


    def isMod(self, id):
        try:
            if DataStore.ContainsKey("Moderators", id):
                if Plugin.GetIni("Settings").GetSetting("Config", "Moderators can be banned?") == "true":
                    return True
                else:
                    return False
            else:
                return False
        except:
            pass

    def isAdmin(self, Player):
        try:
            if Player.Admin:
                if Plugin.GetIni("Settings").GetSetting("Config", "Admins can be banned?") == "true":
                    return True
                else:
                    return False
            else:
                return False
        except:
            pass

    def killtimer(self, name):
        timer = Plugin.GetTimer(name)
        if timer is None:
            return
        timer.Stop()
        Plugin.Timers.Remove(name)

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
            Player.Message("Couldn't find " + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.Message("Found " + str(count) + " players with similar name!")
            Player.Message("Use quotation marks if the name has a space in it.")
            return None

    def removetarget(self):
            self.target = None
            self.targetname = None
            self.targetid = None
            self.targetip = None

    def disconnectplayer(self):
        try:
            self.target.Disconnect()
        except:
            pass

    def logban(self, reason):
        try:
            if not Plugin.IniExists("Bans"):
                Plugin.CreateIni("Bans")
                ini = Plugin.GetIni("Bans")
                ini.Save()
            ini = Plugin.GetIni("Bans")
            ini.AddSetting("BannedIPS", self.targetip, self.targetname + " [" + Plugin.GetDate() + "|" + Plugin.GetTime() + "]  INFO: " + reason)
            ini.AddSetting("BannedIDS", self.targetid, self.targetname + " [" + Plugin.GetDate() + "|" + Plugin.GetTime() + "] INFO: " + reason)
            ini.Save()
            self.disconnectplayer()
            self.removetarget()
        except:
            pass

    def On_PlayerConnected(self, Player):
        if self.isbanned(Player):
            Player.MessageFrom("BANNED", "[color red] - YOU ARE BANNED! - [/color]")
            Player.MessageFrom("BANNED", "[color red] - YOU ARE BANNED! - [/color]")
            Player.MessageFrom("BANNED", "[color red] - YOU ARE BANNED! - [/color]")
            Player.MessageFrom("BANNED", "[color red] - YOU ARE BANNED! - [/color]")
            Player.Disconnect()

    def isbanned(self, Player):
        try:
            if not Plugin.IniExists("Bans"):
                Plugin.CreateIni("Bans")
                ini = Plugin.GetIni("Bans")
                ini.Save()
            bans = Plugin.GetIni("Bans")
            if bans.GetSetting("BannedIPS", Player.IP) or bans.GetSetting("BannedIPS", Player.SteamID):
                return True
            else:
                return False
        except:
            return False

    def On_PlayerDisconnected(self, Player):
        try:
            if DataStore.Get("VoteBanY", Player.SteamID) == "yes":
                DataStore.Remove("VoteBanY", Player.SteamID)
            elif DataStore.Get("VoteBanN", Player.SteamID) == "no":
                DataStore.Remove("VoteBanN", Player.SteamID)
        except:
            pass

    def VoteBanTimerCallback(self):
        self.killtimer("VoteBanTimer")
        if DataStore.Get("RIGGED", "VOTER") == "yes":
            DataStore.Remove("RIGGED", "VOTER")
            Server.Broadcast("--------------------------- [color green]VoteBan[/color] ---------------------------")
            Server.Broadcast("The results are in and [color red]" + self.targetname + " [/color]has been banned from the server!")
            Server.Broadcast("93.0% voted for yes!")
            Server.Broadcast("--------------------------------------------------------------------")
            self.logban("Rigged vote for Yes")
            self.removevotes()
            return
        elif DataStore.Get("RIGGED", "VOTER") == "no":
            DataStore.Remove("RIGGED", "VOTER")
            Server.Broadcast("--------------------------- [color green]VoteBan[/color] ---------------------------")
            Server.Broadcast("The results are in and [color red]" + self.targetname + " [/color]has not been banned from the server!")
            Server.Broadcast("85.0% voted for no!")
            Server.Broadcast("--------------------------------------------------------------------")
            self.removevotes()
            return
        else:
            yes = DataStore.Count("VoteBanY")
            no = DataStore.Count("VoteBanN")
            total = yes + no
            if yes > no:
                Server.Broadcast("--------------------------- [color green]VoteBan[/color] ---------------------------")
                Server.Broadcast("The results are in and [color red]" + self.targetname + " [/color]has been banned from the server!")
                Server.Broadcast(str(round((yes / total) * 100, 2)) + "% voted for yes")
                Server.Broadcast("--------------------------------------------------------------------")
                self.logban(str(round((yes / total) * 100, 2)) + "% voted for yes")
                self.removevotes()
            elif yes < no:
                Server.Broadcast("--------------------------- [color green]VoteBan[/color] ---------------------------")
                Server.Broadcast("The results are in and [color red]" + self.targetname + " [/color]has not been banned from the server!")
                Server.Broadcast(str(round((no / total) * 100, 2)) + "% voted for no")
                Server.Broadcast("--------------------------------------------------------------------")
                self.removevotes()
            elif yes == 0 and no == 0:
                Server.Broadcast("--------------------------- [color green]VoteBan[/color] ---------------------------")
                Server.Broadcast("[color red]" + self.targetname + " [/color]has not been banned!")
                Server.Broadcast("No one voted for [color red]" + self.targetname + " [/color]to be banned!")
                Server.Broadcast("--------------------------------------------------------------------")
            else:
                Server.Broadcast("--------------------------- [color green]VoteBan[/color] ---------------------------")
                Server.Broadcast("The results are in and [color red]" + self.targetname + " [/color]has not been banned from the server!")
                Server.Broadcast("50% voted for yes")
                Server.Broadcast("50% voted for no")
                Server.Broadcast("--------------------------------------------------------------------")
                self.removevotes()

    def removevotes(self):
        try:
            #Might throw an error if a player leaves the server while removing votes, I don't think it would but you can never be sure
            DataStore.Flush("VoteBanY")
            DataStore.Flush("VoteBanN")
            DataStore.Flush("RIGGED")
            self.killtimer("VoteBanTimer")
        except:
            pass

    def On_Command(self, Player, cmd, args):
        if cmd == "vban":
            if len(args) == 0:
                if Player.Admin:
                    Player.Message("---- VoteBan ----")
                    Player.Message("/vban - Shows help")
                    Player.Message("/voteban [Name] - Starts a vote")
                    Player.Message("/vban yes - Votes for yes")
                    Player.Message("/vban no - votes for no")
                    Player.Message("/vban stop - Stops the current vote (useful if something goes wrong)")
                    Player.Message("/vban rig [yes/no] - Rigs the voting")
                else:
                    Player.Message("---- VoteBan ----")
                    Player.Message("/vban - Shows help")
                    Player.Message("/voteban [Name] - Starts a vote")
                    Player.Message("/vban yes - Votes for yes")
                    Player.Message("/vban no - votes for no")
            elif len(args) == 1:
                if args[0] == "stop":
                    if Player.Admin:
                        if Plugin.GetTimer("VoteBanTimer"):
                            DataStore.Remove("VoterBan", "Started")
                            self.killtimer("VoteBanTimer")
                            Server.Broadcast("--------------------------- [color green]VoteBan[/color] ---------------------------")
                            Server.Broadcast("An Admin has cancelled voting to ban [color red]" + self.target + "[/color]")
                            Server.Broadcast("This could of been for a number of reasons")
                            Server.Broadcast("Please do not question or complain to the server staff")
                            Server.Broadcast("--------------------------------------------------------------------")
                            self.removetarget()
                            self.removevotes()
                        else:
                            Player.Message("There is no vote running!")
                    else:
                        Player.Message("You are not allowed to use that command!")
                elif args[0] == "yes":
                    if Plugin.GetTimer("VoteBanTimer"):
                        if DataStore.Get("VoteBanN", Player.SteamID) == "no":
                            DataStore.Remove("VoteBanN", Player.SteamID)
                            DataStore.Add("VoteBanY", Player.SteamID, "yes")
                            Player.Message("You have changed your vote to yes")
                        elif DataStore.Get("VoteBanY", Player.SteamID) == "yes":
                            Player.Message("You have already voted for yes")
                        else:
                            DataStore.Add("VoteBanY", Player.SteamID, "yes")
                            Player.Message("You have voted for yes!")
                    else:
                        Player.Message("There is no vote in progress!")
                        Player.Message("usage: /voteban [name]")
                elif args[0] == "no":
                    if Plugin.GetTimer("VoteBanTimer"):
                        if DataStore.Get("VoteBanY", Player.SteamID) == "yes":
                            DataStore.Remove("VoteBanY", Player.SteamID)
                            DataStore.Add("VoteBanN", Player.SteamID, "no")
                            Player.Message("You have changed your vote to no")
                        elif DataStore.Get("VoteBanN", Player.SteamID) == "no":
                            Player.Message("You have already voted for no")
                        else:
                            DataStore.Add("VoteBanN", Player.SteamID, "no")
                            Player.Message("You have voted for no!")
                    else:
                        Player.Message("There is no vote in progress!")
                        Player.Message("usage: /voteban [name]")
            elif len(args) == 2:
                if args[0] == "rig":
                    if Player.Admin:
                        if args[1] == "yes":
                            if Plugin.GetTimer("VoteBanTimer"):
                                if DataStore.Get("RIGGED", "VOTER") == "no":
                                    DataStore.Remove("RIGGED", "VOTER")
                                    DataStore.Add("RIGGED", "VOTER", "yes")
                                    Player.Message("You have rigged the vote to yes")
                                elif DataStore.Get("RIGGED", "VOTER") == "yes":
                                    Player.Message("The vote was already rigged to yes")
                                else:
                                    DataStore.Add("RIGGED", "VOTER", "yes")
                                    Player.Message("The vote is now rigged to yes")
                            else:
                                Player.Message("There is no vote in progress!")
                                Player.Message("usage: /voteban [Name]")
                        elif args[1] == "no":
                            if Plugin.GetTimer("VoteBanTimer"):
                                if DataStore.Get("RIGGED", "VOTER") == "yes":
                                    DataStore.Remove("RIGGED", "VOTER")
                                    DataStore.Add("RIGGED", "VOTER", "no")
                                    Player.Message("You have rigged the vote to no")
                                elif DataStore.Get("RIGGED", "VOTER") == "no":
                                    Player.Message("The vote was already rigged to no")
                                else:
                                    DataStore.Add("RIGGED", "VOTER", "no")
                                    Player.Message("The vote is now rigged to no")
                            else:
                                Player.Message("There is no vote in progress!")
                                Player.Message("usage: /voteban [Name]")
                        else:
                            Player.Message("usage: /vban rig [yes/no]")
                    else:
                        Player.Message("You are not allowed to use this command!")
        elif cmd == "voteban":
            if not Plugin.GetTimer("VoteBanTimer"):
                ban = self.CheckV(Player, args[0])
                if ban is not None:
                    if ban.Name is not Player.Name:
                        if self.isMod(ban.SteamID):
                            if self.isAdmin(ban):
                                try:
                                    self.target = ban
                                    self.targetname = ban.Name
                                    self.targetip = ban.IP
                                    self.targetid = ban.SteamID
                                    Plugin.CreateTimer("VoteBanTimer", 60000).Start()
                                    Server.Broadcast("--------------------------- [color green]VoteBan[/color] ---------------------------")
                                    Server.Broadcast(Player.Name + " [/color]has started a vote to ban: [color red]" + ban.Name + "[/color]")
                                    Server.Broadcast("How to vote: [color cyan]/vban [yes/no][/color]")
                                    Server.Broadcast("You have 60 seconds to vote")
                                    Server.Broadcast("--------------------------------------------------------------------")
                                    Server.BroadcastNotice("/vban [yes / no] (Voting for: " + ban.Name + ")")
                                    ban.Message("[color red]If you disconnect you will be banned![/color]")
                                except Exception:
                                    Util.Log("VoteBan version:" + __version__)
                                    Util.Log("VoteBan error caused by starting a vote: " + Exception)
                                    Player.MessageFrom("ERROR", "Try again! or contact server staff!")
                            else:
                                Player.Message("That player can not be banned!")
                        else:
                            Player.Message("That player can not be banned!")
                    else:
                        Player.Message("You can not ban yourself!")
                else:
                    return
            else:
                Player.Message("Only one vote is aloud at a time")
