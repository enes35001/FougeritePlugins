using UnityEngine;

namespace StackSizes
{
    public class StackSizesRPC : MonoBehaviour
    {
        public void SendMessageToPlayer(Fougerite.Player player, string function, int uniqueid, int stacksize)
        {
            if (player.NetworkPlayer != null && player.PlayerClient?.networkView != null)
            {
                uLink.NetworkView.Get(player.PlayerClient.networkView).RPC(function, player.NetworkPlayer, uniqueid, stacksize);
            }
        }
    }
}