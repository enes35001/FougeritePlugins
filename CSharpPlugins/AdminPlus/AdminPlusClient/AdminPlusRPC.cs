using RustBuster2016.API;
using System.Collections.Generic;
using UnityEngine;

namespace AdminPlus
{
    public class AdminPlusRPC : MonoBehaviour
    {

        public void Start()
        {
            AdminPlus.Instance.SendMessageToServer("GetPlayers-");
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
        public void AddPlayerToList(string hwid, string name)
        {
            if (AdminPlus.IsAllowed)
            {
                if (!AdminPlus.Instance.GetPlayersList.ContainsKey(hwid))
                {
                    AdminPlus.Instance.PlayersList.Add(hwid, name);
                }
            }
        }
    }
}
