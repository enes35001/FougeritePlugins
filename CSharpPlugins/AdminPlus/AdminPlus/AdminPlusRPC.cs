using System.Collections.Generic;
using UnityEngine;

namespace AdminPlusServer
{
    public class AdminPlusRPC : MonoBehaviour
    {
        private AdminPlusServer svr = new AdminPlusServer();

        public void Start()
        {
            Fougerite.Logger.LogDebug("Starting RPC...");
        }

        public void SendMessageToPlayer(Fougerite.Player player, string function, object data)
        {
            uLink.NetworkView.Get(player.PlayerClient.networkView).RPC(function, player.NetworkPlayer, data);
        }

        public void SendMessageToAll(string function, object data)
        {
            foreach (Fougerite.Player player in Fougerite.Server.GetServer().Players)
            {
                uLink.NetworkView.Get(player.PlayerClient.networkView).RPC(function, player.NetworkPlayer, data);
            }
        }
    }
}
