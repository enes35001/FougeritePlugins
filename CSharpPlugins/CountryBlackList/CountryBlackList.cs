using Fougerite;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;

namespace CountryBlackList
{
    public class CountryBlackList : Fougerite.Module
    {
        public bool Show_Accept_Message = true;
        public bool Show_Denied_Message = true;
        public bool Use_WhiteList = true;
        public bool Log_TimedOut_Connections = true;
        public string Join_Message = "%PLAYER% has connected from %COUNTRY%";
        public string Player_Disconnect_Message = "%COUNTRY% is on the servers blacklist";
        public string Server_Disconnect_Message = "%PLAYER% has connected from %COUNTRY% but is blacklisted";
        public string Unknown_Location = "Unknown Location";
        public List<string> BlackList = new List<string> { "TK", "JO" };
        public IniParser Settings;
        public IniParser WhiteList;
        public static System.IO.StreamWriter file;

        public override string Name
        {
            get
            {
                return "CountryBlackList";
            }
        }

        public override string Author
        {
            get
            {
                return "[DEBUG BUILD]Jakkee";
            }
        }

        public override string Description
        {
            get
            {
                return "[DEBUG BUILD]Block any country you wish";
            }
        }

        public override Version Version
        {
            get
            {
                return new Version("3.0.1");
            }
        }

        public override void Initialize()
        {
            //DEBUG
            Logger.Log("Main ID: " + Util.GetUtil().MainThreadID);
            Logger.Log("Current ID: " + Util.GetUtil().CurrentWorkingThreadID);
            //END OF DEBUG
            Hooks.OnCommand += new Hooks.CommandHandlerDelegate(On_Command);
            Hooks.OnPlayerConnected += new Hooks.ConnectionHandlerDelegate(On_PlayerConnected);
            if (!File.Exists(Path.Combine(ModuleFolder, "Settings.ini")))
            {
                File.Create(Path.Combine(ModuleFolder, "Settings.ini")).Dispose();
                Settings = new IniParser(Path.Combine(ModuleFolder, "Settings.ini"));
                Settings.AddSetting("Settings", "Show Accepted Message", "True");
                Settings.AddSetting("Settings", "Show Denied Message", "True");
                Settings.AddSetting("Settings", "Use WhiteList", "True");
                Settings.AddSetting("Settings", "Log TimedOut Connections", "True");
                Settings.AddSetting("BlackList", "BlackListed Countries", "TK, JO");
                Settings.AddSetting("Messages", "Join Message", "%PLAYER% has connected from %COUNTRY%");
                Settings.AddSetting("Messages", "Unknown Location", "Unknown Location");
                Settings.AddSetting("Messages", "Player Disconnect Message", "%COUNTRY% is on the servers blacklist");
                Settings.AddSetting("Messages", "Server Disconnect Message", "%PLAYER% has connected from %COUNTRY% but is blacklisted");
                Settings.Save();
            }
            else
            {
                Settings = new IniParser(Path.Combine(ModuleFolder, "Settings.ini"));
            }
            try
            {
                Show_Accept_Message = Boolean.Parse(Settings.GetSetting("Settings", "Show Accepted Message"));
                Show_Denied_Message = Boolean.Parse(Settings.GetSetting("Settings", "Show Denied Message"));
                Use_WhiteList = Boolean.Parse(Settings.GetSetting("Settings", "Use WhiteList"));
                Log_TimedOut_Connections = Boolean.Parse(Settings.GetSetting("Settings", "Log TimedOut Connections"));
                BlackList = Settings.GetSetting("BlackList", "BlackListed Countries").Replace(" ", "").Split(',').ToList();
                Join_Message = Settings.GetSetting("Messages", "Join Message");
                Player_Disconnect_Message = Settings.GetSetting("Messages", "Player Disconnect Message");
                Server_Disconnect_Message = Settings.GetSetting("Messages", "Server Disconnect Message");
                Unknown_Location = Settings.GetSetting("Messages", "Unknown Location");
            }
            catch
            {
                Logger.LogError("[CountryBlackList] Error in settings.ini, Check your settings & reload! Using default settings for now");
                Show_Accept_Message = true;
                Show_Denied_Message = true;
                Use_WhiteList = true;
                Log_TimedOut_Connections = true;
                Join_Message = "%PLAYER% has connected from %COUNTRY%";
                Player_Disconnect_Message = "%COUNTRY% is on the servers blacklist";
                Server_Disconnect_Message = "%PLAYER% has connected from %COUNTRY% but is blacklisted";
                Unknown_Location = "Unknown Location";
                BlackList = "TK, JO".Replace(" ", "").Split(',').ToList();
    }
            if (!File.Exists(Path.Combine(ModuleFolder, "WhiteList.ini")))
            {
                File.Create(Path.Combine(ModuleFolder, "WhiteList.ini")).Dispose();
                WhiteList = new IniParser(Path.Combine(ModuleFolder, "WhiteList.ini"));
                WhiteList.AddSetting("SteamID", "IP Address", "Players Name");
                WhiteList.AddSetting("76561198135558142", "127.0.0.1", "Xiled Jakkee");
                WhiteList.Save();
            }
            else
            {
                WhiteList = new IniParser(Path.Combine(ModuleFolder, "WhiteList.ini"));
            }
        }

        public override void DeInitialize()
        {
            Hooks.OnCommand -= new Hooks.CommandHandlerDelegate(On_Command);
            Hooks.OnPlayerConnected -= new Hooks.ConnectionHandlerDelegate(On_PlayerConnected);
        }

        public void On_Command(Fougerite.Player player, string cmd, string[] args)
        {
            if (cmd == "wlist")
            {
                if (player.Admin || player.Moderator)
                {
                    if (args.Length.Equals(0))
                    {
                        player.MessageFrom("CountryBlackList", "Usage: /wlist <User Name>");
                        player.MessageFrom("CountryBlackList", "Adds a user to the whitelist");
                    }
                    else
                    {
                        string search = string.Join(" ", args);
                        Fougerite.Player target = Fougerite.Server.GetServer().FindPlayer(search);
                        if (target != null)
                        {
                            if (!OnWhiteList(player.SteamID, player.IP))
                            {
                                WhiteList.AddSetting(target.SteamID, target.IP, target.Name);
                                WhiteList.Save();
                                player.MessageFrom("CountryBlackList", "You have added " + target.Name + " to the whitelist");
                            }
                            else
                            {
                                player.MessageFrom("CountryBlackList", target.Name + " is already on the whitelist!");
                            }
                        }
                    }
                }
                else
                {
                    player.MessageFrom("CountryBlackList", "You are not allowed to use this command!");
                }
            }
            else if (cmd == "dlist")
            {
                if (player.Admin || player.Moderator)
                {
                    if (args.Length.Equals(0))
                    {
                        player.MessageFrom("CountryBlackList", "Usage: /dlist <User Name>");
                        player.MessageFrom("CountryBlackList", "Removes a user from the whitelist");
                    }
                    else
                    {
                        string search = string.Join(" ", args);
                        Fougerite.Player target = Fougerite.Server.GetServer().FindPlayer(search);
                        if (target != null)
                        {
                            if (OnWhiteList(player.SteamID, player.IP))
                            {
                                WhiteList.DeleteSetting(target.SteamID, target.IP);
                                WhiteList.Save();
                                player.MessageFrom("CountryBlackList", "You have removed " + target.Name + " from the whitelist");
                            }
                            else
                            {
                                player.MessageFrom("CountryBlackList", target.Name + " is not on the whitelist!");
                            }
                        }
                    }
                }
                else
                {
                    player.MessageFrom("CountryBlackList", "You are not allowed to use this command!");
                }
            }
        }

        public bool OnWhiteList(string playerid, string playerip)
        {
            foreach (var steamid in WhiteList.Sections)
            {
                if (WhiteList.ContainsSetting(steamid, playerip))
                {
                    return true;
                }
                if (steamid == playerid)
                {
                    return true;
                }
            }
            return false;
        }

        public void On_PlayerConnected(Fougerite.Player player)
        {
            new Thread(() =>
            {
                Thread.CurrentThread.IsBackground = true;
                Threaded_PlayerConnected(player);
            }).Start();
        }

        public void Threaded_PlayerConnected(Fougerite.Player player)
        {
            //DEBUG
            Logger.Log("Thread ID: " + Util.GetUtil().CurrentWorkingThreadID);
            //END OF DEBUG
            var data = GeoIP.GeoIP.Instance.GetDataOfIP(player.IP);
            if (data == null)
            {
                if (Show_Accept_Message)
                {
                    string message = Join_Message.Replace("%PLAYER%", player.Name).Replace("%COUNTRY%", Unknown_Location);
                    Server.GetServer().BroadcastFrom("CountryBlackList", message);
                }
                if (Log_TimedOut_Connections)
                {
                    file = new System.IO.StreamWriter(Path.Combine(ModuleFolder, "TimedOut Connections.log"), true);
                    file.WriteLine(DateTime.Now + ": " + player.SteamID + "=" + player.Name + " [" + player.IP + "]");
                    file.Close();
                }
                return;
            }
            string countrycode = data.CountryShort;
            if (BlackList.Any(countrycode.Contains))
            {
                if (Use_WhiteList)
                {
                    if (OnWhiteList(player.SteamID, player.IP))
                    {
                        if (Show_Accept_Message)
                        {
                            string message = Join_Message.Replace("%PLAYER%", player.Name).Replace("%COUNTRY%", data.Country);
                            Server.GetServer().BroadcastFrom("CountryBlackList", message);
                        }
                        return;
                    }
                }
                if (Show_Denied_Message)
                {
                    string message = Server_Disconnect_Message.Replace("%PLAYER%", player.Name).Replace("%COUNTRY%", data.Country);
                    Server.GetServer().BroadcastFrom("CountryBlackList", message);
                }
                player.MessageFrom("CountryBlackList", Player_Disconnect_Message.Replace("%PLAYER%", player.Name).Replace("%COUNTRY%", data.Country));
                player.Disconnect();
            }
            else
            {
                if (Show_Accept_Message)
                {
                    string message = Join_Message.Replace("%PLAYER%", player.Name).Replace("%COUNTRY%", data.Country);
                    Server.GetServer().BroadcastFrom("CountryBlackList", message);
                }
                return;
            }
        }
    }
}

