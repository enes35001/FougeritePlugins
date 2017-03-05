using Fougerite;
using Fougerite.Events;
using UnityEngine;
using System.IO;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using RustBuster2016Server;

namespace DonatorRank
{
    public class DonatorRank : Fougerite.Module
	{
		private static System.IO.StreamWriter file;
		private IniParser Settings;
		private IniParser TPLocations;
		private IniParser Users;
		private IniParser Permissions;
        private string defaultRank;
        private int pointstoget;
        private List<string> buyableRanks;
        private List<string> Ranks;
        private List<string> Kits;
		private Dictionary<string, Boolean> SettingsData;
		private Dictionary<string, string> TeleportData;
		private Dictionary<ulong, Dictionary<string, object>> PlayerData;
		private Dictionary<string, string> KitData;
		public Dictionary<string, string> PermissionData;

		public override string Name
		{
			get
			{
				return "DonatorRank";
			}
		}

		public override string Author
		{
			get
			{
				return "Jakkee";
			}
		}

		public override string Description
		{
			get
			{
				return "Manage VIP's and Donators";
			}
		}

		public override Version Version
		{
			get
			{
				return new Version("0.1");
			}
		}

		public override void Initialize()
		{
			Hooks.OnChat += new Hooks.ChatHandlerDelegate(On_Chat);
			Hooks.OnCommand += new Hooks.CommandHandlerDelegate(On_Command);
			//Hooks.OnEntityDeployed += new Hooks.EntityDeployedDelegate(On_EntityDeployed);
			Hooks.OnPlayerConnected += new Hooks.ConnectionHandlerDelegate(On_PlayerConnected);
			Hooks.OnPlayerDisconnected += new Hooks.DisconnectionHandlerDelegate(On_PlayerDisconnected);
            Hooks.OnPlayerHurt += new Hooks.HurtHandlerDelegate(On_PlayerHurt);
            Hooks.OnPlayerKilled += new Hooks.KillHandlerDelegate(On_PlayerKilled);
            Hooks.OnSteamDeny += new Hooks.SteamDenyDelegate(On_SteamDeny);
            Ranks = new List<string>();
            buyableRanks = new List<string>();
            Kits = new List<string>();
			SettingsData = new Dictionary<string, Boolean>();
			TeleportData = new Dictionary<string, string>();
			PlayerData = new Dictionary<ulong, Dictionary<string, object>>();
			KitData = new Dictionary<string, string>();
			PermissionData = new Dictionary<string, string>();
            if (!File.Exists(Path.Combine(ModuleFolder, "Settings.ini")))
			{
				File.Create(Path.Combine(ModuleFolder, "Settings.ini")).Dispose();
				Settings = new IniParser(Path.Combine(ModuleFolder, "Settings.ini"));
				Settings.AddSetting("Settings", "Join Messages", "True");
				Settings.AddSetting("Settings", "Leave Messages", "True");
				Settings.AddSetting("Settings", "Chat Prefix", "True");
				Settings.AddSetting("Settings", "Chat Color", "True");
				Settings.AddSetting("Settings", "Log Moderator Teleports", "True");
				Settings.AddSetting("Settings", "Log Broadcasts", "True");
				Settings.AddSetting("Settings", "Use HomeSystem", "True");
                Settings.AddSetting("Settings", "Points to Give", "1");
                Settings.AddSetting("Settings", "Points Timer", "1800");
                Settings.AddSetting("Settings", "Ranks", "Owner,Admin,Moderator,Vip++,Vip+,Vip,User");
                Settings.AddSetting("Settings", "Buyable Ranks", "Vip++,Vip+,Vip");
                Settings.AddSetting("Settings", "Default Rank", "User");
                Settings.Save();
			}
			else
			{
				Settings = new IniParser(Path.Combine(ModuleFolder, "Settings.ini"));
			}
			foreach (string key in Settings.EnumSection("Settings"))
			{
				if (key.Equals("Ranks"))
				{
                    Ranks = Settings.GetSetting("Settings", key).Split(',').ToList();
				}
                else if (key.Equals("Buyable Ranks"))
                {
                    buyableRanks = Settings.GetSetting("Settings", key).Split(',').ToList();
                }
                else if (key.Equals("Default Rank"))
                {
                    defaultRank = Settings.GetSetting("Settings", key).Trim();
                }
                else if (key.Equals("Points to Give"))
                {
                    pointstoget = int.Parse(Settings.GetSetting("Settings", key).Trim());
                }
                else if (key.Equals("Points Timer"))
                {
                    var timedEvent = CreateParallelTimer(int.Parse(Settings.GetSetting("Settings", key).Trim()) * 1000, null);
                    timedEvent.OnFire += GiveOutPointTimer;
                    timedEvent.Start();
                }
                else
				{
					SettingsData.Add(key.Replace(" ", ""), Boolean.Parse(Settings.GetSetting("Settings", key)));
				}
            }
            if (!File.Exists(Path.Combine(ModuleFolder, "Permissions.ini")))
			{
				File.Create(Path.Combine(ModuleFolder, "Permissions.ini")).Dispose();
				Permissions = new IniParser(Path.Combine(ModuleFolder, "Permissions.ini"));
                foreach (string item in Settings.GetSetting("Settings", "Ranks").Split(',').ToList())
				{
					Permissions.AddSetting(item, "Points needed for rank", "0");
					Permissions.AddSetting(item, "Join On Full Server", "False");
					Permissions.AddSetting(item, "Chat Prefix", "");
					Permissions.AddSetting(item, "Chat Color", "");
					Permissions.AddSetting(item, "Max Homes", "1");
					Permissions.AddSetting(item, "Home Cooldown", "300");
					Permissions.AddSetting(item, "Home Teleport Delay", "10");
					Permissions.AddSetting(item, "Allowed Kits", "Starter");
					Permissions.AddSetting(item, "Teleport Locations", "French Valley,Small Rad");
					Permissions.AddSetting(item, "Can Update Ranks", "True");
					Permissions.AddSetting(item, "Can Use Broadcast", "True");
					Permissions.AddSetting(item, "Can Use Info", "True");
					Permissions.AddSetting(item, "Can Use Moderator Teleport", "True");
					Permissions.AddSetting(item, "Changable Prefix", "True");
					Permissions.AddSetting(item, "Changable Chat Color", "True");
					Permissions.Save();
				}
			}
			else
			{
				Permissions = new IniParser(Path.Combine(ModuleFolder, "Permissions.ini"));
			}
            foreach (string rank in Permissions.Sections)
            {
                foreach (string setting in Permissions.EnumSection(rank))
                {
                    PermissionData.Add(rank + ":" + setting.Replace(" ", ""), Permissions.GetSetting(rank, setting).Trim());
                }
            }
            if (!File.Exists(Path.Combine(ModuleFolder + "\\Data\\", "Users.ini")))
			{
				File.Create(Path.Combine(ModuleFolder + "\\Data\\", "Users.ini")).Dispose();
				Users = new IniParser(Path.Combine(ModuleFolder + "\\Data\\", "Users.ini"));
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Rank", "Owner");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Current Points", "0");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Reserved Slot", "True");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Chat Prefix", "[Owner]");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Chat Color", "Cyan");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Max Homes", "5");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Home Cooldown", "3");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Home Teleport Delay", "3");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Allowed Kits", "Starter,ModKit,OwnerKit");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Teleport Locations", "Small Rad,Big Rad,Factory,Hanger,Oil Tankers,North Hacker Valley,French Valley,North Next Valley");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Can Update Ranks", "True");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Can Use Broadcast", "True");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Can Use Info", "True");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Can Use Moderator Teleport", "True");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Changable Prefix", "True");
				Users.AddSetting("a0e1f8200a5f22f49567f527fd53d022791b1b8f", "Changable Chat Color", "True");
				Users.Save();
			}
			else
			{
				Users = new IniParser(Path.Combine(ModuleFolder + "\\Data\\", "Users.ini"));
			}
			foreach (string user in Users.Sections)
			{
				foreach (string setting in Users.EnumSection(user))
				{
					PermissionData.Add(user + ":" + setting.Replace(" ", ""), Users.GetSetting(user, setting).Trim());
				}
			}
			if (!File.Exists(Path.Combine(ModuleFolder + "\\Data\\", "TPLocations.ini")))
			{
				File.Create(Path.Combine(ModuleFolder + "\\Data\\", "TPLocations.ini")).Dispose();
				TPLocations = new IniParser(Path.Combine(ModuleFolder + "\\Data\\", "TPLocations.ini"));
				TPLocations.AddSetting("Small Rad", "Location", "6050, 381, -3620");
				TPLocations.AddSetting("Small Rad", "Teleport Delay", "5");
				TPLocations.AddSetting("Small Rad", "Teleport Cooldown", "120");
				TPLocations.AddSetting("Big Rad", "Location", "5250, 371, -4850");
				TPLocations.AddSetting("Big Rad", "Teleport Delay", "5");
				TPLocations.AddSetting("Big Rad", "Teleport Cooldown", "120");
				TPLocations.AddSetting("Factory", "Location", "6300, 361, -4650");
				TPLocations.AddSetting("Factory", "Teleport Delay", "5");
				TPLocations.AddSetting("Factory", "Teleport Cooldown", "120");
				TPLocations.AddSetting("Hanger", "Location", "6600, 356, -4400");
				TPLocations.AddSetting("Hanger", "Teleport Delay", "5");
				TPLocations.AddSetting("Hanger", "Teleport Cooldown", "120");
				TPLocations.AddSetting("Oil Tankers", "Location", "6690, 356, -3880");
				TPLocations.AddSetting("Oil Tankers", "Teleport Delay", "5");
				TPLocations.AddSetting("Oil Tankers", "Teleport Cooldown", "120");
				TPLocations.AddSetting("North Hacker Valley", "Location", "5000, 461, -3000");
				TPLocations.AddSetting("North Hacker Valley", "Teleport Delay", "5");
				TPLocations.AddSetting("North Hacker Valley", "Teleport Cooldown", "120");
				TPLocations.AddSetting("French Valley", "Location", "6056, 385, -4162");
				TPLocations.AddSetting("French Valley", "Teleport Delay", "5");
				TPLocations.AddSetting("French Valley", "Teleport Cooldown", "120");
				TPLocations.AddSetting("North Next Valley", "Location", "4668, 445, -3908");
				TPLocations.AddSetting("North Next Valley", "Teleport Delay", "5");
				TPLocations.AddSetting("North Next Valley", "Teleport Cooldown", "120");
				TPLocations.Save();
			}
			else
			{
				TPLocations = new IniParser(Path.Combine(ModuleFolder + "\\Data\\", "TPLocations.ini"));
			}
			foreach (string section in TPLocations.Sections)
			{
				foreach (string key in TPLocations.EnumSection(section))
				{
					TeleportData.Add(section + ":" + key.Replace(" ", ""), TPLocations.GetSetting(section, key).Trim());
				}
			}
			if (!File.Exists(Path.Combine(ModuleFolder + "\\Kits\\", "Starter.ini")))
			{
				File.Create(Path.Combine(ModuleFolder + "\\Kits\\", "Starter.ini")).Dispose();
				var StarterKit = new IniParser(Path.Combine(ModuleFolder + "\\Kits\\", "Starter.ini"));
				StarterKit.AddSetting("Settings", "Cooldown", "300");
				StarterKit.AddSetting("Settings", "ClearHotBar", "True");
				StarterKit.AddSetting("Settings", "ClearArmor", "True");
				StarterKit.AddSetting("Settings", "ClearInventory", "False");
				StarterKit.AddSetting("Armor", "Helmet", "");
				StarterKit.AddSetting("Armor", "Vest", "Cloth Vest");
				StarterKit.AddSetting("Armor", "Pants", "Cloth Pants");
				StarterKit.AddSetting("Armor", "Boots", "");
				StarterKit.AddSetting("Hotbar", "Item0", "Stone Hatchet, 1");
				StarterKit.AddSetting("Hotbar", "Item1", "Bandage, 1");
				StarterKit.AddSetting("Hotbar", "Item2", "");
				StarterKit.AddSetting("Hotbar", "Item3", "");
				StarterKit.AddSetting("Hotbar", "Item4", "");
				StarterKit.AddSetting("BackPack", "Item0", "Cooked Chicken Breast, 5");
				StarterKit.AddSetting("BackPack", "Item1", "Sleeping Bag, 1");
				StarterKit.AddSetting("BackPack", "Item2", "Camp Fire, 1");
				StarterKit.Save();
			}
			Kits = Directory.GetFiles(ModuleFolder + "\\Kits\\", "*.ini").Select(path => Path.GetFileName(path)).ToList();
			foreach (string kit in Kits)
			{
				var ini = new IniParser(Path.Combine(ModuleFolder + "\\Kits\\", kit));
				foreach (string section in ini.Sections)
				{
					foreach (string setting in ini.EnumSection(section))
					{
						if (!ini.GetSetting(section, setting).Trim().Equals(""))
							KitData.Add(kit.Replace(".ini", "") + ":" + section + ":" + setting, ini.GetSetting(section, setting).Trim());
						else
						{
							KitData.Add(kit.Replace(".ini", "") + ":" + section + ":" + setting, null);
						}
					}
				}
			}
		}

        public override void DeInitialize()
		{
			Hooks.OnChat -= new Hooks.ChatHandlerDelegate(On_Chat);
			Hooks.OnCommand -= new Hooks.CommandHandlerDelegate(On_Command);
			//Hooks.OnEntityDeployed -= new Hooks.EntityDeployedDelegate(On_EntityDeployed);
			Hooks.OnPlayerConnected -= new Hooks.ConnectionHandlerDelegate(On_PlayerConnected);
			Hooks.OnPlayerDisconnected -= new Hooks.DisconnectionHandlerDelegate(On_PlayerDisconnected);
            Hooks.OnPlayerHurt -= new Hooks.HurtHandlerDelegate(On_PlayerHurt);
            Hooks.OnPlayerKilled -= new Hooks.KillHandlerDelegate(On_PlayerKilled);
            Hooks.OnSteamDeny -= new Hooks.SteamDenyDelegate(On_SteamDeny);
		}

		private void On_Chat(Fougerite.Player player, ref Fougerite.ChatString text)
		{
			if (Fougerite.Server.GetServer().HasRustPP)
			{
				if (Fougerite.Server.GetServer().GetRustPPAPI().IsMuted(Convert.ToUInt64(player.SteamID)))
				{
					return;
				}
			}
			text = text.ToString().Trim('"');
			if (text.Contains("[color"))
			{
				text = text.Replace("[color", "").Replace("]", "");
			}
			var prefix = CheckPerm(GetHWID(player.Name) + ":" + "ChatPrefix");
			var color = CheckPerm(GetHWID(player.Name) + ":" + "ChatColor").ToLower().Replace(" ", "");
			if (CheckSettings("ChatPrefix"))
			{
				
				if (prefix == null)
				{
					prefix = "";
				}
			}
			if (CheckSettings("ChatColor"))
			{

				if (color == null)
				{
					color = "None";
				}
			}
            Fougerite.Server.GetServer().BroadcastFrom(prefix + player.Name, "[color " + color + "]" + text);
			text.NewText = "*%";
		}

		private void On_Command(Fougerite.Player player, string cmd, string[] args)
		{
			cmd.ToLower();
            if (cmd.Equals("donatorhelp") || cmd.Equals("dhelp"))
            {
                player.MessageFrom("DonatorRank", "/redeem <rank> - Redeem your points for a rank");
                if (bool.Parse(CheckPerm(GetHWID(player.Name) + ":ChangablePrefix")))
                {
                    player.MessageFrom("DonatorRank", "/chatprefix <prefix> - Changes your prefix");
                }
                if (bool.Parse(CheckPerm(GetHWID(player.Name) + ":ChangableChatColor")))
                {
                    player.MessageFrom("DonatorRank", "/chatcolor <color> - Changes your chat color");
                }
                if (CheckPerm(GetHWID(player.Name) + ":AllowedKits") != null || !CheckPerm(GetHWID(player.Name) + ":AllowedKits").Equals(""))
                {
                    player.MessageFrom("DonatorRank", "/kit <kit> - redeem a kit");
                }
                if (CheckPerm(GetHWID(player.Name) + ":TeleportLocations") != null || !CheckPerm(GetHWID(player.Name) + ":TeleportLocations").Equals(""))
                {
                    player.MessageFrom("DonatorRank", "/dtp <location> - Teleport to a location");
                }
                if (bool.Parse(CheckPerm(GetHWID(player.Name) + ":CanUseBroadcast")))
                {
                    player.MessageFrom("DonatorRank", "/broadcast <text> - Broadcast something to the server");
                }
                if (bool.Parse(CheckPerm(GetHWID(player.Name) + ":CanUseInfo")))
                {
                    player.MessageFrom("DonatorRank", "/info <Player Name> - Looks up a player and displays information");
                }
                if (bool.Parse(CheckPerm(GetHWID(player.Name) + ":CanUseModeratorTeleport")))
                {
                    player.MessageFrom("DonatorRank", "/mtp <Player Name> - Teleport to a player");
                    player.MessageFrom("DonatorRank", "/mtpback - Teleport back to where you were last");
                }
                if (bool.Parse(CheckPerm(GetHWID(player.Name) + ":CanUpdateRanks")))
                {
                    player.MessageFrom("DonatorRank", "Usage: /rank [add/remove] [<Rank>/<Amount of Points>] <Player Name>");
                }
            }

            else if (cmd.Equals("redeem"))
            {
                if (!args.Length.Equals(0))
                {
                    var rank = string.Join(" ", args).Trim(' ', '"');
                    if (buyableRanks.Contains(rank))
                    {
                        if (PermissionData[GetHWID(player.Name) + ":Rank"] != rank)
                        {
                            if (int.Parse(PermissionData[GetHWID(player.Name) + ":CurrentPoints"]) >= int.Parse(PermissionData[rank + ":Pointsneededforrank"]))
                            {
                                int calc = int.Parse(PermissionData[GetHWID(player.Name) + ":CurrentPoints"]) - int.Parse(PermissionData[rank + ":Pointsneededforrank"]);
                                PermissionData[GetHWID(player.Name) + ":CurrentPoints"] = calc.ToString();
                                Users.AddSetting(GetHWID(player.Name), "Current Points", calc.ToString());
                                Users.Save();
                                Thread thread = new Thread(() => AddPerms(GetHWID(player.Name), rank));
                                thread.Start();
                                player.MessageFrom("DonatorRank", "You have purchased the rank " + rank);
                            }
                            else
                            {
                                player.MessageFrom("DonatorRank", "You do not have enough points for " + rank);
                            }
                        }
                        else
                        {
                            player.MessageFrom("DonatorRank", "You already have this rank!");
                        }
                    }
                    else
                    {
                        player.MessageFrom("DonatorRank", rank + " does not exist.");
                        foreach (string item in buyableRanks)
                        {
                            player.MessageFrom("DonatorRank", item + " = " + PermissionData[item + ":Pointsneededforrank"] + "points");
                        }
                        player.MessageFrom("DonatorRank", "You have " + PermissionData[GetHWID(player.Name) + ":CurrentPoints"] + "points");
                    }
                }
                else
                {
                    player.MessageFrom("DonatorRank", "Usage: /redeem <rank> - Redeem your points for a rank");
                    foreach (string rank in buyableRanks)
                    {
                        player.MessageFrom("DonatorRank", rank + " = " + PermissionData[rank + ":Pointsneededforrank"] + "points");
                    }
                    player.MessageFrom("DonatorRank", "You have " + PermissionData[GetHWID(player.Name) + ":CurrentPoints"] + "points");
                }
            }

            else if (cmd.Equals("mtp"))
            {
                if (bool.Parse(CheckPerm(GetHWID(player.Name) + ":CanUseModeratorTeleport")))
                {
                    if (!args.Length.Equals(0))
                    {
                        Fougerite.Player target = Fougerite.Server.GetServer().FindPlayer(string.Join(" ", args));
                        if (target != null)
                        {
                            if (!DataStore.GetInstance().ContainsKey("ModeratorLastLoc", GetHWID(player.Name)))
                            {
                                DataStore.GetInstance().Add("ModeratorLastLoc", GetHWID(player.Name), player.Location.ToString());
                            }
                            target.Notice(target.Name + " has teleported to you!");
                            player.TeleportTo(target, 2, false);
                            player.Notice("Teleported to: " + target.Name);
                            player.Message("To teleport back to where you were, Type /mtpback");
                            if (CheckSettings("LogModeratorTeleports"))
                            {
                                file = new System.IO.StreamWriter(Path.Combine(ModuleFolder + "\\Logs\\", "ModeratorTeleport.log"), true);
                                file.WriteLine(DateTime.Now + ": " + player.Name + "=" + GetHWID(player.Name) + " IP:" + player.IP + "|| Teleported to: " + player.Name + "=" + player.SteamID + " IP:" + target.IP);
                                file.Close();
                            }
                        }
                        else
                        {
                            player.MessageFrom("DonatorRank", "Can not find : " + string.Join(" ", args));
                        }
                    }
                    else
                    {
                        player.MessageFrom("DonatorRank", "Usage: /mtp <Player Name>");
                    }
                }
                else
                {
                    player.MessageFrom("DonatorRank", "You do not have permission to use this command");
                }
            }

            else if (cmd.Equals("mtpback"))
            {
                if (bool.Parse(CheckPerm(GetHWID(player.Name) + ":CanUseModeratorTeleport")))
                {
                    if (DataStore.GetInstance().ContainsKey("ModeratorLastLoc", GetHWID(player.Name)))
                    {
                        var location = StringToVector3(DataStore.GetInstance().Get("ModeratorLastLoc", GetHWID(player.Name)).ToString());
                        player.SafeTeleportTo(location, false);
                        DataStore.GetInstance().Remove("ModeratorLastLoc", GetHWID(player.Name));
                        player.MessageFrom("DonatorRank", "You have been teleported back to your orignal position");
                        if (CheckSettings("LogModeratorTeleports"))
                        {
                            file = new StreamWriter(Path.Combine(ModuleFolder + "\\Logs\\", "ModeratorTeleport.log"), true);
                            file.WriteLine(DateTime.Now + ": " + player.Name + "=" + GetHWID(player.Name) + " IP:" + player.IP + "|| Teleported back to their orginal location");
                            file.Close();
                        }

                    }
                    else
                    {
                        player.MessageFrom("DonatorRank", "You do not have any location to go back to!");
                    }
                }
                else
                {
                    player.MessageFrom("DonatorRank", "You do not have permission to use this command");
                }
            }

            else if (cmd.Equals("rank"))
            {
                if (bool.Parse(CheckPerm(GetHWID(player.Name) + ":CanUpdateRanks")))
                {
                    if (args.Length > 2)
                    {
                        if (args[0].ToLower().Equals("add"))
                        {
                            var points = args[1].Trim();
                            if (points.All(char.IsDigit))
                            {
                                var quotes = FindQuotes(args);
                                var search = args[2];
                                Fougerite.Player target = null;
                                if (quotes.Count > 1)
                                {
                                    player.MessageFrom("DonatorRank", "Usage: /rank add [<Rank>/<Amount of Points>] <Player Name>");
                                    return;
                                }
                                else if (quotes.Count.Equals(1))
                                {
                                    target = Fougerite.Server.GetServer().FindPlayer(quotes[0].ToString());
                                    if (target == null)
                                    {
                                        player.MessageFrom("DonatorRank", "Can not find user: " + quotes[0]);
                                        return;
                                    }
                                }
                                else
                                {
                                    target = Fougerite.Server.GetServer().FindPlayer(search);
                                    if (target == null)
                                    {
                                        player.MessageFrom("DonatorRank", "Can not find user: " + search);
                                        return;
                                    }
                                }
                                string current = (int.Parse(points) + int.Parse(CheckPerm(GetHWID(target.Name) + ":CurrentPoints"))).ToString();
                                PermissionData[GetHWID(target.Name) + ":CurrentPoints"] = current.ToString();
                                Users.AddSetting(GetHWID(target.Name), "Current Points", current.ToString());
                                Users.Save();
                                player.MessageFrom("DonatorRank", "You have added " + points + " points to the user " + target.Name);
                                Thread thread = new Thread(() => UpdatePerms(GetHWID(target.Name)));
                                thread.Start();
                                target.MessageFrom("DonatorRank", "You have received " + points + " points. Total: " + current);
                            }
                            else
                            {
                                var quotes = FindQuotes(args);
                                var rank = args[1];
                                var search = args[2];
                                Fougerite.Player target = null;
                                if (quotes.Count.Equals(1))
                                {
                                    target = Fougerite.Server.GetServer().FindPlayer(quotes[0].ToString());
                                    if (!Ranks.Contains(quotes[0].ToString()) && target == null)
                                    {
                                        player.MessageFrom("DonatorRank", "Can not find user " + search + " or rank " + rank);
                                    }
                                    else if (target == null)
                                    {
                                        player.MessageFrom("DonatorRank", "Can not find user " + search);
                                        return;
                                    }
                                    else
                                    {
                                        if (!Ranks.Contains(quotes[0].ToString()))
                                        {
                                            player.MessageFrom("DonatorRank", "Can not find rank " + rank);
                                            return;
                                        }
                                    }
                                }
                                else if (quotes.Count.Equals(2))
                                {
                                    if (Ranks.Contains(quotes[0].ToString()))
                                    {
                                        rank = quotes[0].ToString();
                                    }
                                    else
                                    {
                                        player.MessageFrom("DonatorRank", "Can not find rank: " + quotes[0]);
                                        return;
                                    }
                                    target = Fougerite.Server.GetServer().FindPlayer(quotes[1].ToString());
                                    if (target == null)
                                    {
                                        player.MessageFrom("DonatorRank", "Can not find user: " + quotes[1]);
                                        return;
                                    }
                                }
                                else
                                {
                                    if (!Ranks.Contains(rank))
                                    {
                                        player.MessageFrom("DonatorRank", "Can not find rank: " + rank);
                                        return;
                                    }
                                    target = Fougerite.Server.GetServer().FindPlayer(search);
                                    if (target == null)
                                    {
                                        player.MessageFrom("DonatorRank", "Can not find user: " + search);
                                        return;
                                    }
                                }
                                UppercaseFirst(rank);
                                if (!CheckPerm(GetHWID(target.Name) + ":Rank").Equals(rank))
                                {
                                    Thread thread = new Thread(() => AddPerms(GetHWID(target.Name), rank));
                                    thread.Start();
                                    player.MessageFrom("DonatorRank", "Added " + target.Name + " to group " + rank);
                                    target.MessageFrom("DonatorRank", "You have joined group " + rank);
                                }
                                else
                                {
                                    player.MessageFrom("DonatorRank", "This user is already " + rank);
                                    return;
                                }
                            }
                        }
                        else if (args[0].ToLower().Equals("remove"))
                        {
                            var points = args[1];
                            if (points.All(char.IsDigit))
                            {
                                var quotes = FindQuotes(args);
                                var search = args[2];
                                Fougerite.Player target = null;
                                if (quotes.Count > 1)
                                {
                                    player.MessageFrom("DonatorRank", "Usage: /rank remove [<Rank>/<Amount of Points>] <Player Name>");
                                    return;
                                }
                                else if (quotes.Count.Equals(1))
                                {
                                    target = Fougerite.Server.GetServer().FindPlayer(quotes[1].ToString());
                                    if (target == null)
                                    {
                                        player.MessageFrom("DonatorRank", "Can not find user: " + quotes[1]);
                                        return;
                                    }
                                }
                                else
                                {
                                    target = Fougerite.Server.GetServer().FindPlayer(search);
                                    if (target == null)
                                    {
                                        player.MessageFrom("DonatorRank", "Can not find user: " + search);
                                        return;
                                    }
                                }
                                int current = int.Parse(CheckPerm(GetHWID(target.Name) + ":CurrentPoints"));
                                string toremove = points;
                                int removepoints = current - int.Parse(points);
                                if (current < removepoints)
                                {
                                    removepoints = 0;
                                    toremove = current.ToString();
                                    player.MessageFrom("DonatorRank", target.Name + " did not have " + points + ", Removing all their points instead");
                                }
                                PermissionData[GetHWID(target.Name) + ":CurrentPoints"] = removepoints.ToString();
                                Users.AddSetting(GetHWID(target.Name), "Current Points", removepoints.ToString());
                                Users.Save();
                                Thread thread = new Thread(() => UpdatePerms(GetHWID(player.Name)));
                                thread.Start();
                                player.MessageFrom("DonatorRank", "You have removed " + toremove + " points from " + target.Name);
                                target.MessageFrom("DonatorRank", "You have had " + toremove + " points removed. Total: " + removepoints.ToString());
                            }
                            else
                            {
                                var quotes = FindQuotes(args);
                                var rank = args[1];
                                var search = args[2];
                                Fougerite.Player target = null;
                                if (quotes.Count.Equals(1))
                                {
                                    if (!Ranks.Contains(quotes.ToString()))
                                    {
                                        target = Fougerite.Server.GetServer().FindPlayer(quotes.ToString());
                                        if (target == null)
                                        {
                                            player.MessageFrom("DonatorRank", "Can not find a match for a rank or a user!");
                                            return;
                                        }
                                    }
                                }
                                else if (quotes.Count.Equals(2))
                                {
                                    if (Ranks.Contains(quotes[0].ToString()))
                                    {
                                        rank = quotes[0].ToString();
                                    }
                                    else
                                    {
                                        player.MessageFrom("DonatorRank", "Can not find rank: " + quotes[0]);
                                        return;
                                    }
                                    target = Fougerite.Server.GetServer().FindPlayer(quotes[1].ToString());
                                    if (target == null)
                                    {
                                        player.MessageFrom("DonatorRank", "Can not find user: " + quotes[1]);
                                        return;
                                    }
                                }
                                if (!Ranks.Contains(rank))
                                {
                                    player.MessageFrom("DonatorRank", "Can not find rank: " + rank);
                                    return;
                                }
                                target = Fougerite.Server.GetServer().FindPlayer(search);
                                if (target == null)
                                {
                                    player.MessageFrom("DonatorRank", "Can not find user: " + search);
                                    return;
                                }
                                UppercaseFirst(rank);
                                if (CheckPerm(GetHWID(target.Name) + ":Rank").Equals(rank))
                                {
                                    Thread thread = new Thread(() => AddPerms(GetHWID(target.Name), rank));
                                    thread.Start();
                                    player.MessageFrom("DonatorRank", "Removed " + target.Name + " from group " + rank);
                                    target.MessageFrom("DonatorRank", "You have had your rank removed!");
                                }
                                else
                                {
                                    player.MessageFrom("DonatorRank", target.Name + " is not apart of " + rank);
                                    return;
                                }
                            }
                        }
                        else
                        {
                            player.MessageFrom("DonatorRank", "Usage: /rank [add/remove] [<Rank>/<Amount of Points>] <Player Name>");
                        }
                    }
                    else
                    {
                        player.MessageFrom("DonatorRank", "Usage: /rank [add/remove] [<Rank>/<Amount of Points>] <Player Name>");
                    }
                }
                else
                {
                    player.MessageFrom("DonatorRank", "You do not have permission to use this command");
                }
            }

            else if (cmd.Equals("kit"))
            {
                if (!args.Length.Equals(0))
                {
                    var lookup = string.Join(" ", args).Trim();
                    var allowedkits = CheckPerm(GetHWID(player.Name) + ":AllowedKits").Split(',').ToList();
                    var count = new List<string>();
                    foreach (string kit in allowedkits)
                    {
                        if (kit.Contains(lookup))
                        {
                            foreach (string key in KitData.Keys)
                            {
                                if (key.Contains(lookup))
                                {
                                    if (!count.Contains(key.Split(':')[0]))
                                    {
                                        count.Add(key.Split(':')[0]);
                                    }
                                }
                            }
                        }
                    }
                    if (count.Count.Equals(1))
                    {
                        var kitname = string.Join("", count.ToArray()).Trim();
                        var waittime = new long();
                        var playertime = new long();
                        var currenttime = DateTime.UtcNow.Ticks;
                        try
                        {
                            waittime = long.Parse(KitData[kitname + ":Settings:Cooldown"]) * 10000000;
                        }
                        catch
                        {
                            player.MessageFrom("DonatorRank", "There is no kit called " + kitname);
                            return;
                        }
                        if (DataStore.GetInstance().ContainsKey("DonatorRankKitCooldown", player.SteamID + "+" + kitname.Replace(" ", "")))
                        {
                            playertime = long.Parse(DataStore.GetInstance().Get("DonatorRankKitCooldown", player.SteamID + "+" + kitname.Replace(" ", "")).ToString());
                        }
                        else
                        {
                            playertime = 0;
                        }
                        var calc = currenttime - playertime;
                        player.Message("calc = " + calc.ToString() + ". Waittime = " + waittime.ToString() + ". [playertime = " + playertime.ToString() + "]");
                        if (calc >= waittime)
                        {
                            if (Boolean.Parse(KitData[kitname + ":Settings:ClearHotBar"]))
                            {
                                player.Inventory.ClearBar();
                            }
                            if (Boolean.Parse(KitData[kitname + ":Settings:ClearArmor"]))
                            {
                                player.Inventory.ClearArmor();
                            }
                            if (Boolean.Parse(KitData[kitname + ":Settings:ClearInventory"]))
                            {
                                player.Inventory.ClearAll();
                            }
                            if (!KitData[kitname + ":Armor:Helmet"].Equals("") || KitData[kitname + ":Armor:Helmet"] == null)
                            {
                                player.Inventory.AddItemTo(KitData[kitname + ":Armor:Helmet"], 36, 1);
                            }
                            if (!KitData[kitname + ":Armor:Vest"].Equals("") || KitData[kitname + ":Armor:Vest"] == null)
                            {
                                player.Inventory.AddItemTo(KitData[kitname + ":Armor:Vest"], 37, 1);
                            }
                            if (!KitData[kitname + ":Armor:Pants"].Equals("") || KitData[kitname + ":Armor:Pants"] == null)
                            {
                                player.Inventory.AddItemTo(KitData[kitname + ":Armor:Pants"], 38, 1);
                            }
                            if (!KitData[kitname + ":Armor:Boots"].Equals("") || KitData[kitname + ":Armor:Boots"] == null)
                            {
                                player.Inventory.AddItemTo(KitData[kitname + ":Armor:Boots"], 39, 1);
                            }
                            var hotbar = 0;
                            var backpack = 0;
                            var slot = 30;
                            try
                            {
                                foreach (string key in KitData.Keys)
                                {
                                    if (key.Equals(kitname + ":Hotbar:Item" + hotbar.ToString()))
                                    {
                                        if (!KitData[key].Equals("") || KitData[key] != null)
                                        {
                                            var item = KitData[key].Split(',');
                                            player.Inventory.AddItemTo(item[0].Trim(), slot, int.Parse(item[1].Trim()));
                                            hotbar += 1;
                                            slot += 1;
                                        }
                                    }
                                    else if (key.Equals(kitname + ":BackPack:Item" + backpack.ToString()))
                                    {
                                        if (!KitData[key].Equals("") || KitData[key] != null)
                                        {
                                            var item = KitData[key].Split(',');
                                            player.Inventory.AddItem(item[0].Trim(), int.Parse(item[1].Trim()));
                                            backpack += 1;
                                        }
                                    }
                                }
                            }
                            catch (IndexOutOfRangeException)
                            {
                                player.MessageFrom("DonatorRank", "Error in kit " + kitname + ". Contact server staff to remove unused lines (EG. Item3=)");
                                return;
                            }
                            DataStore.GetInstance().Add("DonatorRankKitCooldown", player.SteamID + "+" + kitname.Replace(" ", ""), DateTime.UtcNow.Ticks);
                            player.InventoryNotice("Used 1x " + kitname);
                        }
                        else
                        {
                            var workingout = (waittime / 10000000) - (calc / 10000000);
                            TimeSpan t = TimeSpan.FromSeconds(workingout);
                            player.MessageFrom("DonatorRank", "Time remaining " + string.Format("{0:D2}h:{1:D2}m:{2:D2}s", t.Hours, t.Minutes, t.Seconds) + " before you can use " + kitname);
                        }
                    }
                    else if (count.Count.Equals(0))
                    {
                        player.MessageFrom("DonatorRank", "Can not find kit " + lookup);
                    }
                    else
                    {
                        player.MessageFrom("DonatorRank", "Found " + count.Count.ToString() + " kits that match!");
                    }
                }
                else
                {
                    var lookup1 = CheckPerm(GetHWID(player.Name) + ":AllowedKits").Split(',').ToList();
                    var count1 = new List<string>();
                    foreach (string kit in lookup1)
                    {
                        foreach (string key in KitData.Keys)
                        {
                            if (key.Split(':')[0].Trim().Equals((kit).Trim()))
                            {
                                if (!count1.Contains(key.Split(':')[0]))
                                {
                                    count1.Add(key.Split(':')[0]);
                                }
                            }
                        }
                    }
                    if (count1.Count.Equals(0))
                    {
                        player.MessageFrom("DonatorRank", "You do not have permission to use this command");
                    }
                    else
                    {
                        player.MessageFrom("DonatorRank", "Kits you can use: " + string.Join(", ", count1.ToArray()));
                    }
                }
            }

            else if (cmd.Equals("broadcast") || cmd.Equals("yell"))
            {
                if (bool.Parse(CheckPerm(GetHWID(player.Name) + ":CanUseBroadcast")))
                {
                    if (!args.Length.Equals(0))
                    {
                        Fougerite.Server.GetServer().BroadcastFrom("[Player Broadcast]", string.Join(" ", args));
                        if (CheckSettings("LogBroadcasts"))
                        {
                            file = new System.IO.StreamWriter(Path.Combine(ModuleFolder + "\\Logs\\", "Broadcasts.log"), true);
                            file.WriteLine(DateTime.Now + ": " + player.Name + "=" + GetHWID(player.Name) + " IP:" + player.IP + "|Said: " + string.Join(" ", args));
                            file.Close();
                        }
                    }
                    else
                    {
                        player.MessageFrom("DonatorRank", "/broadcast <text> - Broadcast something to the server");
                    }
                }
                else
                {
                    player.MessageFrom("DonatorRank", "You do not have permission to use this command");
                }
            }
            else if (cmd.Equals("info"))
            {
                if (bool.Parse(CheckPerm(GetHWID(player.Name) + ":CanUseInfo")))
                {
                    if (!args.Length.Equals(0))
                    {
                        string search = string.Join(" ", args);
                        Fougerite.Player target = Fougerite.Server.GetServer().FindPlayer(search);
                        if (target != null)
                        {
                            player.MessageFrom("DonatorRank", "Info about [color cyan]" + target.Name);
                            player.MessageFrom("DonatorRank", "IP: [color cyan]" + target.IP);
                            player.MessageFrom("DonatorRank", "SteamID: [color cyan]" + target.SteamID);
                            player.MessageFrom("DonatorRank", "HardwareID: [color cyan]" + GetHWID(player.Name));
                            player.MessageFrom("DonatorRank", "Ping: [color cyan]" + target.Ping.ToString());
                            player.MessageFrom("DonatorRank", "Health: [color cyan]" + target.Health.ToString());
                            TimeSpan t = TimeSpan.FromSeconds(target.TimeOnline / 1000);
                            player.MessageFrom("DonatorRank", "Time Online: [color cyan]" + string.Format("{0:D2}d:{1:D2}h:{2:D2}m:{3:D2}s", t.Days, t.Hours, t.Minutes, t.Seconds));
                            player.MessageFrom("DonatorRank", "At home: [color cyan]" + target.AtHome.ToString());
                            player.MessageFrom("DonatorRank", "Free slots: [color cyan]" + target.Inventory.FreeSlots.ToString());
                            if (Fougerite.Server.GetServer().HasRustPP)
                            {
                                var RustPP = Fougerite.Server.GetServer().GetRustPPAPI();
                                player.MessageFrom("DonatorRank", "Is muted: [color cyan]" + RustPP.IsMuted(ulong.Parse(GetHWID(player.Name))));
                            }
                        }
                        else
                        {
                            player.MessageFrom("DonatorRank", "Can not find any user with the name: " + search);
                        }
                    }
                    else
                    {
                        player.MessageFrom("DonatorRank", "Usage /info <Player name>");
                    }
                }
                else
                {
                    player.MessageFrom("DonatorRank", "You do not have permission to use this command!");
                }
            }

            else if (cmd.Equals("dtp"))
            {
                if (!args.Length.Equals(0))
                {
                    var lookup = string.Join(" ", args).Trim();
                    var allowedloc = PermissionData[GetHWID(player.Name) + ":TeleportLocations"].Split(',');
                    var count = new List<string>();
                    foreach (string loc in allowedloc)
                    {
                        if (loc.Contains(lookup))
                        {
                            foreach (string key in TeleportData.Keys)
                            {
                                if (key.Contains(lookup))
                                {
                                    if (!count.Contains(key.Split(':')[0]))
                                    {
                                        count.Add(key.Split(':')[0]);
                                    }
                                }
                            }
                        }
                    }
                    if (count.Count.Equals(1))
                    {
                        var locationname = string.Join("", count.ToArray()).Trim();
                        var waittime = new long();
                        var playertime = new long();
                        var currenttime = DateTime.UtcNow.Ticks;
                        try
                        {
                            waittime = long.Parse(TeleportData[locationname + ":TeleportCooldown"]) * 10000000;
                        }
                        catch
                        {
                            player.MessageFrom("DonatorRank", "There is no location called " + locationname);
                            return;
                        }
                        if (DataStore.GetInstance().ContainsKey("DonatorRankTpCooldown", player.SteamID + "+" + locationname.Replace(" ", "")))
                        {
                            playertime = long.Parse(DataStore.GetInstance().Get("DonatorRankTpCooldown", player.SteamID + "+" + locationname.Replace(" ", "")).ToString());
                        }
                        else
                        {
                            playertime = 0;
                        }
                        var calc = currenttime - playertime;
                        if (calc >= waittime)
                        {
                            var delay = TeleportData[locationname + ":TeleportDelay"];
                            var location = TeleportData[locationname + ":Location"];
                            if (delay != null || !delay.Equals("") || location != null || !location.Equals(""))
                            {
                                Dictionary<string, object> localdict = new Dictionary<string, object>();
                                localdict["Location"] = location;
                                localdict["LocationName"] = locationname;
                                localdict["Player"] = player;
                                localdict["Health"] = player.Health;
                                var timedEvent = CreateParallelTimer(int.Parse(delay) * 1000, localdict);
                                timedEvent.OnFire += TeleportDelay;
                                timedEvent.Start();
                                DataStore.GetInstance().Add("DonatorRankTpCooldown", player.SteamID + "+" + locationname.Replace(" ", ""), DateTime.UtcNow.Ticks);
                                TimeSpan t = TimeSpan.FromSeconds(long.Parse(delay));
                                player.MessageFrom("DonatorRank", "Teleporting in: " + string.Format("{0:D2}s", t.Seconds));
                            }
                            else
                            {
                                player.MessageFrom("DonatorRank", "Contact server staff to setup this teleport's location or teleport delay");
                            }
                        }
                        else
                        {
                            var workingout = (waittime / 10000000) - (calc / 10000000);
                            TimeSpan t = TimeSpan.FromSeconds(workingout);
                            player.MessageFrom("DonatorRank", "Time remaining " + string.Format("{0:D2}h:{1:D2}m:{2:D2}s", t.Hours, t.Minutes, t.Seconds) + " before you can teleport to " + locationname);
                        }
                    }
                    else if (count.Count.Equals(0))
                    {
                        player.MessageFrom("DonatorRank", "Can not find: " + lookup);
                    }
                    else
                    {
                        player.MessageFrom("DonatorRank", "Found " + count.Count.ToString() + " possible matches");
                    }
                }
                else
                {
                    var lookup1 = CheckPerm(GetHWID(player.Name) + ":TeleportLocations").Split(',').ToList();
                    var count1 = new List<string>();
                    foreach (string loc in lookup1)
                    {
                        foreach (string key in TeleportData.Keys)
                        {
                            if (key.Split(':')[0].Trim().Equals((loc).Trim()))
                            {
                                if (!count1.Contains(key.Split(':')[0]))
                                {
                                    count1.Add(key.Split(':')[0]);
                                }
                            }
                        }
                    }
                    if (count1.Count.Equals(0))
                    {
                        player.MessageFrom("DonatorRank", "You do not have permission to use this command");
                    }
                    else
                    {
                        player.MessageFrom("DonatorRank", "Locations you can go to: " + string.Join(", ", count1.ToArray()));
                    }
                }
            }

            else if (cmd.Equals("chatcolor"))
            {
                if (CheckPerm(GetHWID(player.Name) + ":ChatColor") != null || !CheckPerm(GetHWID(player.Name) + ":ChatColor").Equals(""))
                {
                    if (args.Length.Equals(1))
                    {
                        var color = args[0].ToLower();
                        var oldcolor = PermissionData[GetHWID(player.Name) + ":ChatColor"].Replace("[color", "").Replace("]", "").Replace(" ", "");
                        if (!color.Equals(oldcolor))
                        {
                            player.MessageFrom("DonatorRank", "Your chat color has been changed to [color " + color + "]" + color);
                            PermissionData[GetHWID(player.Name) + ":ChatColor"] = color;
                            Permissions.AddSetting(GetHWID(player.Name), "Chat Color", color);
                        }
                        else
                        {
                            player.MessageFrom("DonatorRank", "Your chat color is already [color " + color + "]" + color);
                        }
                    }
                    else
                    {
                        player.MessageFrom("DonatorRank", "Usage: /chatcolor <color>");
                    }
                }
                else
                {
                    player.MessageFrom("DonatorRank", "You do not have permission to use this command!");
                }
            }

            else if (cmd.Equals("chatprefix"))
            {
                if (CheckPerm(GetHWID(player.Name) + ":ChatPrefix") != null || !CheckPerm(GetHWID(player.Name) + ":ChatPrefix").Equals(""))
                {
                    if (args.Length.Equals(1))
                    {
                        var prefix = args[0].ToLower();
                        var oldprefix = PermissionData[GetHWID(player.Name) + ":ChatPrefix"].Replace("[", "").Replace("]", "").Replace(" ", "");
                        if (!prefix.Equals(oldprefix))
                        {
                            player.MessageFrom("DonatorRank", "Your chat prefix has been changed to [" + prefix + "]");
                            PermissionData[GetHWID(player.Name) + ":ChatPrefix"] = "[" + prefix + "]";
                        }
                        else
                        {
                            player.MessageFrom("DonatorRank", "Your chat prefix is already [" + prefix + "]");
                        }
                    }
                    else
                    {
                        player.MessageFrom("DonatorRank", "Usage: /chatprefix <prefix>");
                    }
                }
                else
                {
                    player.MessageFrom("DonatorRank", "You do not have permission to use this command!");
                }
            }
		}

		private void On_PlayerConnected(Fougerite.Player player)
		{
            Thread thread = new Thread(() => UpdatePerms(GetHWID(player.Name)));
            thread.Start();
            var maxhomes = CheckPerm(GetHWID(player.Name) + ":" + "MaxHomes");
			var Cooldown = CheckPerm(GetHWID(player.Name) + ":" + "HomeCooldown");
			var TpDelay = CheckPerm(GetHWID(player.Name) + ":" + "HomeTeleportDelay");
			if (maxhomes == null || maxhomes.Equals(""))
			{
				maxhomes = "1";
			}
			if (Cooldown == null || Cooldown.Equals(""))
			{
				Cooldown = "300";
			}
			if (TpDelay == null || TpDelay.Equals(""))
			{
				TpDelay = "10";
			}
			DataStore.GetInstance().Add("DonatorRank-MaxHomes", player.SteamID, int.Parse(maxhomes));
			DataStore.GetInstance().Add("DonatorRank-Cooldown", player.SteamID, int.Parse(Cooldown));
			DataStore.GetInstance().Add("DonatorRank-TpDelay", player.SteamID, int.Parse(TpDelay));
			if (CheckSettings("JoinMessages"))
			{
				var rank = CheckPerm(GetHWID(player.Name) + ":Rank");
				if (rank == null)
				{
					rank = "";
				}
                Fougerite.Server.GetServer().BroadcastFrom(rank, player.Name + " has connected to the server!");
			}
		}

		private void On_PlayerDisconnected(Fougerite.Player player)
		{
			if (SettingsData["LeaveMessages"])
			{
				var rank = CheckPerm(GetHWID(player.Name) + ":Rank");
				if (rank == null)
				{
					rank = "";
				}
                Fougerite.Server.GetServer().BroadcastFrom(rank, player.Name + " has connected to the server!");
			}
			RemovePerms(GetHWID(player.Name));
		}

        private void On_PlayerHurt(HurtEvent hurtevent)
        {
            if (hurtevent.AttackerIsPlayer && hurtevent.VictimIsPlayer)
            {
                Fougerite.Player player = hurtevent.Attacker as Fougerite.Player;
                Fougerite.Player victim = hurtevent.Victim as Fougerite.Player;
                if (DataStore.GetInstance().ContainsKey("ModeratorLastLoc", GetHWID(player.Name)))
                {
                    if (CheckSettings("LogModeratorTeleports"))
                    {
                        file = new System.IO.StreamWriter(Path.Combine(ModuleFolder + "\\Logs\\", "ModeratorTeleport.log"), true);
                        file.WriteLine(DateTime.Now + ": " + player.Name + "=" + GetHWID(player.Name) + " IP:" + player.IP + "|| Hurt: " + victim.Name + "=" + victim.SteamID + " Damage:" + hurtevent.DamageAmount.ToString());
                        file.Close();
                    }
                }
            }
        }

        private void On_PlayerKilled(DeathEvent deathevent)
        {
            if (deathevent.AttackerIsPlayer && deathevent.VictimIsPlayer)
            {
                Fougerite.Player player = deathevent.Attacker as Fougerite.Player;
                Fougerite.Player victim = deathevent.Victim as Fougerite.Player;
                if (DataStore.GetInstance().ContainsKey("ModeratorLastLoc", player.SteamID))
                {
                    if (CheckSettings("LogModeratorTeleports"))
                    {
                        file = new System.IO.StreamWriter(Path.Combine(ModuleFolder + "\\Logs\\", "ModeratorTeleport.log"), true);
                        file.WriteLine(DateTime.Now + ": " + player.Name + "=" + GetHWID(player.Name) + " IP:" + player.IP + "|| Killed: " + victim.Name + "=" + victim.SteamID);
                        file.Close();
                    }
                }
            }
        }

		private void On_SteamDeny(SteamDenyEvent denyevent)
		{
			if (denyevent.ErrorNumber.ToString().Equals("TooManyConnectedPlayers"))
			{
				if (Boolean.Parse(CheckPerm(denyevent.NetUser.userID.ToString() + ":" + "JoinOnFullServer")))
				{
					denyevent.ForceAllow = true;
				}
			}
		}

        private void GiveOutPointTimer(DonatorRankTimedEvent TimedEvent)
        {
            foreach (Fougerite.Player player in Fougerite.Server.GetServer().Players)
            {
                if (player != null)
                {
                    int current = int.Parse(CheckPerm(GetHWID(player.Name) + ":CurrentPoints"));
                    current += pointstoget;
                    PermissionData.Add(GetHWID(player.Name) + ":CurrentPoints", current.ToString());
                    Users.AddSetting(GetHWID(player.Name), "Current Points", current.ToString());
                    Users.Save();
                    player.MessageFrom("DonatorRank", "You have gained " + pointstoget.ToString() + "point(s)! Redeem your points using /redeem");
                }
            }
        }

        private void AddPerms(string HWID, string rank = null)
        {
            if (rank != null && Users.ContainsSetting(HWID, "Rank"))
            {
                Users.AddSetting(HWID, "Rank", rank);
                Users.AddSetting(HWID, "Current Points", PermissionData[HWID + ":CurrentPoints"]);
                Users.AddSetting(HWID, "Reserved Slot", PermissionData[rank + ":JoinOnFullServer"]);
                Users.AddSetting(HWID, "Chat Prefix", PermissionData[rank + ":ChatPrefix"]);
                Users.AddSetting(HWID, "Chat Color", PermissionData[rank + ":ChatColor"]);
                Users.AddSetting(HWID, "Max Homes", PermissionData[rank + ":MaxHomes"]);
                Users.AddSetting(HWID, "Home Cooldown", PermissionData[rank + ":HomeCooldown"]);
                Users.AddSetting(HWID, "Home Teleport Delay", PermissionData[rank + ":HomeTeleportDelay"]);
                Users.AddSetting(HWID, "Allowed Kits", PermissionData[rank + ":AllowedKits"]);
                Users.AddSetting(HWID, "Teleport Locations", PermissionData[rank + ":TeleportLocations"]);
                Users.AddSetting(HWID, "Can Update Ranks", PermissionData[rank + ":CanUpdateRanks"]);
                Users.AddSetting(HWID, "Can Use Broadcast", PermissionData[rank + ":CanUseBroadcast"]);
                Users.AddSetting(HWID, "Can Use Info", PermissionData[rank + ":CanUseInfo"]);
                Users.AddSetting(HWID, "Can Use Moderator Teleport", PermissionData[rank + ":CanUseModeratorTeleport"]);
                Users.Save();
            }
            else
            {
                Users.AddSetting(HWID, "Rank", defaultRank);
                Users.AddSetting(HWID, "Current Points", "0");
                Users.AddSetting(HWID, "Reserved Slot", PermissionData[defaultRank + ":JoinOnFullServer"]);
                Users.AddSetting(HWID, "Chat Prefix", PermissionData[defaultRank + ":ChatPrefix"]);
                Users.AddSetting(HWID, "Chat Color", PermissionData[defaultRank + ":ChatColor"]);
                Users.AddSetting(HWID, "Max Homes", PermissionData[defaultRank + ":MaxHomes"]);
                Users.AddSetting(HWID, "Home Cooldown", PermissionData[defaultRank + ":HomeCooldown"]);
                Users.AddSetting(HWID, "Home Teleport Delay", PermissionData[defaultRank + ":HomeTeleportDelay"]);
                Users.AddSetting(HWID, "Allowed Kits", PermissionData[defaultRank + ":AllowedKits"]);
                Users.AddSetting(HWID, "Teleport Locations", PermissionData[defaultRank + ":TeleportLocations"]);
                Users.AddSetting(HWID, "Can Update Ranks", PermissionData[defaultRank + ":CanUpdateRanks"]);
                Users.AddSetting(HWID, "Can Use Broadcast", PermissionData[defaultRank + ":CanUseBroadcast"]);
                Users.AddSetting(HWID, "Can Use Info", PermissionData[defaultRank + ":CanUseInfo"]);
                Users.AddSetting(HWID, "Can Use Moderator Teleport", PermissionData[defaultRank + ":CanUseModeratorTeleport"]);
                Users.Save();
            }
            foreach (string setting in Users.EnumSection(HWID))
            {
                if (PermissionData.ContainsKey(HWID + ":" + setting.Replace(" ", "")))
                {
                    PermissionData.Remove(HWID + ":" + setting.Replace(" ", ""));
                }
                PermissionData.Add(HWID + ":" + setting.Replace(" ", ""), Users.GetSetting(HWID, setting));
            }
        }

        public void UpdatePerms(string HWID = null)
		{
			if (HWID == null)
			{
				PermissionData.Clear();
                foreach (var obj in API.RustBusterUsersList)
                {
					foreach (string setting in Users.EnumSection(obj.HardwareID))
					{
						PermissionData.Add(obj.HardwareID + ":" + setting.Replace(" ", ""), Users.GetSetting(obj.HardwareID, setting));
					}
				}
			}
			else
			{
                if (Users.ContainsSetting(HWID, "Rank"))
                {
                    Thread thread = new Thread(() => AddPerms(HWID, CheckPerm(HWID + ":Rank")));
                    thread.Start();
                }
                else
                {
                    Thread thread = new Thread(() => AddPerms(HWID, defaultRank));
                    thread.Start();
                }
			}
		}

		public string CheckPerm(string perm)
		{
			try
			{
				if (PermissionData.ContainsKey(perm))
				{
					return PermissionData[perm];
				}
				else
				{
					return null;
				}
			}
			catch
			{
				return null;
			}
		}

		public void RemovePerms(string HWID)
		{
			foreach (string key in PermissionData.Keys)
			{
				if (key.Contains(HWID))
				{
					PermissionData.Remove(key);
				}
			}
		}

        private static Vector3 StringToVector3(string sVector)
        {
            if (sVector.StartsWith("(") && sVector.EndsWith(")"))
            {
                sVector = sVector.Substring(1, sVector.Length - 2);
            }
            string[] sArray = sVector.Split(',');
            Vector3 result = new Vector3(float.Parse(sArray[0]), float.Parse(sArray[1]), float.Parse(sArray[2]));
            return result;
        }

        private Boolean CheckSettings(string setting)
		{
			try
			{
				if (SettingsData.ContainsKey(setting))
				{
					return SettingsData[setting];
				}
				else
				{
					return false;
				}
			}
			catch
			{
				return false;
			}
		}

		private List<string> FindQuotes(string[] args)
		{
            string str = string.Join(" ", args);
            string[] stringArray = str.Split('\"');
            List<string> matches = new List<string>();
            int count = 1;
            foreach (string item in stringArray)
            {
                if ((count % 2) == 0)
                {
                    matches.Add(item.Trim('"', ' ', '\\'));
                }
                count += 1;
            }
            return matches;
			
		}

		private string UppercaseFirst(string s)
		{
			if (string.IsNullOrEmpty(s))
			{
				return string.Empty;
			}
			return char.ToUpper(s[0]) + s.Substring(1);
		}

		private void TeleportDelay(DonatorRankTimedEvent TimedEvent)
		{
			var localdict = TimedEvent.Args;
			TimedEvent.Kill();
			var locationname = localdict["LocationName"].ToString();
			var location = localdict["Location"].ToString().Replace(" ", "");
			Fougerite.Player player = (Fougerite.Player)localdict["Player"];
			if (player != null)
			{
				if (float.Parse(localdict["Health"].ToString()) <= player.Health)
				{
					player.SafeTeleportTo(StringToVector3(location));
					DataStore.GetInstance().Add("DonatorRankTpCooldown", player.SteamID + "+" + locationname.Replace(" ", ""), DateTime.UtcNow.Ticks);
					player.InventoryNotice(locationname);
				}
				else
				{
					DataStore.GetInstance().Add("DonatorRankTpCooldown", player.SteamID + "+" + locationname.Replace(" ", ""), 0);
					player.MessageFrom("DonatorRank", "Teleport failed, You have taken damage! Try again!");
				}
			}
			else
			{
				DataStore.GetInstance().Add("DonatorRankTpCooldown", player.SteamID + "+" + locationname.Replace(" ", ""), 0);
				return;
			}
		}

		private DonatorRankTimedEvent CreateParallelTimer(int timeoutDelay, Dictionary<string, object> args = null)
		{
			DonatorRankTimedEvent timedEvent = new DonatorRankTimedEvent(timeoutDelay);
			timedEvent.Args = args;
			return timedEvent;
		}

        public object Find_Player(string HWID)
        {
            foreach (var obj in API.RustBusterUsersList)
            {
                if (obj.HardwareID == HWID)
                {
                    return obj;
                }
            }
            return null;
        }

        public string GetHWID(string name)
        {
            List<string> list1 = new List<string>();
            foreach (var obj in API.RustBusterUsersList)
            {
                if (obj.Name.ToLower().Contains(name.ToLower()))
                {
                    list1.Add(obj.HardwareID);
                }
            }
            if (list1.Count >= 1)
                return list1[0];
            return null;
        }
    }
}
