using UnityEngine;

namespace AdminPlusServer
{
    public class AdminPlusRPC : MonoBehaviour
    {
        public void SendMessageToPlayer(Fougerite.Player player, string function, string data, string data0)
        {
            if (player.NetworkPlayer != null && player.PlayerClient?.networkView != null)
            {
                uLink.NetworkView.Get(player.PlayerClient.networkView).RPC(function, player.NetworkPlayer, data, data0);
            }
        }

        public void SendMessageToPlayer(Fougerite.Player player, string function, object data)
        {
            if (player.NetworkPlayer != null && player.PlayerClient?.networkView != null)
            {
                uLink.NetworkView.Get(player.PlayerClient.networkView).RPC(function, player.NetworkPlayer, data);
            }
        }

        public void SendMessageToPlayer(Fougerite.Player player, string function, bool data)
        {
            if (player.NetworkPlayer != null && player.PlayerClient?.networkView != null)
            {
                uLink.NetworkView.Get(player.PlayerClient.networkView).RPC(function, player.NetworkPlayer, data);
            }
        }
    }
}
