using Fougerite;
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading;

namespace Permissions
{
    internal class Permissions : Fougerite.Module
    {
        private API api;
        internal IniParser permissionsData;
        internal Dictionary<string, List<string>> GroupData;
        internal Dictionary<string, string> PlayerGroup;
        internal string DefaultGroup = "User";

        #region Init

        public override string Name
        {
            get
            {
                return "Permissions";
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
                return "Permission system for Fougerite";
            }
        }

        public override Version Version
        {
            get
            {
                return new Version("1.0");
            }
        }

        public override void DeInitialize()
        {
            Hooks.OnCommand -= OnCommand;
        }

        public override void Initialize()
        {
            LoadPermissions();
            Hooks.OnCommand += OnCommand;
        }

        private void LoadPermissions()
        {
            if (!File.Exists(Path.Combine(ModuleFolder, "PermissionsData.ini")))
            {
                UnityEngine.Debug.Log("[Permissions] Creating new PermissionsData file...");
                File.Create(Path.Combine(ModuleFolder, "PermissionsData.ini")).Dispose();
                permissionsData = new IniParser(Path.Combine(ModuleFolder, "Settings.ini"));
                permissionsData.AddSetting("Groups", "Admin", "server.*, permission.*");
                permissionsData.AddSetting("Groups", "Moderator", "server.kick, server.mute, server.unmute, server.chat, server.build");
                permissionsData.AddSetting("Groups", "User", "server.chat, server.build");
                permissionsData.AddSetting("PlayerGroups", "50FA20E2708B2B2D97A0F092025EBCF3C1AF957D71154425431C00DC99F9A484", "Admin");
                permissionsData.Save();
            }
            permissionsData = new IniParser(Path.Combine(ModuleFolder, "PermissionsData.ini"));

            foreach (string group in permissionsData.EnumSection("Groups"))
            {
                List<string> _groupdata = new List<string>();
                foreach (string perm in permissionsData.GetSetting("Groups", group).ToLower().RemoveWhiteSpaces().Split(','))
                {
                    _groupdata.Add(perm);
                }
                if (!GroupData.ContainsKey(group))
                {
                    GroupData.Add(group, _groupdata);
                }
            }

            foreach (string hwid in permissionsData.EnumSection("PlayerGroups"))
            {
                PlayerGroup.Add(hwid, permissionsData.GetSetting("PlayerGroups", hwid));
            }
            UnityEngine.Debug.Log("[Permissions] Permissions loaded");
        }

        #endregion

        #region Core
        
        private void OnCommand(Fougerite.Player Player, string cmd, string[] args)
        {
            if (cmd == "grant")
            {
                //      /grant <group> <perm>
                //      /grant <user> <group>
                //      /create <group> <inherit group>
                //      /create <group>
                //      /delete <group>
                //      /reloadpermissions
                if (Player.Admin || api.HasPerm("", "permission.*") || api.HasPerm("", "permission.grant"))
                {
                    if (args.Length == 2)
                    {
                        string group = null;
                        bool Group_Perm = false;
                        if (GroupData.ContainsKey(args[0].ToLower().RemoveWhiteSpaces()))
                        {
                            group = args[0].ToLower().RemoveWhiteSpaces();
                            Group_Perm = true;
                        }
                        else if (GroupData.ContainsKey(args[1].ToLower().RemoveWhiteSpaces()))
                        {
                            group = args[1].ToLower().RemoveWhiteSpaces();
                        }
                        else
                        {
                            Player.MessageFrom("Permissions", "Can not find group!");
                            return;
                        }
                        if (Group_Perm)
                        {
                            string perm = args[1].ToLower().RemoveWhiteSpaces();
                            if (GiveGroupPerm(group, perm))
                            {
                                Player.MessageFrom("Permissions", "Added permission: " + perm + " to group: " + group);
                            }
                            else
                            {
                                Player.MessageFrom("Permissions", "Unable to add permission: " + perm + " to group: " + group);
                            }
                        }
                        else
                        {
                            // Look for player (HWID)
                            // add group to user
                        }
                    }
                }
                else
                {
                    Player.MessageFrom("Permissions", "You do not have permission to use this command!");
                }
            }
        }

        private bool GiveGroupPerm(string Group, string Permission)
        {
            if (GroupData.ContainsKey(Group))
            {
                if (GroupData[Group].Contains(Permission))
                {
                    UnityEngine.Debug.Log("[Permissions] " + Group + " already has permission: " + Permission);
                    return false;
                }
                else
                {
                    bool threaderror = false;
                    Thread thread = new Thread(() =>
                    {
                        try
                        {
                            GroupData[Group].Add(Permission);
                            permissionsData.DeleteSetting("Groups", Group);
                            permissionsData.AddSetting("Groups", Group, string.Join(", ", GroupData[Group].ToArray()));
                            permissionsData.Save();
                        }
                        catch
                        {
                            threaderror = true;
                        }
                    })
                    {
                        IsBackground = true
                    };
                    thread.Start();
                    if (threaderror)
                    {
                        UnityEngine.Debug.LogError("[Permissions] Unable to add permission: " + Permission + " to: " + Group);
                        return false;
                    }
                    else
                    {
                        UnityEngine.Debug.Log("[Permissions] Gave " + Group + " group permission: " + Permission);
                        return true;
                    }
                }
            }
            else
            {
                UnityEngine.Debug.Log("[Permissions] Can not find group: " + Group);
                return false;
            }
        }

        private bool DeleteGroupPerm(string Group, string Permission)
        {
            if (GroupData.ContainsKey(Group))
            {
                if (GroupData[Group].Contains(Permission))
                {
                    bool threaderror = false;
                    Thread thread = new Thread(() =>
                    {
                        try
                        {
                            GroupData[Group].Remove(Permission);
                            permissionsData.DeleteSetting("Groups", Group);
                            permissionsData.AddSetting("Groups", Group, string.Join(", ", GroupData[Group].ToArray()));
                            permissionsData.Save();
                        }
                        catch
                        {
                            threaderror = true;
                        }
                    })
                    {
                        IsBackground = true
                    };
                    thread.Start();
                    if (threaderror)
                    {
                        UnityEngine.Debug.LogError("[Permissions] Unable to remove permission: " + Permission + " from: " + Group);
                        return false;
                    }
                    else
                    {
                        UnityEngine.Debug.Log("[Permissions] " + Permission + " has been removed from: " + Group);
                        return true;
                    }
                }
                else
                {
                    UnityEngine.Debug.Log("[Permissions] " + Group + " does not contain permission: " + Permission);
                    return false;
                }
            }
            else
            {
                UnityEngine.Debug.Log("[Permissions] Can not find group: " + Group);
                return false;
            }
        }

        private bool CreateGroup(string Group)
        {
            if (GroupData.ContainsKey(Group))
            {
                UnityEngine.Debug.Log("[Permissions] " + Group + " already exists");
                return false;
            }
            else
            {
                bool threaderror = false;
                Thread thread = new Thread(() =>
                {
                    try
                    {
                        List<string> list = new List<string>();
                        GroupData.Add(Group, list);
                        permissionsData.AddSetting("Groups", Group);
                        permissionsData.Save();
                    }
                    catch
                    {
                        threaderror = true;
                    }
                })
                {
                    IsBackground = true
                };
                thread.Start();
                if (threaderror)
                {
                    UnityEngine.Debug.LogError("[Permissions] Error creating group: " + Group);
                    return false;
                }
                else
                {
                    UnityEngine.Debug.Log("[Permissions] " + Group + " has been created and contains no permissions, Add some.");
                    return true;
                }
            }
        }

        private bool CreateGroup(string Group, string Inherit)
        {
            if (GroupData.ContainsKey(Group))
            {
                UnityEngine.Debug.Log("[Permissions] " + Group + " already exists");
                return false;
            }
            else if (!GroupData.ContainsKey(Inherit))
            {
                UnityEngine.Debug.Log("[Permissions] " + Inherit + " does not exist, Inherit from another group!");
                return false;
            }
            else
            {
                bool threaderror = false;
                Thread thread = new Thread(() =>
                {
                    try
                    {
                        List<string> list = new List<string>(GroupData[Inherit]);
                        GroupData.Add(Group, list);
                        permissionsData.AddSetting("Groups", Group, string.Join(", ", list.ToArray()));
                        permissionsData.Save();
                    }
                    catch
                    {
                        threaderror = true;
                    }
                })
                {
                    IsBackground = true
                };
                thread.Start();
                if (threaderror)
                {
                    UnityEngine.Debug.LogError("[Permissions] Unable to create group: " + Group + " using permissions from group: " + Inherit);
                    return false;
                }
                else
                {
                    UnityEngine.Debug.Log("[Permissions] " + Group + " has been created and uses permissions from: " + Inherit);
                    return true;
                }
            }
        }

        private bool DeleteGroup(string Group)
        {
            if (Group != DefaultGroup)
            {
                if (GroupData.ContainsKey(Group))
                {
                    bool threaderror = false;
                    Thread thread = new Thread (() =>
                    {
                        try
                        {
                            GroupData.Remove(Group);
                            permissionsData.DeleteSetting("Groups", Group);
                            foreach (string user in PlayerGroup.Keys)
                            {
                                if (PlayerGroup.ContainsKey(user))
                                {
                                    if (PlayerGroup[user] == Group)
                                    {
                                        permissionsData.DeleteSetting("PlayerGroups", user);
                                        permissionsData.AddSetting("PlayerGroups", user, DefaultGroup);
                                        PlayerGroup[user] = DefaultGroup;
                                    }
                                }
                            }
                            permissionsData.Save();
                        }
                        catch
                        {
                            threaderror = true;
                        }
                    })
                    {
                        IsBackground = true
                    };
                    thread.Start();
                    if (threaderror)
                    {
                        UnityEngine.Debug.LogError("[Permissions] Error deleting group: " + Group);
                        return false;
                    }
                    else
                    {
                        UnityEngine.Debug.Log("[Permissions] " + Group + " has been deleted!");
                        return true;
                    }
                        
                }
                else
                {
                    UnityEngine.Debug.Log("[Permissions] " + Group + " does not exist!");
                    return false;
                }
            }
            else
            {
                UnityEngine.Debug.Log("[Permissions] " + Group + " is the default group and can not be removed!");
                return false;
            }
        }

        #endregion
    }

    public class API
    {
        private Permissions Permissions;
        public string DefaultGroup
        {
            get
            {
                return Permissions.DefaultGroup;
            }
        }
        public string[] GetGroupNames
        {
            get
            {
                return Permissions.GroupData.Keys.ToArray();
            }
        }

        public bool HasPerm(string HWID, string perm)
        {
            try
            {
                if (Permissions.PlayerGroup.ContainsKey(HWID) && Permissions.GroupData.ContainsKey(Permissions.PlayerGroup[HWID]))
                {
                    if (Permissions.GroupData[Permissions.PlayerGroup[HWID]].Contains(perm))
                    {
                        return true;
                    }
                }
                return false;
            }
            catch
            {
                return false;
            }
        }
    }
}
