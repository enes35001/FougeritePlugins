__title__ = 'Voter'
__author__ = 'Jakkee'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")
import Fougerite


class Voter:

    RS = None
    #TRS = None
    RSL = None

    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "ShowVoteMessage", "true")
            ini.AddSetting("Settings", "Message", "Type /reward to vote for our server and collect a reward!")
            ini.AddSetting("Settings", "LogTimedOutConnection", "true")
            ini.AddSetting("Settings", "Rust-Servers", "http://rust-servers.net/MYSERVER")
            ini.AddSetting("Settings", "TopRustServers", "Currently not available")
            ini.AddSetting("Settings", "Rust-Serverlist", "http://www.rust-serverlist.net/MYSERVER")
            ini.AddSetting("Rust-Servers", "ServerKey", "")
            ini.AddSetting("TopRustServer", "API key", "Currently not available")
            ini.AddSetting("Rust-Serverlist", "ServerID", "")
            ini.AddSetting("Rust-Serverlist", "APIKey", "")
            ini.AddSetting("Rewards", "UseEconomy", "true")
            ini.AddSetting("Rewards", "EconomyGiveAmount", "250")
            ini.AddSetting("Rewards", "UseKit", "false")
            ini.AddSetting("Rewards", "Item0", "P250")
            ini.AddSetting("Rewards", "Qty0", "1")
            ini.AddSetting("Rewards", "Item1", "9mm Ammo")
            ini.AddSetting("Rewards", "Qty1", "50")
            ini.AddSetting("Rewards", "Item2", "")
            ini.AddSetting("Rewards", "Qty2", "")
            ini.AddSetting("Rewards", "Item3", "")
            ini.AddSetting("Rewards", "Qty3", "")
            ini.AddSetting("Rewards", "Item4", "")
            ini.AddSetting("Rewards", "Qty4", "")
            ini.Save()
        DataStore.Flush("Voter")
        self.RS = None
        #self.TRS = None
        self.RSL = None
        ini = Plugin.GetIni("Settings")
        DataStore.Add("Voter", "ShowMessage", ini.GetSetting("Settings", "ShowVoteMessage"))
        DataStore.Add("Voter", "MSG", ini.GetSetting("Settings", "Message"))
        DataStore.Add("Voter", "LogTimedOut", ini.GetSetting("Settings", "LogTimedOutConnection"))
        DataStore.Add("Voter", "RSlink", ini.GetSetting("Settings", "Rust-Servers"))
        #DataStore.Add("Voter", "TRSlink", ini.GetSetting("Settings", "TopRustServers"))
        DataStore.Add("Voter", "RSLlink", ini.GetSetting("Settings", "Rust-Serverlist"))
        DataStore.Add("Voter", "RS", ini.GetSetting("Rust-Servers", "ServerKey"))
        #DataStore.Add("Voter", "TRS", ini.GetSetting("TopRustServer", "API key"))
        DataStore.Add("Voter", "RSLI", ini.GetSetting("Rust-Serverlist", "ServerID"))
        DataStore.Add("Voter", "RSLA", ini.GetSetting("Rust-Serverlist", "APIKey"))
        DataStore.Add("Voter", "UseEcon", ini.GetSetting("Rewards", "UseEconomy"))
        DataStore.Add("Voter", "Econ", ini.GetSetting("Rewards", "EconomyGiveAmount"))
        DataStore.Add("Voter", "UseKit", ini.GetSetting("Rewards", "UseKit"))
        DataStore.Add("Voter", "I0", ini.GetSetting("Rewards", "Item0"))
        DataStore.Add("Voter", "Q0", ini.GetSetting("Rewards", "Qty0"))
        DataStore.Add("Voter", "I1", ini.GetSetting("Rewards", "Item1"))
        DataStore.Add("Voter", "Q1", ini.GetSetting("Rewards", "Qty1"))
        DataStore.Add("Voter", "I2", ini.GetSetting("Rewards", "Item2"))
        DataStore.Add("Voter", "Q2", ini.GetSetting("Rewards", "Qty2"))
        DataStore.Add("Voter", "I3", ini.GetSetting("Rewards", "Item3"))
        DataStore.Add("Voter", "Q3", ini.GetSetting("Rewards", "Qty3"))
        DataStore.Add("Voter", "I4", ini.GetSetting("Rewards", "Item4"))
        DataStore.Add("Voter", "Q4", ini.GetSetting("Rewards", "Qty4"))

    def prize(self, Player):
        if DataStore.Get("Voter", "UseEcon") == "true":
            self.giveEcon(Player, DataStore.Get("Voter", "Econ"))
        if DataStore.Get("Voter", "UseKit") == "true":
            if DataStore.Get("Voter", "I0") is not None and DataStore.Get("Voter", "Q0") is not None:
                Player.Inventory.AddItem(DataStore.Get("Voter", "I0"), int(DataStore.Get("Voter", "Q0")))
            if DataStore.Get("Voter", "I1") is not None and DataStore.Get("Voter", "Q1") is not None:
                Player.Inventory.AddItem(DataStore.Get("Voter", "I1"), int(DataStore.Get("Voter", "Q1")))
            if DataStore.Get("Voter", "I2") is not None and DataStore.Get("Voter", "Q2") is not None:
                Player.Inventory.AddItem(DataStore.Get("Voter", "I2"), int(DataStore.Get("Voter", "Q2")))
            if DataStore.Get("Voter", "I3") is not None and DataStore.Get("Voter", "Q3") is not None:
                Player.Inventory.AddItem(DataStore.Get("Voter", "I3"), int(DataStore.Get("Voter", "Q3")))
            if DataStore.Get("Voter", "I4") is not None and DataStore.Get("Voter", "Q4") is not None:
                Player.Inventory.AddItem(DataStore.Get("Voter", "I4"), int(DataStore.Get("Voter", "Q4")))

    def giveEcon(self, Player, amount):
        Player.MessageFrom(DataStore.Get("iConomy", "SysName"), "You magically found " + amount + DataStore.Get("iConomy", "MoneyMark"))
        m = self.GetMoney(Player.SteamID)
        DataStore.Add("iConomy", Player.SteamID, m + float(amount))

    def GetMoney(self, id):
        if DataStore.ContainsKey("iConomy", id):
            m = DataStore.Get("iConomy", id)
        else:
            m = DataStore.Get("iConomy", "DefaultMoney")
            DataStore.Add("iConomy", id, float(m))
        return float(m)

    def getvote(self, Player):
        if not DataStore.Get("Voter", "RS") == "":
            try:
                self.RS = Web.GET("http://rust-servers.net/api/?object=votes&element=claim&key=" + DataStore.Get("Voter", "RS") + "&steamid=" + Player.SteamID)
            except:
                if DataStore.Get("Voter", "LogTimedOut") == "true":
                    self.log(Player)
        """if not DataStore.Get("Voter", "TRS") == "":
            try:
                self.TRS = Web.GET("http://api.toprustservers.com/api/get?plugin=voter&key=" + DataStore.Get("Voter", "TRS") + "&uid=" + Player.SteamID)
            except:
                if DataStore.Get("Voter", "LogTimedOut") == "true":
                    self.log(Player)"""
        if not DataStore.Get("Voter", "RSLI") == "":
            try:
                self.RSL = Web.GET("http://www.rust-serverlist.net/api.php?sid=" + DataStore.Get("Voter", "RSLI") + "&apikey=" + DataStore.Get("Voter", "RSLA") + "&uid=" + Player.SteamID + "&mode=vote")
            except:
                if DataStore.Get("Voter", "LogTimedOut") == "true":
                    self.log(Player)
        return True

    def sendvote(self, Player):
        if not DataStore.Get("Voter", "RS") == "":
            try:
                self.RS = Web.GET("http://rust-servers.net/api/?action=post&element=claim&key=" + DataStore.Get("Voter", "RS") + "&steamid=" + Player.SteamID)
            except:
                if DataStore.Get("Voter", "LogTimedOut") == "true":
                    self.log(Player)
        """if not DataStore.Get("Voter", "TRS") == "":
            try:
                self.TRS = Web.GET("http://api.toprustservers.com/api/put?plugin=voter&key=" + DataStore.Get("Voter", "TRS") + "&uid=" + Player.SteamID)
            except:
                if DataStore.Get("Voter", "LogTimedOut") == "true":
                    self.log(Player)"""
        if not DataStore.Get("Voter", "RSLI") == "":
            try:
                self.RSL = Web.GET("http://www.rust-serverlist.net/api.php?sid=" + DataStore.Get("Voter", "RSLI") + "&apikey=" + DataStore.Get("Voter", "RSLA") + "&uid=" + Player.SteamID + "&mode=claimed")
            except:
                if DataStore.Get("Voter", "LogTimedOut") == "true":
                    self.log(Player)
        return True

    def log(self, Player):
        if not Plugin.IniExists("ConnectionLog"):
            Plugin.CreateIni("ConnectionLog").Save()
        Plugin.GetIni("ConnectionLog").AddSetting("Timed out connections", "[" + Plugin.GetDate() + "|" + Plugin.GetTime() + " ]", "[ SteamID: " + Player.SteamID + ". Name: " + Player.Name + "]").Save()

    def On_PlayerConnected(self, Player):
        try:
            if DataStore.Get("Voter", "ShowMessage") == "true":
                Player.Message(DataStore.Get("Voter", "MSG"))
        except:
            pass

    def On_Command(self, Player, cmd, args):
        if cmd == "reward":
            if len(args) == 0:
                Player.Message("/reward vote - Voting links so you can vote and get a prize")
                Player.Message("/reward check - Checks to see if you have voted within the last 24 hours")
                Player.Message("/reward claim - Never fear, your prize is here!")
            elif len(args) == 1:
                if args[0] == "vote":
                    if DataStore.Get("Voter", "RS") is not None:
                        Player.Message("Vote here: " + DataStore.Get("Voter", "RSlink"))
                    #if DataStore.Get("Voter", "TRS") is not None:
                        #Player.Message("Vote here: " + DataStore.Get("Voter", "TRSlink"))
                    if DataStore.Get("Voter", "RSL") is not None:
                        Player.Message("Vote here: " + DataStore.Get("Voter", "RSLlink"))
                elif args[0] == "check":
                    Player.Message("Searching for votes...")
                    if self.getvote(Player):
                        if DataStore.Get("Voter", "RS") is not None:
                            if self.RS == "0":
                                Player.Message("You have not voted at: Rust-Servers within the last 24 hours!")
                            elif self.RS == "1":
                                Player.Message("You voted at: Rust-Servers but you have not claimed your prize!")
                            elif self.RS == "2":
                                Player.Message("You have voted at: Rust-Servers within the last 24 hours and claimed your prize")
                        #if DataStore.Get("Voter", "TRS") is not None:
                            #if self.TRS == "0":
                                #Player.Message("You have not voted at: TopRustServers within the last 24 hours!")
                            #elif self.TRS == "1":
                                #Player.Message("You have voted at: TopRustServers within the last 24 hours and may have claimed your prize")
                        if DataStore.Get("Voter", "RSL") is not None:
                            if self.RSL == "0":
                                Player.Message("You have not voted at: Rust-Serverlist within the last 24 hours!")
                            elif self.RSL == "1":
                                Player.Message("You voted at: Rust-Serverlist but you have not claimed your prize!")
                            elif self.RSL == "2":
                                Player.Message("You have voted at: Rust-Serverlist within the last 24 hours and claimed your prize")
                        self.RS = None
                        #self.TRS = None
                        self.RSL = None
                    else:
                        Player.Message("Try again in a minute")
                elif args[0] == "claim":
                    if self.getvote(Player):
                        count = 0
                        if DataStore.Get("Voter", "RS") is not None:
                            if self.RS == "1":
                                count += 1
                                self.prize(Player)
                        #if DataStore.Get("Voter", "TRS") is not None:
                            #if self.TRS == "0":
                                count += 1
                                #self.prize(Player)
                        if DataStore.Get("Voter", "RSL") is not None:
                            if self.RSL == "1":
                                count += 1
                                self.prize(Player)
                        if count == 0:
                            Player.Message("You have nothing to claim!")
                        else:
                            Player.Message("You have claimed your prizes!")
                    else:
                        Player.Message("Try again in a minute")
                else:
                    Player.Message("/reward vote - Voting links so you can vote and get a prize")
                    Player.Message("/reward check - Checks to see if you have voted within the last 24 hours")
                    Player.Message("/reward claim - Never fear, your prize is here!")
            else:
                Player.Message("/reward vote - Voting links so you can vote and get a prize")
                Player.Message("/reward check - Checks to see if you have voted within the last 24 hours")
                Player.Message("/reward claim - Never fear, your prize is here!")