using RustBuster2016.API;
using System.Collections.Generic;
using UnityEngine;

namespace AdminPlus
{
    public class AdminPlusRPC : MonoBehaviour
    {

        public void Start()
        {
            Debug.Log("Server sent RPC: " + AdminPlus.Instance.StringToBool(AdminPlus.Instance.SendMessageToServer("GetPlayers-")).ToString());
        }

        [RPC]
        public void FreezeMode(bool freeze)
        {
            Hooks.LocalPlayer.rootControllable.lockMovement = freeze;
            Hooks.LocalPlayer.rootControllable.lockLook = freeze;
        }

        [RPC]
        public void RemovePlayerFromList(string hwid)
        {
            if (AdminPlus.Instance.GetPlayersList.ContainsKey(hwid))
            {
                AdminPlus.Instance.PlayersList.Remove(hwid);
            }
        }

        [RPC]
        public void AddPlayerToList(Dictionary<string, string> player)
        {
            if (player != null && player.Keys.Count > 0)
            {
                if (AdminPlus.IsAllowed)
                {
                    foreach (string x in player.Keys)
                    {
                        if (!AdminPlus.Instance.GetPlayersList.ContainsKey(x))
                        {
                            AdminPlus.Instance.PlayersList.Add(x, player[x]);
                        }
                    }
                }
            }
            
        }
    }
}
