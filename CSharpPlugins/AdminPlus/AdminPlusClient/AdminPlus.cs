using RustBuster2016.API;
using System;
using System.Collections.Generic;
using UnityEngine;

namespace AdminPlus
{
    public class AdminPlus : RustBusterPlugin
    {
        public static AdminPlus Instance;
        private GameObject obj;
        private AdminPlusGUI GUI;
        private AdminPlusRPC rpc;

        internal Dictionary<string, string> PlayersList = new Dictionary<string, string>();

        internal static bool IsAllowed = false;
        internal static bool Enabled = false;

        public override string Name
        {
            get { return "AdminPlusClient"; }
        }

        public override string Author
        {
            get { return "Jakkee"; }
        }

        public override Version Version
        {
            get { return new Version("3.1.0"); }
        }

        public override void DeInitialize()
        {
            if (GUI != null)
            {
                UnityEngine.Object.DestroyImmediate(GUI);
            }
            IsAllowed = false;
            Enabled = false;
            if (rpc != null)
            {
                UnityEngine.Object.DestroyImmediate(rpc);
            }
            Hooks.OnRustBusterClientConsole -= OnRustBusterClientConsole;
        }

        public override void Initialize()
        {
            Instance = this;
            Hooks.OnRustBusterClientConsole += OnRustBusterClientConsole;
            //wobj = new GameObject();
            //waiter = wobj.AddComponent<AdminPlusWaiter>();
        }

        public void StartPlugin()
        {
            IsAllowed = StringToBool(this.SendMessageToServer("IsAllowed-"));
            if (rpc == null && GUI == null)
            {
                if (GUI != null)
                {
                    UnityEngine.Object.Destroy(GUI);
                }
                obj = new GameObject();
                GUI = obj.AddComponent<AdminPlusGUI>();
                UnityEngine.Object.DontDestroyOnLoad(GUI);

                if (rpc != null)
                {
                    UnityEngine.Object.Destroy(rpc);
                }
                try
                {
                    rpc = PlayerClient.GetLocalPlayer().gameObject.AddComponent<AdminPlusRPC>();
                }
                catch (Exception ex)
                {
                    Debug.LogError(ex.Message);
                }
            }
            else
            {
                Debug.Log("AdminPlus UI and RPC's are already loaded!");
            }
        }

        private void OnRustBusterClientConsole(string msg)
        {
            string[] message = msg.ToLower().RemoveWhiteSpaces().Split('.');
            if (message[0] == "adminplus" && message.Length == 2)
            {
                switch (message[1])
                {
                    case "load":
                        StartPlugin();
                        break;
                }
            }
        }

        public bool StringToBool(string text)
        {
            if (text == "yes")
            {
                return true;
            }
            else
            {
                return false;
            }
        }

        public Dictionary<string, string> GetPlayersList
        {
            get
            {
                return new Dictionary<string, string>(PlayersList);
            }
        }
    }
}
