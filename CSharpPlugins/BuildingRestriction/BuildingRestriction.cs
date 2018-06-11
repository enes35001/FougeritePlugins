using Fougerite;
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading;

namespace BuildingRestriction
{
    public class BuildingRestriction : Module
    {
        private IniParser _settingsini;
        private IniParser _errorLog;
        private bool _internalError;
        private bool _adminsCanBypass;
        private bool _moderatorsCanBypass;
        private bool _refund = true;
        private Dictionary<string, float> _settings = new Dictionary<string, float>();

        public override string Name
        {
            get { return "BuildingRestriction"; }
        }

        public override string Author
        {
            get { return "Jakkee"; }
        }

        public override string Description
        {
            get { return "Restrict the height and maximum foundations of bases"; }
        }

        public override Version Version
        {
            get { return new Version("2.0.0"); }
        }

        public override void DeInitialize()
        {
            if (!_internalError)
            {
                Hooks.OnEntityDeployedWithPlacer -= OnEntityDeployed;
            }
        }

        public override void Initialize()
        {
            LoadConfig();
            if (!_internalError)
            {
                Hooks.OnEntityDeployedWithPlacer += OnEntityDeployed;
            }
            else
            {
                Logger.LogError("[BuildingRestriction] Error in settings file, Plugin is disabled");
            }
        }

        private void OnEntityDeployed(Fougerite.Player oldplayer, Entity entity, Fougerite.Player player)
        {
            var internalerror = false;

            if (CanBypass(player)) { return; }

            var thread = new Thread(() =>
            {
                try
                {
                    if (entity.Name.Contains("Pillar"))
                    {
                        var height = entity.Name.Contains("WoodPillar")
                            ? _settings["Maximum Wood Height"]
                            : _settings["Maximum Metal Height"];

                        foreach (var ent in entity.GetLinkedStructs())
                        {
                            if (!ent.Name.Contains("Foundation"))
                            {
                                continue;
                            }

                            if (((entity.Y - ent.Y) / 4) > height)
                            {
                                if (_refund)
                                {
                                    player.Inventory.AddItem(entity.Name, 1);
                                    player.InventoryNotice("1 x " + entity.Name);
                                }

                                if (!entity.IsDestroyed)
                                {
                                    entity.Destroy();
                                }

                                player.Notice("You have reached the maximum build height!");
                            }

                            break;
                        }
                    }
                    else if (entity.Name.Contains("Foundation"))
                    {
                        var foundations = entity.Name.Contains("WoodFoundation")
                            ? _settings["Maximum Wood Foundations"]
                            : _settings["Maximum Metal Foundations"];

                        var count = 0f;

                        foreach (var ent in entity.GetLinkedStructs())
                        {
                            if (!ent.Name.Contains("Foundation"))
                            {
                                continue;
                            }     
                            count += 1f;
                        }
                        
                        if (count >= foundations)
                        {
                            if (_refund)
                            {
                                player.Inventory.AddItem(entity.Name);
                                player.InventoryNotice("1 x " + entity.Name);
                            }

                            if (!entity.IsDestroyed)
                            {
                                entity.Destroy();
                            }

                            player.Notice("You have reached the maximum foundations!");
                        }
                    }
                }
                catch (Exception e)
                {
                    internalerror = true;
                    if (!File.Exists(Path.Combine(ModuleFolder, "ErrorLog.ini")))
                    {
                        File.Create(Path.Combine(ModuleFolder, "ErrorLog.ini")).Dispose();
                        _errorLog = new IniParser(Path.Combine(ModuleFolder, "ErrorLog.ini"));
                        _errorLog.Save();
                    }
                    _errorLog = new IniParser(Path.Combine(ModuleFolder, "ErrorLog.ini"));

                    _errorLog.AddSetting(DateTime.Now.ToString("dd_MM_yyyy"), DateTime.Now.ToString("h:mm:ss"), Author + ":" + Version + " | Message: " + e.Message + " StackTrace: " + e.StackTrace);
                    _errorLog.Save();
                }
            })
            {
                IsBackground = true
            };
            thread.Start();

            if (internalerror)
            {
                if (player.Admin || player.Moderator)
                {
                    player.MessageFrom("BuildingRestriction", "Error in plugin, Check ErrorLog.ini for details on this error");
                }
                Logger.LogError("[BuildingRestriction] Error in plugin, See ErrorLog.ini for details!");
            }

        }

        private bool CanBypass(Fougerite.Player player)
        {
            try
            {
                if (player.Admin && _adminsCanBypass)
                {
                    return true;
                }
                else if (player.Moderator && _moderatorsCanBypass)
                {
                    return true;
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

        private void LoadConfig()
        {
            if (!File.Exists(Path.Combine(ModuleFolder, "Settings.ini")))
            {
                Logger.LogDebug("[BuildingRestriction] Creating new settings file...");
                File.Create(Path.Combine(ModuleFolder, "Settings.ini")).Dispose();
                _settingsini = new IniParser(Path.Combine(ModuleFolder, "Settings.ini"));
                _settingsini.AddSetting("Bypass Limits", "Admins", "True");
                _settingsini.AddSetting("Bypass Limits", "Moderators", "False");
                _settingsini.AddSetting("Refund", "Enabled", "True");
                _settingsini.AddSetting("Settings", "Maximum Wood Height", "5");
                _settingsini.AddSetting("Settings", "Maximum Metal Height", "5");
                _settingsini.AddSetting("Settings", "Maximum Wood Foundations", "16");
                _settingsini.AddSetting("Settings", "Maximum Metal Foundations", "16");
                _settingsini.Save();
            }
            _settingsini = new IniParser(Path.Combine(ModuleFolder, "Settings.ini"));

            try
            {
                _adminsCanBypass = _settingsini.GetBoolSetting("Bypass Limits", "Admins");
                _moderatorsCanBypass = _settingsini.GetBoolSetting("Bypass Limits", "Moderators");
                _refund = _settingsini.GetBoolSetting("Refund", "Enabled");
            }
            catch (Exception e)
            {
                _internalError = true;
                Logger.LogError("[BuildingRestriction] Error converting string to bool");
                Logger.LogError(e.Message);
            }

            foreach (var value in _settingsini.EnumSection("Settings"))
            {
                try
                {
                    _settings.Add(value, float.Parse(_settingsini.GetSetting("Settings", value)));
                }
                catch (Exception e)
                {
                    _internalError = true;
                    Logger.LogError("[BuildingRestriction] Error converting " + value + " setting to a number");
                    Logger.LogError(e.Message);
                }
            }
            if (!_internalError) { Logger.LogDebug("[BuildingRestriction] Loaded settings file."); }
        }
    }
}
