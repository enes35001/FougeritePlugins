using RustBuster2016.API;
using System;
using UnityEngine;

namespace StackSizesClient
{
    public class StackSizesClient : RustBusterPlugin
    {
        public static StackSizesClient Instance;
        private StackSizesRPC rpc;

        public override string Name { get { return "StackSizes"; } }

        public override string Author { get { return "Jakkee"; } }

        public override Version Version { get { return new Version("1.0.0"); } }

        public override void DeInitialize()
        {
            if (rpc != null)
            {
                UnityEngine.Object.DestroyImmediate(rpc);
                Hooks.OnRustBusterClientConsole -= OnRustBusterClientConsole;
            }
        }

        public override void Initialize()
        {
            Instance = this;
            Hooks.OnRustBusterClientConsole += OnRustBusterClientConsole;
        }

        private void OnRustBusterClientConsole(string msg)
        {
            string[] message = msg.ToLower().RemoveWhiteSpaces().Split('.');
            if (message[0] == "stacksizes" && message.Length == 2)
            {
                switch (message[1])
                {
                    case "load":
                        StartPlugin();
                        break;
                }
            }
        }

        private void StartPlugin()
        {
            if (rpc != null)
            {
                UnityEngine.Object.Destroy(rpc);
            }
            try
            {
                rpc = PlayerClient.GetLocalPlayer().gameObject.AddComponent<StackSizesRPC>();
            }
            catch (Exception ex)
            {
                Debug.LogError(ex.Message);
            }
        }
    }
}
