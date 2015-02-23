__title__ = 'AdminPlus'
__author__ = 'Jakkee'
__version__ = '1.8'

import clr
clr.AddReferenceByPartialName("UnityEngine")
clr.AddReferenceByPartialName("Fougerite")
import UnityEngine
import Fougerite


class AdminPlus:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "DestroyEnabled", "true")
            ini.AddSetting("Config", "DestroyWeapon", "9mm Pistol")
            ini.AddSetting("Config", "TPDistance", "30")
            ini.AddSetting("Config", "ModeratorsCanUse", "true")
            ini.AddSetting("Commands", "Player must run duty first?", "true")
            ini.AddSetting("Commands", "InvisibleSuit", "true")
            ini.AddSetting("Commands", "WoodKit", "true")
            ini.AddSetting("Commands", "MetalKit", "true")
            ini.AddSetting("Commands", "UberKit", "true")
            ini.AddSetting("Commands", "KevlarKit", "true")
            ini.AddSetting("Commands", "AccessDoors", "true")
            ini.AddSetting("Commands", "ClearInventory", "true")
            ini.AddSetting("Commands", "TpAdmin", "true")
            ini.AddSetting("Players", "76561198135558142", "Jakkee")
            ini.Save()
        DataStore.Flush("AdminPlus")
        ini = Plugin.GetIni("Settings")
        DataStore.Add("AdminPlus", "DestroyEnabled", ini.GetSetting("Config", "DestroyEnabled"))
        DataStore.Add("AdminPlus", "Distance", ini.GetSetting("Config", "TPDistance"))
        DataStore.Add("AdminPlus", "DestroyWeapon", ini.GetSetting("Config", "DestroyWeapon"))
        DataStore.Add("AdminPlus", "ModeratorsCanUse", ini.GetSetting("Config", "ModeratorsCanUse"))
        DataStore.Add("AdminPlus", "DutyFirst", ini.GetSetting("Commands", "Player must run duty first?"))
        DataStore.Add("AdminPlus", "InvisibleSuit", ini.GetSetting("Commands", "InvisibleSuit"))
        DataStore.Add("AdminPlus", "MetalKit", ini.GetSetting("Commands", "MetalKit"))
        DataStore.Add("AdminPlus", "TpAdmin", ini.GetSetting("Commands", "TpAdmin"))
        DataStore.Add("AdminPlus", "WoodKit", ini.GetSetting("Commands", "WoodKit"))
        DataStore.Add("AdminPlus", "UberKit", ini.GetSetting("Commands", "UberKit"))
        DataStore.Add("AdminPlus", "KevlarKit", ini.GetSetting("Commands", "KevlarKit"))
        DataStore.Add("AdminPlus", "AccessDoors", ini.GetSetting("Commands", "AccessDoors"))
        DataStore.Add("AdminPlus", "ClearInventory", ini.GetSetting("Commands", "ClearInventory"))

    def On_DoorUse(self, Player, DoorUseEvent):
        if self.toggled(Player):
            if DataStore.Get("AdminPlus", "AccessDoors") == "true":
                DoorUseEvent.Open = True

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            if DataStore.Get("AdminPlus", "ModeratorsCanUse"):
                return True
            else:
                return False
        else:
            return False

    def On_Command(self, Player, cmd, args):
        if cmd == "admin":
            if Player.Admin or self.isMod(Player.SteamID):
                if len(args) == 0:
                    Player.MessageFrom("AdminPlus", "Commands;")
                    Player.MessageFrom("AdminPlus", "/tpadmin [name] (Teleports you 30units away from the target)")
                    Player.MessageFrom("AdminPlus", "/tpback (Teleports you back to where you were)")
                    Player.MessageFrom("AdminPlus", "/duty [on / off] (Tells the server if your on duty or not)")
                    Player.MessageFrom("AdminPlus", "/admin [on / off] (Invisible suit)")
                    Player.MessageFrom("AdminPlus", "/admin metal (Spawns metal building parts)")
                    Player.MessageFrom("AdminPlus", "/admin wood (Spawns wood building parts)")
                    Player.MessageFrom("AdminPlus", "/admin uber (Spawns uber items)")
                    Player.MessageFrom("AdminPlus", "/admin kevlar (Spawns kevlar)")
                    Player.MessageFrom("AdminPlus", "/admin clear (Clears your inventory)")
                    Player.MessageFrom("AdminPlus", "/admin doors (Toggles you to open all doors)")
                elif len(args) == 1:
                    if args[0] == "on":
                        if DataStore.Get("AdminPlus", "InvisibleSuit") == "true":
                            if self.dutyfirst(Player):
                                Player.Inventory.RemoveItem(36)
                                Player.Inventory.RemoveItem(37)
                                Player.Inventory.RemoveItem(38)
                                Player.Inventory.RemoveItem(39)
                                Player.Inventory.AddItemTo("Invisible Helmet", 36, 1)
                                Player.Inventory.AddItemTo("Invisible Vest", 37, 1)
                                Player.Inventory.AddItemTo("Invisible Pants", 38, 1)
                                Player.Inventory.AddItemTo("Invisible Boots", 39, 1)
                                Player.MessageFrom("AdminPlus", "You're now Invisible!")
                            else:
                                Player.MessageFrom("AdminPlus", "You are not on duty!")
                        else:
                            Player.MessageFrom("AdminPlus", "This command has been disabled!")
                    elif args[0] == "off":
                        if DataStore.Get("AdminPlus", "InvisibleSuit") == "true":
                            if self.dutyfirst(Player):
                                Player.Inventory.RemoveItem(36)
                                Player.Inventory.RemoveItem(37)
                                Player.Inventory.RemoveItem(38)
                                Player.Inventory.RemoveItem(39)
                                Player.MessageFrom("AdminPlus", "You're now visible!")
                            else:
                                Player.MessageFrom("AdminPlus", "You are not on duty!")
                        else:
                            Player.MessageFrom("AdminPlus", "This command has been disabled!")
                    elif args[0] == "wood":
                        if DataStore.Get("AdminPlus", "WoodKit") == "true":
                            if self.dutyfirst(Player):
                                Player.Inventory.AddItem("Wood Pillar", 250)
                                Player.Inventory.AddItem("Wood Foundation", 250)
                                Player.Inventory.AddItem("Wood Wall", 250)
                                Player.Inventory.AddItem("Wood Doorway", 250)
                                Player.Inventory.AddItem("Wood Window", 250)
                                Player.Inventory.AddItem("Wood Stairs", 250)
                                Player.Inventory.AddItem("Wood Ramp", 250)
                                Player.Inventory.AddItem("Wood Ceiling", 250)
                                Player.Inventory.AddItem("Metal Door", 15)
                                Player.Inventory.AddItem("Metal Window Bars", 15)
                                Player.MessageFrom("AdminPlus", "Wood building parts spawned!")
                            else:
                                Player.MessageFrom("AdminPlus", "You are not on duty!")
                        else:
                            Player.MessageFrom("AdminPlus", "This command has been disabled!")
                    elif args[0] == "metal":
                        if DataStore.Get("AdminPlus", "MetalKit") == "true":
                            if self.dutyfirst(Player):
                                Player.Inventory.AddItem("Metal Pillar", 250)
                                Player.Inventory.AddItem("Metal Foundation", 250)
                                Player.Inventory.AddItem("Metal Wall", 250)
                                Player.Inventory.AddItem("Metal Doorway", 250)
                                Player.Inventory.AddItem("Metal Window", 250)
                                Player.Inventory.AddItem("Metal Stairs", 250)
                                Player.Inventory.AddItem("Metal Ramp", 250)
                                Player.Inventory.AddItem("Metal Ceiling", 250)
                                Player.Inventory.AddItem("Metal Door", 15)
                                Player.Inventory.AddItem("Metal Window Bars", 15)
                                Player.MessageFrom("AdminPlus", "Metal building parts spawned!")
                            else:
                                Player.MessageFrom("AdminPlus", "You are not on duty!")
                        else:
                            Player.MessageFrom("AdminPlus", "This command has been disabled!")
                    elif args[0] == "uber":
                        if DataStore.Get("AdminPlus", "UberKit") == "true":
                            if self.dutyfirst(Player):
                                Player.Inventory.AddItem("Uber Hatchet", 1)
                                Player.Inventory.AddItem("Uber Hunting Bow", 1)
                                Player.Inventory.AddItem("Arrow", 40)
                                Player.MessageFrom("AdminPlus", "Uber items spawned!")
                            else:
                                Player.MessageFrom("AdminPlus", "You are not on duty!")
                        else:
                            Player.MessageFrom("AdminPlus", "This command has been disabled!")
                    elif args[0] == "kevlar":
                        if DataStore.Get("AdminPlus", "KevlarKit") == "true":
                            if self.dutyfirst(Player):
                                Player.Inventory.RemoveItem(36)
                                Player.Inventory.RemoveItem(37)
                                Player.Inventory.RemoveItem(38)
                                Player.Inventory.RemoveItem(39)
                                Player.Inventory.AddItemTo("Kevlar Helmet", 36, 1)
                                Player.Inventory.AddItemTo("Kevlar Vest", 37, 1)
                                Player.Inventory.AddItemTo("Kevlar Pants", 38, 1)
                                Player.Inventory.AddItemTo("Kevlar Boots", 39, 1)
                                Player.MessageFrom("AdminPlus", "I hope you have a legitimate reason why need this!")
                            else:
                                Player.MessageFrom("AdminPlus", "You are not on duty!")
                        else:
                            Player.MessageFrom("AdminPlus", "This command has been disabled!")
                    elif args[0] == "clear":
                        if DataStore.Get("AdminPlus", "ClearInventory") == "true":
                            if self.dutyfirst(Player):
                                Player.Inventory.ClearAll()
                                Player.MessageFrom("AdminPlus", "Inventory cleared!")
                            else:
                                Player.MessageFrom("AdminPlus", "You are not on duty!")
                        else:
                            Player.MessageFrom("AdminPlus", "This command has been disabled!")
                    elif args[0] == "doors":
                        if DataStore.Get("AdminPlus", "AccessDoors") == "true":
                            if self.dutyfirst(Player):
                                self.toggle(Player)
                            else:
                                Player.MessageFrom("AdminPlus", "You are not on duty!")
                        else:
                            Player.MessageFrom("AdminPlus", "This command has been disabled!")
                    else:
                        Player.MessageFrom("AdminPlus", "Unknown command")
                else:
                    Player.MessageFrom("AdminPlus", "usage: /admin")
            else:
                Player.MessageFrom("AdminPlus", "You're not allowed to use this command!")
        elif cmd == "duty":
            if Player.Admin or self.isMod(Player.SteamID):
                if len(args) == 0:
                    Player.MessageFrom("AdminPlus", "Usage: /duty [on/off]")
                elif len(args) == 1:
                    if args[0] == "on":
                        DataStore.Add("OnDuty", Player.SteamID, "on")
                        Server.Broadcast(Player.Name + " is now on duty! Let him/her know if you need anything!")
                    elif args[0] == "off":
                        DataStore.Remove("OnDuty", Player.SteamID)
                        Server.Broadcast(Player.Name + " is now off duty! Please direct questions to another admin!")
                    else:
                        Player.MessageFrom("AdminPlus", "Unknown Command")
                else:
                    Player.MessageFrom("AdminPlus", "Usage: /duty [on/off]")
            else:
                Player.MessageFrom("AdminPlus", "You are not allowed to use that command!")
        elif cmd == "tpadmin":
            if Player.Admin or self.isMod(Player.SteamID):
                if DataStore.Get("AdminPlus", "TpAdmin") == "true":
                    if self.dutyfirst(Player):
                        if len(args) == 0:
                            Player.MessageFrom("AdminPlus", "Usage: /tpadmin [Player Name]")
                        elif len(args) > 0:
                            targetname = self.CheckV(Player, args)
                            if targetname is None:
                                return
                            DataStore.Add("SavedLocation", Player.SteamID, Player.Location)
                            distance = DataStore.Get("AdminPlus", "Distance")
                            Player.TeleportTo(targetname, int(distance))
                            Player.MessageFrom("AdminPlus", "Teleported: " + distance + "m Behind: " + targetname.Name)
                            Player.MessageFrom("AdminPlus", "Use /tpback to go back to your last location")
                        else:
                            Player.MessageFrom("AdminPlus", "Unknown Command")
                    else:
                        Player.MessageFrom("AdminPlus", "You are not on duty!")
                else:
                    Player.MessageFrom("AdminPlus", "This command has been disabled!")
            else:
                Player.MessageFrom("AdminPlus", "You are not allowed to use that command!")
        elif cmd == "tpback":
            if Player.Admin or self.isMod(Player.SteamID):
                if self.dutyfirst(Player):
                    if len(args) == 0:
                        if DataStore.Get("SavedLocation", Player.SteamID):
                            BLocation = DataStore.Get("SavedLocation", Player.SteamID)
                            Player.TeleportTo(BLocation)
                            DataStore.Remove("SavedLocation", Player.SteamID)
                            Player.MessageFrom("AdminPlus", "Teleported back!")
                        else:
                            Player.MessageFrom("AdminPlus", "You have no last known locations")
                    elif len(args) > 0:
                        Player.MessageFrom("AdminPlus", "Usage: /tpback")
                else:
                    Player.MessageFrom("AdminPlus", "You are not on duty!")
            else:
                Player.MessageFrom("AdminPlus", "You are not allowed to use that command!")

    def On_PlayerDisconnected(self, Player):
        try:
            DataStore.Remove("SavedLocation", Player.SteamID)
            if DataStore.Get("OnDuty", Player.SteamID) == "on":
                DataStore.Remove("OnDuty", Player.SteamID)
                Server.Broadcast(Player.Name + " is now off duty! Please direct questions to another admin!")
        except:
            pass

    def On_EntityHurt(self, HurtEvent):
        try:
            if HurtEvent.Attacker.Admin:
                if DataStore.Get("AdminPlus", "DestroyEnabled") == "true":
                    if HurtEvent.WeaponName == DataStore.Get("AdminPlus", "DestroyWeapon"):
                        if HurtEvent.Entity.Name is not None:
                            HurtEvent.Entity.Destroy()
        except:
            pass

    def dutyfirst(self, Player):
        try:
            if DataStore.Get("AdminPlus", "DutyFirst"):
                return True
            elif DataStore.Get("OnDuty", Player.SteamID) == "on":
                return True
            else:
                return False
        except:
            pass

    def toggle(self, Player):
        ini = Plugin.GetIni("Settings")
        if ini.GetSetting("Players", Player.SteamID) is None:
            ini.AddSetting("Players", Player.SteamID, Player.Name)
            ini.Save()
            Player.MessageFrom("AdminPlus", "You have been added to the config!")
            Player.MessageFrom("AdminPlus", "You can now open any door")
        else:
            ini.DeleteSetting("Players", Player.SteamID)
            ini.Save()
            Player.MessageFrom("AdminPlus", "You have been removed from the config!")
            Player.MessageFrom("AdminPlus", "You can now only open your own doors")

    def toggled(self, Player):
        ini = Plugin.GetIni("Settings")
        if ini.GetSetting("Players", Player.SteamID) is not None:
            return True
        else:
            return False

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def GetPlayerName(self, name):
        try:
            name = name.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

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
