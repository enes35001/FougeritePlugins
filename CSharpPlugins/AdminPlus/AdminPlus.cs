using Fougerite;
using System;
using System.Collections.Generic;
using System.IO;
using RustBuster2016Server;
using UnityEngine;

namespace AdminPlus
{
    public class AdminPlus : Fougerite.Module
    {
        public bool Admin_Destroy;
        public bool Moderators_Use;
        public bool Use_On_Duty;
        public string Admin_Destroy_Weapon;
        public float Admin_TP_Distance;
        private IniParser Settings;
        private List<string> ToggledUsers = new List<string> { "a0e1f8200a5f22f49567f527fd53d022791b1b8f" };
        private List<string> OnDutyUsers = new List<string> { "a0e1f8200a5f22f49567f527fd53d022791b1b8f" };
        private Dictionary<String, Vector3> TeleportData = new Dictionary<string, Vector3> { };

        #region Plugin Info

        public override string Name
        {
            get
            {
                return "AdminPlus";
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
                return "[All-In-One]Admin tool that makes you Invisible, Spawns kits, Clears inventory, AdminTP/Doors + MORE";
            }
        }

        public override Version Version
        {
            get
            {
                return new Version("2.0.1");
            }
        }

        #endregion

        #region Initialize

        public override void Initialize()
        {
            if (!File.Exists(Path.Combine(ModuleFolder, "Settings.ini")))
            {
                File.Create(Path.Combine(ModuleFolder, "Settings.ini")).Dispose();
                Settings = new IniParser(Path.Combine(ModuleFolder, "Settings.ini"));
                Settings.AddSetting("Config", "Use Admin destroy", "True");
                Settings.AddSetting("Config", "Moderators can use", "True");
                Settings.AddSetting("Config", "Use /duty", "true");
                Settings.AddSetting("Config", "Admin destroy weapon", "Uber Hatchet");
                Settings.AddSetting("Config", "Admin TP distance", "30");
                Settings.Save();
            }
            else
            {
                Settings = new IniParser(Path.Combine(ModuleFolder, "Settings.ini"));
                Admin_Destroy = bool.Parse(Settings.GetSetting("Config", "Use Admin destroy"));
                Moderators_Use = bool.Parse(Settings.GetSetting("Config", "Moderators can use"));
                Use_On_Duty = bool.Parse(Settings.GetSetting("Config", "Use /duty"));
                Admin_Destroy_Weapon = Settings.GetSetting("Config", "Admin destroy weapon");
                Admin_TP_Distance = float.Parse(Settings.GetSetting("Config", "Admin TP distance"));
            }

            Hooks.OnCommand += new Hooks.CommandHandlerDelegate(On_Command);
            Hooks.OnDoorUse += new Hooks.DoorOpenHandlerDelegate(On_DoorUse);
            Hooks.OnPlayerDisconnected += new Hooks.DisconnectionHandlerDelegate(On_PlayerDisconnected);
            Hooks.OnEntityHurt += new Hooks.EntityHurtDelegate(On_EntityHurt);

        }

        #endregion

        #region DeInitialize

        public override void DeInitialize()
        {
            Hooks.OnCommand -= new Hooks.CommandHandlerDelegate(On_Command);
            Hooks.OnDoorUse -= new Hooks.DoorOpenHandlerDelegate(On_DoorUse);
            Hooks.OnPlayerDisconnected -= new Hooks.DisconnectionHandlerDelegate(On_PlayerDisconnected);
            Hooks.OnEntityHurt -= new Hooks.EntityHurtDelegate(On_EntityHurt);
        }

        #endregion

        #region Core

        public void On_Command(Fougerite.Player player, string cmd, string[] args)
        {
            if (cmd == "admin")
            {
                if (Allowed(player))
                {
                    if (args.Length.Equals(0))
                    {
                        player.MessageFrom("AdminPlus", "/tpadmin [name] (Teleports you " + Admin_TP_Distance.ToString() + "m away from the target)");
                        player.MessageFrom("AdminPlus", "/tpback (Teleports you back to where you were)");
                        player.MessageFrom("AdminPlus", "/duty [on / off] (Tells the server if your on duty or not)");
                        player.MessageFrom("AdminPlus", "/admin [on / off] (Invisible suit)");
                        player.MessageFrom("AdminPlus", "/admin metal (Spawns metal building parts)");
                        player.MessageFrom("AdminPlus", "/admin wood (Spawns wood building parts)");
                        player.MessageFrom("AdminPlus", "/admin uber (Spawns uber items)");
                        player.MessageFrom("AdminPlus", "/admin kevlar (Spawns kevlar)");
                        player.MessageFrom("AdminPlus", "/admin clear (Clears your inventory)");
                        player.MessageFrom("AdminPlus", "/admin doors (Toggles you to open all doors)");
                        player.MessageFrom("AdminPlus", "/admin weapons (Gives you weapons + Ammo)");
                    }
                    else if (CheckDuty(player))
                    {
                        if (args[0] == "on")
                        {
                            player.Inventory.RemoveItem(36);
                            player.Inventory.RemoveItem(37);
                            player.Inventory.RemoveItem(38);
                            player.Inventory.RemoveItem(39);
                            player.Inventory.AddItemTo("Invisible Helmet", 36, 1);
                            player.Inventory.AddItemTo("Invisible Vest", 37, 1);
                            player.Inventory.AddItemTo("Invisible Pants", 38, 1);
                            player.Inventory.AddItemTo("Invisible Boots", 39, 1);
                            player.MessageFrom("AdminPlus", "You're now Invisible!");
                        }
                        else if (args[0] == "off")
                        {
                            player.Inventory.RemoveItem(36);
                            player.Inventory.RemoveItem(37);
                            player.Inventory.RemoveItem(38);
                            player.Inventory.RemoveItem(39);
                            player.MessageFrom("AdminPlus", "You're now Visible!");
                        }
                        else if (args[0] == "wood")
                        {
                            player.Inventory.AddItem("Wood Pillar", 250);
                            player.Inventory.AddItem("Wood Foundation", 250);
                            player.Inventory.AddItem("Wood Wall", 250);
                            player.Inventory.AddItem("Wood Doorway", 250);
                            player.Inventory.AddItem("Wood Window", 250);
                            player.Inventory.AddItem("Wood Stairs", 250);
                            player.Inventory.AddItem("Wood Ramp", 250);
                            player.Inventory.AddItem("Wood Ceiling", 250);
                            player.Inventory.AddItem("Metal Door", 15);
                            player.Inventory.AddItem("Metal Window Bars", 15);
                            player.MessageFrom("AdminPlus", "Wood building parts spawned!");
                        }
                        else if (args[0] == "weapons")
                        {
                            player.Inventory.AddItem("Bolt Action Rifle", 1);
                            player.Inventory.AddItem("M4", 1);
                            player.Inventory.AddItem("MP5A4", 1);
                            player.Inventory.AddItem("9mm Pistol", 1);
                            player.Inventory.AddItem("P250", 1);
                            player.Inventory.AddItem("Shotgun", 1);
                            player.Inventory.AddItem("556 Ammo", 250);
                            player.Inventory.AddItem("9mm Ammo", 250);
                            player.Inventory.AddItem("Shotgun Shells", 250);
                            player.MessageFrom("AdminPlus", "Weapons plus Ammo spawned!");
                        }
                        else if (args[0] == "metal")
                        {
                            player.Inventory.AddItem("Metal Pillar", 250);
                            player.Inventory.AddItem("Metal Foundation", 250);
                            player.Inventory.AddItem("Metal Wall", 250);
                            player.Inventory.AddItem("Metal Doorway", 250);
                            player.Inventory.AddItem("Metal Window", 250);
                            player.Inventory.AddItem("Metal Stairs", 250);
                            player.Inventory.AddItem("Metal Ramp", 250);
                            player.Inventory.AddItem("Metal Ceiling", 250);
                            player.Inventory.AddItem("Metal Door", 15);
                            player.Inventory.AddItem("Metal Window Bars", 15);
                            player.MessageFrom("AdminPlus", "Metal building parts spawned!");
                        }
                        else if (args[0] == "uber")
                        {
                            player.Inventory.AddItem("Uber Hatchet", 1);
                            player.Inventory.AddItem("Uber Hunting Bow", 1);
                            player.Inventory.AddItem("Arrow", 40);
                            player.MessageFrom("AdminPlus", "Uber items spawned!");
                        }
                        else if (args[0] == "kevlar")
                        {
                            player.Inventory.RemoveItem(36);
                            player.Inventory.RemoveItem(37);
                            player.Inventory.RemoveItem(38);
                            player.Inventory.RemoveItem(39);
                            player.Inventory.AddItemTo("Kevlar Helmet", 36, 1);
                            player.Inventory.AddItemTo("Kevlar Vest", 37, 1);
                            player.Inventory.AddItemTo("Kevlar Pants", 38, 1);
                            player.Inventory.AddItemTo("Kevlar Boots", 39, 1);
                            player.MessageFrom("AdminPlus", "I hope you have a legitimate reason why need this!");
                        }
                        else if (args[0] == "clear")
                        {
                            player.Inventory.ClearAll();
                            player.MessageFrom("AdminPlus", "Inventory cleared!");
                        }
                        else if (args[0] == "doors")
                        {
                            string hwid = GetHWID(player);
                            if (ToggledUsers.Contains(hwid))
                            {
                                ToggledUsers.Remove(hwid);
                                player.MessageFrom("AdminPlus", "You can now only open your own doors");
                            }
                            else
                            {
                                ToggledUsers.Add(hwid);
                                player.MessageFrom("AdminPlus", "You can now open any door");
                            }
                        }
                        else
                        {
                            player.MessageFrom("AdminPlus", "/tpadmin [name] (Teleports you " + Admin_TP_Distance.ToString() + "m away from the target)");
                            player.MessageFrom("AdminPlus", "/tpback (Teleports you back to where you were)");
                            player.MessageFrom("AdminPlus", "/duty [on / off] (Tells the server if your on duty or not)");
                            player.MessageFrom("AdminPlus", "/admin [on / off] (Invisible suit)");
                            player.MessageFrom("AdminPlus", "/admin metal (Spawns metal building parts)");
                            player.MessageFrom("AdminPlus", "/admin wood (Spawns wood building parts)");
                            player.MessageFrom("AdminPlus", "/admin uber (Spawns uber items)");
                            player.MessageFrom("AdminPlus", "/admin kevlar (Spawns kevlar)");
                            player.MessageFrom("AdminPlus", "/admin clear (Clears your inventory)");
                            player.MessageFrom("AdminPlus", "/admin doors (Toggles you to open all doors)");
                            player.MessageFrom("AdminPlus", "/admin weapons (Gives you weapons + Ammo)");
                        }
                    }
                    else
                    {
                        player.MessageFrom("AdminPlus", "You're not on duty!");
                    }
                }
                else
                {
                    player.MessageFrom("AdminPlus", "You're not allowed to use this command!");
                }
            }
            else if (cmd == "duty")
            {
                if (Allowed(player))
                {
                    if (args.Length.Equals(0))
                    {
                        player.MessageFrom("AdminPlus", "Usage: /duty [on/off]");
                    }
                    else if (args[0] == "on")
                    {
                        string hwid = GetHWID(player);
                        if (OnDutyUsers.Contains(hwid))
                        {
                            player.MessageFrom("AdminPlus", "You are already on duty!");
                        }
                        else
                        {
                            OnDutyUsers.Add(hwid);
                            Fougerite.Server.GetServer().BroadcastFrom("AdminPlus", player.Name + " is now on duty! Let him/her know if you need anything!");
                        }
                    }
                    else if (args[0] == "off")
                    {
                        string hwid = GetHWID(player);
                        if (OnDutyUsers.Contains(hwid))
                        {
                            OnDutyUsers.Remove(hwid);
                            Fougerite.Server.GetServer().BroadcastFrom("AdminPlus", player.Name + " is now off duty! Please direct questions to another admin!");
                        }
                        else
                        {
                            player.MessageFrom("AdminPlus", "You are already off duty!");
                        }
                    }
                    else
                    {
                        player.MessageFrom("AdminPlus", "Usage: /duty [on/off]");
                    }
                }
                else
                {
                    player.MessageFrom("AdminPlus", "You're not allowed to use this command!");
                }
            }
            else if (cmd == "tpadmin")
            {
                if (Allowed(player))
                {
                    if (CheckDuty(player))
                    {
                        if (args.Length.Equals(0))
                        {
                            player.MessageFrom("AdminPlus", "Usage: /tpadmin [Player Name]");
                        }
                        else
                        {
                            Fougerite.Player target = Fougerite.Server.GetServer().FindPlayer(string.Join(" ", args)) ?? null;
                            if (!target.Equals(null))
                            {
                                string hwid = GetHWID(player);
                                if (!TeleportData.ContainsKey(hwid))
                                {
                                    TeleportData.Add(hwid, player.Location);
                                }
                                Vector3 loc = Util.GetUtil().Infront(target, Admin_TP_Distance);
                                player.TeleportTo(loc.x, loc.y, loc.z);
                                player.MessageFrom("AdminPlus", "Teleported: " + Admin_TP_Distance.ToString() + "m infront of " + target.Name);
                                player.MessageFrom("AdminPlus", "Use /tpback to go back to your last location");
                            }
                            else
                            {
                                player.MessageFrom("AdminPlus", "Can not find player: " + string.Join(" ", args));
                            }
                        }
                    }
                    else
                    {
                        player.MessageFrom("AdminPlus", "You're not on duty!");
                    }
                }
                else
                {
                    player.MessageFrom("AdminPlus", "You're not allowed to use this command!");
                }
            }
            else if (cmd == "tpback")
            {
                if (Allowed(player))
                {
                    if (CheckDuty(player))
                    {
                        string hwid = GetHWID(player);
                        if (TeleportData.ContainsKey(hwid))
                        {
                            Vector3 loc = TeleportData[hwid];
                            player.TeleportTo(loc.x, loc.y, loc.z);
                            TeleportData.Remove(hwid);
                            player.MessageFrom("AdminPlus", "Teleported back!");
                        }
                        else
                        {
                            player.MessageFrom("AdminPlus", "Can not find any previous locations!");
                        }
                    }
                    else
                    {
                        player.MessageFrom("AdminPlus", "You're not on duty!");
                    }
                }
                else
                {
                    player.MessageFrom("AdminPlus", "You're not allowed to use this command!");
                }
            }
        }

        public void On_PlayerDisconnected(Fougerite.Player player)
        {
            try
            {
                string hwid = GetHWID(player);
                if (OnDutyUsers.Contains(hwid))
                {
                    Fougerite.Server.GetServer().BroadcastFrom("AdminPlus", player.Name + " is now off duty! Please direct questions to another admin!");
                    OnDutyUsers.Remove(hwid);
                }
            }
            catch
            {
                Fougerite.Logger.LogDebug("AdminPlus encountered an error during On_PlayerDisconnected (This will NOT effect the plugin)");
            }
        }

        public void On_DoorUse(Fougerite.Player player, Fougerite.Events.DoorEvent DoorEvent)
        {
            if (DoorCheck(player))
            {
                DoorEvent.Open = true;
            }
        }

        public void On_EntityHurt(Fougerite.Events.HurtEvent HurtEvent)
        {
            if (Admin_Destroy)
            {
                if (HurtEvent.AttackerIsPlayer && HurtEvent.VictimIsEntity)
                {
                    if (Allowed(HurtEvent.Attacker as Fougerite.Player))
                    {
                        if (HurtEvent.WeaponName == Admin_Destroy_Weapon)
                        {
                            HurtEvent.Entity.Destroy();
                        }
                    }
                }
            }
        }

        #endregion

        #region Helper Methods

        public bool Allowed(Fougerite.Player player)
        {
            if (player.Admin)
            {
                return true;
            }
            else
            {
                if (player.Moderator && Moderators_Use)
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
        }

        public bool CheckDuty(Fougerite.Player player)
        {
            if (Use_On_Duty)
            {
                if (OnDutyUsers.Contains(GetHWID(player)))
                {
                    return true;
                }
                else
                {
                    return false;
                }
            }
            else
            {
                return true;
            }
        }

        public bool DoorCheck(Fougerite.Player player)
        {
            if (ToggledUsers.Contains(GetHWID(player)))
            {
                return true;
            }
            else
            {
                return false;
            }
        }

        public string GetHWID(Fougerite.Player player)
        {
            string hwid = null;
            foreach (API.RustBusterUserAPI obj in API.RustBusterUsersList)
            {
                if (obj.Name == player.Name && obj.SteamID == player.SteamID)
                {
                    hwid = obj.HardwareID;
                    break;
                }
            }
            return hwid;
       }

        #endregion

    }
}