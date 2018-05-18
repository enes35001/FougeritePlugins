using Fougerite;
using RustBuster2016Server;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using UnityEngine;

namespace AdminPlusServer
{
    public class AdminPlusServer : Module
    {
        internal Dictionary<string, string> _boundSteamIDs = new Dictionary<string, string>();
        internal Dictionary<string, Vector3> LastUserLocation = new Dictionary<string, Vector3>();
        internal List<string> AllowedToUse = new List<string>();
        internal List<string> DestroyMode = new List<string>();
        internal List<string> onlineplayers = new List<string>();
        internal IniParser Boundini;
        internal RustPPExtension rpp = new RustPPExtension();
        //HWID - SLOT - ITEM NAME - QTY
        internal Dictionary<string, Dictionary<int, Dictionary<string, int>>> AdminInventory = new Dictionary<string, Dictionary<int, Dictionary<string, int>>>();

        private GameObject myGameObject;
        private AdminPlusRPC rpc;

        internal bool RustBusterSupport = false;

        public override string Name
        {
            get { return "AdminPlusServer"; }
        }

        public override string Author
        {
            get { return "Jakkee"; }
        }

        public override string Description
        {
            get { return "Server module for AdminPlus"; }
        }

        public override Version Version
        {
            get { return new Version("3.0.1"); }
        }

        public override void DeInitialize()
        {
            Hooks.OnModulesLoaded -= OnModulesLoaded;
            
            if (RustBusterSupport)
            {
                Hooks.OnPlayerApproval -= OnPlayerApproval;
                API.OnRustBusterUserMessage -= OnRustBusterUserMessage;
                Hooks.OnEntityHurt -= OnEntityHurt;
                Hooks.OnPlayerConnected -= OnPlayerConnected;
                Hooks.OnPlayerDisconnected -= OnPlayerDisconnected;
                if (myGameObject != null)
                {
                    UnityEngine.Object.Destroy(myGameObject);
                }
            }
        }

        public override void Initialize()
        {
            Hooks.OnModulesLoaded += OnModulesLoaded;
        }

        private void OnModulesLoaded()
        {
            try
            {
                Logger.LogDebug("-------AdminPlus V" + Version + "-------");
                foreach (var x in ModuleManager.Modules)
                {
                    if (!x.Plugin.Name.ToLower().Contains("rustbuster")) continue;
                    RustBusterSupport = true;
                    break;
                }
                if (RustBusterSupport)
                {
                    Logger.LogDebug("Found Rustbuster...");

                    Hooks.OnPlayerApproval += OnPlayerApproval;
                    API.OnRustBusterUserMessage += OnRustBusterUserMessage;
                    Hooks.OnEntityHurt += OnEntityHurt;
                    Hooks.OnPlayerConnected += OnPlayerConnected;
                    Hooks.OnPlayerDisconnected += OnPlayerDisconnected;

                    Logger.LogDebug("Loaded hooks...");

                    myGameObject = new GameObject();
                    rpc = myGameObject.AddComponent<AdminPlusRPC>();

                    if (!File.Exists(Path.Combine(ModuleFolder, "BoundSteamIDs.ini")))
                    {
                        File.Create(Path.Combine(ModuleFolder, "BoundSteamIDs.ini")).Dispose();
                        Boundini = new IniParser(Path.Combine(ModuleFolder, "BoundSteamIDs.ini"));
                        Boundini.Save();
                        Logger.LogDebug("Created new BoundSteamIDs.ini file...");
                    }
                    Boundini = new IniParser(Path.Combine(ModuleFolder, "BoundSteamIDs.ini"));

                    Logger.LogDebug("Loaded BoundSteamIDs.ini file...");

                    BoundIniToList();

                    if (truth.punish)
                    {
                        truth.punish = false;
                        Logger.LogDebug("Disabling turth.punish...");
                    }
                }
                else
                {
                    Logger.LogWarning("AdminPlus: Could not find RustBuster");
                    Logger.LogWarning("AdminPlus: This plugin is useless without it!");
                }
                Logger.LogDebug("-------AdminPlus Loaded-------");
            }
            catch (Exception ex)
            {
                Logger.LogError("[AdminPlus] Error starting plugin");
                Logger.LogException(ex);
            }
        }

        public void OnRustBusterUserMessage(API.RustBusterUserAPI user, Message msgc)
        {
            if (msgc.PluginSender == "AdminPlusClient")
            {
                string msg = msgc.MessageByClient;
                string[] split = msg.Split('-');
                if (split[0] == "IsAllowed")
                {
                    Fougerite.Player player = user.Player;
                    if (player.Admin || player.Moderator)
                    {
                        msgc.ReturnMessage = "yes";
                    }
                    else
                    {
                        msgc.ReturnMessage = "no";
                    }
                }
                else
                {
                    //Fougerite.Server.GetServer().Broadcast("Message: " + split[0]);
                    Fougerite.Player SenderPlayer = FindPlayerByHWID(user.HardwareID);
                    if (SenderPlayer != null && SenderPlayer.Admin || SenderPlayer.Moderator)
                    {
                        Fougerite.Player target;
                        switch (split[0])
                        {
                            case "GetPlayers":
                                if (split.Length == 2)
                                {
                                    Dictionary<string, string> temp = new Dictionary<string, string>();
                                    List<Fougerite.Player> here = Fougerite.Server.GetServer().Players;
                                    try
                                    {
                                        if (here.Count > 0)
                                        {
                                            foreach (Fougerite.Player player in here)
                                            {
                                                if (player.SteamID != SenderPlayer.SteamID)
                                                {
                                                    temp.Add(GetHWIDFromSteamID(player.SteamID), player.Name);
                                                }
                                                else
                                                {
                                                    temp.Add(user.HardwareID, user.Name);
                                                }
                                            }
                                            rpc.SendMessageToPlayer(SenderPlayer, "AddPlayerToList", temp);
                                            msgc.ReturnMessage = "yes";
                                        }
                                    }
                                    catch (Exception ex)
                                    {
                                        Fougerite.Server.GetServer().Broadcast(ex.StackTrace);
                                        Fougerite.Server.GetServer().Broadcast(ex.Message);
                                    }
                                }
                                break;

                            case "AdminMode":
                                if (split.Length == 2)
                                {
                                    target = SenderPlayer;
                                    if (target != null && target.IsOnline && target.IsAlive)
                                    {
                                        if (AdminInventory.ContainsKey(user.HardwareID))
                                        {
                                            target.Inventory.ClearAll();
                                            foreach (int slot in AdminInventory[user.HardwareID].Keys)
                                            {
                                                foreach (string item in AdminInventory[user.HardwareID][slot].Keys)
                                                {
                                                    target.Inventory.AddItemTo(item, slot, AdminInventory[user.HardwareID][slot][item]);
                                                }
                                            }
                                            AdminInventory.Remove(user.HardwareID);
                                            Fougerite.Server.GetServer().BroadcastNotice(user.Name + " has gone off duty!");
                                        }
                                        else
                                        {
                                            try
                                            {
                                                int count = 0;
                                                Dictionary<int, Dictionary<string, int>> dictslot = new Dictionary<int, Dictionary<string, int>>();
                                                foreach (PlayerItem x in target.Inventory.Items)
                                                {
                                                    if (!x.IsEmpty())
                                                    {
                                                        //HWID - SLOT - ITEM NAME - QTY
                                                        count++;
                                                        dictslot.Add(x.Slot, new Dictionary<string, int> { { x.Name, x.Quantity} });
                                                    }
                                                }
                                                foreach (PlayerItem x in target.Inventory.ArmorItems)
                                                {
                                                    if (!x.IsEmpty())
                                                    {
                                                        //HWID - SLOT - ITEM NAME - QTY
                                                        count++;
                                                        dictslot.Add(x.Slot, new Dictionary<string, int> { { x.Name, x.Quantity } });
                                                    }
                                                }
                                                foreach (PlayerItem x in target.Inventory.BarItems)
                                                {
                                                    if (!x.IsEmpty())
                                                    {
                                                        //HWID - SLOT - ITEM NAME - QTY
                                                        count++;
                                                        dictslot.Add(x.Slot, new Dictionary<string, int> { { x.Name, x.Quantity } });
                                                    }
                                                }
                                                AdminInventory.Add(user.HardwareID, dictslot);
                                                target.Inventory.ClearAll();
                                                target.Inventory.AddItemTo("Invisible Helmet", 36, 1);
                                                target.Inventory.AddItemTo("Invisible Vest", 37, 1);
                                                target.Inventory.AddItemTo("Invisible Pants", 38, 1);
                                                target.Inventory.AddItemTo("Invisible Boots", 39, 1);
                                                Fougerite.Server.GetServer().BroadcastNotice(user.Name + " is now on duty!");
                                            }
                                            catch (Exception ex)
                                            {
                                                Fougerite.Server.GetServer().Broadcast(ex.StackTrace);
                                                Fougerite.Server.GetServer().Broadcast(ex.Message);
                                            }
                                        }
                                    }
                                }    
                                break;

                            case "ServerTime":
                                float time = float.Parse(split[1]);
                                World.GetWorld().Time = time;
                                break;

                            case "GiveKit":
                                if (split.Length == 4)
                                {
                                    //GiveKit - Kit - HWID
                                    //Fougerite.Player target;
                                    if (split[2] == user.HardwareID)
                                    {
                                        target = SenderPlayer;
                                    }
                                    else
                                    {
                                        target = FindPlayerByHWID(split[2]);
                                    }
                                    if (target != null && target.IsOnline && target.IsAlive)
                                    {
                                        if (target.Inventory.FreeSlots > 0)
                                        {
                                            switch (split[1])
                                            {
                                                case "KitWood":
                                                    target.Inventory.AddItem("Wood Pillar", 250);
                                                    target.Inventory.AddItem("Wood Foundation", 250);
                                                    target.Inventory.AddItem("Wood Wall", 250);
                                                    target.Inventory.AddItem("Wood Doorway", 250);
                                                    target.Inventory.AddItem("Wood Window", 250);
                                                    target.Inventory.AddItem("Wood Stairs", 250);
                                                    target.Inventory.AddItem("Wood Ramp", 250);
                                                    target.Inventory.AddItem("Wood Ceiling", 250);
                                                    target.Inventory.AddItem("Metal Door", 15);
                                                    target.Inventory.AddItem("Metal Window Bars", 15);
                                                    target.InventoryNotice("Received Wood Kit");
                                                    break;
                                                case "KitMetal":
                                                    target.Inventory.AddItem("Metal Pillar", 250);
                                                    target.Inventory.AddItem("Metal Foundation", 250);
                                                    target.Inventory.AddItem("Metal Wall", 250);
                                                    target.Inventory.AddItem("Metal Doorway", 250);
                                                    target.Inventory.AddItem("Metal Window", 250);
                                                    target.Inventory.AddItem("Metal Stairs", 250);
                                                    target.Inventory.AddItem("Metal Ramp", 250);
                                                    target.Inventory.AddItem("Metal Ceiling", 250);
                                                    target.Inventory.AddItem("Metal Door", 15);
                                                    target.Inventory.AddItem("Metal Window Bars", 15);
                                                    target.InventoryNotice("Received Metal Kit");
                                                    break;
                                                case "KitWeapons":
                                                    target.Inventory.AddItem("Bolt Action Rifle", 1);
                                                    target.Inventory.AddItem("M4", 1);
                                                    target.Inventory.AddItem("MP5A4", 1);
                                                    target.Inventory.AddItem("9mm Pistol", 1);
                                                    target.Inventory.AddItem("P250", 1);
                                                    target.Inventory.AddItem("Shotgun", 1);
                                                    target.Inventory.AddItem("556 Ammo", 250);
                                                    target.Inventory.AddItem("9mm Ammo", 250);
                                                    target.Inventory.AddItem("Shotgun Shells", 250);
                                                    target.InventoryNotice("Received Weapons Kit");
                                                    break;
                                                case "KitUber":
                                                    target.Inventory.AddItem("Uber Hatchet", 1);
                                                    target.Inventory.AddItem("Uber Hunting Bow", 1);
                                                    target.Inventory.AddItem("Arrow", 80);
                                                    target.InventoryNotice("Received Uber Kit");
                                                    break;
                                                case "KitKevlar":
                                                    target.Inventory.RemoveItem(36);
                                                    target.Inventory.RemoveItem(37);
                                                    target.Inventory.RemoveItem(38);
                                                    target.Inventory.RemoveItem(39);
                                                    target.Inventory.AddItemTo("Kevlar Helmet", 36, 1);
                                                    target.Inventory.AddItemTo("Kevlar Vest", 37, 1);
                                                    target.Inventory.AddItemTo("Kevlar Pants", 38, 1);
                                                    target.Inventory.AddItemTo("Kevlar Boots", 39, 1);
                                                    target.InventoryNotice("Received Kevlar Armour");
                                                    break;
                                                case "KitAdmin":
                                                    target.Inventory.RemoveItem(36);
                                                    target.Inventory.RemoveItem(37);
                                                    target.Inventory.RemoveItem(38);
                                                    target.Inventory.RemoveItem(39);
                                                    target.Inventory.AddItemTo("Invisible Helmet", 36, 1);
                                                    target.Inventory.AddItemTo("Invisible Vest", 37, 1);
                                                    target.Inventory.AddItemTo("Invisible Pants", 38, 1);
                                                    target.Inventory.AddItemTo("Invisible Boots", 39, 1);
                                                    target.InventoryNotice("Received Admin Suit");
                                                    break;
                                            }
                                            if (split[2] != user.HardwareID)
                                            {
                                                target.Notice(user.Name + " has given you a kit");
                                            }
                                        }
                                    }

                                }
                                break;

                            case "GiveItem":
                                if (split.Length == 5)
                                {
                                    //GiveItem - Item Name - Amount - Target HWID
                                    if (split[3] == user.HardwareID)
                                    {
                                        target = SenderPlayer;
                                    }
                                    else
                                    {
                                        target = FindPlayerByHWID(split[3]);
                                    }
                                    if (target != null && target.IsOnline && target.IsAlive)
                                    {
                                        if (target.Inventory.FreeSlots > 0)
                                        {
                                            target.Inventory.AddItem(split[1], int.Parse(split[2]));
                                            if (split[3] == user.HardwareID)
                                            {
                                                target.InventoryNotice(split[2] + "x " + split[1]);
                                            }
                                            else
                                            {
                                                target.Notice(user.Name + " has given you " + split[2] + "x " + split[1]);
                                            }
                                        }
                                    }
                                }
                                break;

                            case "Mute":
                                if (split.Length == 3)
                                {
                                    //Mute - Target HWID
                                    if (split[1] == user.HardwareID)
                                    {
                                        target = SenderPlayer;
                                    }
                                    else
                                    {
                                        target = FindPlayerByHWID(split[1]);
                                    }
                                    if (target != null && target.IsOnline && target.IsAlive)
                                    {
                                        rpp.Mute(target.UID, target.Name);
                                        target.Notice("", "You have been muted by " + user.Name, 15);
                                    }
                                }
                                break;

                            case "UnMute":
                                if (split.Length == 3)
                                {
                                    //UnMute - Target HWID
                                    if (split[1] == user.HardwareID)
                                    {
                                        target = SenderPlayer;
                                    }
                                    else
                                    {
                                        target = FindPlayerByHWID(split[1]);
                                    }
                                    if (target != null && target.IsOnline && target.IsAlive)
                                    {
                                        rpp.UnMute(target.UID);
                                        target.Notice("", "You have been unmuted by " + user.Name, 15);
                                    }
                                }
                                break;

                            case "Freeze":
                                if (split.Length == 3)
                                {
                                    //Freeze - Target HWID
                                    if (split[1] == user.HardwareID)
                                    {
                                        target = SenderPlayer;
                                    }
                                    else
                                    {
                                        target = FindPlayerByHWID(split[1]);
                                    }
                                    if (target != null && target.IsOnline && target.IsAlive)
                                    {
                                        rpc.SendMessageToPlayer(target, "FreezeMode", true);
                                        target.Notice("", "You have been frozen by " + user.Name, 15);
                                    }
                                }
                                break;

                            case "UnFreeze":
                                if (split.Length == 3)
                                {
                                    //UnFreeze - Target HWID
                                    if (split[1] == user.HardwareID)
                                    {
                                        target = SenderPlayer;
                                    }
                                    else
                                    {
                                        target = FindPlayerByHWID(split[1]);
                                    }
                                    if (target != null && target.IsOnline && target.IsAlive)
                                    {
                                        rpc.SendMessageToPlayer(target, "FreezeMode", false);
                                        target.Notice("", "You have been unfrozen by " + user.Name, 15);
                                    }
                                }
                                break;

                            case "ClearInventory":
                                if (split.Length == 3)
                                {

                                    //ClearInventory - Target HWID
                                    if (split[1] == user.HardwareID)
                                    {
                                        target = SenderPlayer;
                                    }
                                    else
                                    {
                                        target = FindPlayerByHWID(split[1]);
                                    }
                                    if (target != null && target.IsOnline && target.IsAlive)
                                    {
                                        target.Inventory.ClearAll();
                                        target.InventoryNotice("Inventory cleared");
                                    }
                                }
                                break;

                            case "ClearArmour":
                                if (split.Length == 3)
                                {

                                    //ClearInventory - Target HWID
                                    if (split[1] == user.HardwareID)
                                    {
                                        target = SenderPlayer;
                                    }
                                    else
                                    {
                                        target = FindPlayerByHWID(split[1]);
                                    }
                                    if (target != null && target.IsOnline && target.IsAlive)
                                    {
                                        target.Inventory.ClearArmor();
                                        target.InventoryNotice("Armour cleared");
                                    }
                                }
                                break;

                            case "Ban":
                                if (split.Length == 3)
                                {
                                    //Ban - Target HWID
                                    target = FindPlayerByHWID(split[1]);
                                    if (target != null && target.IsOnline)
                                    {
                                        Logger.LogWarning(user.Name + " has banned " + target.Name);
                                        Fougerite.Server.GetServer().BanPlayerIPandID(target.IP, target.SteamID, target.Name, "You have been banned [AdminPlus]", user.Name);
                                    }
                                }
                                break;

                            case "Kick":
                                if (split.Length == 3)
                                {
                                    //Kick - Target HWID
                                    target = FindPlayerByHWID(split[1]);
                                    if (target != null && target.IsOnline)
                                    {
                                        Logger.LogWarning(user.Name + " has kicked " + target.Name);
                                        target.Notice("You were kicked by " + user.Name);
                                        target.Disconnect(false);
                                    }
                                }
                                break;

                            case "Rename":
                                if (split.Length == 4)
                                {
                                    //Rename - NewName - Target HWID
                                    target = FindPlayerByHWID(split[2]);
                                    if (target != null && target.IsOnline && target.IsAlive)
                                    {
                                        target.Name = Base64ToString(split[1]);
                                        target.InventoryNotice("Name changed!");
                                        if (user.HardwareID != split[2])
                                        {
                                            target.Notice(user.Name + " has changed your name to: " + split[1]);
                                        }
                                    }
                                }
                                break;

                            case "GodMode":
                                if (split.Length == 2)
                                {
                                    target = SenderPlayer;
                                    if (rpp.HasGod(target.UID))
                                    {
                                        rpp.RemoveGod(target.UID);
                                        target.InventoryNotice("Disabled");
                                    }
                                    else
                                    {
                                        rpp.AddGod(target.UID);
                                        target.InventoryNotice("Enabled");
                                    }
                                }
                                break;

                            case "AdminDestroy":
                                if (split.Length == 2)
                                {
                                    target = SenderPlayer;
                                    if (target != null)
                                    {
                                        string steamid = target.SteamID;

                                        if (DestroyMode.Contains(steamid))
                                        {
                                            DestroyMode.Remove(steamid);
                                            target.InventoryNotice("Disabled");
                                        }
                                        else
                                        {
                                            DestroyMode.Add(steamid);
                                            target.InventoryNotice("Enabled");
                                        }
                                    }
                                }
                                break;

                            case "TeleportTo":
                                if (split.Length == 3)
                                {
                                    //TeleportTo - Target HWID
                                    if (split[1] == user.HardwareID)
                                    {
                                        target = SenderPlayer;
                                    }
                                    else
                                    {
                                        target = FindPlayerByHWID(split[1]);
                                    }
                                    if (target != null)
                                    {
                                        if (target.IsOnline)
                                        {
                                            if (target.IsAlive)
                                            {
                                                target.Notice("", user.Name + " has teleported to you!", 10);
                                                user.Player.SafeTeleportTo(target.Location, true);
                                                user.Player.Notice("✔", "You have teleported to " + target.Name, 10);
                                                
                                            }
                                            else
                                            {
                                                user.Player.Notice("✘", target.Name + " is currently not alive!");
                                            }
                                        }
                                        else
                                        {
                                            user.Player.Notice("✘", target.Name + " is not online!");
                                        }
                                    }
                                    else
                                    {
                                        user.Player.Notice("✘", "Could not find that player!");
                                    }
                                }
                                break;

                            case "TeleportToMe":
                                if (split.Length == 3)
                                {
                                    //TeleportToMe - Target HWID
                                    if (split[1] == user.HardwareID)
                                    {
                                        target = SenderPlayer;
                                    }
                                    else
                                    {
                                        target = FindPlayerByHWID(split[1]);
                                    }
                                    if (target != null)
                                    {
                                        if (target.IsOnline)
                                        {
                                            if (target.IsAlive)
                                            {
                                                LastUserLocation[split[1]] = target.Location;
                                                target.SafeTeleportTo(user.Player.Location, true);
                                                target.Notice("", user.Name + " has teleported you to them!", 10);
                                            }
                                            else
                                            {
                                                user.Player.Notice("✘", target.Name + " is currently not alive!");
                                            }
                                        }
                                        else
                                        {
                                            user.Player.Notice("✘", target.Name + " is not online!");
                                        }
                                    }
                                    else
                                    {
                                        user.Player.Notice("✘", "Could not find that player!");
                                    }
                                }
                                break; ;

                            case "SilentTeleport":
                                if (split.Length == 3)
                                {
                                    //Silent - Target HWID
                                    if (split[1] == user.HardwareID)
                                    {
                                        target = SenderPlayer;
                                    }
                                    else
                                    {
                                        target = FindPlayerByHWID(split[1]);
                                    }
                                    if (target != null)
                                    {
                                        if (target.IsOnline)
                                        {
                                            if (target.IsAlive)
                                            {
                                                user.Player.Inventory.RemoveItem(36);
                                                user.Player.Inventory.RemoveItem(37);
                                                user.Player.Inventory.RemoveItem(38);
                                                user.Player.Inventory.RemoveItem(39);
                                                user.Player.Inventory.AddItemTo("Invisible Helmet", 36, 1);
                                                user.Player.Inventory.AddItemTo("Invisible Vest", 37, 1);
                                                user.Player.Inventory.AddItemTo("Invisible Pants", 38, 1);
                                                user.Player.Inventory.AddItemTo("Invisible Boots", 39, 1);
                                                user.Player.SafeTeleportTo(Util.GetUtil().Infront(target, 10), true);
                                            }
                                            else
                                            {
                                                user.Player.Notice("✘", target.Name + " is currently not alive!", 10);
                                            }
                                        }
                                        else
                                        {
                                            user.Player.Notice("✘", target.Name + " is not online!", 10);
                                        }
                                    }
                                    else
                                    {
                                        user.Player.Notice("✘", "Could not find that player!", 10);
                                    }
                                }
                                break;

                            default:
                                break;
                        }
                    }
                    else
                    {
                        Logger.LogError("AdminPlus: " + user.Name + " just tried to use AdminPlus GUI but isn't an admin or moderator!");
                        Logger.LogError("AdminPlus: " + user.Name + " has possibly bypassed Admin authorization inside of the Client plugin");
                    }
                }
            }
        }

        public void OnPlayerConnected(Fougerite.Player player)
        {
            player.SendConsoleMessage("adminplus.load");
            onlineplayers.Add(GetHWIDFromSteamID(player.SteamID));
        }

        public void OnPlayerApproval(Fougerite.Events.PlayerApprovalEvent approvalEvent)
        {
            string id = approvalEvent.ClientConnection.UserID.ToString();
            string HWID = GetHWIDFromSteamID(id);
            string username = approvalEvent.ClientConnection.UserName;
            if (HWID != null)
            {
                if (_boundSteamIDs.ContainsValue(HWID))
                {
                    if (_boundSteamIDs.ContainsKey(id))
                    {
                        if (_boundSteamIDs[id] == HWID)
                        {
                            Logger.LogDebug("AdminPlus: " + username + " passed SteamID and HWID check");
                        }
                        else
                        {
                            Logger.LogDebug("AdminPlus: Rejected " + username + " due to another user using that SteamID, Needs to use Unban Tool");
                            approvalEvent.ClientConnection.playerApproval.Deny(uLink.NetworkConnectionError.DetectedDuplicatePlayerID);
                        }
                    }
                    else
                    {
                        string oldid = GetSteamIDFromHWID(HWID);
                        if (oldid != null)
                        {
                            BoundSteamIDs.Remove(oldid);
                            BoundSteamIDs.Add(id, HWID);
                            Logger.LogDebug("AdminPlus: " + username + " has changed their SteamID");
                            Logger.LogDebug("AdminPlus: Previous SteamID: " + oldid + " New SteamID: " + id);
                            Thread thread = new Thread(() =>
                            {
                                Boundini.AddSetting("BoundIDandHWID", id, HWID);
                                Boundini.Save();
                            })
                            {
                                IsBackground = true
                            };
                            thread.Start();
                        }
                    }
                }
                else
                {
                    BoundSteamIDs.Add(id, HWID);
                    Thread thread = new Thread(() =>
                    {
                        Boundini.AddSetting("BoundIDandHWID", id, HWID);
                        Boundini.Save();
                    })
                    {
                        IsBackground = true
                    };
                    thread.Start();
                    Logger.LogDebug("AdminPlus: " + username + " is a new player, Binding SteamID and HWID together");
                }
            }
        }

        public void OnEntityHurt(Fougerite.Events.HurtEvent hurtEvent)
        {
            try
            {
                if (!hurtEvent.IsDecay && hurtEvent.AttackerIsPlayer)
                {
                    Fougerite.Player player = hurtEvent.Attacker as Fougerite.Player;
                    if (DestroyMode.Contains(player.SteamID))
                    {
                        if (hurtEvent.Entity != null)
                        {
                            hurtEvent.Entity.Destroy();
                        }
                    }
                }
            }
            catch
            {

            }
        }

        public void OnPlayerDisconnected(Fougerite.Player notused)
        {
            List<string> players = new List<string>();
            foreach (Fougerite.Player player in Fougerite.Server.GetServer().Players)
            {
                players.Add(GetHWIDFromSteamID(player.SteamID));
            }

            var offline = players.Except(onlineplayers);
            foreach (string hwid in offline)
            {
                Logger.Log(hwid);
                rpc.SendMessageToAll("RemovePlayerFromList", hwid);
                if (AdminInventory.ContainsKey(hwid))
                {
                    Fougerite.Server.GetServer().BroadcastNotice(notused.Name + " has gone off duty!");
                }
            }
        }

        internal string ToBase64(string text)
        {
            if (text == null)
            {
                return null;
            }

            try
            {
                byte[] textAsBytes = Encoding.UTF8.GetBytes(text);
                return Convert.ToBase64String(textAsBytes);
            }
            catch
            {
                return null;
            }
        }

        internal string Base64ToString(string encodedText)
        {
            if (encodedText == null)
            {
                return null;
            }

            try
            {
                byte[] textAsBytes = Convert.FromBase64String(encodedText);
                return Encoding.UTF8.GetString(textAsBytes);
            }
            catch
            {
                return null;
            }
        }

        public Fougerite.Player FindPlayerByHWID(string HWID)
        {
            foreach (API.RustBusterUserAPI x in API.RustBusterUsersList)
            {
                if (HWID == x.HardwareID)
                {
                    return Fougerite.Server.GetServer().FindPlayer(x.SteamID);
                }
            }
            return null;
        }

        public string GetHWIDFromSteamID(string steamid)
        {
            foreach (API.RustBusterUserAPI obj in API.RustBusterUsersList)
            {
                if (obj.SteamID == steamid)
                {
                    return obj.HardwareID;
                }
            }
            return null;
        }

        public string GetSteamIDFromHWID(string hwid)
        {
            string key = null;
            foreach (KeyValuePair<string, string> pair in _boundSteamIDs)
            {
                if (pair.Value == hwid)
                {
                    key = pair.Key;
                    break;
                }
            }
            return key;
        }

        public Dictionary<string, string> BoundSteamIDs
        {
            get
            {
                return _boundSteamIDs;
            }
        }

        public Dictionary<string, string> ReverseBoundIDs()
        {
            Dictionary<string, string> temp = new Dictionary<string, string>();
            foreach (string x in BoundSteamIDs.Keys)
            {
                temp.Add(BoundSteamIDs[x], x);
            }
            return temp;
        }

        private void BoundIniToList()
        {
            foreach (string key in Boundini.EnumSection("BoundIDandHWID"))
            {
                BoundSteamIDs.Add(key, Boundini.GetSetting("BoundIDandHWID", key));
            }
        }

    }
}
