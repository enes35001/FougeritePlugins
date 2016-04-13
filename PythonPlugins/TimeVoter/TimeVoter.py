__title__ = 'TimeVoter'
__author__ = 'Jakkee'
__version__ = '1.1.1'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import System


class TimeVoter:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "Percentage Needed", "60%")
            ini.AddSetting("Config", "Cooldown in seconds", "60")
            ini.AddSetting("Config", "VoteTime in seconds", "60")
            ini.AddSetting("Config", "Moderators can use", "true")
            ini.Save()
        DataStore.Flush("VoteDay")
        DataStore.Flush("VoteNight")
        DataStore.Flush("Voter")
        DataStore.Flush("TimeVoter")
        DataStore.Flush("RIGGED")
        self.killtimer("VotingTimer")
        ini = Plugin.GetIni("Settings")
        DataStore.Add("TimeVoter", "Mods", ini.GetSetting("Config", "Moderators can use"))
        i = self.cn(ini.GetSetting("Config", "VoteTime in seconds"))
        if i is not None:
            DataStore.Add("TimeVoter", "VoteTime", i * 1000)
        else:
            DataStore.Add("TimeVoter", "Cooldown", 60000)
        i = self.cn(ini.GetSetting("Config", "Cooldown in seconds"))
        if i is not None:
            DataStore.Add("TimeVoter", "Cooldown", i * 1000)
        else:
            DataStore.Add("TimeVoter", "Cooldown", 60000)
        i = self.cn(ini.GetSetting("Config", "Percentage Needed").Replace("%", ""))
        if i is not None:
            DataStore.Add("TimeVoter", "Min", i)
        else:
            DataStore.Add("TimeVoter", "Min", 50)

    def isMod(self, Player):
        if Player.Admin:
            return True
        elif DataStore.ContainsKey("Moderators", Player.SteamID):
            if DataStore.Get("TimeVoter", "Mods") == "true":
                return True
        return False


    def killtimer(self, name):
        timer = Plugin.GetTimer(name)
        if timer is None:
            return
        timer.Stop()
        Plugin.Timers.Remove(name)

    def cn(self, arg):
        try:
            i = int(arg)
            return i
            #Return number from string
        except:
            return None
            #Return None when string is not a number

    def checkstringifnumber(self, arg):
        try:
            b = int(arg)
            if b > 24 or b < 1:
                return 101
                #returns 101 when number is less than 1 or greater than 24
            return b
            #returns a number between 1 - 24 (includes 1 and 24)
        except:
            return 100
            #returns 100 when string is not a number

    def On_PlayerDisconnected(self, Player):
        try:
            if DataStore.Get("VoteNight", Player.SteamID) == "night":
                DataStore.Remove("VoteNight", Player.SteamID)
            elif DataStore.Get("VoteDay", Player.SteamID) == "day":
                DataStore.Remove("VoteDay", Player.SteamID)
        except:
            pass

    def VotingTimerCallback(self):
        DataStore.Add("TimeVoter", "SysTick", System.Environment.TickCount)
        self.killtimer("VotingTimer")
        if DataStore.Get("RIGGED", "VOTER") == "night":
            DataStore.Remove("RIGGED", "VOTER")
            Server.Broadcast("--------------------------- [color green]TimeVoter[/color] ---------------------------")
            Server.Broadcast("The results are in and the servers time has not been changed!")
            Server.Broadcast("85.0% voted for Night")
            Server.Broadcast("--------------------------------------------------------------------")
            self.removevotes()
            return
        elif DataStore.Get("RIGGED", "VOTER") == "day":
            DataStore.Remove("RIGGED", "VOTER")
            World.Time = 6
            Server.Broadcast("--------------------------- [color green]TimeVoter[/color] ---------------------------")
            Server.Broadcast("The results are in and the servers time has been changed to Day!")
            Server.Broadcast("85.0% voted for Day")
            Server.Broadcast("--------------------------------------------------------------------")
            self.removevotes()
            return
        else:
            day = float(DataStore.Count("VoteDay"))
            night = float(DataStore.Count("VoteNight"))
            min = float(DataStore.Get("TimeVoter", "Min"))
            total = float(day + night)
            if round((day / total) * 100, 2) > min:
                World.Time = 6
                Server.Broadcast("--------------------------- [color green]TimeVoter[/color] ---------------------------")
                Server.Broadcast("The results are in and the servers time has been changed to Day!")
                Server.Broadcast(str(round((day / total) * 100, 2)) + "% voted for Day")
                Server.Broadcast("--------------------------------------------------------------------")
                self.removevotes()
            else:
                Server.Broadcast("--------------------------- [color green]TimeVoter[/color] ---------------------------")
                Server.Broadcast("The results are in and the servers time has not been changed!")
                Server.Broadcast(str(round((night / total) * 100, 2)) + "% voted for Night")
                Server.Broadcast("--------------------------------------------------------------------")
                self.removevotes()

    def removevotes(self):
        DataStore.Flush("RIGGED")
        DataStore.Flush("VoteDay")
        DataStore.Flush("VoteNight")
        DataStore.Flush("Voter")

    def On_Command(self, Player, cmd, args):
        if cmd == "vote":
            if len(args) == 0:
                Player.Message("--- TimeVoter ---")
                Player.Message("/vote - Shows help")
                Player.Message("/vote start - Starts a vote")
                Player.Message("/vote day - Votes for day")
                Player.Message("/vote night - votes for night")
                if Player.Admin or self.isMod(Player):
                    Player.Message("-Admin Commands-")
                    Player.Message("/vote stop - Stops the current vote (useful if something goes wrong)")
                    Player.Message("/vote rig [day/night] - Rigs the voting")
                    Player.Message("/settime [time] - Sets the time")
            elif len(args) == 1:
                if args[0] == "stop":
                    if self.isMod(Player):
                        if DataStore.Get("Voter", "Started") == "true":
                            DataStore.Remove("Voter", "Started")
                            self.killtimer("VotingTimer")
                            self.removevotes()
                            Server.Broadcast("--------------------------- [color green]TimeVoter[/color] ---------------------------")
                            Server.Broadcast("An [color cyan]Admin[/color] has cancelled voting to change the servers time!")
                            Server.Broadcast("This could of been for a number of reasons")
                            Server.Broadcast("Please do not question or complain to the server staff")
                            Server.Broadcast("--------------------------------------------------------------------")
                        else:
                            Player.Message("There is no vote running!")
                    else:
                        Player.Message("You are not allowed to use that command!")
                elif args[0] == "start":
                    if not DataStore.Get("Voter", "Started") == "true":
                        waittime = DataStore.Get("TimeVoter", "Cooldown")
                        time = DataStore.Get("TimeVoter", "SysTick")
                        if time is None:
                            time = 0
                        else:
                            time = int(time)
                        calc = System.Environment.TickCount - time
                        if calc >= waittime or self.isMod(Player):
                            DataStore.Add("Voter", "Started", "true")
                            Plugin.CreateTimer("VotingTimer", int(DataStore.Get("TimeVoter", "VoteTime"))).Start()
                            Server.Broadcast("--------------------------- [color green]TimeVoter[/color] ---------------------------")
                            Server.Broadcast(Player.Name + " has started a vote to change the servers time!")
                            Server.Broadcast("How to vote: /vote [day/night]")
                            Server.Broadcast("You have 60 seconds to vote")
                            Server.Broadcast("--------------------------------------------------------------------")
                            DataStore.Add("VoteDay", Player.SteamID, "day")
                            Player.Message("You have voted for Day!")
                        else:
                            workingout = (round(waittime / 1000, 2) / 60) - round(int(calc) / 1000, 2) / 60
                            current = round(workingout, 2)
                            Player.Message(str(current) + " Minutes remaining before you can use this.")
                    else:
                        Player.Message("There is already a vote in progress")

                elif args[0] == "day":
                    if DataStore.Get("Voter", "Started") == "true":
                        if DataStore.Get("VoteNight", Player.SteamID) == "night":
                            DataStore.Remove("VoteNight", Player.SteamID)
                            DataStore.Add("VoteDay", Player.SteamID, "day")
                            Player.Message("You have changed your vote to Day")
                        elif DataStore.Get("VoteDay", Player.SteamID) == "day":
                            Player.Message("You have already voted for Day")
                        else:
                            DataStore.Add("VoteDay", Player.SteamID, "day")
                            Player.Message("You have voted for Day!")
                    else:
                        Player.Message("There is no vote in progress!")
                        Player.Message("usage: /vote start")
                elif args[0] == "night":
                    if DataStore.Get("Voter", "Started") == "true":
                        if DataStore.Get("VoteDay", Player.SteamID) == "day":
                            DataStore.Remove("VoteDay", Player.SteamID)
                            DataStore.Add("VoteNight", Player.SteamID, "night")
                            Player.Message("You have changed your vote to Night")
                        elif DataStore.Get("VoteNight", Player.SteamID) == "night":
                            Player.Message("You have already voted for Night")
                        else:
                            DataStore.Add("VoteNight", Player.SteamID, "night")
                            Player.Message("You have voted for Night!")
                    else:
                        Player.Message("There is no vote in progress!")
                        Player.Message("usage: /vote start")
            elif len(args) == 2:
                if args[0] == "rig":
                    if self.isMod(Player):
                        if args[1] == "day":
                            if DataStore.Get("Voter", "Started") == "true":
                                if DataStore.Get("RIGGED", "VOTER") == "night":
                                    DataStore.Remove("RIGGED", "VOTER")
                                    DataStore.Add("RIGGED", "VOTER", "day")
                                    Player.Message("You have rigged the vote to Day")
                                elif DataStore.Get("RIGGED", "VOTER") == "day":
                                    Player.Message("The vote was already rigged to Day")
                                else:
                                    DataStore.Add("RIGGED", "VOTER", "day")
                                    Player.Message("The vote is now rigged to Day")
                            else:
                                Player.Message("There is no vote in progress!")
                                Player.Message("usage: /vote start")
                        elif args[1] == "night":
                            if DataStore.Get("Voter", "Started") == "true":
                                if DataStore.Get("RIGGED", "VOTER") == "day":
                                    DataStore.Remove("RIGGED", "VOTER")
                                    DataStore.Add("RIGGED", "VOTER", "night")
                                    Player.Message("You have rigged the vote to Night")
                                elif DataStore.Get("RIGGED", "VOTER") == "night":
                                    Player.Message("The vote was already rigged to Night")
                                else:
                                    DataStore.Add("RIGGED", "VOTER", "night")
                                    Player.Message("The vote is now rigged to Night")
                            else:
                                Player.Message("There is no vote in progress!")
                                Player.Message("usage: /vote start")
                        else:
                            Player.Message("usage: /vote rig [day/night]")
                    else:
                        Player.Message("You are not allowed to use this command!")
        elif cmd == "settime":
            if self.isMod(Player):
                if len(args) == 0:
                    Player.Message("usage: /settime [time]")
                elif len(args) == 1:
                    time = self.checkstringifnumber((args[0]))
                    if time == 100:
                        Player.Message("You have not used a number, Try again")
                    elif time == 101:
                        Player.Message("You can only use a number from 1 - 24")
                    else:
                        World.Time = time
                        Server.Broadcast("--------------------------- [color green]TimeVoter[/color] ---------------------------")
                        Server.Broadcast("The server staff has changed the time!")
                        Server.Broadcast("The servers time has been set to: " + str(time) + " (24 hour time)")
                        Server.Broadcast("--------------------------------------------------------------------")
                else:
                    Player.Message("usage: /settime [number]")
            else:
                Player.Message("You are not allowed to use this command!")
