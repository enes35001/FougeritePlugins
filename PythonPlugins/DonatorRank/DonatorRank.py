# -*- coding: utf-8 -*-
__title__ = 'DonatorRank'
__author__ = 'Jakkee'
__version__ = '1.5.1'
 
import clr
clr.AddReferenceByPartialName("Fougerite")
import System
import math
import Fougerite
 
 
class DonatorRank:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Settings", "JoinMessages", "true")
            ini.AddSetting("Settings", "LeaveMessages", "true")
            ini.AddSetting("Settings", "ChatPrefix", "true")
            ini.AddSetting("Settings", "OwnerSteamID", "76561198135558142")
            ini.AddSetting("Settings", "OwnerColour", "[color cyan]")
            ini.AddSetting("Settings", "AdminColour", "[color cyan]")
            ini.AddSetting("Settings", "LogTps", "true")
            ini.AddSetting("Settings", "LogBroadcast", "true")
            ini.AddSetting("Settings", ";Below only works with HomeSystem installed", "")
            ini.AddSetting("Settings", "PlayerMaxhomes", "1")
            ini.AddSetting("ModSettings", "ModeratorColour", "[color white]")
            ini.AddSetting("ModSettings", "Maxhomes", "3")
            ini.AddSetting("DonatorSettings", "DonatorColour", "[color white]")
            ini.AddSetting("DonatorSettings", "Maxhomes", "3")
            ini.AddSetting("DonatorSettings", "LVL1KitCooldown", "80")
            ini.AddSetting("DonatorSettings", "LVL2KitCooldown", "80")
            ini.AddSetting("VIPSettings", "VIPColour", "[color white]")
            ini.AddSetting("VIPSettings", "Maxhomes", "2")
            ini.AddSetting("VIPSettings", "LVL1KitCooldown", "120")
            ini.AddSetting("VIPSettings", "LVL2KitCooldown", "120")
            ini.AddSetting("VKIT_Level1", "Inv1", "P250")
            ini.AddSetting("VKIT_Level1", "Qty1", "1")
            ini.AddSetting("VKIT_Level1", "Inv2", "9mm Ammo")
            ini.AddSetting("VKIT_Level1", "Qty2", "50")
            ini.AddSetting("VKIT_Level1", "Inv3", "Leather Helmet")
            ini.AddSetting("VKIT_Level1", "Qty3", "1")
            ini.AddSetting("VKIT_Level1", "Inv4", "Cloth Vest")
            ini.AddSetting("VKIT_Level1", "Qty4", "1")
            ini.AddSetting("VKIT_Level1", "Inv5", "Cloth Pants")
            ini.AddSetting("VKIT_Level1", "Qty5", "1")
            ini.AddSetting("VKIT_Level1", "Inv6", "Leather Boots")
            ini.AddSetting("VKIT_Level1", "Qty6", "1")
            ini.AddSetting("VKIT_Level1", "Inv7", "Large Medkit")
            ini.AddSetting("VKIT_Level1", "Qty7", "3")
            ini.AddSetting("VKIT_Level1", "Inv8", "Small Rations")
            ini.AddSetting("VKIT_Level1", "Qty8", "1")
            ini.AddSetting("VKIT_Level1", "Inv9", "Silencer")
            ini.AddSetting("VKIT_Level1", "Qty9", "1")
            ini.AddSetting("VKIT_Level2", "Inv1", "P250")
            ini.AddSetting("VKIT_Level2", "Qty1", "1")
            ini.AddSetting("VKIT_Level2", "Inv2", "9mm Ammo")
            ini.AddSetting("VKIT_Level2", "Qty2", "50")
            ini.AddSetting("VKIT_Level2", "Inv3", "Leather Helmet")
            ini.AddSetting("VKIT_Level2", "Qty3", "1")
            ini.AddSetting("VKIT_Level2", "Inv4", "Cloth Vest")
            ini.AddSetting("VKIT_Level2", "Qty4", "1")
            ini.AddSetting("VKIT_Level2", "Inv5", "Cloth Pants")
            ini.AddSetting("VKIT_Level2", "Qty5", "1")
            ini.AddSetting("VKIT_Level2", "Inv6", "Leather Boots")
            ini.AddSetting("VKIT_Level2", "Qty6", "1")
            ini.AddSetting("VKIT_Level2", "Inv7", "Large Medkit")
            ini.AddSetting("VKIT_Level2", "Qty7", "3")
            ini.AddSetting("VKIT_Level2", "Inv8", "Small Rations")
            ini.AddSetting("VKIT_Level2", "Qty8", "1")
            ini.AddSetting("VKIT_Level2", "Inv9", "Silencer")
            ini.AddSetting("VKIT_Level2", "Qty9", "1")
            ini.AddSetting("DKIT_Level1", "Inv1", "M4")
            ini.AddSetting("DKIT_Level1", "Qty1", "1")
            ini.AddSetting("DKIT_Level1", "Inv2", "556 Ammo")
            ini.AddSetting("DKIT_Level1", "Qty2", "90")
            ini.AddSetting("DKIT_Level1", "Inv3", "Leather Helmet")
            ini.AddSetting("DKIT_Level1", "Qty3", "1")
            ini.AddSetting("DKIT_Level1", "Inv4", "Leather Vest")
            ini.AddSetting("DKIT_Level1", "Qty4", "1")
            ini.AddSetting("DKIT_Level1", "Inv5", "Leather Pants")
            ini.AddSetting("DKIT_Level1", "Qty5", "1")
            ini.AddSetting("DKIT_Level1", "Inv6", "Leather Boots")
            ini.AddSetting("DKIT_Level1", "Qty6", "1")
            ini.AddSetting("DKIT_Level1", "Inv7", "Silencer")
            ini.AddSetting("DKIT_Level1", "Qty7", "1")
            ini.AddSetting("DKIT_Level1", "Inv8", "Large Medkit")
            ini.AddSetting("DKIT_Level1", "Qty8", "5")
            ini.AddSetting("DKIT_Level1", "Inv9", "Small Rations")
            ini.AddSetting("DKIT_Level1", "Qty9", "10")
            ini.AddSetting("DKIT_Level2", "Inv1", "M4")
            ini.AddSetting("DKIT_Level2", "Qty1", "1")
            ini.AddSetting("DKIT_Level2", "Inv2", "556 Ammo")
            ini.AddSetting("DKIT_Level2", "Qty2", "90")
            ini.AddSetting("DKIT_Level2", "Inv3", "Leather Helmet")
            ini.AddSetting("DKIT_Level2", "Qty3", "1")
            ini.AddSetting("DKIT_Level2", "Inv4", "Leather Vest")
            ini.AddSetting("DKIT_Level2", "Qty4", "1")
            ini.AddSetting("DKIT_Level2", "Inv5", "Leather Pants")
            ini.AddSetting("DKIT_Level2", "Qty5", "1")
            ini.AddSetting("DKIT_Level2", "Inv6", "Leather Boots")
            ini.AddSetting("DKIT_Level2", "Qty6", "1")
            ini.AddSetting("DKIT_Level2", "Inv7", "Silencer")
            ini.AddSetting("DKIT_Level2", "Qty7", "1")
            ini.AddSetting("DKIT_Level2", "Inv8", "Large Medkit")
            ini.AddSetting("DKIT_Level2", "Qty8", "5")
            ini.AddSetting("DKIT_Level2", "Inv9", "Small Rations")
            ini.AddSetting("DKIT_Level2", "Qty9", "10")
            ini.Save()
        if not Plugin.IniExists("TPLocations"):
            Plugin.CreateIni("TPLocations")
            ini = Plugin.GetIni("TPLocations")
            ini.AddSetting("EXAMPLE", ";location name here", "X, Y, Z")
            ini.AddSetting("EXAMPLE", ";ADDING A NEW LOCATION", "Just add the location name plus X/Y/Z location (Add 1 to the Y so players don't glitch into the ground)")
            ini.AddSetting("EXAMPLE", ";COOLDOWNS/DELAYS", "Cooldowns/delays are in seconds")
            ini.AddSetting("EXAMPLE", ";VIP House", "-1000, 450, 200")
            ini.AddSetting("Settings", "VTP Delay", "5")
            ini.AddSetting("Settings", "VTP Cooldown", "30")
            ini.AddSetting("Settings", "DTP Delay", "5")
            ini.AddSetting("Settings", "DTP Cooldown", "30")
            ini.AddSetting("VTP", "Small Rad", "6050, 381, -3620")
            ini.AddSetting("VTP", "Big Rad", "5250, 371, -4850")
            ini.AddSetting("VTP", "Factory Rad", "6300, 361, -4650")
            ini.AddSetting("VTP", "Hanger", "6600, 356, -4400")
            ini.AddSetting("DTP", "Small Rad", "6050, 381, -3620")
            ini.AddSetting("DTP", "Big Rad", "5250, 371, -4850")
            ini.AddSetting("DTP", "Factory Rad", "6300, 361, -4650")
            ini.AddSetting("DTP", "Hanger", "6600, 356, -4400")
            ini.AddSetting("DTP", "Oil Tankers", "6690, 356, -3880")
            ini.AddSetting("DTP", "North Hacker Valley", "5000, 461, -3000")
            ini.AddSetting("DTP", "French Valley", "6056, 385, -4162")
            ini.AddSetting("DTP", "North Next Valley", "4668, 445, -3908")
            ini.Save()
        users = self.getUserIni()
        if not len(users.Sections) == 0:
            for steamidKey in users.Sections:
                users.DeleteSetting(steamidKey, "CanKick")
                users.DeleteSetting(steamidKey, "CanBan")
        DataStore.Flush("DonatorRank")
        tp = Plugin.GetIni("TPLocations")
        DataStore.Add("DonatorRank", "VTPDELAY", int(tp.GetSetting("Settings", "VTP Delay")) * 1000)
        DataStore.Add("DonatorRank", "VTPCoolDown", int(tp.GetSetting("Settings", "VTP Cooldown")) * 1000)
        DataStore.Add("DonatorRank", "DTPDELAY", int(tp.GetSetting("Settings", "DTP Delay")) * 1000)
        DataStore.Add("DonatorRank", "DTPCoolDown", int(tp.GetSetting("Settings", "DTP Cooldown")) * 1000)
        count = 1
        for key in tp.EnumSection("VTP"):
            DataStore.Add("DonatorRank", "VTP" + str(count), key)
            DataStore.Add("DonatorRank", key, tp.GetSetting("VTP", key))
            count += 1
        count = 1
        for key in tp.EnumSection("DTP"):
            DataStore.Add("DonatorRank", "DTP" + str(count), key)
            DataStore.Add("DonatorRank", key, tp.GetSetting("DTP", key))
            count += 1
        ini = Plugin.GetIni("Settings")
        vkit1 = ini.EnumSection("VKIT_Level1")
        inv = 1
        qty = 1
        for key in vkit1:
            if key == "Inv" + str(inv):
                DataStore.Add("DonatorRank", "VKIT1_INV" + str(inv), ini.GetSetting("VKIT_Level1", key))
                inv += 1
            elif key == "Qty" + str(qty):
                DataStore.Add("DonatorRank", "VKIT1_QTY" + str(qty), ini.GetSetting("VKIT_Level1", key))
                qty += 1
        vkit2 = ini.EnumSection("VKIT_Level2")
        inv = 1
        qty = 1
        for key in vkit2:
            if key == "Inv" + str(inv):
                DataStore.Add("DonatorRank", "VKIT2_INV" + str(inv), ini.GetSetting("VKIT_Level2", key))
                inv += 1
            elif key == "Qty" + str(qty):
                DataStore.Add("DonatorRank", "VKIT2_QTY" + str(qty), ini.GetSetting("VKIT_Level2", key))
                qty += 1
        dkit1 = ini.EnumSection("DKIT_Level1")
        inv = 1
        qty = 1
        for key in dkit1:
            if key == "Inv" + str(inv):
                DataStore.Add("DonatorRank", "DKIT1_INV" + str(inv), ini.GetSetting("DKIT_Level1", key))
                inv += 1
            elif key == "Qty" + str(qty):
                DataStore.Add("DonatorRank", "DKIT1_QTY" + str(qty), ini.GetSetting("DKIT_Level1", key))
                qty += 1
        dkit2 = ini.EnumSection("DKIT_Level2")
        inv = 1
        qty = 1
        for key in dkit2:
            if key == "Inv" + str(inv):
                DataStore.Add("DonatorRank", "DKIT2_INV" + str(inv), ini.GetSetting("DKIT_Level2", key))
                inv += 1
            elif key == "Qty" + str(qty):
                DataStore.Add("DonatorRank", "DKIT2_QTY" + str(qty), ini.GetSetting("DKIT_Level2", key))
                qty += 1
        DataStore.Add("DonatorRank", "JoinMSG", ini.GetSetting("Settings", "JoinMessages"))
        DataStore.Add("DonatorRank", "LeaveMSG", ini.GetSetting("Settings", "LeaveMessages"))
        DataStore.Add("DonatorRank", "ChatPrefix", ini.GetSetting("Settings", "ChatPrefix"))
        DataStore.Add("DonatorRank", "OwnerID", ini.GetSetting("Settings", "OwnerSteamID"))
        DataStore.Add("DonatorRank", "OwnerColour", ini.GetSetting("Settings", "OwnerColour"))
        DataStore.Add("DonatorRank", "AdminColour", ini.GetSetting("Settings", "AdminColour"))
        DataStore.Add("DonatorRank", "ModColour", ini.GetSetting("ModSettings", "ModeratorColour"))
        DataStore.Add("DonatorRank", "DonatorColour", ini.GetSetting("DonatorSettings", "DonatorColour"))
        DataStore.Add("DonatorRank", "VIPColour", ini.GetSetting("VIPSettings", "VIPColour"))
        DataStore.Add("DonatorRank", "LogTPS", ini.GetSetting("Settings", "LogTps"))
        DataStore.Add("DonatorRank", "LogKicks", ini.GetSetting("Settings", "LogKicks"))
        DataStore.Add("DonatorRank", "LogBroadcasts", ini.GetSetting("Settings", "LogBroadcast"))
        DataStore.Add("DonatorRank", "PlayerHomesMax", ini.GetSetting("Settings", "PlayerMaxhomes"))
        DataStore.Add("DonatorRank", "ModHomesMax", ini.GetSetting("ModSettings", "Maxhomes"))
        DataStore.Add("DonatorRank", "DonatorHomesMax", ini.GetSetting("DonatorSettings", "Maxhomes"))
        DataStore.Add("DonatorRank", "VIPHomesMax", ini.GetSetting("VIPSettings", "Maxhomes"))
        DataStore.Add("DonatorRank", "LVL1DKITCoolDown", int(ini.GetSetting("DonatorSettings", "LVL1KitCooldown")) * 1000)
        DataStore.Add("DonatorRank", "LVL1VKITCoolDown", int(ini.GetSetting("VIPSettings", "LVL1KitCooldown")) * 1000)
        DataStore.Add("DonatorRank", "LVL2DKITCoolDown", int(ini.GetSetting("DonatorSettings", "LVL2KitCooldown")) * 1000)
        DataStore.Add("DonatorRank", "LVL2VKITCoolDown", int(ini.GetSetting("VIPSettings", "LVL2KitCooldown")) * 1000)
 
    def On_Command(self, Player, cmd, args):
        if cmd == "donatorhelp":
            if len(args) == 0:
                users = self.getUserIni()
                rank = users.GetSetting(Player.SteamID, "Rank")
                if Player.Admin or rank == "VIP" or rank == "Donator" or rank == "Mod":
                    if users.GetSetting(Player.SteamID, "AddVIPS") == "true" or Player.Admin:
                        Player.Message("/vadd [playername] - Add a player as Vip")
                    if users.GetSetting(Player.SteamID, "AddDonators") == "true" or Player.Admin:
                        Player.Message("/dadd [playername] - Add a player as Donator")
                    if users.GetSetting(Player.SteamID, "AddMods") == "true" or Player.Admin:
                        Player.Message("/madd [playername] - Add a player as Mod")
                    if users.GetSetting(Player.SteamID, "DelVIPS") == "true" or Player.Admin:
                        Player.Message("/vdel [playername] - Remove a player as Vip")
                    if users.GetSetting(Player.SteamID, "DelDonators") == "true" or Player.Admin:
                        Player.Message("/ddel [playername] - Remove a player as Donator")
                    if users.GetSetting(Player.SteamID, "DelMods") == "true" or Player.Admin:
                        Player.Message("/mdel [playername] - Remove a player as Mod")
                    if users.GetSetting(Player.SteamID, "LVL1VKIT") == "true" or Player.Admin:
                        Player.Message("/vkit basic - Get the basic VIP kit")
                    if users.GetSetting(Player.SteamID, "LVL2VKIT") == "true" or Player.Admin:
                        Player.Message("/vkit advanced - Get the advanced VIP kit")
                    if users.GetSetting(Player.SteamID, "LVL1DKIT") == "true" or Player.Admin:
                        Player.Message("/dkit basic - Get the basic Donator kit")
                    if users.GetSetting(Player.SteamID, "LVL2DKIT") == "true" or Player.Admin:
                        Player.Message("/dkit advanced - Get the advanced Donator kit")
                    if users.GetSetting(Player.SteamID, "MODKIT") == "true" or Player.Admin:
                        Player.Message("/mkit - Gives you invisible suit + uber items")
                    if users.GetSetting(Player.SteamID, "VTP") == "true" or Player.Admin:
                        Player.Message("/vtp - Teleport to preset locations")
                    if users.GetSetting(Player.SteamID, "DTP") == "true" or Player.Admin:
                        Player.Message("/dtp - Teleport to preset locations")
                    if users.GetSetting(Player.SteamID, "MTP") == "true" or Player.Admin:
                        Player.Message("/mtp [Name] - Teleport to a player")
                        Player.Message("/mtpback - Teleport back to where you were")
                    if users.GetSetting(Player.SteamID, "UseBroadcast") == "true" or Player.Admin:
                        Player.Message("/yell - Tell the server something")
                    if users.GetSetting(Player.SteamID, "AccessInfo") == "true" or Player.Admin:
                        Player.Message("/info [Name] - Get info about a player")
                else:
                    Player.MessageFrom("DonatorRank", "Contact a staff member about becoming a VIP or Donator")
            else:
                Player.Message("Usage: /donatorhelp")
 
        elif cmd == "yell":
            users = self.getUserIni()
            if users.GetSetting(Player.SteamID, "UseBroadcast") == "true" or Player.Admin:
                if args.Length > 0:
                    text = self.argsToText(args)
                    Server.BroadcastFrom("Player Broadcast", text)
                    if DataStore.Get("DonatorRank", "LogBroadcasts") == "true":
                        ini = self.getLogIni()
                        date = Plugin.GetDate()
                        time = Plugin.GetTime()
                        ini.AddSetting("BoardCasterLog", date + "|" + time + " || " + Player.Name, Player.SteamID + " said: [" + text + "]")
                        ini.Save()
                    else:
                        return
                else:
                    Player.Message("Usage: /yell [Message]")
            else:
                Player.Message("You don't have permission to use this command!")
 
        elif cmd == "vadd":
            users = self.getUserIni()
            if users.GetSetting(Player.SteamID, "AddVIPS") == "true" or Player.Admin:
                if len(args) == 0:
                    Player.Message("Usage: /vadd [playername]")
                elif len(args) > 0:
                    vipname = self.CheckV(Player, args)
                    if vipname is not None:
                        if self.isDonator(vipname):
                            Player.Message(vipname.Name + " is a Donator, use /ddel " + vipname.Name)
                        elif self.isMod(vipname):
                            Player.Message(vipname.Name + " is a Moderator, use /mdel " + vipname.Name)
                        elif not self.isVIP(vipname):
                            d = Plugin.GetDate()
                            t = Plugin.GetTime()
                            p = Player.Name
                            users.AddSetting(vipname.SteamID, "UserName", vipname.Name)
                            users.AddSetting(vipname.SteamID, "INFO", "Time: " + t + "||Date: " + d + "||By: " + p)
                            users.AddSetting(vipname.SteamID, "Rank", "VIP")
                            users.AddSetting(vipname.SteamID, "MaxHomes", DataStore.Get("DonatorRank", "VIPHomesMax"))
                            users.AddSetting(vipname.SteamID, "AddVIPS", "false")
                            users.AddSetting(vipname.SteamID, "AddDonators", "false")
                            users.AddSetting(vipname.SteamID, "AddMods", "false")
                            users.AddSetting(vipname.SteamID, "DelVIPS", "false")
                            users.AddSetting(vipname.SteamID, "DelDonators", "false")
                            users.AddSetting(vipname.SteamID, "DelMods", "false")
                            users.AddSetting(vipname.SteamID, "LVL1VKIT", "true")
                            users.AddSetting(vipname.SteamID, "LVL2VKIT", "false")
                            users.AddSetting(vipname.SteamID, "LVL1DKIT", "false")
                            users.AddSetting(vipname.SteamID, "LVL2DKIT", "false")
                            users.AddSetting(vipname.SteamID, "MODKIT", "false")
                            users.AddSetting(vipname.SteamID, "VTP", "true")
                            users.AddSetting(vipname.SteamID, "DTP", "false")
                            users.AddSetting(vipname.SteamID, "MTP", "false")
                            users.AddSetting(vipname.SteamID, "UseBroadcast", "true")
                            users.AddSetting(vipname.SteamID, "AccessInfo", "false")
                            users.Save()
                            Server.Broadcast("[color#FFFF00]" + vipname.Name + " [color#FFFFFF]is now a VIP!")
                            vipname.Message("Use /donatorhelp to show the command list available for you.")
                        else:
                            Player.Message(vipname.Name + " is already a VIP.")
            else:
                Player.Message("You don't have permission to use this command!")
 
        elif cmd == "dadd":
            users = self.getUserIni()
            if users.GetSetting(Player.SteamID, "AddDonators") == "true" or Player.Admin:
                if len(args) == 0:
                    Player.Message("Usage: /dadd [playername]")
                elif len(args) > 0:
                    donname = self.CheckV(Player, args)
                    if donname is not None:
                        if self.isVIP(donname):
                            Player.Message(donname.Name + " is a VIP, use /vdel " + donname.Name)
                        elif self.isMod(donname):
                            Player.Message(donname.Name + " is a Moderator, use /mdel " + donname.Name)
                        elif not self.isDonator(donname):
                            d = Plugin.GetDate()
                            t = Plugin.GetTime()
                            p = Player.Name
                            ds = DataStore
                            users.AddSetting(donname.SteamID, "UserName", donname.Name)
                            users.AddSetting(donname.SteamID, "INFO", "Time: " + t + "||Date: " + d + "||By: " + p)
                            users.AddSetting(donname.SteamID, "Rank", "Donator")
                            users.AddSetting(donname.SteamID, "MaxHomes", ds.Get("DonatorRank", "DonatorHomesMax"))
                            users.AddSetting(donname.SteamID, "AddVIPS", "false")
                            users.AddSetting(donname.SteamID, "AddDonators", "false")
                            users.AddSetting(donname.SteamID, "AddMods", "false")
                            users.AddSetting(donname.SteamID, "DelVIPS", "false")
                            users.AddSetting(donname.SteamID, "DelDonators", "false")
                            users.AddSetting(donname.SteamID, "DelMods", "false")
                            users.AddSetting(donname.SteamID, "LVL1VKIT", "false")
                            users.AddSetting(donname.SteamID, "LVL2VKIT", "false")
                            users.AddSetting(donname.SteamID, "LVL1DKIT", "true")
                            users.AddSetting(donname.SteamID, "LVL2DKIT", "false")
                            users.AddSetting(donname.SteamID, "MODKIT", "false")
                            users.AddSetting(donname.SteamID, "VTP", "false")
                            users.AddSetting(donname.SteamID, "DTP", "true")
                            users.AddSetting(donname.SteamID, "MTP", "false")
                            users.AddSetting(donname.SteamID, "UseBroadcast", "true")
                            users.AddSetting(donname.SteamID, "AccessInfo", "false")
                            users.Save()
                            Server.Broadcast("[color#FFFF00]" + donname.Name + " [color#FFFFFF]is now a Donator!")
                            donname.Message("Use /donatorhelp to show the command list available for you.")
                        else:
                            Player.Message(donname.Name + " is already a Donator")
            else:
                Player.Message("You don't have permission to use this command!")
 
        elif cmd == "madd":
            users = self.getUserIni()
            if users.GetSetting(Player.SteamID, "AddMods") == "true" or Player.Admin:
                if len(args) == 0:
                    Player.Message("Usage: /madd [playername]")
                elif len(args) > 0:
                    modname = self.CheckV(Player, args)
                    if modname is not None:
                        if self.isVIP(modname):
                            Player.Message(modname.Name + " is a VIP, use /vdel " + modname.Name)
                        elif self.isDonator(modname):
                            Player.Message(modname.Name + " is a Donator, use /ddel " + modname.Name)
                        elif not self.isMod(modname):
                            d = Plugin.GetDate()
                            t = Plugin.GetTime()
                            p = Player.Name
                            users.AddSetting(modname.SteamID, "UserName", modname.Name)
                            users.AddSetting(modname.SteamID, "INFO", "Time: " + t + "||Date: " + d + "||By: " + p)
                            users.AddSetting(modname.SteamID, "Rank", "Mod")
                            users.AddSetting(modname.SteamID, "MaxHomes", DataStore.Get("DonatorRank", "ModHomesMax"))
                            users.AddSetting(modname.SteamID, "AddVIPS", "true")
                            users.AddSetting(modname.SteamID, "AddDonators", "true")
                            users.AddSetting(modname.SteamID, "AddMods", "false")
                            users.AddSetting(modname.SteamID, "DelVIPS", "true")
                            users.AddSetting(modname.SteamID, "DelDonators", "true")
                            users.AddSetting(modname.SteamID, "DelMods", "false")
                            users.AddSetting(modname.SteamID, "LVL1VKIT", "false")
                            users.AddSetting(modname.SteamID, "LVL2VKIT", "false")
                            users.AddSetting(modname.SteamID, "LVL1DKIT", "false")
                            users.AddSetting(modname.SteamID, "LVL2DKIT", "false")
                            users.AddSetting(modname.SteamID, "MODKIT", "true")
                            users.AddSetting(modname.SteamID, "VTP", "false")
                            users.AddSetting(modname.SteamID, "DTP", "false")
                            users.AddSetting(modname.SteamID, "MTP", "true")
                            users.AddSetting(modname.SteamID, "UseBroadcast", "true")
                            users.AddSetting(modname.SteamID, "AccessInfo", "true")
                            users.Save()
                            Server.Broadcast("[color#FFFF00]" + modname.Name + " [color#FFFFFF]is now a Moderator!")
                            modname.Message("Use /donatorhelp to show the command list available for you.")
                        else:
                            Player.Message(modname.Name + " is already a Moderator")
            else:
                Player.Message("You don't have permission to use this command!")

        elif cmd == "addmoderator":
            if self.isMod(Player):
                if len(args) > 0:
                    name = self.CheckV(Player, args)
                    self.isMod(name)
            return
 
        elif cmd == "vdel":
            users = self.getUserIni()
            if users.GetSetting(Player.SteamID, "DelVIPS") == "true" or Player.Admin:
                if len(args) == 0:
                    Player.Message("Usage: /vdel [playername]")
                elif len(args) > 0:
                    vipname = self.CheckV(Player, args)
                    if vipname is not None:
                        if self.isDonator(vipname):
                            Player.Message(vipname.Name + " is a Donator, use /ddel " + vipname.Name)
                        elif self.isMod(vipname):
                            Player.Message(vipname.Name + " is a Moderator, use /mdel " + vipname.Name)
                        else:
                            users.DeleteSetting(vipname.SteamID, "UserName")
                            users.DeleteSetting(vipname.SteamID, "INFO")
                            users.DeleteSetting(vipname.SteamID, "Rank")
                            users.DeleteSetting(vipname.SteamID, "MaxHomes")
                            users.DeleteSetting(vipname.SteamID, "AddVIPS")
                            users.DeleteSetting(vipname.SteamID, "AddDonators")
                            users.DeleteSetting(vipname.SteamID, "AddMods")
                            users.DeleteSetting(vipname.SteamID, "DelVIPS")
                            users.DeleteSetting(vipname.SteamID, "DelDonators")
                            users.DeleteSetting(vipname.SteamID, "DelMods")
                            users.DeleteSetting(vipname.SteamID, "LVL1VKIT")
                            users.DeleteSetting(vipname.SteamID, "LVL2VKIT")
                            users.DeleteSetting(vipname.SteamID, "LVL1DKIT")
                            users.DeleteSetting(vipname.SteamID, "LVL2DKIT")
                            users.DeleteSetting(vipname.SteamID, "MODKIT")
                            users.DeleteSetting(vipname.SteamID, "VTP")
                            users.DeleteSetting(vipname.SteamID, "DTP")
                            users.DeleteSetting(vipname.SteamID, "MTP")
                            users.DeleteSetting(vipname.SteamID, "UseBroadcast")
                            users.DeleteSetting(vipname.SteamID, "AccessInfo")
                            users.Save()
                            Player.Message(vipname.Name + " is no longer a VIP")
                            vipname.Message("You are not longer a VIP")
            else:
                Player.Message("You don't have permission to use this command!")
 
        elif cmd == "ddel":
            users = self.getUserIni()
            if users.GetSetting(Player.SteamID, "DelDonators") == "true" or Player.Admin:
                if len(args) == 0:
                    Player.Message("Usage: /ddel [playername]")
                elif len(args) > 0:
                    donname = self.CheckV(Player, args)
                    if donname is not None:
                        if self.isVIP(donname):
                            Player.Message(donname.Name + " is a VIP, use /vdel " + donname.Name)
                        elif self.isMod(donname):
                            Player.Message(donname.Name + " is a Moderator, use /mdel " + donname.Name)
                        else:
                            users.DeleteSetting(donname.SteamID, "UserName")
                            users.DeleteSetting(donname.SteamID, "INFO")
                            users.DeleteSetting(donname.SteamID, "Rank")
                            users.DeleteSetting(donname.SteamID, "MaxHomes")
                            users.DeleteSetting(donname.SteamID, "AddVIPS")
                            users.DeleteSetting(donname.SteamID, "AddDonators")
                            users.DeleteSetting(donname.SteamID, "AddMods")
                            users.DeleteSetting(donname.SteamID, "DelVIPS")
                            users.DeleteSetting(donname.SteamID, "DelDonators")
                            users.DeleteSetting(donname.SteamID, "DelMods")
                            users.DeleteSetting(donname.SteamID, "LVL1VKIT")
                            users.DeleteSetting(donname.SteamID, "LVL2VKIT")
                            users.DeleteSetting(donname.SteamID, "LVL1DKIT")
                            users.DeleteSetting(donname.SteamID, "LVL2DKIT")
                            users.DeleteSetting(donname.SteamID, "MODKIT")
                            users.DeleteSetting(donname.SteamID, "VTP")
                            users.DeleteSetting(donname.SteamID, "DTP")
                            users.DeleteSetting(donname.SteamID, "MTP")
                            users.DeleteSetting(donname.SteamID, "UseBroadcast")
                            users.DeleteSetting(donname.SteamID, "AccessInfo")
                            users.Save()
                            Player.Message(donname.Name + " is no longer a Donator")
                            donname.Message("you are no longer a Donator")
            else:
                Player.Message("You don't have permission to use this command!")
 
        elif cmd == "mdel":
            users = self.getUserIni()
            if users.GetSetting(Player.SteamID, "DelMods") == "true" or Player.Admin:
                if len(args) == 0:
                    Player.Message("Usage: /mdel [playername]")
                elif len(args) > 0:
                    modname = self.CheckV(Player, args)
                    if modname is not None:
                        if self.isVIP(modname):
                            Player.Message(modname.Name + " is a VIP, use /vdel " + modname.Name)
                        elif self.isDonator(modname):
                            Player.Message(modname.Name + " is a Donator, use /ddel " + modname.Name)
                        else:
                            users.DeleteSetting(modname.SteamID, "UserName")
                            users.DeleteSetting(modname.SteamID, "INFO")
                            users.DeleteSetting(modname.SteamID, "Rank")
                            users.DeleteSetting(modname.SteamID, "MaxHomes")
                            users.DeleteSetting(modname.SteamID, "AddVIPS")
                            users.DeleteSetting(modname.SteamID, "AddDonators")
                            users.DeleteSetting(modname.SteamID, "AddMods")
                            users.DeleteSetting(modname.SteamID, "DelVIPS")
                            users.DeleteSetting(modname.SteamID, "DelDonators")
                            users.DeleteSetting(modname.SteamID, "DelMods")
                            users.DeleteSetting(modname.SteamID, "LVL1VKIT")
                            users.DeleteSetting(modname.SteamID, "LVL2VKIT")
                            users.DeleteSetting(modname.SteamID, "LVL1DKIT")
                            users.DeleteSetting(modname.SteamID, "LVL2DKIT")
                            users.DeleteSetting(modname.SteamID, "MODKIT")
                            users.DeleteSetting(modname.SteamID, "VTP")
                            users.DeleteSetting(modname.SteamID, "DTP")
                            users.DeleteSetting(modname.SteamID, "MTP")
                            users.DeleteSetting(modname.SteamID, "UseBroadcast")
                            users.DeleteSetting(modname.SteamID, "AccessInfo")
                            users.Save()
                            Player.Message(modname.Name + " is no longer a Moderator")
                            modname.Message("You are no longer a Moderator")
            else:
                Player.Message("You don't have permission to use this command!")
 
        elif cmd == "vkit":
            if len(args) == 0:
                Player.Message("Usage: /vkit [basic / advanced]")
            elif len(args) == 1:
                if args[0] == "basic":
                    users = self.getUserIni()
                    if users.GetSetting(Player.SteamID, "LVL1VKIT") == "true" or Player.Admin:
                        if Player.Inventory.FreeSlots < 10:
                            Player.Message("You need atleast 10 free spaces!")
                        else:
                            sett = self.GetSettingsIni()
                            waittime = DataStore.Get("DonatorRank", "LVL1VKITCoolDown")
                            time = DataStore.Get("LVL1VKitCooldown", Player.SteamID)
                            try:
                                time = int(time)
                            except:
                                time = 0
                            calc = System.Environment.TickCount - time
                            if calc >= waittime or Player.Admin:
                                DataStore.Add("LVL1VKitCooldown", Player.SteamID, System.Environment.TickCount)
                                ds = DataStore.Keys("DonatorRank")
                                count = 1
                                for key in ds:
                                    if key == "VKIT1_INV" + str(count):
                                        Player.Inventory.AddItem(DataStore.Get("DonatorRank", "VKIT1_INV" + str(count)), int(DataStore.Get("DonatorRank", "VKIT1_QTY" + str(count))))
                                        count += 1
                                Player.Notice("You have redeemed kit: VIPKit Basic")
                            else:
                                workingout = round((waittime / 1000) - float(calc / 1000), 3)
                                Player.Message(str(workingout) + " seconds remaining before you can use this.")
                    else:
                        Player.Message("You don't have permission to use this command!")
                elif args[0] == "advanced":
                    users = self.getUserIni()
                    if users.GetSetting(Player.SteamID, "LVL2VKIT") == "true" or Player.Admin:
                        if Player.Inventory.FreeSlots < 10:
                            Player.Message("You need atleast 10 free spaces!")
                        else:
                            sett = self.GetSettingsIni()
                            waittime = DataStore.Get("DonatorRank", "LVL2VKITCoolDown")
                            time = DataStore.Get("LVL2VKitCooldown", Player.SteamID)
                            try:
                                time = int(time)
                            except:
                                time = 0
                            calc = System.Environment.TickCount - time
                            if calc >= waittime or Player.Admin or time == 0:
                                DataStore.Add("LVL2VKitCooldown", Player.SteamID, System.Environment.TickCount)
                                ds = DataStore.Keys("DonatorRank")
                                count = 1
                                for key in ds:
                                    if key == "VKIT2_INV" + str(count):
                                        Player.Inventory.AddItem(DataStore.Get("DonatorRank", "VKIT2_INV" + str(count)), int(DataStore.Get("DonatorRank", "VKIT2_QTY" + str(count))))
                                        count += 1
                                    else:
                                        continue
                                Player.Notice("You have redeemed kit: VIPKit Advanced")
                            else:
                                workingout = round((waittime / 1000) - float(calc / 1000), 3)
                                Player.Message(str(workingout) + " seconds remaining before you can use this.")
                    else:
                        Player.Message("You don't have permission to use this command!")
 
        elif cmd == "dkit":
            if len(args) == 0:
                Player.Message("Usage: /dkit [basic / advanced]")
            elif len(args) == 1:
                if args[0] == "basic":
                    users = self.getUserIni()
                    if users.GetSetting(Player.SteamID, "LVL1DKIT") == "true" or Player.Admin:
                        if Player.Inventory.FreeSlots < 10:
                            Player.Message("You need atleast 10 free spaces!")
                        else:
                            sett = self.GetSettingsIni()
                            waittime = DataStore.Get("DonatorRank", "LVL1DKITCoolDown")
                            time = DataStore.Get("LVL1DKitCooldown", Player.SteamID)
                            try:
                                time = int(time)
                            except:
                                time = 0
                            calc = System.Environment.TickCount - int(time)
                            if calc >= waittime or Player.Admin or time == 0:
                                DataStore.Add("LVL1DKitCooldown", Player.SteamID, System.Environment.TickCount)
                                ds = DataStore.Keys("DonatorRank")
                                count = 1
                                for key in ds:
                                    if key == "DKIT1_INV" + str(count):
                                        Player.Inventory.AddItem(DataStore.Get("DonatorRank", "DKIT1_INV" + str(count)), int(DataStore.Get("DonatorRank", "DKIT1_QTY" + str(count))))
                                        count += 1
                                    else:
                                        continue
                                Player.Notice("You have redeemed kit: DonatorKit Basic")
                            else:
                                workingout = round((waittime / 1000) - float(calc / 1000), 3)
                                Player.Message(str(workingout) + " seconds remaining before you can use this.")
                    else:
                        Player.Message("You don't have permission to use this command!")
                elif args[0] == "advanced":
                    users = self.getUserIni()
                    if users.GetSetting(Player.SteamID, "LVL2DKIT") == "true" or Player.Admin:
                        if Player.Inventory.FreeSlots < 10:
                            Player.Message("You need atleast 10 free spaces!")
                        else:
                            sett = self.GetSettingsIni()
                            waittime = DataStore.Get("DonatorRank", "LVL2DKITCoolDown")
                            time = DataStore.Get("LVL2DKitCooldown", Player.SteamID)
                            try:
                                time = int(time)
                            except:
                                time = 0
                            calc = System.Environment.TickCount - time
                            if calc >= waittime or Player.Admin or time == 0:
                                DataStore.Add("LVL2DKitCooldown", Player.SteamID, System.Environment.TickCount)
                                ds = DataStore.Keys("DonatorRank")
                                count = 1
                                for key in ds:
                                    if key == "DKIT2_INV" + str(count):
                                        Player.Inventory.AddItem(DataStore.Get("DonatorRank", "DKIT2_INV" + str(count)), int(DataStore.Get("DonatorRank", "DKIT2_QTY" + str(count))))
                                        count += 1
                                    else:
                                        continue
                                Player.Notice("You have redeemed kit: DonatorKit Advanced")
                            else:
                                workingout = round((waittime / 1000) - float(calc / 1000), 3)
                                Player.Message(str(workingout) + " seconds remaining before you can use this.")
                    else:
                        Player.Message("You don't have permission to use this command!")
 
        elif cmd == "mkit":
            users = self.getUserIni()
            if users.GetSetting(Player.SteamID, "MODKIT") == "true" or Player.Admin:
                if len(args) == 0:
                    if Player.Inventory.FreeSlots < 4:
                        Player.Message("You need atleast 4 spots free!")
                    else:
                        Player.Inventory.RemoveItem(36)
                        Player.Inventory.RemoveItem(37)
                        Player.Inventory.RemoveItem(38)
                        Player.Inventory.RemoveItem(39)
                        Player.Inventory.AddItemTo("Invisible Helmet", 36, 1)
                        Player.Inventory.AddItemTo("Invisible Vest", 37, 1)
                        Player.Inventory.AddItemTo("Invisible Pants", 38, 1)
                        Player.Inventory.AddItemTo("Invisible Boots", 39, 1)
                        Player.Inventory.AddItem("Uber Hatchet", 1)
                        Player.Inventory.AddItem("Uber Hunting Bow", 1)
                        Player.Inventory.AddItem("Arrow", 20)
                        Player.Inventory.AddItem("Small Rations", 5)
                        Player.Message("You are now invisible!")
                else:
                    Player.Message("Usage: /mkit")
            else:
                Player.Message("You don't have permission to use this command!")
 
        elif cmd == "vtp":
            users = self.getUserIni()
            if users.GetSetting(Player.SteamID, "VTP") == "true" or Player.Admin:
                if len(args) == 0:
                    ds = DataStore.Keys("DonatorRank")
                    count = 1
                    Player.Message("Usage: /vtp [Number]")
                    for key in ds:
                        if key == "VTP" + str(count):
                            Player.Message(str(count) + ") - " + DataStore.Get("DonatorRank", key))
                            count += 1
                elif len(args) == 1:
                    waittime = DataStore.Get("DonatorRank", "VTPCoolDown")
                    time = DataStore.Get("VTPCooldown", Player.SteamID)
                    try:
                        time = int(time)
                    except:
                        time = 0
                    calc = System.Environment.TickCount - time
                    if DataStore.Get("DonatorRank", "VTP" + args[0]) is not None:
                        if calc >= waittime or Player.Admin:
                            delay = DataStore.Get("DonatorRank", "VTPDELAY")
                            locname = DataStore.Get("DonatorRank", "VTP" + args[0])
                            Data = Plugin.CreateDict()
                            Data["Player"] = Player
                            Data["LocationName"] = locname
                            Data["Location"] = DataStore.Get("DonatorRank", locname).split(",")
                            Data["Health"] = Player.Health
                            Data["Type"] = "VTPCooldown"
                            Plugin.CreateParallelTimer("TeleportDelay", int(delay), Data).Start()
                            Player.Message("Teleporting in " + str(delay / 1000) + " seconds.")
                        else:
                            workingout = round((waittime / 1000) - float(calc / 1000), 3)
                            Player.Message(str(workingout) + " seconds remaining before you can use this.")
                    else:
                        Player.Message("Usage: /vtp [Number]")
                else:
                    Player.Message("Usage: /vtp [Number]")
            else:
                Player.Message("You don't have permission to use this command!")
 
        elif cmd == "dtp":
            users = self.getUserIni()
            if users.GetSetting(Player.SteamID, "DTP") == "true" or Player.Admin:
                if len(args) == 0:
                    ds = DataStore.Keys("DonatorRank")
                    count = 1
                    Player.Message("Usage: /dtp [Number]")
                    for key in ds:
                        if key == "DTP" + str(count):
                            Player.Message(str(count) + ") - " + DataStore.Get("DonatorRank", key))
                            count += 1
                elif len(args) == 1:
                    waittime = DataStore.Get("DonatorRank", "DTPCoolDown")
                    time = DataStore.Get("DTPCooldown", Player.SteamID)
                    time = int(time)
                    try:
                        time = int(time)
                    except:
                        time = 0
                    calc = System.Environment.TickCount - time
                    if DataStore.Get("DonatorRank", "DTP" + args[0]) is not None:
                        if calc >= waittime or Player.Admin:
                            delay = DataStore.Get("DonatorRank", "DTPDELAY")
                            locname = DataStore.Get("DonatorRank", "DTP" + args[0])
                            Data = Plugin.CreateDict()
                            Data["Player"] = Player
                            Data["LocationName"] = locname
                            Data["Location"] = DataStore.Get("DonatorRank", locname).split(",")
                            Data["Health"] = Player.Health
                            Data["Type"] = "DTPCooldown"
                            Plugin.CreateParallelTimer("TeleportDelay", int(delay), Data).Start()
                            Player.Message("Teleporting to " + locname + " in " + str(delay / 1000) + " seconds.")
                        else:
                            workingout = round((waittime / 1000) - float(calc / 1000), 3)
                            Player.Message(str(workingout) + " seconds remaining before you can use this.")
                    else:
                        Player.Message("Usage: /dtp [Number]")
                else:
                    Player.Message("Usage: /dtp [Number]")
            else:
                Player.Message("You don't have permission to use this command!")
 
        elif cmd == "mtp":
            users = self.getUserIni()
            if users.GetSetting(Player.SteamID, "MTP") == "true" or Player.Admin: 
                if len(args) > 0:
                    targetname = self.CheckV(Player, args)
                    if targetname is not None:
                        plocation = Player.Location
                        DataStore.Add("MODLOCATION", Player.SteamID, plocation)
                        targetname.Notice(Player.Name + " has teleported to you!")
                        Player.TeleportTo(targetname)
                        Player.Message("Teleported to: " + targetname.Name)
                        Player.Message("To teleport back to where you were, Type /mtpback")
                        Player.TeleportTo(targetname)
                        if DataStore.Get("DonatorRank", "LogTPS") == "true":
                            ini = self.getLogIni()
                            date = Plugin.GetDate()
                            tym = Plugin.GetTime()
                            ini.AddSetting("TPLog", date + "| " + tym + " || " + Player.Name + " Teleported to: " + targetname.Name, targetname.SteamID)
                            ini.Save()
                        else:
                            return
                    else:
                        return
                else:
                    Player.Message("Usage: /mtp [Player Name]")
            else:
                Player.Message("You don't have permission to use this command!")
 
        elif cmd == "mtpback":
            users = self.getUserIni()
            if users.GetSetting(Player.SteamID, "MTP") == "true" or Player.Admin:
                if DataStore.Get("MODLOCATION", Player.SteamID):
                    plocation = DataStore.Get("MODLOCATION", Player.SteamID)
                    Player.TeleportTo(plocation)
                    Player.Message("You have been teleported back")
                    DataStore.Remove("MODLOCATION", Player.SteamID)
                else:
                    Player.Message("You have no last locations")
            else:
                Player.Message("You don't have permission to use this command!")
 
        elif cmd == "info":
            users = self.getUserIni()
            if users.GetSetting(Player.SteamID, "AccessInfo") == "true" or Player.Admin:
                if len(args) > 0:
                    target = self.CheckV(Player, args)
                    if target is not None:
                        Player.Message("Info about [color cyan]" + target.Name)
                        Player.Message("IP: [color cyan]" + target.IP)
                        Player.Message("SteamID: [color cyan]" + target.SteamID)
                        Player.Message("Ping: [color cyan]" + str(target.Ping))
                        Player.Message("Health: [color cyan]" + str(target.Health))
                        Player.Message("Time Online: [color cyan]" + str(target.TimeOnline)[:-3] + "[color white] seconds")
                        if target.AtHome:
                            Player.Message("Is at home: [color cyan]True")
                        else:
                            Player.Message("Is at home: [color cyan]False")
                    else:
                        return
                else:
                    Player.Message("usage: /info [name]")
            else:
                Player.Message("You don't have permission to use this command!")

    def TeleportDelayCallback(self, timer):
        timer.Kill()
        Data = timer.Args
        Player = Data["Player"]
        if Data["Health"] <= Player.Health:
            locname = Data["LocationName"]
            loc = Data["Location"]
            Player.TeleportTo(float(loc[0]), float(loc[1]), float(loc[2]))
            Player.InventoryNotice(locname)
            DataStore.Add(Data["Type"], Player.SteamID, System.Environment.TickCount)
        else:
            Player.Message("You have been hurt, Canceled teleport!")
            

    def On_PlayerConnected(self, Player):
        try:
            ini = self.getUserIni()
            if ini.GetSetting(Player.SteamID, "MaxHomes") is not None:
                DataStore.Add("MaxHomes", Player.SteamID, int(ini.GetSetting(Player.SteamID, "MaxHomes")))
            if DataStore.Get("DonatorRank", "JoinMMSG") == "true":
                if Player.SteamID == DataStore.Get("DonatorRank", "OwnerID"):
                    Server.BroadcastFrom("Owner", Player.Name + " is now Online.")
                elif Player.Admin:
                    Server.BroadcastFrom("Admin", Player.Name + " is now Online.")
                elif self.isMod(Player):
                    Server.BroadcastFrom("Moderator", Player.Name + " is now Online.")
                elif self.isDonator(Player):
                    Server.BroadcastFrom("Donator", Player.Name + " is now Online.")
                elif self.isVIP(Player):
                    Server.BroadcastFrom("VIP", Player.Name + " is now Online.")
                else:
                    Server.Broadcast(Player.Name + " is now Online!")
        except:
            pass
 
    def On_PlayerDisconnected(self, Player):
        try:
            DataStore.Remove("MaxHomes", Player.SteamID)
            DataStore.Remove("MODLOCATION", Player.SteamID)
            if DataStore.Get("DonatorRank", "LeaveMSG") == "true":
                if Player.SteamID == DataStore.Get("DonatorRank", "OwnerID"):
                    Server.BroadcastFrom("Owner", Player.Name + " is now Offline.")
                elif Player.Admin:
                    Server.BroadcastFrom("Admin", Player.Name + " is now Offline.")
                elif self.isMod(Player):
                    Server.BroadcastFrom("Moderator", Player.Name + " is now Offline.")
                elif self.isDonator(Player):
                    Server.BroadcastFrom("Donator", Player.Name + " is now Offline.")
                elif self.isVIP(Player):
                    Server.BroadcastFrom("VIP", Player.Name + " is now Offline.")
                else:
                    Server.Broadcast(Player.Name + " is now Offline!")
        except:
            pass
 
    def On_Chat(self, Player, ChatMessage):
        try:
            if DataStore.Get("DonatorRank", "ChatPrefix") == "true":
                if DataStore.Get("DonatorRank", "OwnerID") == str(Player.SteamID):
                    chatmsg = str(ChatMessage)[1:-1]
                    ocolour = DataStore.Get("DonatorRank", "OwnerColour")
                    Server.BroadcastFrom("[Owner]♚" + Player.Name, ocolour + chatmsg)
                    ChatMessage.NewText = "*%"
                    #Having these to replace the chat message seems to stop errors in the console
                    return
                elif Player.Admin:
                    chatmsg = str(ChatMessage)[1:-1]
                    acolour = DataStore.Get("DonatorRank", "AdminColour")
                    Server.BroadcastFrom("[Admin]♚" + Player.Name, acolour + chatmsg)
                    ChatMessage.NewText = "*%"
                elif self.isMod(Player):
                    chatmsg = str(ChatMessage)[1:-1]
                    mcolour = DataStore.Get("DonatorRank", "ModColour")
                    Server.BroadcastFrom("[Mod]♚" + Player.Name, mcolour + chatmsg)
                    ChatMessage.NewText = "*%"
                elif self.isDonator(Player):
                    chatmsg = str(ChatMessage)[1:-1]
                    dcolour = DataStore.Get("DonatorRank", "DonatorColour")
                    Server.BroadcastFrom("[Donator]☠" + Player.Name, dcolour + chatmsg)
                    ChatMessage.NewText = "*%"
                elif self.isVIP(Player):
                    chatmsg = str(ChatMessage)[1:-1]
                    vcolour = DataStore.Get("DonatorRank", "VIPColour")
                    Server.BroadcastFrom("[VIP]☠" + Player.Name, vcolour + chatmsg)
                    ChatMessage.NewText = "*%"
        except:
            pass

    def isMod(self, Player):
        try:
            ini = self.getUserIni()
            if ini.GetSetting(Player.SteamID, "Rank") == "Mod":
                return True
            elif DataStore.ContainsKey("Moderators", Player.SteamID) or Player.Moderator:
                if ini.GetSetting(Player.SteamID, "Rank") == "Mod":
                    return True
                d = Plugin.GetDate()
                t = Plugin.GetTime()
                ini.AddSetting(modname.SteamID, "UserName", modname.Name)
                ini.AddSetting(modname.SteamID, "INFO", "Time: " + t + "||Date: " + d + "||By: DonatorRank-AutoAdd")
                ini.AddSetting(modname.SteamID, "Rank", "Mod")
                ini.AddSetting(modname.SteamID, "MaxHomes", DataStore.Get("DonatorRank", "ModHomesMax"))
                ini.AddSetting(modname.SteamID, "AddVIPS", "true")
                ini.AddSetting(modname.SteamID, "AddDonators", "true")
                ini.AddSetting(modname.SteamID, "AddMods", "false")
                ini.AddSetting(modname.SteamID, "DelVIPS", "true")
                ini.AddSetting(modname.SteamID, "DelDonators", "true")
                ini.AddSetting(modname.SteamID, "DelMods", "false")
                ini.AddSetting(modname.SteamID, "LVL1VKIT", "false")
                ini.AddSetting(modname.SteamID, "LVL2VKIT", "false")
                ini.AddSetting(modname.SteamID, "LVL1DKIT", "false")
                ini.AddSetting(modname.SteamID, "LVL2DKIT", "false")
                ini.AddSetting(modname.SteamID, "MODKIT", "true")
                ini.AddSetting(modname.SteamID, "VTP", "false")
                ini.AddSetting(modname.SteamID, "DTP", "false")
                ini.AddSetting(modname.SteamID, "MTP", "true")
                ini.AddSetting(modname.SteamID, "UseBroadcast", "true")
                ini.AddSetting(modname.SteamID, "AccessInfo", "true")
                ini.Save()
                return True
            else:
                return False
        except:
            pass
 
    def isDonator(self, Player):
        try:
            ini = self.getUserIni()
            if ini.GetSetting(Player.SteamID, "Rank") == "Donator":
                return True
            else:
                return None
        except:
            pass
 
    def isVIP(self, Player):
        try:
            ini = self.getUserIni()
            if ini.GetSetting(Player.SteamID, "Rank") == "VIP":
                return True
            else:
                return None
        except:
            pass
 
    def GetSettingsIni(self):
        if not Plugin.IniExists("Settings"):
            ini = Plugin.CreateIni("Settings")
            ini.Save()
        return Plugin.GetIni("Settings")
 
    def getUserIni(self):
        if not Plugin.IniExists("Users"):
            ini = Plugin.CreateIni("Users")
            ini.Save()
        return Plugin.GetIni("Users")
 
    def getLogIni(self):
        if not Plugin.IniExists("Logs"):
            ini = Plugin.CreateIni("Logs")
            ini.Save()
        return Plugin.GetIni("Logs")
 
    def argsToText(self, args):
        text = str.join(" ", args)
        return text
 
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
            Player.Message("Couldn't find " + str.join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.Message("Found " + str(count) + " players with similar a name. Use a more correct name!")
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

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None
