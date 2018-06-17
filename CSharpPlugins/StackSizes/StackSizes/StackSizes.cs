using Facepunch;
using Fougerite;
using RustBuster2016Server;
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading;
using UnityEngine;

namespace StackSizes
{
    public class StackSizes : Module
    {
        private GameObject myGameObject;
        private StackSizesRPC rpc;
        private StackSizesItemList itemList = new StackSizesItemList();

        private IniParser config;

        private Dictionary<int, int> _stackSizes = new Dictionary<int, int>();

        private bool RustBusterSupport = false;

        public override string Name
        {
            get { return "Stacksizes"; }
        }

        public override string Author
        {
            get { return "Jakkee"; }
        }

        public override string Description
        {
            get { return "Server module for stacksizes"; }
        }

        public override Version Version
        {
            get { return new Version("1.0.0"); }
        }

        public override void DeInitialize()
        {
            Hooks.OnModulesLoaded -= OnModulesLoaded;

            if (RustBusterSupport)
            {
                Hooks.OnPlayerConnected -= OnPlayerConnected;
                Hooks.OnServerLoaded -= OnServerStarted;
                API.OnRustBusterUserMessage -= OnRustBusterUserMessage;
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
                foreach (var x in ModuleManager.Modules)
                {
                    if (!x.Plugin.Name.ToLower().Contains("rustbuster")) continue;
                    RustBusterSupport = true;
                    break;
                }
                if (RustBusterSupport)
                {
                    Hooks.OnPlayerConnected += OnPlayerConnected;
                    Hooks.OnServerLoaded += OnServerStarted;
                    API.OnRustBusterUserMessage += OnRustBusterUserMessage;

                    myGameObject = new GameObject();
                    rpc = myGameObject.AddComponent<StackSizesRPC>();
                }
                else
                {
                    Logger.LogWarning("StackSizes: Could not find RustBuster");
                    Logger.LogWarning("StackSizes: This plugin is useless without it!");
                }
            }
            catch (Exception ex)
            {
                Logger.LogError("[StackSizes] Error starting plugin");
                Logger.LogException(ex);
            }
        }
        
        public void OnServerStarted()
        {
            LoadConfig();
        }

        public void LoadConfig()
        {
            if (!File.Exists(Path.Combine(ModuleFolder, "Config.ini")))
            {
                File.Create(Path.Combine(ModuleFolder, "Config.ini")).Dispose();
                config = new IniParser(Path.Combine(ModuleFolder, "Config.ini"));
                config.Save();
                foreach (ItemDataBlock item in Bundling.LoadAll<ItemDataBlock>())
                {
                    if (itemList.ItemList.Contains(item.name))
                    {
                        config.AddSetting("Config", item.name + ":" + item.uniqueID.ToString(), item._maxUses.ToString());
                    }
                }
                config.Save();
            }
            config = new IniParser(Path.Combine(ModuleFolder, "Config.ini"));

            foreach (string itemid in config.EnumSection("Config"))
            {
                int id = int.Parse(itemid.Split(':')[1]);
                int amount = int.Parse(config.GetSetting("Config", itemid));
                _stackSizes.Add(id, amount);
                DatablockDictionary.GetByUniqueID(id)._maxUses = amount;
            }
        }

        public void OnPlayerConnected(Fougerite.Player player)
        {
            player.SendConsoleMessage("stacksizes.load");
        }

        public void OnRustBusterUserMessage(API.RustBusterUserAPI user, Message msgc)
        {
            if (msgc.PluginSender == "StackSizesClient")
            {
                string msg = msgc.MessageByClient;
                string[] split = msg.Split('-');
                if (split[0] == "UpdateStackSizes")
                {
                    SendStackSizes(user.Player);
                }
            }
        }

        private void SendStackSizes(Fougerite.Player player)
        {
            Thread thread = new Thread(() =>
            {
                Dictionary<int, int> items = _stackSizes;
                foreach (int id in items.Keys)
                {
                    rpc.SendMessageToPlayer(player, "StackSizes", id, items[id]);
                }
            })
            {
                IsBackground = true
            };
            thread.Start();
        }
    }
}
